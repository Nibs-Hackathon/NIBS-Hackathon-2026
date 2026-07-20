from datetime import datetime

from mao.core.context import ExecutionContext
from mao.models.execution_report import ExecutionReport


class Orchestrator:
    """
    Coordinates the complete execution lifecycle for a single event.
    """

    def __init__(
        self,
        *,
        planner,
        workflow_engine,
        scheduler,
        executor,
        supervisor,
        state_manager,
        memory_manager,
        logger,
        event_store,
    ):
        self.planner = planner
        self.workflow_engine = workflow_engine
        self.scheduler = scheduler
        self.executor = executor
        self.supervisor = supervisor

        self.state = state_manager
        self.memory = memory_manager
        self.logger = logger
        self.event_store = event_store

    def run(self, event):

        # -------------------------
        # Create execution context
        # -------------------------

        context = ExecutionContext(
            event=event,
            state_manager=self.state,
            memory_manager=self.memory,
            logger=self.logger,
        )

        self.logger.info("Kernel", f"Received event '{event.name}'")

        # -------------------------
        # Persist event
        # -------------------------

        self.state.add_event(event)
        self.event_store.save(event)

        # -------------------------
        # Select workflow
        # -------------------------

        workflow_name = self.planner.choose_workflow(event)

        context.workflow = workflow_name

        self.logger.info(
            "Planner",
            f"Selected workflow '{workflow_name}'",
        )

        # -------------------------
        # Build tasks
        # -------------------------

        tasks = self.workflow_engine.create_tasks(
            workflow_name,
            event,
        )

        self.logger.info(
            "WorkflowEngine",
            f"Generated {len(tasks)} task(s)",
        )

        # -------------------------
        # Schedule tasks
        # -------------------------

        for task in tasks:
            self.scheduler.submit(task)

        # -------------------------
        # Execute tasks
        # -------------------------

        while not self.scheduler.empty():

            task = self.scheduler.next()

            self.logger.info(
                "Executor",
                f"Executing '{task.name}'",
            )

            result = self.executor.execute(task)

            context.results.append(result)

            self.state.add_task(task)

        # -------------------------
        # Aggregate results
        # -------------------------

        decision = self.supervisor.summarize(
            context.results
        )

        report = ExecutionReport(
            execution_id=context.execution_id,
            workflow_name=workflow_name,
            success=decision["success"],
            started_at=context.started_at,
            completed_at=datetime.now(),
            agent_results=context.results,
            final_summary=decision["summary"],
            recommendations=decision["recommendations"],
        )

        self.logger.info(
            "Kernel",
            "Execution completed.",
        )

        return report