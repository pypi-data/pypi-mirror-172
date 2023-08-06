from __future__ import annotations

from cleo.helpers import argument
from poetry.console.commands.command import Command

from poetry_aliases_plugin import utils
from poetry_aliases_plugin.aliases import AliasesSet
from poetry_aliases_plugin.config import AliasesConfig
from poetry_aliases_plugin.triggers import TriggerCommand


class BaseAliasCommand(Command):
    @property
    def aliases_config(self):
        return AliasesConfig(self.poetry.pyproject)

    def exec_command(self, command: str):
        try:
            self.call('run', command)

        except PermissionError as ex:
            if ex.errno == 13:
                raise utils.PluginException(f'У процесса poetry недостаточно прав для запуска программы: {ex.filename}')

            raise ex

        raise utils.PluginException('Так быть не должно...')

    @property
    def trigger_command(self):
        raise NotImplementedError()

    @utils.plugin_exception_wrapper
    def handle(self) -> None:
        aliases_set = AliasesSet.from_raw(self.aliases_config.aliases)
        target_aliases = aliases_set.get_target_aliases(self.trigger_command)

        for alias in target_aliases:
            for command in alias.commands:
                self.exec_command(command)


class PreAliasCommand(BaseAliasCommand):
    name = 'alias'

    arguments = [argument('alias', 'Registered alias')]

    @property
    def description(self):
        return 'Run aliases. Available: {0}'.format(', '.join(list(self.aliases_config.aliases)))

    @property
    def trigger_command(self):
        return TriggerCommand(self.argument('alias'))


class AliasCommand(BaseAliasCommand):
    name = 'for_aliases'
    description = 'Run aliases without poetry parent command'

    arguments = [argument('alias', 'Registered alias')]

    @property
    def aliases(self):
        return list(self.aliases_config.aliases)

    @property
    def trigger_command(self):
        return TriggerCommand(self.argument('self.argument("alias")'))
