# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['matflow', 'matflow.data']

package_data = \
{'': ['*']}

install_requires = \
['hpcflow-new2>=0.2.0a7,<0.3.0']

extras_require = \
{'pyinstaller': ['pyinstaller>=5.5,<6.0']}

entry_points = \
{'console_scripts': ['matflow = matflow.cli:MatFlow.CLI'],
 'pyinstaller40': ['hook-dirs = pyinstaller.__init__:get_hook_dirs']}

setup_kwargs = {
    'name': 'matflow-new',
    'version': '0.3.0a5',
    'description': 'Computational workflows for materials science',
    'long_description': '<img src="https://docs.matflow.io/stable/_static/images/logo-90dpi.png" width="250" alt="MatFlow logo"/>\n\n**Design, run, and share computational materials science workflows**\n\nDocumentation: [https://matflow.io/docs](https://matflow.io/docs)\n\n## Acknowledgements\n\n\nMatFlow was developed using funding from the [LightForm](https://lightform.org.uk/) EPSRC programme grant ([EP/R001715/1](https://gow.epsrc.ukri.org/NGBOViewGrant.aspx?GrantRef=EP/R001715/1))\n\n<img src="https://lightform-group.github.io/wiki/assets/images/site/lightform-logo.png" width="150"/>\n',
    'author': 'aplowman',
    'author_email': 'adam.plowman@manchester.ac.uk',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<3.11',
}


setup(**setup_kwargs)
