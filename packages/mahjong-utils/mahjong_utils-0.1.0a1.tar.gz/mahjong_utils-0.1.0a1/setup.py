# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['mahjong_utils',
 'mahjong_utils.internal',
 'mahjong_utils.internal.utils',
 'mahjong_utils.models',
 'mahjong_utils.yaku']

package_data = \
{'': ['*']}

install_requires = \
['lazy>=1.5,<2.0', 'pydantic>=1.10.2,<2.0.0']

setup_kwargs = {
    'name': 'mahjong-utils',
    'version': '0.1.0a1',
    'description': '',
    'long_description': 'mahjong-utils\n========\n\n已实现功能：\n\n- [x] 获取番符对应和牌点数\n- [x] 向听数计算（包括K\\*3+1张牌和K\\*3+2张牌）\n- [x] 和了分析（役种、番数、符数）\n',
    'author': 'ssttkkl',
    'author_email': 'huang.wen.long@hotmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
