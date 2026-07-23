"""
services/kernel_factory.py

Compatibility access point for the shared MAO kernel.
"""

from mao import MAOKernel
from services.runtime import kernel


def create_kernel() -> MAOKernel:
    """
    Return the already initialized production kernel.
    """

    return kernel



def get_kernel() -> MAOKernel:
    """
    Return the shared MAO kernel instance.
    """

    return kernel