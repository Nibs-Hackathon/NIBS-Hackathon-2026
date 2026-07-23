"""
Centralized, failover-safe access to Gemini models.

Supports:
- Local development (.env)
- Streamlit Cloud (st.secrets)
- Multiple API keys with automatic failover
"""

import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


logger = logging.getLogger(__name__)


# Load local .env
PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(
    PROJECT_ROOT / ".env"
)


class LLMManager:
    """
    Central Gemini router.

    Agents should NEVER directly call Gemini.
    They should use this class.
    """


    def __init__(
        self,
        model_name="gemini-2.5-flash",
        temperature=0.2
    ):

        self.model_name = model_name
        self.temperature = temperature

        self.keys = self._load_keys()

        self.current_key_index = 0


        if not self.keys:
            raise RuntimeError(
                "No Gemini API keys configured. "
                "Add GOOGLE_API_KEY_1 and GOOGLE_API_KEY_2 "
                "to .env or Streamlit secrets."
            )


        logger.info(
            "LLMManager initialized with %s Gemini key(s)",
            len(self.keys)
        )


    @staticmethod
    def _load_keys():

        key_names = [
            "GOOGLE_API_KEY_1",
            "GOOGLE_API_KEY_2",
            "GEMINI_API_KEY_1",
            "GEMINI_API_KEY_2",
        ]


        keys = []


        # ---------------------------------
        # Local environment (.env)
        # ---------------------------------

        for name in key_names:

            value = os.getenv(name)

            if value:
                keys.append(value)



        # ---------------------------------
        # Streamlit Cloud secrets
        # ---------------------------------

        try:

            import streamlit as st


            for name in key_names:

                if name in st.secrets:

                    keys.append(
                        st.secrets[name]
                    )


        except Exception:

            # Running outside Streamlit
            pass



        # Remove duplicates
        return list(
            dict.fromkeys(keys)
        )


    def _create_model(self, key):

        return ChatGoogleGenerativeAI(

            model=self.model_name,

            google_api_key=key,

            temperature=self.temperature,
        )



    def generate(self, prompt):

        """
        Generate Gemini response.

        Automatically rotates keys if one fails.
        """

        last_error = None


        total_keys = len(self.keys)


        for attempt in range(total_keys):


            index = self.current_key_index


            key = self.keys[index]


            try:

                logger.info(
                    "Using Gemini key %s",
                    index + 1
                )


                response = (
                    self
                    ._create_model(key)
                    .invoke(prompt)
                )


                return response.content



            except Exception as error:


                last_error = error


                logger.warning(

                    "Gemini key %s failed. Switching key.",

                    index + 1,

                    exc_info=True
                )


                # Move to next key

                self.current_key_index = (
                    self.current_key_index + 1
                ) % total_keys



        raise RuntimeError(
            "All Gemini API keys failed. "
            "Check quota, permissions, and configuration."
        ) from last_error