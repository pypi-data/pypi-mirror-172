# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': '.'}

packages = \
['amis']

package_data = \
{'': ['*'], 'amis': ['templates/*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0', 'pydantic>=1.10.2,<2.0.0', 'ujson>=5.4.0,<6.0.0']

setup_kwargs = {
    'name': 'amis-python',
    'version': '1.0.0',
    'description': '基于百度amis前端框架的python pydantic模型封装。',
    'long_description': "## amis-py\n基于[百度amis](https://github.com/baidu/amis)前端框架的python pydantic模型封装。\n\n由于[原版本](https://github.com/amisadmin/fastapi_amis_admin/tree/master/fastapi_amis_admin/amis)缺少大量amis新版本的组件，因此本项目在其版本的基础上进行了扩充。\n\n相比fastapi-amis-admin的版本：\n- 涵盖amis截至2.3.1版本的所有组件\n- 使用jinja2模板\n- 支持修改主题\n## 安装\n```\npip install amis-py\n```\n## 简单使用\n```python\nfrom amis_py.components import Page\n\npage = Page(title='新页面', body='Hello World')\n# 输出为python字典\nprint(page.to_dict())\n# 输出为json\nprint(page.to_json())\n# 输出为str\nprint(page.render())\n# 保存为html文件\nwith open('HelloWorld.html', 'w', encoding='utf-8') as f:\n    f.write(page.render())\n```\n\n## 详细使用\n详见[amis官方文档](https://aisuda.bce.baidu.com/amis/zh-CN/docs/index)\n\n## 感谢\n- [amis](https://github.com/baidu/amis)\n- [fastapi-amis-admin](https://github.com/amisadmin/fastapi_amis_admin/tree/master/fastapi_amis_admin/amis)\n",
    'author': '惜月',
    'author_email': '277073121@qq.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/CMHopeSunshine/amis-py',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
