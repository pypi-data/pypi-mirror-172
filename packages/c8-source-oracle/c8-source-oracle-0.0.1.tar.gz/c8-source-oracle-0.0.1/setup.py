# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['c8_source_oracle', 'c8_source_oracle.sync_strategies']

package_data = \
{'': ['*']}

install_requires = \
['c8connector==0.0.5', 'pipelinewise-singer-python==1.2.0']

entry_points = \
{'console_scripts': ['c8-source-oracle = c8_source_oracle:main']}

setup_kwargs = {
    'name': 'c8-source-oracle',
    'version': '0.0.1',
    'description': 'Pipelinewise tap for reading from oracle databases. This includes support for PDBs.',
    'long_description': '# c8-source-oracle\n\n[![License: MIT](https://img.shields.io/badge/License-GPLv3-yellow.svg)](https://opensource.org/licenses/GPL-3.0)\n\n[Singer](https://www.singer.io/) tap that extracts data from a [Oracle](https://www.oracle.com/database/) database and produces JSON-formatted data following the [Singer spec](https://github.com/singer-io/getting-started/blob/master/docs/SPEC.md).\n\n## How to use it\n\nRun and configuration of this [Singer Tap](https://singer.io) depends of the desired replication mode (INCREMENTAL or STREAMING)\n\n\n## Prerequisites : Create user on targeted PDB\n\nConnect to CDB, then switch to targetted PDB\n\n```\nSQL> show con_name\n\nCON_NAME\n------------------------------\nCDB$ROOT\n\n\nSQL> alter session set container=wms17;\n\nSession altered.\n\nSQL> show con_name\n\nCON_NAME\n------------------------------\nWMS17\n```\n\nTap-Oracle user need to be created with the following rights on DB :\n\n* CREATE_SESSION system privilege\n```\ngrant CREATE SESSION to singer_user;\n```\n* SELECT right on  V_$DATABASE\n```\ngrant select on V_$DATABASE to singer_user;\n```\n\nYou can also grant select on table to singer, table by table or via SELECT ANY TABLE privilege (up to you)\n\n* SELECT ANY TABLE system privilege\n```\ngrant SELECT ANY TABLE to singer_user;\n```\n\n## Log based replication\n\nTap-Oracle Log-based replication requires some configuration changes in Oracle database:\n\n* Enable `ARCHIVELOG` mode\n\n* Set retention period a reasonable and long enough period, ie. 1 day, 3 days, etc.\n\n* Enable Supplemental logging\n\n### Setting up Log-based replication on a self hosted Oracle Database: \n\nTo verify the current archiving mode, if the result is `ARCHIVELOG`, archiving is enabled:\n```\n  SQL> SELECT LOG_MODE FROM V$DATABASE\n```\n\nTo enable `ARCHIVELOG` mode (if not enabled yet):\n```\n  SQL> SHUTDOWN IMMEDIATE\n  SQL> STARTUP MOUNT\n  SQL> ALTER DATABASE ARCHIVELOG\n  SQL> ALTER DATABASE OPEN\n```\n\nTo set retention period, use RMAN:\n```\n  RMAN> CONFIGURE RETENTION POLICY TO RECOVERY WINDOW OF 1 DAYS;\n```\n\nTo enable supplemental logging:\n```\n  SQL> ALTER DATABASE ADD SUPPLEMENTAL LOG DATA (ALL) COLUMNS\n```\n\n\n### Install and Run\n\nFirst, make sure Python 3 is installed on your system or follow these\ninstallation instructions for [Mac](http://docs.python-guide.org/en/latest/starting/install3/osx/) or\n[Ubuntu](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-ubuntu-16-04).\n\n\nIt\'s recommended to use a virtualenv:\n\n```bash\n  python3 -m venv venv\n  pip install extended-tap-oracle\n```\n\nor\n\n```bash\n  python3 -m venv venv\n  . venv/bin/activate\n  pip install --upgrade pip\n  pip install .\n```\n\n### Configuration\n\nRunning the the tap requires a `config.json` file. \n\nExample with the minimal settings:\n\n```json\n  {\n    "host": "foo.com",\n    "port": 1521,\n    "user": "my_user",\n    "password": "password",\n    "sid": "ORCL",\n    "filter_schemas": "HR" # Lets get only the HR sample schema\n  }\n```\n\nYou can run a discover run using the previous `config.json` file to acquire all the tables definition\n \n```\ntap-oracle --config /tmp/config.json --discover >> /tmp/catalog.json\n```\n\nThen use the catalog.json to run a full export:\n\n```\ntap-oracle --config /tmp/config.json --catalog /tmp/catalog.json\n```\n\n',
    'author': 'Macrometa',
    'author_email': 'info@macrometa.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://www.macrometa.com/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
