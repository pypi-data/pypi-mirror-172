# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['verser', 'verser.common', 'verser.tests']

package_data = \
{'': ['*']}

install_requires = \
['rich>=12.5.1,<13.0.0']

setup_kwargs = {
    'name': 'verser',
    'version': '0.0.0.5',
    'description': 'Automatic next version number for your project, you may keep tracks history of your package.',
    'long_description': '\n# verser\n\n    from verser import Project, get_next_version\n\nVersion tracker for your python package\n\n### next version\n    project = Project(package_name="my_cool_package", default_version="0.0.0.0")\n\n    next_version = get_next_version(\n        project=project,\n        increment_=True,\n        pre_release=False,\n        verbose=True\n    )  \n    print(next_version)\n    # 0.0.0.1\n\n### pre release \n    project = Project(package_name="my_cool_package", default_version="0.0.0.0")\n\n    next_version = get_next_version(\n        project=project,\n        increment_=True,\n        pre_release=True ,\n        verbose=True\n    )  \n    print(next_version)\n    # 0.0.0.1rc1\n\n### creates __version__.py file with your new version\n    project = Project(package_name="my_cool_package", default_version="0.0.0.0")\n\n    next_version = get_next_version(\n        project=project,\n        increment_=True,\n        pre_release=True ,\n        verbose=True\n    )  \n    print(next_version)\n    # 0.0.0.1rc1',
    'author': 'Sermet Pekin',
    'author_email': 'sermet.pekin@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/SermetPekin/verser-repo',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
