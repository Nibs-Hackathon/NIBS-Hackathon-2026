from typing import Any


class MemoryManager:
    """
    Shared runtime memory for the MAO Kernel.

    This is NOT the vector database.
    This is NOT PostgreSQL.

    It is simply a shared in-memory state that allows
    agents to exchange information during execution.
    """

    def __init__(self):
        self._memory: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        """Store a value."""
        self._memory[key] = value

    def get(self, key: str, default=None):
        """Retrieve a value."""
        return self._memory.get(key, default)

    def delete(self, key: str) -> None:
        """Delete a value."""
        self._memory.pop(key, None)

    def exists(self, key: str) -> bool:
        """Check if a key exists."""
        return key in self._memory

    def clear(self) -> None:
        """Clear all memory."""
        self._memory.clear()

    def all(self) -> dict[str, Any]:
        """Return the full memory dictionary."""
        return self._memory.copy()