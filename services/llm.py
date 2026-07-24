"""Centralized, failover-safe access to Gemini models with multi-key rotation and caching."""

import hashlib
import logging
import os
import socket
import time
from pathlib import Path
from typing import Optional, Dict, List
from collections import deque
from datetime import datetime
from urllib.parse import urlsplit

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

logger = logging.getLogger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")

# ✅ SUPPORTED ENV VARS - ALL POSSIBLE NAMING CONVENTIONS
SUPPORTED_GEMINI_ENV_VARS = (
    # Standard naming
    "GEMINI_API_KEY_1", "GEMINI_API_KEY_2", "GEMINI_API_KEY_3",
    "GEMINI_API_KEY_4", "GEMINI_API_KEY_5", "GEMINI_API_KEY_6",
    "GEMINI_API_KEY_7", "GEMINI_API_KEY_8", "GEMINI_API_KEY_9",
    "GEMINI_API_KEY_10",
    # Alternative naming
    "GOOGLE_API_KEY_1", "GOOGLE_API_KEY_2", "GOOGLE_API_KEY_3",
    "GOOGLE_API_KEY_4", "GOOGLE_API_KEY_5", "GOOGLE_API_KEY_6",
    "GOOGLE_API_KEY_7",
    # Single key fallback
    "GEMINI_API_KEY", "GOOGLE_API_KEY",
)

DEFAULT_GEMINI_MODEL = "gemini-3.5-flash-lite"

_PROXY_ENV_VARS = (
    "HTTP_PROXY", "HTTPS_PROXY", "ALL_PROXY",
    "http_proxy", "https_proxy", "all_proxy",
)
_LOOPBACK_HOSTS = {"localhost", "127.0.0.1", "::1"}


def _has_invalid_gemini_proxy() -> bool:
    """Return whether this process inherited the known dead loopback proxy."""
    for name in _PROXY_ENV_VARS:
        value = os.getenv(name)
        if not value:
            continue
        try:
            proxy = urlsplit(value)
            if proxy.hostname not in _LOOPBACK_HOSTS or proxy.port is None:
                continue
            if proxy.port == 9:
                return True
            with socket.create_connection((proxy.hostname, proxy.port), timeout=0.15):
                pass
        except OSError:
            return True
        except ValueError:
            continue
    return False


class RateLimiter:
    """Simple rate limiter for API calls with per-key tracking."""

    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.call_timestamps: Dict[str, deque] = {}

    def wait_if_needed(self, key: str):
        """Wait if rate limit would be exceeded for a specific key."""
        now = time.time()

        if key not in self.call_timestamps:
            self.call_timestamps[key] = deque(maxlen=self.calls_per_minute)

        timestamps = self.call_timestamps[key]

        while timestamps and now - timestamps[0] > 60:
            timestamps.popleft()

        if len(timestamps) >= self.calls_per_minute:
            oldest = timestamps[0]
            wait_time = 60 - (now - oldest) + 0.5
            if wait_time > 0:
                logger.warning(f"Rate limit reached for key, waiting {wait_time:.2f}s")
                time.sleep(wait_time)

        timestamps.append(time.time())


class KeyStatus:
    """Track status of each API key."""

    def __init__(self, key: str, index: int):
        self.key = key
        self.index = index
        self.failures = 0
        self.successes = 0
        self.last_used: Optional[float] = None
        self.last_error: Optional[str] = None
        self.is_active = True
        self.cooldown_until: Optional[float] = None
        self.total_requests = 0

    def record_success(self):
        self.successes += 1
        self.failures = 0
        self.last_used = time.time()
        self.total_requests += 1
        self.is_active = True

    def record_failure(self, error: str):
        self.failures += 1
        self.last_error = error
        self.total_requests += 1

        # ✅ More aggressive cooldown - 30 seconds instead of 60
        if self.failures >= 3:
            self.is_active = False
            self.cooldown_until = time.time() + 30
            logger.warning(f"Key {self.index + 1} deactivated for 30s due to {self.failures} failures")

    def reactivate_if_ready(self):
        if not self.is_active and self.cooldown_until:
            if time.time() >= self.cooldown_until:
                self.is_active = True
                self.failures = 0
                self.cooldown_until = None
                logger.info(f"Key {self.index + 1} reactivated after cooldown")
                return True
        return False

    @property
    def success_rate(self) -> float:
        if self.total_requests == 0:
            return 0.0
        return (self.successes / self.total_requests) * 100

    @property
    def is_available(self) -> bool:
        if not self.is_active:
            return False
        if self.cooldown_until and time.time() < self.cooldown_until:
            return False
        return True

    def to_dict(self) -> Dict:
        return {
            "index": self.index + 1,
            "key_preview": self.key[:8] + "..." + self.key[-4:],
            "is_active": self.is_active,
            "is_available": self.is_available,
            "failures": self.failures,
            "successes": self.successes,
            "total_requests": self.total_requests,
            "success_rate": f"{self.success_rate:.1f}%",
            "last_used": datetime.fromtimestamp(self.last_used).strftime("%H:%M:%S") if self.last_used else "Never",
            "last_error": self.last_error or "None",
        }


