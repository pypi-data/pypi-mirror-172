# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['poetry_aliases_plugin']

package_data = \
{'': ['*']}

install_requires = \
['poetry>=1.2.0']

entry_points = \
{'poetry.application.plugin': ['poetry-aliases-plugin = '
                               'poetry_aliases_plugin.plugin:PoetryAliasesApplicationPlugin']}

setup_kwargs = {
    'name': 'poetry-aliases-plugin',
    'version': '0.0.7',
    'description': 'Poetry plugin to run commands through aliases',
    'long_description': '# poetry-aliases-plugin\n\nPoetry plugin to run commands through aliases\n\n## Functionality\n\n- Запуск команд через псевдонимы\n  - Запуск\n  - Запуск множества команд разделенных `&&`\n  - Преобразование команд для запуска через poetry\n  - ~~Дополнение команд~~\n- ~~Добавление / Просмотр / Изменение / Удаление псевдонимов~~\n\n## Quick start\n\n```bash\npoetry self add poetry-aliases-plugin\npoetry alias this # ==> poetry run python -m this\npoetry this # ==> poetry run python -m this\n```\n\n## Dependencies\n\n```toml\n[tool.poetry.dependencies]\npython = ">=3.10"\npoetry = ">=1.2.0"\n```\n\nPS. Adaptation for earlier versions of python will someday appear\n\n## Install\n\n```bash\npoetry self add poetry-aliases-plugin\n\n# uninstall: poetry self remove poetry-aliases-plugin\n# but update: rm -r ~/.cache/pypoetry/{artifacts,cache} && poetry self update poetry-aliases-plugin\n```\n\n## Setup\n\nOn `0.N.N` version setup only in `pyproject.toml`:\n\n```toml\n[tool.aliases] # config dict, where key - alias, value - full command / commands with "&&"\nalias = "full command / commands with \'&&\'"\ntests = "poetry run pytest"\nrunserver = "poetry run python manage.py runserver"\n```\n\n## Use\n\nplugin command - "l"\n\n```bash\npoetry l --help\npoetry l tests # ==> poetry run pytest\npoetry l runserver # ==> poetry run python manage.py runserver\n```\n\n## Contribute\n\nIssue Tracker: <https://gitlab.com/rocshers/python/poetry-alias-plugin/-/issues>\nSource Code: <https://gitlab.com/rocshers/python/poetry-alias-plugin>\n',
    'author': 'irocshers',
    'author_email': 'develop.iam@rocshers.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rocshers/poetry-alias-plugin',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10',
}


setup(**setup_kwargs)
