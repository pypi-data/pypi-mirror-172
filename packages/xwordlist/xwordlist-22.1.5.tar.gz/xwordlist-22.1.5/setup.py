# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['xwordlist']
install_requires = \
['anyascii==0.3.1',
 'beautifulsoup4==4.11.1',
 'configargparse==1.5.3',
 'prompt-toolkit==3.0.20',
 'requests==2.28.1']

setup_kwargs = {
    'name': 'xwordlist',
    'version': '22.1.5',
    'description': 'Software to help create, build and organize crossword puzzle word lists',
    'long_description': '# xwordlist\n\n`xwordlist` is a command line Python program designed to help you create, build and organize crossword puzzle word lists. As I started to think about constructing crossword puzzles with heavy themes — trying to make the entire puzzle themed, not just three or four long entries — I realized that I would need the ability to acquire and organize large amounts of text on very specific topics. After hacking around with a combination of search-and-replace text editors and Excel, I realized I needed to build someting more custom and thus `xwordlist` was born. \n\nBesides helping with basic text functions such as deduping, alphabetizing and changing case, this program is able to pull content out of structured web pages and parse large blocks of text, including lists of web pages with similarly structured content. Although I first started using the software to grab the lyrics of songs, I have added regex and better html parsing functionality to make it easier to get data from Wikipedia and less structured sites.\n\nFor more information, see the project’s main website hosted at [xwl.ist](https://xwl.ist). For an example of a themed 5x5 mini puzzle built with a word list assembled using this software, see [my personal website](https://quid.pro/xwords/tom-petty-mini/).\n\n## Installation\n\nFor now, you are mostly on your own if you wish to install `xwordlist`. After making sure your Python is up-to-date and you have activated a virtual environment (see [Installing Python Packages](https://packaging.python.org/en/latest/tutorials/installing-packages/) for helpful instructions on that), you can copy the `xwordlist` code to your local working environment by either cloning this repository or downloading the [zip archive](https://github.com/aanker/xwordlist/archive/refs/heads/main.zip). To install the dependencies required to make `xwordlist` work, use your terminal program to find the directory in which you have copied the files and type\n```\npython3 -m pip install -r requirements.txt\n```\nTo run the program, type\n```\npython3 xwordlist.py\n```\nIf you need more instructions than that, you might be better off waiting until the project is further along. If you have comments or questions beyond what is provided on this site, please refer to the main [GitHub repository](https://github.com/aanker/xwordlist) and feel free to email me or open an [issue](https://github.com/aanker/xwordlist/issues) if you have further questions.\n\n## Usage\n\nFor quick help instructions on the command line, type\n```\npython3 xwordlist.py --help\n```\nPlease see the [project’s main website](https://xwl.ist) for more information about using the software including a [basic example](https://xwl.ist/help/#basic-example), [recipes for common patterns](https://xwl.ist/resources/#recipes) and a [reference](https://xwl.ist/help/#list-of-available-options) to all options.\n\n## License\n\nThis software is available as open source under the terms of the [MIT License](http://opensource.org/licenses/MIT).\n',
    'author': 'Andrew Anker',
    'author_email': 'aa@quid.pro',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
