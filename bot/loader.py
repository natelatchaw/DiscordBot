import asyncio
import importlib.util
import inspect
import logging
from asyncio import AbstractEventLoop
from importlib.machinery import ModuleSpec
from pathlib import Path
from types import MethodType, ModuleType
from typing import Any, Awaitable, Coroutine, List, MutableMapping, Optional, Tuple, Type

from discord.abc import Snowflake
from discord.app_commands import Command, CommandTree

from .settings import Settings

log: logging.Logger = logging.getLogger(__name__)

MAX_DESCRIPTION_LENGTH: int = 100
"""The maximum string length accepted for a description"""

DEFAULT_DOCSTRING: str = '…'
"""The string to use when docstring info is missing"""

TRUNCATOR: str = '…'
"""The string to use for docstring truncation"""


class Loader():

    def __init__(self, tree: CommandTree, *, settings: Settings):
        #
        self._tree: CommandTree = tree
        self._settings: Settings = settings

    async def load(self, directory: Path, extension: str = 'py', loop: Optional[AbstractEventLoop] = None, *args: Any, **kwargs: Any):
        """
        Load package files from a directory.
        Failed package assemblies are logged as warning messages.
        """

        # resolve the provided directory path
        directory = directory.resolve()
        # if the provided directory doesn't exist, create it
        if not directory.exists(): directory.mkdir(parents=True, exist_ok=True)

        # define the filename pattern to search for
        pattern: str = f'*.{extension}'
        # get all resolved paths for files with filenames matching the pattern in the provided directory
        references: List[Path] = [reference.resolve() for reference in directory.glob(pattern) if reference.is_file()]

        # for each module reference
        for reference in references:
            # handle module initialization
            try:
                # get the module spec located at the reference
                spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location(reference.stem, reference)
                # if no spec was found, continue
                if not spec: raise Exception('No spec available for reference module.')
                # retrieve all class objects from the module spec
                class_objects: List[Type] = await self.__import_classes__(spec)

                # for each class object
                for class_object in class_objects:
                    # handle class initialization
                    try:
                        # add reference to application-specific configuration section to the kwargs
                        kwargs['config']: MutableMapping = self._settings.application[class_object.__name__]
                        # initialize the class object
                        instance: object = class_object(*args, **kwargs)
                        # call instance setup hooks
                        await self.__call_hooks__(instance, ['__setup__'], loop=loop)
                        # retrieve all coroutines from the instance
                        method_objects: List[MethodType] = await self.__import_coroutines__(instance)

                        # for each method object
                        for method_object in method_objects:
                            # handle coroutine registration
                            try:
                                # add the coroutine as a command
                                await self.__register_coroutine__(method_object)

                            except KeyboardInterrupt: return
                            # catch method object initialization errors
                            except Exception as error:
                                log.error(f'{method_object.__name__}: {error}')

                    except KeyboardInterrupt: return
                    # catch class object initialization errors
                    except TypeError as error:
                        log.debug(f'Ignoring class {class_object.__name__}: Initialization failed: {error}')
                    except Exception as error:
                        log.debug(f'Ignoring class {class_object.__name__}: Initialization failed; unhandled {error.__class__.__name__}: {error}')
            
            except KeyboardInterrupt: return
            # catch module reference initialization errors
            except NameError as error:
                log.debug(f'Ignoring module {reference.name}: Initialization failed; error in module source: {error}')
            except ModuleNotFoundError as error:
                log.debug(f'Ignoring module {reference.name}: Initialization failed; dependency unavailable: {error}')
            except Exception as error:
                log.debug(f'Ignoring module {reference.name}: Initialization failed; unhandled {error.__class__.__name__}: {error}')


    async def sync(self, *, guild: Optional[Snowflake] = None) -> None:
        """
        Syncs the underlying command tree to Discord.
        """

        # sync the command tree
        await self._tree.sync(guild=guild)


    async def __call_hooks__(self, instance: object, hooks: List[str], loop: Optional[AbstractEventLoop]) -> None:
        """
        Call specified coroutine hooks for the provided instance
        """

        # log setup start
        log.info(f'Calling setup hooks for {instance.__class__.__name__}')
        # get all coroutines in the instance
        members: List[Tuple[str, MethodType]] = inspect.getmembers(instance, inspect.iscoroutinefunction)
        # get all members with a name contained in the hook list
        hook_coroutines: List[MethodType] = [member_object for member_name, member_object in members if member_name in hooks]
        # define args
        args: List[Any] = []
        # define kwargs
        kwargs: dict[str, Any] = { }

        # call each hook
        for hook_coroutine in hook_coroutines:
            # wrap in try block to prevent hook coroutine from cancelling further hooks
            try:
                # if the event loop is available
                if loop:
                    # assemble source string
                    source: str = '.'.join([instance.__class__.__name__, hook_coroutine.__name__])
                    # wrap hook coroutine in exception handler
                    awaitable: Coroutine[Any, Any, Any] = self.__log_exceptions__(hook_coroutine(*args, **kwargs), source=source)
                    # call the hook via a created task
                    _: asyncio.Task[Any] = loop.create_task(awaitable)
                # if the event loop is not available
                else:
                    # call the hook and await the call
                    await hook_coroutine(*args, **kwargs)
            
            # catch exceptions raised by hook
            except Exception as error:
                log.error(f'{instance.__class__.__name__}.{hook_coroutine.__name__}: {error}')



    async def __import_classes__(self, spec: ModuleSpec) -> List[Type]:
        """
        Retrieves all class objects from a file reference.

        Raises:
        - ImportError during `ModuleSpec.loader.exec_module`
        """

        # create the module from the module spec
        module: ModuleType = importlib.util.module_from_spec(spec)
        # execute the module via the spec loader if available
        if spec.loader: spec.loader.exec_module(module)
        # get all class members of the module
        members: List[Tuple[str, Type]] = inspect.getmembers(module, inspect.isclass)
        # filter members without a matching module name
        members = [(member_name, member_object) for member_name, member_object in members if member_object.__module__ == module.__name__]
        # return class objects
        return [member_object for member_name, member_object in members]


    async def __import_coroutines__(self, instance: Any) -> List[MethodType]:
        """
        Retrieves all coroutine objects from a class instance
        """

        # get all method members of the instance
        members: List[Tuple[str, MethodType]] = inspect.getmembers(instance, inspect.iscoroutinefunction)
        # filter members that start with a double underscore
        members = [(member_name, member_object) for member_name, member_object, in members if not member_name.startswith('__')]
        # return coroutine function objects
        return [member_object for member_name, member_object in members]


    async def __register_coroutine__(self, coroutine: MethodType):
        """
        Register the provided coroutine as a command
        """

        # get the command name
        name: str = coroutine.__name__
        # get the command description
        description: str = self.__trim_docstring__(coroutine)

        # initialize a command from the provided coroutine
        command: Command = Command(name=name, description=description, callback=coroutine)
        # add the command to the tree
        self._tree.add_command(command)


    def __trim_docstring__(self, obj: object, max_length: int = MAX_DESCRIPTION_LENGTH) -> str:
        """
        Trims and cleans the provided object's docstring to the provided length
        """

        # fallback to DEFAULT_DOCSTRING if __doc__ string is empty or missing
        docstring: str = obj.__doc__ if obj.__doc__ else DEFAULT_DOCSTRING
        # clean the docstring
        docstring = inspect.cleandoc(docstring)
        # get the max length for text truncation
        length: int = max_length - len(TRUNCATOR)
        # determine if the docstring exceeds the maximum description length
        exceeds_max_length: bool = len(docstring) > max_length
        # truncate docstring if necessary
        return docstring[:length] + TRUNCATOR if exceeds_max_length else docstring


    async def __log_exceptions__(self, awaitable: Awaitable[Any], source: Optional[str]) -> Any:
        try:
            return await awaitable
        except Exception as error:
            log.warn(f'{source}: {error}')


