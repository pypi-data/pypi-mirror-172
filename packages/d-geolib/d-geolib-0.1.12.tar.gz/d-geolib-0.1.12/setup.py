# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['geolib',
 'geolib.geometry',
 'geolib.models',
 'geolib.models.dfoundations',
 'geolib.models.dsettlement',
 'geolib.models.dsheetpiling',
 'geolib.models.dstability',
 'geolib.service',
 'geolib.soils']

package_data = \
{'': ['*'],
 'geolib.models': ['dfoundations/soil_csv/*',
                   'dfoundations/templates/*',
                   'dsettlement/templates/*',
                   'dsheetpiling/templates/*']}

install_requires = \
['jinja2>=3.1.2,<4.0.0',
 'pydantic[dotenv]>=1.6.1,<1.10',
 'requests>=2.24.0,<3.0.0',
 'zipp>=3.1.0,<4.0.0']

extras_require = \
{'server': ['fastapi>=0.58,<0.79', 'uvicorn>=0.11,<0.19']}

entry_points = \
{'console_scripts': ['geolib_server = geolib.service.main:app']}

setup_kwargs = {
    'name': 'd-geolib',
    'version': '0.1.12',
    'description': 'Python wrappers around the input and output files of the Deltares D-Serie models',
    'long_description': 'GEOLib\n=============================\n\nGEOLib is a Python package to generate, execute and parse several D-Serie numerical models.\n\nInstallation\n------------\n\nInstall GEOLib with:\n\n.. code-block:: bash\n\n    $ pip install d-geolib\n\n\nRequirements\n------------\n\nTo install the required dependencies to run GEOLib code, run:\n\n.. code-block:: bash\n\n    $ pip install -r requirements\n\nOr, when having poetry installed (you should):\n\n.. code-block:: bash\n\n    $ poetry install\n\n\nTesting & Development\n---------------------\n\nMake sure to have the server dependencies installed: \n\n.. code-block:: bash\n\n    $ poetry install -E server\n\nIn order to run the testcode, from the root of the repository, run:\n\n.. code-block:: bash\n\n    $ pytest\n\nor, in case of using Poetry\n\n.. code-block:: bash\n\n    $ poetry run pytest\n\nRunning flake8, mypy is also recommended. For mypy use:\n\n.. code-block:: bash\n\n    $ mypy --config-file pyproject.toml geolib\n\n\nDocumentation\n-------------\n\nIn order to run the documentation, from the root of the repository, run:\n\n.. code-block:: bash\n\n    $ cd docs\n    $ sphinx-build . build -b html -c .\n\n\nThe documentation is now in the `build` subfolder, where you can open \nthe `index.html` in your browser.\n\nBuild wheel\n-----------\n\nTo build a distributable wheel package, run:\n\n.. code-block:: bash\n\n    $ poetry build\n\nThe distributable packages are now built in the `dist` subfolder.',
    'author': 'Maarten Pronk',
    'author_email': 'maarten.pronk@deltares.nl',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://deltares.github.io/GEOLib/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
