"""Optimized Simulator controller - NO circular imports."""

import threading
import time
from typing import Dict, List, Optional, Any


class SimulatorController:
    """Controls the simulation lifecycle with UI integration and auto-refresh."""

    def __init__(self):
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.tick_count = 0
        self._latest_telemetry: List[Any] = []
        self._latest_reports: List[Any] = []
        self._config_refresh_interval = 30
        self._simulator = None
        self._kernel = None

    @property
    def simulator(self):
        """Lazy load simulator."""
        if self._simulator is None:
            from services.runtime import get_simulator
            self._simulator = get_simulator()
        return self._simulator

    @property
    def kernel(self):
        """Lazy load kernel."""
        if self._kernel is None:
            from services.runtime import get_kernel
            self._kernel = get_kernel()
        return self._kernel

    def start(self, interval: float = 1.0):
        if self.running:
            return

        self.running = True
        self.kernel._simulation_running = True
        self._thread = threading.Thread(
            target=self._run,
            args=(interval,),
            daemon=True
        )
        self._thread.start()
        print(f"✅ Simulation started with interval {interval}s")

    def stop(self):
        self.running = False
        self.kernel._simulation_running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        print("⏹️ Simulation stopped")

    def step(self) -> tuple[List[Any], List[Any]]:
        self.tick_count += 1
        
        if self.tick_count % self._config_refresh_interval == 0:
            self._refresh_config()
        
        telemetry, reports = self.simulator.tick(self.tick_count)
        self._latest_telemetry = telemetry
        self._latest_reports = reports
        return telemetry, reports

    def _run(self, interval: float):
        while self.running:
            try:
                self.step()
            except Exception as e:
                print(f"⚠️ Simulation error: {e}")
                continue
            time.sleep(interval)

    def _refresh_config(self):
        try:
            from services.config_services import ConfigService
            ConfigService().clear_cache()
            
            from simulator.event_generator import EventGenerator
            EventGenerator().clear_cache()
            
            print(f"🔄 [Tick {self.tick_count}] Refreshed Gemini configuration")
        except Exception as e:
            print(f"⚠️ Config refresh failed: {e}")

    def get_latest_telemetry(self) -> List[Any]:
        return self._latest_telemetry

    def get_latest_reports(self) -> List[Any]:
        return self._latest_reports

    def get_status(self) -> Dict:
        return {
            "running": self.running,
            "ticks": self.tick_count,
            "assets": len(self.kernel.asset_service.all_assets()),
            "events": len(self.kernel.event_store.all()),
            "reports": len(self.kernel.state.execution_reports),
            "agent_results": len(self.kernel.state.agent_results),
        }


sim_controller = SimulatorController()