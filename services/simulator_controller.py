"""Simulator controller with threading support."""

import threading
import time
from typing import Dict, List, Optional, Any
from services.runtime import simulator, kernel


class SimulatorController:
    """Controls the simulation lifecycle with UI integration."""

    def __init__(self):
        self.running = False
        self._thread: Optional[threading.Thread] = None
        self.tick_count = 0
        self._latest_telemetry: List[Any] = []
        self._latest_reports: List[Any] = []

    def start(self, interval: float = 1.0):
        """Start the simulation in a background thread."""
        if self.running:
            return

        self.running = True
        kernel._simulation_running = True
        self._thread = threading.Thread(
            target=self._run,
            args=(interval,),
            daemon=True
        )
        self._thread.start()
        print(f"✅ Simulation started with interval {interval}s")

    def stop(self):
        """Stop the simulation."""
        self.running = False
        kernel._simulation_running = False
        if self._thread:
            self._thread.join(timeout=2.0)
        print("⏹️ Simulation stopped")

    def step(self) -> tuple[List[Any], List[Any]]:
        """Advance simulation by one tick (synchronous)."""
        self.tick_count += 1
        telemetry, reports = simulator.tick(self.tick_count)
        self._latest_telemetry = telemetry
        self._latest_reports = reports
        return telemetry, reports

    def _run(self, interval: float):
        """Main simulation loop."""
        while self.running:
            try:
                telemetry, reports = self.step()
            except Exception as e:
                print(f"⚠️ Simulation error: {e}")
                continue
            time.sleep(interval)

    def get_latest_telemetry(self) -> List[Any]:
        """Get the latest telemetry from the last tick."""
        return self._latest_telemetry

    def get_latest_reports(self) -> List[Any]:
        """Get the latest reports from the last tick."""
        return self._latest_reports

    def get_status(self) -> Dict:
        """Get current simulation status."""
        return {
            "running": self.running,
            "ticks": self.tick_count,
            "assets": len(kernel.asset_service.all_assets()),
            "events": len(kernel.event_store.all()),
            "reports": len(kernel.state.execution_reports),
            "agent_results": len(kernel.state.agent_results),
        }


# Singleton controller
sim_controller = SimulatorController()