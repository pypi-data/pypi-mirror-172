from poetry.core.pyproject.toml import PyProjectTOML

PLUGIN_NAME = 'poetry-version-plugin'


class AliasesConfig(object):
    """Обертка над конфигурацией pyproject"""

    pyproject: PyProjectTOML

    def __init__(self, pyproject: PyProjectTOML) -> None:
        self.pyproject = pyproject

    @property
    def _common_raw_aliases(self):
        return {'this': 'poetry run python -m this'}

    @property
    def _default_raw_aliases(self):
        return {'this': 'poetry run python -m this'}

    @property
    def aliases(self) -> dict:
        aliases = self.pyproject.data.get('tool', {}).get('aliases', self._default_raw_aliases)
        return self._common_raw_aliases | aliases
