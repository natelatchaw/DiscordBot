from abc import abstractmethod
from typing import Any, MutableMapping, Protocol, TypedDict, Unpack, runtime_checkable


class Payload(TypedDict, total=False):
    """
    A TypedDict of kwargs to be provided to the Component 
    initializer.
    """

    config: MutableMapping[str, Any]
    """
    A dictionary-style configuration instance.
    Values stored here will be stored across runs.
    """


@runtime_checkable
class Component(Protocol):
    """
    A protocol to be implemented by a class containing 
    commands.
    """

    def __init__(self, *args: Any, **kwargs: Unpack[Payload]):
        raise NotImplementedError()

    @abstractmethod
    async def __setup__(self) -> None:
        """
        Defines an asynchronous routine to perform once the component
        has been initialized.
        """
        raise NotImplementedError()