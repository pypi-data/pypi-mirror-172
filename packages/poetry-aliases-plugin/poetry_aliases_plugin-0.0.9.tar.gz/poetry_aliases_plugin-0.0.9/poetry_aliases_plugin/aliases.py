from __future__ import annotations


from poetry_aliases_plugin import utils
from poetry_aliases_plugin.triggers import TriggerCommand

RawAlias = str | dict[str, str | bool]


class Alias(object):

    commands: list[str]

    def __init__(self, command_raw: str) -> None:
        if command_raw is None:
            raise TypeError('Alias command data must have the key "command"')

        self.commands = [utils.normalize_command(command) for command in command_raw.split('&&')]

    @classmethod
    def from_raw(cls, raw_alias: RawAlias) -> Alias:
        if isinstance(raw_alias, str):
            return cls(raw_alias)

        if isinstance(raw_alias, dict):
            return cls(raw_alias.get('command'))

        raise TypeError(f'Alias command must be str or dict, not {type(raw_alias)}')


class AliasesSet(object):
    """Множество списков"""

    aliases: dict[str, Alias]

    def __init__(self, aliases: dict[str, Alias]) -> None:
        self.aliases = aliases

    @classmethod
    def from_raw(cls, raw_aliases: dict[str, RawAlias]) -> AliasesSet:
        aliases = {alias_key: Alias.from_raw(raw_alias) for alias_key, raw_alias in raw_aliases.items()}
        return cls(aliases)

    def get_target_aliases(self, trigger: TriggerCommand) -> list[Alias]:
        if trigger.alias not in self.aliases:
            raise utils.PluginException(f'alias "{trigger.alias}" not found')

        return [self.aliases[trigger.alias]]
