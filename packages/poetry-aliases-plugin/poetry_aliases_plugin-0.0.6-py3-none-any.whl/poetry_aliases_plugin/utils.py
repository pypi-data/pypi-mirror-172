from typing import Callable

from poetry_aliases_plugin import config


class PluginException(RuntimeError):
    def __str__(self) -> str:
        return f'{config.PLUGIN_NAME}: {super().__str__()}'


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
