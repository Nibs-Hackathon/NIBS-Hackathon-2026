"""
services/kernel_factory.py

Creates and caches the global MAO kernel instance.

The kernel is initialized only once and all production workflows
are registered automatically.
"""

from __future__ import annotations

import logging
from functools import lru_cache

from mao import MAOKernel
from mao.workflows.flow_workflow import FlowWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow
from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.temperature_workflow import TemperatureWorkflow

logger = logging.getLogger(__name__)


@lru_cache(maxsize=1)
def create_kernel() -> MAOKernel:
    """
    Create and return the singleton MAO kernel.

    The kernel is cached so the entire application
    shares a single workflow registry.
    """

    logger.info("Initializing MAO Kernel...")

    kernel = MAOKernel()

    workflows = [
        PressureWorkflow(),
        TemperatureWorkflow(),
        GasWorkflow(),
        FlowWorkflow(),
        MaintenanceWorkflow(),
    ]

    for workflow in workflows:
        kernel.register_workflow(workflow)
        logger.info(
            "Registered workflow: %s",
            workflow.__class__.__name__,
        )

    logger.info(
        "MAO Kernel initialized with %d workflows.",
        len(workflows),
    )

    return kernel