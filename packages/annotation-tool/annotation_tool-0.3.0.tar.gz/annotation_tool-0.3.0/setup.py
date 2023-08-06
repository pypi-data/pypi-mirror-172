# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['src',
 'src.annotation',
 'src.annotation.manual',
 'src.annotation.retrieval',
 'src.annotation.retrieval.retrieval_backend',
 'src.dataclasses',
 'src.dialogs',
 'src.media',
 'src.media.backend',
 'src.media.backend.type_specific_player',
 'src.network',
 'src.network.LARa',
 'src.qt_helper_widgets',
 'src.utility']

package_data = \
{'': ['*']}

modules = \
['main']
install_requires = \
['PyOpenGL',
 'distinctipy',
 'filetype',
 'matplotlib==3.5.0',
 'numpy',
 'opencv-python>=4.5.3.56,<4.6.0.0',
 'pyqtgraph==0.11.0',
 'scipy',
 'torch']

extras_require = \
{':sys_platform != "win32"': ['PyQt5>=5.14.2,<5.15.0'],
 ':sys_platform == "win32"': ['PyQt5>=5.15,<6.0']}

entry_points = \
{'console_scripts': ['annotation-tool = main:start']}

setup_kwargs = {
    'name': 'annotation-tool',
    'version': '0.3.0',
    'description': '',
    'long_description': '<div align="center">\n\n![](https://img.shields.io/badge/license-MIT-green)\n\n</div>\n\n# Installation\n\nAll stable versions can be installed from [PyPI](https://pypi.org/) by using [pip](https://pypi.org/project/pip/) or your favorite package manager\n\n    pip install annotation-tool\n\nYou can get pre-published versions from the [TestPyPI](https://test.pypi.org/project/annotation-tool/) repository by running\n\n    pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple/ annotation-tool\n\nAfter installation the annotation tool can be run as simple as\n\n    annotation-tool\n\n# Development\n\nFor installing the requirements you can use [poetry](https://python-poetry.org/). After you installed poetry just run\n\n    poetry install\n\nBuilding the executable requires [docker](https://www.docker.com/). After you installed docker on your system you can run one of\n\n    make build-linux\n    make build-windows\n\nto build the executables for linux or windows.\n',
    'author': 'Fernando Moya Rueda',
    'author_email': 'fernando.moya@cs.tu-dortmund.de',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4',
}


setup(**setup_kwargs)
