from abc import abstractmethod
from typing import Any, MutableMapping, Protocol, TypedDict, runtime_checkable
from typing_extensions import TypeAlias, Unpack, Required


class Payload(TypedDict, total=False):
    """
    A TypedDict of kwargs to be provided to the Component 
    initializer.
    """

    config: Required[MutableMapping[str, Any]]
    """
    A dictionary-style configuration instance.
    Values stored here will be stored across runs.
    """
    
KWARGTYPE: TypeAlias = Unpack[Payload] # type: ignore


@runtime_checkable
class Component(Protocol):
    """
    A protocol to be implemented by a class containing 
    commands.
    """

    def __init__(self, *args: Any, **kwargs: KWARGTYPE):
        raise NotImplementedError()

    @abstractmethod
    async def __setup__(self) -> None:
        """
        Defines an asynchronous routine to perform once the component
        has been initialized.
        """
        raise NotImplementedError()