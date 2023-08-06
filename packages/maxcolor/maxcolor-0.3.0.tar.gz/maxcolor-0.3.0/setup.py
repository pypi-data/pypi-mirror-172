# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['maxcolor']
install_requires = \
['rich[all]>=12.6.0,<13.0.0']

entry_points = \
{'console_scripts': ['gradient_panel = maxcolor.maxcolor:gradient_panel',
                     'rainbow = maxcolor.maxcolor:rainbow']}

setup_kwargs = {
    'name': 'maxcolor',
    'version': '0.3.0',
    'description': 'Helper scripts to print gradient text.',
    'long_description': '# MaxColor\n\n## Based of Rich by Textualize\n\n## Installation\nEasy to install right from PyPi.\n\n\n### Pipx\n\n```bash\npipx install maxcolor\n```\n\n### Pip\n\n```bash\npip install maxcolor\n```\n\n### Poetry\n\n```bash\npoetry add maxcolor\n```\n\n## Usage\n\n```python\nfrom maxcolor import console, rainbow, gradient_panel, progress\n\nconsole.print(\n    rainbow("Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in."\n    )\n)\n\nconsole.print(\n    gradient_panel(\n        "Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in. Fugiat veniam labore aliquip nostrud incididunt elit cupidatat occaecat quis deserunt do eu sit consectetur dolore. Aute excepteur laboris sunt. Laborum culpa incididunt pariatur ut adipisicing proident in ex adipisicing cupidatat consequat exercitation reprehenderit. Veniam sint esse velit in.",\n        "Max Color\'s Gradient Panel"\n    )\n)\n',
    'author': 'Max Ludden',
    'author_email': 'dev@maxludden.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
