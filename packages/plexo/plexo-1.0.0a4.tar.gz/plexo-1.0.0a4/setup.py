# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['plexo',
 'plexo.codec',
 'plexo.ganglion',
 'plexo.namespace',
 'plexo.neuron',
 'plexo.schema',
 'plexo.synapse',
 'plexo.typing']

package_data = \
{'': ['*']}

install_requires = \
['capnpy @ '
 'https://github.com/agates/capnpy/releases/download/0.9.1dev0/capnpy-0.9.1.dev0-cp310-cp310-manylinux_2_17_x86_64.manylinux2014_x86_64.manylinux_2_28_x86_64.whl',
 'pyrsistent>=0.18.0,<0.19.0',
 'python-jsonschema-objects>=0.4.1,<0.5.0',
 'pyzmq>=24.0.0,<25.0.0',
 'returns>=0.19.0,<0.20.0',
 'typing_extensions>=4.0,<5.0']

setup_kwargs = {
    'name': 'plexo',
    'version': '1.0.0a4',
    'description': 'Opinionated, reactive, schema-driven, distributed message passing',
    'long_description': '_This is a **highly experimental** project in a pre-alpha state.  Use at your own risk._\n',
    'author': 'Alecks Gates',
    'author_email': 'agates@mail.agates.io',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://gitlab.com/agates/pyplexo/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}
from build import *
build(setup_kwargs)

setup(**setup_kwargs)
