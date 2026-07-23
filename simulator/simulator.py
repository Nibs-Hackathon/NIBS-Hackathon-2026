from simulator.event_generator import EventGenerator
from services.persistence import PersistenceService


class Simulator:

    def __init__(self, facility, kernel):

        self.facility = facility
        self.kernel = kernel

        self.state = kernel.state

        self.generator = EventGenerator()

        self.persistence = PersistenceService()


    def tick(self, tick_number,fault=None):

        telemetry = self.facility.tick(tick_number, fault)

        self.state.add_telemetry(telemetry)

        self.persistence.record_telemetry(telemetry)


        # Update asset health

        for asset in self.facility.assets:

            history = self.state.get_history(asset.asset.id)

            health = self.kernel.health.calculate_health(history)


            self.kernel.asset_service.update_health(
                asset.asset.id,
                health,
            )


            if health > 80:
                status = "Running"

            elif health > 50:
                status = "Warning"

            else:
                status = "Critical"


            self.kernel.asset_service.update_status(
                asset.asset.id,
                status,
            )


        # Handle incidents

        reports = []

        events = self.generator.generate(telemetry)


        for event in events:

            report = self.kernel.handle_event(event)

            reports.append(report)


        return telemetry, reports
