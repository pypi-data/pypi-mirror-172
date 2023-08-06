# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

modules = \
['opPrint']
install_requires = \
['PyYAML>=6.0,<7.0']

setup_kwargs = {
    'name': 'opprint',
    'version': '1.0.2',
    'description': 'Override print formatter',
    'long_description': "## installation ##\n```\npython3 -m pip install opprint\n```\n\n## usage ##\nop(***arg***, ***var***=None, ***format***=False, ***yml***=False)\n```\nfrom opPrint import op\ngreeting = 'hello world!'\n\n# basic\nop(greeting)\n\n# with label\nop('op says...', greeting)\n\n# with standard format\nop(greeting, format=True)\n\n# with yaml format\nop(greeting, format=True, yml=True)\n\n# with all params\nop('op says...', greeting, format=True, yml=True)\n```\n",
    'author': 'rapid537',
    'author_email': 'rapid537@zoho.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/rapid537/op.git',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
