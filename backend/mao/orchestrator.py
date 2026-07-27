"""Orchestrator with deterministic, dependency-safe agent execution."""

import time
from datetime import datetime
from mao.core.context import ExecutionContext
from mao.models.execution_report import ExecutionReport
from mao.models.task import TaskStatus


class Orchestrator:
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
        health_service=None,
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
        self.health_service = health_service

    def run(self, event):
        context = ExecutionContext(
            event=event,
            state_manager=self.state,
            memory_manager=self.memory,
            logger=self.logger,
            health_service=self.health_service,
        )

        self.logger.info("Kernel", f"[{context.execution_id}] Received event '{event.name}'")

        self.state.add_event(event)
        self.event_store.save(event)

        workflow_name = self.planner.choose_workflow(event)
        context.workflow = workflow_name

        self.logger.info("Planner", f"[{context.execution_id}] Selected workflow '{workflow_name}'")

        tasks = self.workflow_engine.create_tasks(workflow_name, event)

        self.logger.info("WorkflowEngine", f"[{context.execution_id}] Generated {len(tasks)} task(s)")

        # Schedule tasks
        for task in tasks:
            # Preserve operational context on every task.  Agent output and
            # maintenance planning can then be traced to the exact asset and
            # incident instead of being rendered as anonymous workflow cards.
            task.input_data = {
                **(task.input_data or {}),
                "incident_id": event.id,
                "asset_id": event.source,
                "incident_type": event.name,
                "event_payload": event.payload or {},
            }
            # State is registered before execution so the Operations Center can
            # represent pending and running MAO stages without a second engine.
            self.state.add_task(task)
            self.scheduler.submit(task)

        # Execute one task at a time because agents exchange context metadata.
        def execute_task(task):
            task.status = TaskStatus.RUNNING
            result = self.executor.execute(task, context)
            context.add_result(result)
            task.status = TaskStatus.COMPLETED if result.success else TaskStatus.FAILED
            return result

        start = time.time()

        # Agents share metadata, results, and metrics through the execution
        # context. Process them by scheduler priority so downstream agents see
        # the outputs produced by their dependencies.
        while not self.scheduler.empty():
            execute_task(self.scheduler.next())

        elapsed = time.time() - start
        self.logger.info("Executor", f"[{context.execution_id}] All agents completed in {elapsed:.2f}s")

        # Aggregate results
        decision = self.supervisor.summarize(context)

        report = ExecutionReport(
            execution_id=context.execution_id,
            workflow_name=workflow_name,
            success=decision["success"],
            started_at=context.started_at,
            completed_at=datetime.now(),
            agent_results=context.results,
            final_summary=decision["summary"],
            recommendations=decision["recommendations"],
            total_agents=context.execution_metrics["agents_executed"],
            successful_agents=context.execution_metrics["successful_agents"],
            failed_agents=context.execution_metrics["failed_agents"],
            average_confidence=context.execution_metrics["average_confidence"],
            approval_required=context.requires_human_approval,
            incident_severity=context.incident_level or "Unknown",
            metadata={
                **context.metadata,
                "incident_id": event.id,
                "incident_type": event.name,
                "asset_id": event.source,
            },
        )

        self.state.add_report(report)
        self.memory.remember_event(event)
        self.memory.remember_report(report)

        for result in report.agent_results:
            self.memory.remember_result(result)

        return report
