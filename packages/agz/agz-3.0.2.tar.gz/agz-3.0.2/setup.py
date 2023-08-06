from setuptools import setup, find_packages

requirements = ['requests']
readme = """
## AGZ Library

**This is fast and easy library for making rubika self bots**

## Example
``` python
from agz.rubika import Bot
from agz.socket import _Socket

auth = "Auth Acount"
socket , bot = _Socket(auth) , Bot(auth)

for msg in agz.handler():
    guid = socket.object_guid(msg)
    user = socket.author_object_guid(msg)
    msg_id = socket.message_id(msg)
    guid_type = socket.guid_type(msg)
    action = socket.action(msg)
    text = socket.text(msg)
    print(text)

    if text == "hello":
        bot.sendMessage(guid , "hi" , msg_id)
```

### Installing

``` bash
pip3 install agz
```

© 2022 Ali Ganji zadeh
"""

setup(
    name = 'agz',
    version = '3.0.2',
    author='Ali Ganji zadeh',
    author_email = 'yb.windows.plus@gmail.com',
    description = 'This is fastest library for deploying robots on Rubika accounts.',
    keywords = ["agz","agz lib","agz-lib","library","rubikalib","rubika","bot","robot"],
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
