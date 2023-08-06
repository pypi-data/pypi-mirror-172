from setuptools import (setup, find_packages,)

requirements = ['requests']
readme = """
## AGZ

**This is fast and easy library for making rubika self bots**

## Example
``` python
from AGZ.Socket.AGZ_Socket import _Socket
from AGZ.Lib.AGZ_lib import Bot

auth = "Auth Acount"
agz , bot = _Socket(auth) , Bot(auth)

for msg in agz.handler():
    guid = agz.object_guid(msg)
    user = agz.author_object_guid(msg)
    msg_id = agz.message_id(msg)
    guid_type = agz.guid_type(msg)
    action = agz.action(msg)
    text = agz.text(msg)
    print(text)

    if text == "hello":
        bot.sendMessage(guid , "hi" , msg_id)
```

### Installing

``` bash
pip3 install AGZ
```

© 2022 Ali Ganji zadeh
"""

setup(
    name = 'AGZ',
    version = '3.0.4',
    author='Ali Ganji zadeh',
    author_email = 'yb.windows.plus@gmail.com',
    description = 'This is an unofficial library and fastest library for deploying robots on Rubika accounts.',
    keywords = ["agz","bot","robot","library","rubikalib","rubika","agz lib","agz-lib"],
    long_description = readme,
    python_requires="~=3.7",
    long_description_content_type = 'text/markdown',
    url = 'https://github.com/aliexers',
    packages = find_packages(),
    install_requires = requirements,
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'License :: OSI Approved :: MIT License',
        'Topic :: Internet',
        'Topic :: Communications',
        'Topic :: Communications :: Chat',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Libraries :: Application Frameworks'
    ],
)
