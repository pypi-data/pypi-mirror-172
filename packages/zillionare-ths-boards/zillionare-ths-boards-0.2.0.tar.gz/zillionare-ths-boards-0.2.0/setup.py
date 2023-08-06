# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['boards', 'tests']

package_data = \
{'': ['*']}

install_requires = \
['APScheduler>=3.9.1,<4.0.0',
 'akshare>=1.7.29,<2.0.0',
 'arrow>=1.2.3,<2.0.0',
 'fire==0.4.0',
 'httpx>=0.23.0,<0.24.0',
 'retry>=0.9.2,<0.10.0',
 'sanic>=22.6.2,<23.0.0',
 'zarr>=2.13.0,<3.0.0']

extras_require = \
{'dev': ['tox>=3.24.5,<4.0.0',
         'pip>=22.0.3,<23.0.0',
         'twine>=3.8.0,<4.0.0',
         'pre-commit>=2.17.0,<3.0.0',
         'toml>=0.10.2,<0.11.0'],
 'doc': ['mkdocs>=1.2.3,<2.0.0',
         'mkdocs-include-markdown-plugin>=3.2.3,<4.0.0',
         'mkdocs-material>=8.1.11,<9.0.0',
         'mkdocstrings>=0.18.0,<0.19.0',
         'mkdocs-autorefs>=0.3.1,<0.4.0',
         'mike>=1.1.2,<2.0.0'],
 'test': ['black>=22.3.0,<23.0.0',
          'isort==5.10.1',
          'flake8==4.0.1',
          'flake8-docstrings>=1.6.0,<2.0.0',
          'pytest>=7.0.1,<8.0.0',
          'pytest-cov>=3.0.0,<4.0.0']}

entry_points = \
{'console_scripts': ['boards = boards.cli:main']}

setup_kwargs = {
    'name': 'zillionare-ths-boards',
    'version': '0.2.0',
    'description': '同花顺行业板块及概念板块数据本地化',
    'long_description': '# boards\n\n\n<p align="center">\n<a href="https://pypi.org/pypi/zillionare-ths-boards">\n    <img src="https://img.shields.io/pypi/v/zillionare-ths-boards.svg"\n        alt = "Release Status">\n</a>\n\n<a href="https://github.com/zillionare/boards/actions">\n    <img src="https://github.com/zillionare/boards/actions/workflows/release.yml/badge.svg?branch=release" alt="CI Status">\n</a>\n\n<a href="https://zillionare.github.io/boards/">\n    <img src="https://img.shields.io/website/https/zillionare.github.io/boards/index.html.svg?label=docs&down_message=unavailable&up_message=available" alt="Documentation Status">\n</a>\n\n</p>\n\n\n同花顺概念板块与行业板块数据本地化项目\n\n\n* Free software: MIT\n* Documentation: <https://zillionare.github.io/boards/>\n\n\n## Features\n\n### 自动同步\n通过boards serve启动服务器之后，每日凌晨5时自动同步板块数据，并将其按当天日期保存。\n\n注意我们使用了akshare来从同花顺获取板块数据。akshare的相应接口并没有时间参数，也即，所有同步的板块数据都只能是最新的板块数据。但如果在当天5时之后，同花顺更新的板块数据，则更新的数据将不会反映在当天日期为索引的数据当中。\n\n### 板块操作\n提供了根据板块代码获取板块名字(get_name)、根据名字查代码(get_code)、根据名字进行板块名的模糊查找（fuzzy_match_board_name增）等功能。\n\n此外，我们还提供了filter方法，允许查找同时属于于多个板块的个股。\n\n### 获取新增加的概念板块\n新概念板块往往是近期炒作的热点。您可以通过ConceptBoard.find_new_concept_boards来查询哪些板块是新增加的。\n\n此功能对行业板块无效。\n\n### 获取新加入概念板块的个股\n对某个概念而言，新加入的个股可能是有资金将要运作的标志。通过ConceptBoard.new_members_in_board可以查询新加入某个概念板块的个股列表。\n\n### 命令行接口\n提供了命令行接口以启动和停止服务，以及进行一些查询，详情请见[][#]\n#### 查询同时处于某几个概念板块中的个股\n```\nboards filter --industry 计算机应用 --with-concpets 医药 医疗器械 --without 跨境支付\n```\n## 其他\nboards使用akshare来下载数据。下载速度较慢，且可能遇到服务器拒绝应答的情况。这种情况下，boards将会以退火算法，自动延迟下载速度重试5次，以保证最终能完全下载数据，且不被封IP。在此过程中，您可能看到诸如下面的信息输出，这是正常现象。\n```text\nDocument is empty, retrying in 30 seconds...\nDocument is empty, retrying in 30 seconds...\nDocument is empty, retrying in 30 seconds...\nDocument is empty, retrying in 60 seconds...\nDocument is empty, retrying in 120 seconds...\n```\n\n## Credits\n\nThis package was created with the [ppw](https://zillionare.github.io/python-project-wizard) tool. For more information, please visit the [project page](https://zillionare.github.io/python-project-wizard/).\n',
    'author': 'aaron yang',
    'author_email': 'aaron_yang@jieyu.ai',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/zillionare/boards',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
