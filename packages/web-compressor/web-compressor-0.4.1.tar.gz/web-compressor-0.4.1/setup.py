# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['web_compressor', 'web_compressor.cli', 'web_compressor.handlers']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4,<5']

extras_require = \
{'cli': ['click>=8,<9', 'tomli-w>=1,<2', 'xdg>=5,<6'],
 'cli:python_version < "3.11"': ['tomli>=2,<3'],
 'images': ['Pillow>=9,<10', 'pillow-avif-plugin>=1.2,<2.0'],
 'minify': ['tdewolff-minify>=2,<3']}

entry_points = \
{'console_scripts': ['webcompr = web_compressor.cli:cli']}

setup_kwargs = {
    'name': 'web-compressor',
    'version': '0.4.1',
    'description': 'Supercharges HTML files & web assets',
    'long_description': "# WebCompressor\n\nSupercharge HTML files & web assets - ideal for improving 'static site generator' output\n\n## Getting started\n\n## Configuration\n\n## Roadmap\n\n- [ ] Update `README.md`\n- [x] Add tests\n- [x] Add more tests\n- [x] Add even more tests\n",
    'author': 'Digitalbüro',
    'author_email': 'post@digitalbuero.eu',
    'maintainer': 'Martin Folkers',
    'maintainer_email': 'hello@twobrain.io',
    'url': 'https://digitalbuero.eu',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
