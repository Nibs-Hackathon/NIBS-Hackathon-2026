from simulator.event_generator import EventGenerator

class Simulator:

    def __init__(self, facility, kernel):

        self.facility = facility
        self.kernel = kernel

        self.state = kernel.state

        self.generator = EventGenerator()

    def tick(self, tick_number: int):

        telemetry = self.facility.tick(tick_number)

        self.state.add_telemetry(telemetry)

        event = self.generator.generate(telemetry)

        if event:

            report = self.kernel.handle_event(event)

            return telemetry, report

        return telemetry, None
    