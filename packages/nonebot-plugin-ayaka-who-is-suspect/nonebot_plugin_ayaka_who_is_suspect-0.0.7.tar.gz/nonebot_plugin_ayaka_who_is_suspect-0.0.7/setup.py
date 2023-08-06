# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

modules = \
['ayaka_who_is_suspect']
install_requires = \
['nonebot-adapter-onebot>=2.1.3,<3.0.0',
 'nonebot-plugin-ayaka>=0.3.5,<0.4.0',
 'nonebot2>=2.0.0b5,<3.0.0']

setup_kwargs = {
    'name': 'nonebot-plugin-ayaka-who-is-suspect',
    'version': '0.0.7',
    'description': '谁是卧底',
    'long_description': '# 谁是卧底 0.0.7\n\n基于ayaka开发的 谁是卧底 小游戏\n\n任何问题请发issue\n\n<b>注意：由于更新pypi的readme.md需要占用版本号，因此其readme.md可能不是最新的，强烈建议读者前往[github仓库](https://github.com/bridgeL/nonebot-plugin-ayaka-who-is-suspect)以获取最新版本的帮助</b>\n\n\n# How to start\n\n## 安装 ayaka\n\n安装 [前置插件](https://github.com/bridgeL/nonebot-plugin-ayaka) \n\n`poetry add nonebot-plugin-ayaka`\n\n\n## 安装 本插件\n\n安装 本插件\n\n`poetry add nonebot-plugin-ayaka-who-is-suspect`\n\n修改nonebot2  `bot.py` \n\n```python\nnonebot.load_plugin("ayaka_who_is_suspect")\n```\n\n## 导入数据\n\n将本仓库的data文件夹，放到nonebot的工作目录下\n\n之后运行nonebot即可\n',
    'author': 'Su',
    'author_email': 'wxlxy316@163.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/bridgeL/nonebot-plugin-ayaka-who-is-suspect',
    'package_dir': package_dir,
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
