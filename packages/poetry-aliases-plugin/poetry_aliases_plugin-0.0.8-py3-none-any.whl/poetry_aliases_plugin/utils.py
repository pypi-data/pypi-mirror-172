from typing import Callable

from poetry_aliases_plugin import config


class PluginException(RuntimeError):
    def __str__(self) -> str:
        return f'{config.PLUGIN_NAME}: {self.args[0]}'


class PluginCommandException(PluginException):

    command: str

    def __init__(self, command: str, *args: object) -> None:
        self.command = command
        super().__init__(*args)

    def __str__(self) -> str:
        return f'{config.PLUGIN_NAME}: {self.command}: {self.args[0]}'


def plugin_exception_wrapper(func: Callable):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except PluginException as ex:
            raise ex

        except BaseException as ex:
            raise PluginException(ex) from ex

    return wrapper


def normalize_command(command: str) -> str:
    command = command.removeprefix('poetry').strip()
    command = command if command.startswith('run') else f'run {command}'
    return command.strip()