# Response Cache
_response_cache: Dict[str, tuple] = {}
_CACHE_MAX_SIZE = 100


class LLMManager:
    """Central Gemini router with automatic multi-key rotation and caching."""

    def __init__(self, model_name: Optional[str] = None):
        self.model_name = model_name or os.getenv("GEMINI_MODEL", DEFAULT_GEMINI_MODEL)
        self.keys = self._load_keys()
        self.current_key_index = 0
        self.key_statuses: Dict[str, KeyStatus] = {}
        self.rate_limiter = RateLimiter(calls_per_minute=60)

        for idx, key in enumerate(self.keys):
            self.key_statuses[key] = KeyStatus(key, idx)

        if not self.keys:
            raise RuntimeError(
                "No Gemini API key was found. Configure one of:\n"
                + "\n".join(f"  - {var}" for var in SUPPORTED_GEMINI_ENV_VARS)
            )

        logger.info(f"LLMManager initialized with {len(self.keys)} Gemini key(s)")

    def _load_keys(self) -> List[str]:
        """✅ Load API keys from ALL possible sources."""
        keys = []
        seen = set()

        # 1. Check environment variables
        print("\n🔑 Loading Gemini API Keys...")
        for var in SUPPORTED_GEMINI_ENV_VARS:
            value = os.getenv(var)
            if value and value not in seen:
                seen.add(value)
                keys.append(value)
                print(f"  ✅ Loaded from {var}: {value[:8]}...{value[-4:]}")

        # 2. Check .env file directly
        try:
            env_path = PROJECT_ROOT / ".env"
            if env_path.exists():
                with open(env_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line.startswith('GEMINI_API_KEY') or line.startswith('GOOGLE_API_KEY'):
                            if '=' in line:
                                key = line.split('=', 1)[1].strip()
                                if key and key not in seen:
                                    seen.add(key)
                                    keys.append(key)
                                    print(f"  ✅ Loaded from .env: {key[:8]}...{key[-4:]}")
        except Exception as e:
            print(f"  ⚠️ Could not read .env: {e}")

        # 3. Check Streamlit secrets
        try:
            import streamlit as st
            for var in SUPPORTED_GEMINI_ENV_VARS:
                if var in st.secrets:
                    value = st.secrets[var]
                    if value and value not in seen:
                        seen.add(value)
                        keys.append(value)
                        print(f"  ✅ Loaded from secrets[{var}]: {value[:8]}...{value[-4:]}")
        except Exception:
            pass

        print(f"\n✅ Total keys loaded: {len(keys)}\n")
        return keys

    def _get_next_available_key(self) -> Optional[str]:
        """✅ Get the next available API key with rotation."""
        total_keys = len(self.keys)
        attempts = 0

        # Try all keys in rotation
        while attempts < total_keys:
            idx = self.current_key_index
            key = self.keys[idx]
            self.current_key_index = (self.current_key_index + 1) % total_keys

            status = self.key_statuses[key]
            
            # Try to reactivate if cooldown expired
            if not status.is_active:
                status.reactivate_if_ready()

            if status.is_available:
                status.last_used = time.time()
                return key

            attempts += 1

        # If all keys are exhausted, try to reactivate one
        for key in self.keys:
            status = self.key_statuses[key]
            if status.reactivate_if_ready():
                return key

        # Last resort: use first key (even if it's failing)
        return self.keys[0]

    def _create_model(self, key: str):
        """Create a Gemini model instance."""
        client_args = {"trust_env": False} if _has_invalid_gemini_proxy() else None
        return ChatGoogleGenerativeAI(
            model=self.model_name,
            google_api_key=key,
            client_args=client_args,
            temperature=0.3,
        )

    def generate(self, prompt: str, max_retries_per_key: int = 2, use_cache: bool = True) -> str:
        """✅ Generate Gemini response with automatic multi-key rotation."""
        
        # Check cache first
        if use_cache:
            cache_key = hashlib.md5(prompt.encode()).hexdigest()
            if cache_key in _response_cache:
                cached_response, cached_time = _response_cache[cache_key]
                if time.time() - cached_time < 300:
                    logger.info(f"✅ Cache hit for prompt (key: {cache_key[:8]})")
                    return cached_response
                else:
                    del _response_cache[cache_key]
        
        last_error = None
        
        # ✅ Try each key in rotation
        for attempt in range(len(self.keys) * max_retries_per_key):
            try:
                key = self._get_next_available_key()
                if key is None:
                    raise RuntimeError("No available API keys")

                status = self.key_statuses[key]
                logger.info(f"Using Gemini key {status.index + 1}/{len(self.keys)}")

                self.rate_limiter.wait_if_needed(key)
                response = self._create_model(key).invoke(prompt)

                status.record_success()

                content = response.content
                if isinstance(content, str):
                    response_text = content
                elif isinstance(content, list):
                    response_text = "".join(
                        part if isinstance(part, str) else part.get("text", "")
                        for part in content
                        if isinstance(part, str) or isinstance(part, dict)
                    )
                else:
                    response_text = str(content)
                
                # Cache the response
                if use_cache and response_text:
                    cache_key = hashlib.md5(prompt.encode()).hexdigest()
                    _response_cache[cache_key] = (response_text, time.time())
                    
                    if len(_response_cache) > _CACHE_MAX_SIZE:
                        oldest_keys = sorted(_response_cache.keys(), key=lambda k: _response_cache[k][1])[:10]
                        for key in oldest_keys:
                            del _response_cache[key]
                
                return response_text

            except Exception as error:
                last_error = error
                error_str = str(error)
                
                # ✅ Handle rate limiting specially
                if "429" in error_str or "RESOURCE_EXHAUSTED" in error_str:
                    logger.warning(f"⚠️ Key {status.index + 1} rate limited (429). Moving to next key.")
                    # ✅ Don't deactivate on rate limit - just use next key
                    if key and key in self.key_statuses:
                        status = self.key_statuses[key]
                        status.failures += 1
                        status.last_error = error_str
                    time.sleep(0.5)
                else:
                    if key and key in self.key_statuses:
                        status = self.key_statuses[key]
                        status.record_failure(error_str)
                        logger.warning(f"Key {status.index + 1} failed: {error_str[:100]}")
                    time.sleep(0.5)
                
                continue

        raise RuntimeError(
            f"All {len(self.keys)} Gemini API keys failed. Last error: {last_error}"
        ) from last_error

    def get_key_status(self) -> Dict[str, any]:
        """Get status of all API keys for monitoring."""
        return {
            "total_keys": len(self.keys),
            "model": self.model_name,
            "current_index": self.current_key_index + 1,
            "keys": [self.key_statuses[key].to_dict() for key in self.keys],
            "summary": {
                "active_keys": sum(1 for s in self.key_statuses.values() if s.is_active),
                "available_keys": sum(1 for s in self.key_statuses.values() if s.is_available),
                "total_requests": sum(s.total_requests for s in self.key_statuses.values()),
                "overall_success_rate": (
                    sum(s.successes for s in self.key_statuses.values()) /
                    max(1, sum(s.total_requests for s in self.key_statuses.values())) * 100
                ),
            }
        }

    def reset_key(self, key_index: int) -> bool:
        """Reset a specific key's status."""
        try:
            key = self.keys[key_index - 1]
            status = self.key_statuses[key]
            status.failures = 0
            status.is_active = True
            status.cooldown_until = None
            status.last_error = None
            logger.info(f"Key {key_index} reset successfully")
            return True
        except (IndexError, KeyError):
            return False

    def clear_cache(self):
        """Clear the response cache."""
        global _response_cache
        _response_cache.clear()
        logger.info("LLM response cache cleared")