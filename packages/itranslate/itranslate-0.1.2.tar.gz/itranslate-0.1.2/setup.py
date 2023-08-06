# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['itranslate']

package_data = \
{'': ['*']}

install_requires = \
['httpx>=0.18.2,<0.19.0', 'joblib>=1.0.1,<2.0.0', 'logzero>=1.7.0,<2.0.0']

setup_kwargs = {
    'name': 'itranslate',
    'version': '0.1.2',
    'description': 'Google translate free and unlimited, itranslate since gtranslate is taken',
    'long_description': '# stranslate\n[![tests](https://github.com/ffreemt/google-stranslate/actions/workflows/routine-tests.yml/badge.svg)](https://github.com/ffreemt/google-stranslate/actions)[![python](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)](https://img.shields.io/static/v1?label=python+&message=3.7%2B&color=blue)[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)[![PyPI version](https://badge.fury.io/py/itranslate.svg)](https://badge.fury.io/py/itranslate)\n\nGoogle translate free and unlimited access, `stranslate` because gtranslate is taken\n\n## Install it\n\n```shell\npip install itranslate\n\n# or pip install git+https://github.com/ffreemt/google-itranslate\n# or use poetry\n# poetry add itranslate\n# poetry add git+https://github.com/ffreemt/google-itranslate\n\n# to upgrade:\npip install itranslate -U\n\n# or poetry add itranslate@latest\n```\n\n## Use it\n\nThe quality from this service is not as good as web google translate. There is nothing we can do about it.\n\nIt\'s unclear whether your ip will be blocked if you relentlessly use the service. Please feedback should you find out any information.\n\n```python\nfrom itranslate import itranslate as itrans\n\nitrans("test this and that")  # \'测试这一点\'\n\n# new lines are preserved, tabs are not\nitrans("test this \\n\\nand test that \\t and so on")\n# \'测试这一点\\n\\n并测试这一点等等\'\n\nitrans("test this and that", to_lang="de")  # \'Testen Sie das und das\'\nitrans("test this and that", to_lang="ja")  # \'これとそれをテストします\'\n```\nFor those who cannot access google translate, a temporary solution has been implemented. Set `cf` (it stands for cloudflare) to True, e.g.,\n```\nitrans("test this and that", to_lang="de", cf=True) \n```\n\nText longer than 5000 characters will be trimmed to 5000. Hence for a long document, you may try something like the following or similar.\n```python\nfrom textwrap import wrap\nfrom itranslate import itranslate as itrans\n\nlong_doc = """ long long text formatted with \\n and so on"""\ntr_doc = " ".join([itrans(elm) for elm in wrap(long_doc,\n    width=5000,\n    break_long_words=False,\n    break_on_hyphens=False,\n    drop_whitespace=False,\n    replace_whitespace=False,\n)])\n```\n\n### `async version`: `atranslate`\nIf you feel so inclined, you may use the async version of itranslate ``atranslate``:\n```python\nimport asyncio\nfrom itranslate import atranslate as atrans\n\ntexts = ["test this", "test that"]\ncoros = [atrans(elm) for elm in texts]\n\nloop = asyncio.get_event_loop()\n\ntrtexts = loop.run_until_complete(asyncio.gather(*coros))\n\nprint(trtexts)\n# [\'测试这一点\', \'测试\']\n```\n\n### Proxy support\n```\nitrans("test this and that", proxies="http://localhost:8030")\n```\nor\n```python\nproxies = {\n    "http": "http://localhost:8030",\n    "https": "http://localhost:8031",\n}\nitrans("test this and that\\n another test", proxies=proxies)\n```\n\n`itranslate` uses ``httpx`` to fetch contents and inherits ``httpx``\'s proxy mechanism. Check [https://www.python-httpx.org/advanced/](https://www.python-httpx.org/advanced/) for other ways of setting up proxies.\n\n## Other google translate related repos\nMuch more sophisticated than `itranslate`\n*   [https://github.com/ssut/py-googletrans](https://github.com/ssut/py-googletrans) [![](https://img.shields.io/github/stars/ssut/py-googletrans)](https://github.com/ssut/py-googletrans)\n*   [https://github.com/nidhaloff/deep-translator](https://github.com/nidhaloff/deep-translator) [![](https://img.shields.io/github/stars/nidhaloff/deep-translator)](https://github.com/nidhaloff/deep-translator)\n\n*   [https://github.com/mouuff/mtranslate](https://github.com/mouuff/mtranslate) [![](https://img.shields.io/github/stars/mouuff/mtranslate)](https://github.com/mouuff/mtranslate)\n*   [https://github.com/lushan88a/google_trans_new](https://github.com/lushan88a/google_trans_new) [![https://github.com/lushan88a/google_trans_new](https://img.shields.io/github/stars/lushan88a/google_trans_new)](https://github.com/lushan88a/google_trans_new)\n*   [https://github.com/Animenosekai/translate](https://github.com/Animenosekai/translate) [![https://github.com/Animenosekai/translate](https://img.shields.io/github/stars/Animenosekai/translate)](https://github.com/Animenosekai/translate)\n\n## Disclaimer\n``google-stranslate`` makes use of a translate interface floating around the net and is for study and research purpose only. The interface may become invalid without notice, which would of course render the package totally unusable.\n',
    'author': 'ffreemt',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ffreemt/google-stranslate',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
