# DiscordBot

## Introduction
DiscordBot is a discord bot based on [discord.py](https://github.com/Rapptz/discord.py), utilizing dynamic import to find, intialize and register [Application Commands]() implemented as [Python classes](https://docs.python.org/3/tutorial/classes.html). This helps to further abstract boilerplate setup from the command implementation, allowing users to write modular commands and have them imported from a directory.

## Setup


## Packages

### Structure
A package, at minimum, is comprised of 2 facets:
- A [Python module](https://docs.python.org/3/tutorial/modules.html#modules) containing any number of [Component](#components) classes
- A [Requirements file](https://pip.pypa.io/en/stable/reference/requirements-file-format/) containing all dependencies required by the module

The requirements file is used to install dependencies ahead of time, as imports listed at the top are not installed automatically. Automated installation is not implemented for two reasons:
- Installing dependencies programmatically [can cause issues](https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program).
- Recursively installing lists of dependencies is what certain security-minded individuals might describe as "bad".

Any errors encountered during package import are logged, after which the current package import is skipped.

## Components
A Component is any module-scoped class object with asynchronous methods that have a [compatible method signature](#method-signature). The `Loader` class handles module-level execution, class initialization, and calling any implemented [lifecycle hooks](#lifecycle-hooks).

### Method Signature
The `Loader` class attempts to import all class members that are asynchronous methods, with the following exceptions:
- Method name follows the dunder/magic method naming convention.

These methods have a signature where the first (non-self) positional argument is a parameter of [discord.Interaction](https://discordpy.readthedocs.io/en/latest/interactions/api.html#interaction) type:
>```async def test_command(self, interaction: discord.Interaction, ...)```

Further positional and keyword arguments are used to add arguments to the application command. Supported argument types are limited to:
- [Text Sequence Types](https://docs.python.org/3/library/stdtypes.html#text-sequence-type-str)
- [Numeric Types](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)
- [discord.app_commands.Transformer](https://discordpy.readthedocs.io/en/latest/interactions/api.html#transformer)
- [discord.app_commands.Range](https://discordpy.readthedocs.io/en/latest/interactions/api.html#range)
- other applicable types provided by discord.app_commands

### Method Decorators
Most decorators included in [discord.app_commands](https://github.com/Rapptz/discord.py/tree/master/discord/app_commands) can be used to provide metadata about the command in the same way shown by the documentation:
- [describe](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=describe#discord.app_commands.describe)
- [rename](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=describe#discord.app_commands.rename)
- [choices](https://discordpy.readthedocs.io/en/latest/interactions/api.html?highlight=describe#discord.app_commands.choices)
- many others

### Lifecycle Hooks
Lifecycle hooks are dunder/magic methods that are called at key points in the command's lifecycle. The available hooks are as following:
| Hook Method | Async | Description |
| --- | --- | --- |
| `__init__` | No | Standard class initializer. First hook to be called. |
| `__setup__` | Yes | Called immediately after class initializer. Awaited or run in seperate thread, depending on availability of the [Event Loop](https://docs.python.org/3/library/asyncio-eventloop.html#event-loop). |