"""
services/kernel_factory.py

Compatibility access point for the shared MAO kernel.
"""

from mao import MAOKernel
# ✅ FIXED - Use runtime proxy
from services.runtime import runtime


def create_kernel() -> MAOKernel:
    """
    Return the already initialized production kernel.
    """
    return runtime.kernel


def get_kernel() -> MAOKernel:
    """
    Return the shared MAO kernel instance.
    """
    return runtime.kernel