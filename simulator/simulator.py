from simulator.event_generator import EventGenerator

<<<<<<< HEAD
=======

>>>>>>> origin/dev-ashutosh-zinia
class Simulator:

    def __init__(self, facility, kernel):

        self.facility = facility
        self.kernel = kernel

        self.state = kernel.state

        self.generator = EventGenerator()

<<<<<<< HEAD
    def tick(self, tick_number: int):
=======
    def tick(self, tick_number):
>>>>>>> origin/dev-ashutosh-zinia

        telemetry = self.facility.tick(tick_number)

        self.state.add_telemetry(telemetry)

<<<<<<< HEAD
        event = self.generator.generate(telemetry)

        if event:

            report = self.kernel.handle_event(event)

            return telemetry, report

        return telemetry, None
    
=======
        for asset in self.facility.assets:
            history = self.state.get_history(asset.asset.id)
            health = self.kernel.health.calculate_health(history)
            
            self.kernel.asset_service.update_health(
                asset.asset.id,
                health,
            )
            if health > 80:
                status = "Running"
            elif health >50:
                status = "Warning"
            else:
                status = "Critical"
            
            self.kernel.asset_service.update_status(
                asset.asset.id,
                status,
            )

        reports = []

        events = self.generator.generate(telemetry)

        for event in events:

            report = self.kernel.handle_event(event)

            reports.append(report)

        return telemetry, reports
>>>>>>> origin/dev-ashutosh-zinia
