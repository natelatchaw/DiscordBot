import importlib.util
import inspect
import logging
from asyncio import AbstractEventLoop, Task
from importlib.machinery import ModuleSpec
from pathlib import Path
import sys
from types import MethodType, ModuleType
from typing import Any, Coroutine, List, MutableMapping, Optional, Tuple, Type, TypeVar
from typing_extensions import TypeAlias

from discord.abc import Snowflake
from discord.app_commands import Command, CommandTree

from .component import Component, KWARGTYPE
from .settings import Settings


log: logging.Logger = logging.getLogger(__name__)

if sys.version_info < (3, 10):
    ELLIPSIS_TYPE: TypeAlias = Any
else:
    ELLIPSIS_TYPE: TypeAlias = ...

MAX_DESCRIPTION_LENGTH: int = 100
"""The maximum string length accepted for a description"""

DEFAULT_DOCSTRING: str = '…'
"""The string to use when docstring info is missing"""

TRUNCATOR: str = '…'
"""The string to use for docstring truncation"""

ReturnType = TypeVar('ReturnType')


class Loader():

    def __init__(self, tree: CommandTree, *, settings: Settings):
        #
        self._tree: CommandTree = tree
        self._settings: Settings = settings


    async def load(self, directory: Path, *args: Any, extension: str = 'py', loop: Optional[AbstractEventLoop] = None, **kwargs: KWARGTYPE) -> None:
        """
        Load package files from a directory.
        Failed package assemblies are logged as warning messages.
        """
        await self._process_directory(directory, extension=extension, loop=loop, *args, **kwargs)

    async def sync(self, *, guild: Optional[Snowflake] = None) -> None:
        """
        Syncs the underlying command tree to Discord.
        """

        # sync the command tree
        await self._tree.sync(guild=guild)

    async def clear(self, *, guild: Optional[Snowflake] = None) -> None:
        """
        Clears the underlying commmand tree.
        """

        # clear the command tree
        await self._tree.clear_commands(guild=guild)


    #region level processing

    async def _process_directory(self, directory: Path, *args: Any, extension: str = 'py', loop: Optional[AbstractEventLoop] = None, **kwargs: KWARGTYPE) -> None:
        try:
            # define the filename pattern to search for
            pattern: str = f'*.{extension}'
            # create the directory if it doesn't exist
            directory.mkdir(parents=True, exist_ok=True)
            # get all resolved paths for files with filenames matching the pattern in the provided directory
            file_objects: List[Path] = [path.resolve() for path in directory.glob(pattern) if path.is_file()]
        except KeyboardInterrupt: raise
        except Exception as exception:
            name: str = directory.name
            action: str = f'loading {directory.name}'
            log.warn(f'{name}: {exception.__class__.__name__} occurred {action}: {exception}')
            return

        for file_object in file_objects: await self._process_path(file_object, loop=loop, *args, **kwargs)

    async def _process_path(self, file_object: Path, *args: Any, loop: Optional[AbstractEventLoop] = None, **kwargs: KWARGTYPE) -> None:
        try:
            # get the module spec located at the reference
            spec: ModuleSpec = await self._get_module_spec(file_object)
            # create the module from the module spec
            module: ModuleType = await self._get_module(spec)
            # execute the module via the spec loader if available
            if spec.loader: spec.loader.exec_module(module)
            # retrieve all class objects from the module spec
            class_objects: List[Type[Component]] = await self._get_class_objects(module)
        except KeyboardInterrupt: raise
        except Exception as exception:
            name: str = file_object.name
            action: str = f'loading {file_object.name}'
            log.warn(f'{name}: {exception.__class__.__name__} occurred {action}: {exception}')
            return
        
        for class_object in class_objects: await self._process_class(class_object, loop=loop, *args, **kwargs)

    async def _process_class(self, class_object: Type[Component], *args: Any, loop: Optional[AbstractEventLoop] = None, **kwargs: KWARGTYPE) -> None:
        try:
            # initialize the class object
            instance: Component = await self._get_instance(class_object, *args, **kwargs)
            # perform setup on the instance
            await self._setup_instance(instance, loop=loop)
            # retrieve all coroutine objects from the instance
            coroutine_objects: List[MethodType] = await self._get_coroutine_objects(instance)
        except KeyboardInterrupt: raise
        except Exception as exception:
            name: str = class_object.__name__
            action: str = f'starting {class_object.__name__}'
            log.warn(f'{name}: {exception.__class__.__name__} occurred {action}: {exception}')
            return

        for coroutine_object in coroutine_objects: await self._process_coroutine(coroutine_object)

    async def _process_coroutine(self, coroutine_object: MethodType) -> None:
        try:
            # get a command from the coroutine
            command: Command[Any, ELLIPSIS_TYPE, Any] = await self._get_command(coroutine_object)
            # add the command to the command tree
            self._tree.add_command(command)
        except KeyboardInterrupt: raise
        except Exception as exception:
            name: str = coroutine_object.__qualname__
            action: str = f'loading {coroutine_object.__name__}'
            log.warn(f'{name}: {exception.__class__.__name__} occurred {action}: {exception}')
            return
        
    #endregion


    #region module level methods
        
    async def _get_module_spec(self, path: Path) -> ModuleSpec:
        """
        Retrieves the module spec from a file path.
        """

        try:
            # get the filename from the path
            filename: str = path.stem
            # get the module spec located at the reference
            spec: Optional[ModuleSpec] = importlib.util.spec_from_file_location(name=filename, location=path)
            # if no spec was found, continue
            if not spec: raise ValueError('No spec available for reference module.')
            # return the module spec
            return spec
        except Exception:
            raise    
    
    async def _get_module(self, spec: ModuleSpec) -> ModuleType:
        """
        Retrieves the module from a module spec.
        """
        
        try:
            # create the module from the module spec
            module: ModuleType = importlib.util.module_from_spec(spec)
            # return the module
            return module
        except Exception:
            raise

    async def _get_class_objects(self, module: ModuleType) -> List[Type[Component]]:
        """
        Retrieves all class objects from a module.

        Raises:
        - ImportError during `ModuleSpec.loader.exec_module`
        """
        try:
            # get all class members of the module
            module_members: List[Tuple[str, Type[Any]]] = inspect.getmembers(module, inspect.isclass)
            # get all class objects contained in the module
            class_objects: List[Type[Any]] = [class_object for class_name, class_object in module_members]
            # filter class objects without a matching module name
            class_objects = [class_object for class_object in class_objects if class_object.__module__ == module.__name__]
            # return all eligible class objects
            return [class_object for class_object in class_objects if isinstance(class_object, Component)]
        except Exception:
            raise

    #endregion
    
    
    #region class level methods
        
    async def _get_instance(self, class_object: Type[Component], *args: Any, **kwargs: KWARGTYPE) -> Component:
        """
        Initializes the provided class object and returns the created instance.
        """

        try:
            # get the configuration section for the class object
            configuration: MutableMapping = self._settings.application[class_object.__name__]
            # add a configuration section reference to the initializer kwargs 
            kwargs['config'] = configuration

            log.debug(f'{class_object.__name__}: Initializing instance')
            # initialize the class object
            instance: Component = class_object(*args, **kwargs)
            # return the instance
            return instance
        except Exception:
            raise

    async def _setup_instance(self, instance: Component, *args: Any, loop: Optional[AbstractEventLoop] = None, **kwargs: Any) -> None:
        """
        Performs setup on the provided Component instance.
        """

        try:
            # define message for logging purposes
            message: str = f'{instance.__class__.__name__}: An error occurred during {instance.__setup__.__name__}'

            log.debug(f'{instance.__class__.__name__}: Performing setup')
            # if an event loop was provided
            if loop:
                # wrap setup coroutine in exception handler
                awaitable: Coroutine[Any, Any, None] = self._log_exceptions(instance.__setup__(*args, **kwargs), message=message)
                # create a task for the coroutine
                _: Task[None] = loop.create_task(awaitable)
            # if an event loop was not provided
            else:
                log.warn(f'{instance.__class__.__name__}: No {Loader.__name__} event loop available. {instance.__setup__.__name__} will be awaited inline.')
                # call the setup coroutine
                await instance.__setup__(*args, **kwargs)
            return
        except Exception:
            raise

    async def _get_coroutine_objects(self, instance: Component) -> List[MethodType]:
        """
        Retrieves all coroutine objects from an instance.
        """

        try:
            # get all coroutine members of the instance
            instance_members: List[Tuple[str, MethodType]] = inspect.getmembers(instance, inspect.iscoroutinefunction)
            # get all coroutine objects contained in the instance
            coroutine_objects: List[MethodType] = [coroutine_object for coroutine_name, coroutine_object in instance_members]
            # filter coroutine objects that are private (prefixed by an underscore)
            coroutine_objects = [coroutine_object for coroutine_object in coroutine_objects if not coroutine_object.__name__.startswith('_')]
            # return all eligible coroutine objects
            return coroutine_objects
        except Exception:
            raise
    
    async def _log_exceptions(self, coroutine: Coroutine[Any, Any, ReturnType], message: Optional[str]) -> Optional[ReturnType]:
        try:
            return await coroutine
        except Exception as error:
            log.warn(f'{message}: {error}')
            raise
        
    #endregion
        
    
    #region coroutine level methods
        
    async def _get_command(self, coroutine: MethodType) -> Command[Any, ELLIPSIS_TYPE, Any]:
        """
        Register the provided coroutine as a command.
        """

        # get the command name
        name: str = coroutine.__name__
        # get the command description
        description: str = self._trim_docstring(coroutine)

        # initialize a command from the provided coroutine
        command: Command[Any, Any, Any] = Command(name=name, description=description, callback=coroutine)
        return command

    def _trim_docstring(self, obj: object, max_length: int = MAX_DESCRIPTION_LENGTH) -> str:
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
    
    #endregion


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
