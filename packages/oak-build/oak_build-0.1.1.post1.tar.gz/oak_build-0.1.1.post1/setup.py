# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['oak_build', 'oak_build.tools']

package_data = \
{'': ['*']}

install_requires = \
['colorlog>=6.7.0,<7.0.0', 'rusty-results>=1.1.1,<2.0.0', 'toposort>=1.7,<2.0']

entry_points = \
{'console_scripts': ['oak = oak_build.main:main']}

setup_kwargs = {
    'name': 'oak-build',
    'version': '0.1.1.post1',
    'description': '',
    'long_description': '# oak-build\n\nA make-like build system written on python\n\n\n## How to use\n\nCreate `oak_build.py` file in your project directory.\nEvery method marked with `@task` decorator can be called from CLI.\n\n```python\nfrom pathlib import Path\n\nfrom oak_build import task\n\n\n@task\ndef create_file():\n    with open(Path("result.txt"), "w") as txt:\n        txt.write("test content\\n")\n```\n\nTo execute `create_file` task call `oak create_file` from console.\n\n## Task dependencies\n\nYou can link dependent tasks with `depends_on` parameter.\n\n```python\nfrom oak_build import task, run\n\n\n@task\ndef unit_tests():\n    run("poetry run pytest tests")\n\n\n@task\ndef integration_tests():\n    run("poetry run pytest integration_tests")\n\n\n@task(\n    depends_on=[\n        unit_tests,\n        integration_tests,\n    ]\n)\ndef tests():\n    pass\n```\n\nWhen `oak tests` is called oak build will execute `unit_tests` and `integration_tests` tasks as well.\n\n## Examples\n\nFor examples see [integration tests files](integration_tests/resources) and self build [oak_file.py](oak_file.py).\n',
    'author': 'Kirill Sulim',
    'author_email': 'kirillsulim@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
