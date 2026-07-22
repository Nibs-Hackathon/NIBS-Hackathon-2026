from mao import MAOKernel

from mao.workflows.pressure_workflow import PressureWorkflow
from mao.workflows.temperature_workflow import TemperatureWorkflow
from mao.workflows.gas_workflow import GasWorkflow
from mao.workflows.flow_workflow import FlowWorkflow
from mao.workflows.maintenance_workflow import MaintenanceWorkflow


def create_kernel():

    kernel = MAOKernel()

    kernel.register_workflow(
        PressureWorkflow()
    )

    kernel.register_workflow(
        TemperatureWorkflow()
    )

    kernel.register_workflow(
        GasWorkflow()
    )

    kernel.register_workflow(
        FlowWorkflow()
    )

    kernel.register_workflow(
        MaintenanceWorkflow()
    )


    return kernel