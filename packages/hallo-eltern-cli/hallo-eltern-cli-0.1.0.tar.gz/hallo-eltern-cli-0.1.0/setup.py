# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['hallo_eltern_cli', 'hallo_eltern_cli.commands']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.17.0,<3.0.0']

entry_points = \
{'console_scripts': ['hallo-eltern-cli = hallo_eltern_cli.cli:run',
                     'hallo-eltern4email = hallo_eltern_cli.cli4email:run']}

setup_kwargs = {
    'name': 'hallo-eltern-cli',
    'version': '0.1.0',
    'description': "A command-line/Python/email interface for Education Group GmbH's 'Hallo!Eltern' App for Upper-Austrian schools.",
    'long_description': '# hallo-eltern-cli\n\n`hallo-eltern-cli` is a command-line/Python/email interface for\n[Education Group GmbH](https://www.edugroup.at/)\'s\n"[Hallo!Eltern](https://hallo-eltern.klassenpinnwand.at/)" application\nfor Upper-Austrian schools.\n\n`hallo-eltern-cli` is not affiliated with Education Group GmbH or the\n"Hallo!Eltern" Application in any way. "Hallo!Eltern" Application is a\nproduct of the Education Group GmbH.\n\n`hallo-eltern-cli` allows to list, messages, read them, download\nattachments, etc directly from your Linux terminal and allows to get\nfull messages including attachments directly to your local inbox.\n\n## Table of Contents\n\n1. [Installation](#installation)\n1. [CLI Commands](#cli-commands)\n1. [Email Integration](#email-integration)\n\n## Installation\n\nOn a Linux-like system with a recent Python (`>=3.7`) run:\n\n```\n# Install Python\'s "requests" library:\nsudo apt-get install python3-requests\n\n# Clone this repo:\ngit clone https://github.com/somechris/hallo-eltern-cli\n\n# Switch to the cloned repo:\ncd hallo-eltern-cli\n\n# Configure your credentials:\n./halloelterncli.py config --email YOUR-EMAIL@EXAMPLE.ORG --password YOUR-PASSWORD\n\n# Done. \\o/\n\n# You can now use the hallo-eltern-cli\n# E.g.: List your messages:\n./halloelterncli.py list\n[...]\n\nFlags |   Id    | Subject\n---------------------------------------------------\n CC   | 1234567 | Wandertag am Donnerstag\n CC   | 3456789 | Schikurs Anmeldung\n  C   | 2345678 | Fehlendes Arbeitsblatt\n```\n\n## CLI commands\n\nThe CLI offers the following commands:\n\n* `list` lists available messages\n* `show` shows a message\n* `open` marks a message as open\n* `close` marks a message as closed\n* `config` updates and dumps the configuration\n* `test` tests the configured user againts the API\n\n## Email integration\n\n`hallo-eltern-cli` comes with `halloeltern4email.py` which allows to\nformat messages as emails (containing the full message\'s text and\nattachments) and submit them to a mail delivery agent (MDA,\ne.g. `procmail`). To run it for example 12 minutes into every hour,\nsimply add a crontab entry like:\n\n```\n12 * * * * /path/to/hallo-eltern-cli/halloeltern4email.py --mode=procmail\n```\n',
    'author': 'Christian Aistleitner',
    'author_email': 'christian@quelltextlich.at',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/somechris/hallo-eltern-cli',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6',
}


setup(**setup_kwargs)