class HandlerError(Exception):
    """Base exception class for handler related errors."""
    
    def __init__(self, message: str, exception: Optional[Exception] = None):
        self._message = message
        self._inner_exception = exception
        self.__traceback__ = exception.__traceback__ if exception else None


    def __str__(self) -> str:
        return self._message


class HandlerLoadError(HandlerError):
    """Raised when an exception occurs while loading handler inputs."""

    def __init__(self, reference: Path, exception: Optional[Exception] = None):
        message: str = f'Failed to load {reference}: {exception}'
        super().__init__(message, exception)


class MissingCommandError(HandlerError):
    """Raised when a command name could not be determined from the message."""

    def __init__(self, exception: Optional[Exception] = None):
        message: str = f'Could not determine a command from the message.'
        super().__init__(message, exception)


class HandlerExecutionError(HandlerError):
    """Raised when an exception occurs during command execution."""

    def __init__(self, command_name: str, exception: Optional[Exception] = None):
        message: str = f'An exception occurred while executing command \'{command_name}\': {exception}'
        super().__init__(message, exception)
        

class HandlerLookupError(HandlerError):
    """Raised when a command cannot be looked up by command name."""

    def __init__(self, command_name: str, exception: Optional[Exception] = None):
        message: str = f'Lookup for command \'{command_name}\' failed.'
        super().__init__(message, exception)
