from abc import abstractmethod
from typing import Protocol

class Component(Protocol):
    """
    A protocol to be implemented by a class containing commands
    """

    @abstractmethod
    async def setup() -> None:
        """
        Defines an asynchronous routine to perform once the component
        has been initialized.
        """
        raise NotImplementedError()