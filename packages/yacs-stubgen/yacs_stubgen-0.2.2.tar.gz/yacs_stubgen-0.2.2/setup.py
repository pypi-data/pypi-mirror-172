# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['yacs_stubgen']

package_data = \
{'': ['*']}

install_requires = \
['yacs>=0.1.4,<0.2.0']

entry_points = \
{'console_scripts': ['yacstub = genstub:main']}

setup_kwargs = {
    'name': 'yacs-stubgen',
    'version': '0.2.2',
    'description': 'Generate stub file for yacs config.',
    'long_description': '# yacs-stubgen\n\nAdd typing support for your YACS config by generating stub file.\n\n[![python](https://img.shields.io/pypi/pyversions/yacs-stubgen?logo=python&logoColor=white)][home]\n[![version](https://img.shields.io/pypi/v/yacs-stubgen?logo=python)][pypi]\n[![workflow](https://github.com/JamzumSum/yacs-stubgen/actions/workflows/test-pub.yml/badge.svg)](https://github.com/JamzumSum/yacs-stubgen/actions/workflows/test-pub.yml)\n\n![screencap](assets/screencap.gif)\n\n## Install\n\nInstall from PyPI:\n\n```sh\npip install yacs-stubgen\n```\n\n<details>\n\n<summary>Other methods</summary>\n\nInstall from this repo directly:\n\n```sh\npip install git+https://github.com/JamzumSum/yacs-stubgen.git\n```\n\nOr you can download from our GitHub release and install package manually.\n\n</details>\n\n## Usage\n\n### Auto-Generate\n\nAdd typing support for your [yacs][yacs] config by appending just three lines:\n\n```py\nfrom yacs.config import CfgNode as CN\n\n_C.MODEL.DEVICE = \'cuda\'\n...\n# your config items above\n\n# this line can be moved to the import header\nfrom yacs_stubgen import build_pyi\n# this alias ensure you can import `AutoConfig` and use something like `isinstance`\nAutoConfig = CN\n# _C is the CfgNode object, "_C" should be its varname correctly\n# AutoConfig is an alias of CfgNode, "AutoConfig" should be its varname correctly\nbuild_pyi(_C, __file__, cls_name=\'AutoConfig\', var_name=\'_C\')\n```\n\n**After** any run/import of this file, a stub file (*.pyi) will be generated.\nThen you will get typing and auto-complete support **if your IDE supports stub files**.\n\nEach time you change your config, you have to run/import this file again to apply the changes.\n\n### Build Script\n\nWe have provided a script as an entrypoint. Simply run `yacstub <file/dir>` and it\nwill generate stub file if one module contains a `CfgNode` object in global scope.\n\n```sh\n> yacstub ./conf    # specify a directory\nINFO: Generated conf/default.pyi\n> yacstub ./conf/default.py # specify a file\nINFO: Generated conf/default.pyi\n```\n\nSimilarly, each time you change the config, you have to re-run the script to apply the changes.\n\n## How it works\n\n<details>\n\n**Stub files take precedence** in the case of both `filename.py` and `filename.pyi` exists.\nOnce you pass in the config node, we will iterate over it and generate a stub file then save\nit as `filename.pyi` (that\'s why a path is required). Now supporting IDE will detect the stub\nfile and is able to type-check and intellisense your code.\n\nHowever, the stub file does nothing with actual code executing. If you import the generated\nclass (default as "AutoConfig"), an `ImportError` will be raised. This time you can add a variable\n(aka. type alias) refers to `CfgNode` in the `*.py` file. We will override the type of this alias\nto our generated class ("AutoConfig") in the stub file. Thus you can import the "AutoConfig"\nnormally and intuitively, while the type alias is treated as "AutoConfig" by IDE but is actually a `CfgNode` type.\n\n</details>\n\n## License\n\n- [MIT](LICENSE)\n- [yacs][yacs] is under [Apache-2.0](https://github.com/rbgirshick/yacs/LICENSE)\n\n[yacs]: https://github.com/rbgirshick/yacs\n[home]: https://github.com/JamzumSum/yacs-stubgen\n[pypi]: https://pypi.org/project/yacs-stubgen\n',
    'author': 'JamzumSum',
    'author_email': 'zzzzss990315@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/JamzumSum/yacs-stubgen',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6.2,<4.0.0',
}


setup(**setup_kwargs)
