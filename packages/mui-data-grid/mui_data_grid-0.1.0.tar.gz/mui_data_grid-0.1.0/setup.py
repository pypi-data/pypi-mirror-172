# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['mui',
 'mui.integrations',
 'mui.integrations.flask',
 'mui.v5',
 'mui.v5.grid',
 'mui.v5.grid.filter',
 'mui.v5.grid.link',
 'mui.v5.grid.sort']

package_data = \
{'': ['*']}

install_requires = \
['pydantic>=1,<2']

setup_kwargs = {
    'name': 'mui-data-grid',
    'version': '0.1.0',
    'description': "Unofficial backend utilities for using Material-UI's X-Data-Grid component",
    'long_description': '# MUI Data Grid\n\nThis is an unofficial toolbox to make integrating a Python web application with Material UI\'s data grid simpler.\n\n## Documentation\n\n- [Material-UI Data Grid](https://mui.com/x/react-data-grid/)\n\n## Requirements\n\n- Python 3.10+\n\n## Installation\n\n### Pip\n\n```sh\npython -m pip install -U mui-data-grid\n```\n\nor with extras:\n\n```sh\npython -m pip install -U mui-data-grid[flask]\n```\n\n### Poetry\n\n```sh\npoetry add mui-data-grid\n```\n\n## Usage\n\n### Integrations\n\n#### Flask\n\n```python\n#!/usr/bin/env python\n# examples/main.py\n\nfrom flask import Flask, jsonify\nfrom flask.wrappers import Response\n\nfrom mui.integrations.flask import (\n    grid_filter_model_from_request,\n    grid_sort_model_from_request,\n)\n\napp = Flask(__name__)\n\n\n@app.route("/")\ndef print_sorted_details() -> Response:\n    sort_model = grid_sort_model_from_request(key="sort_model[]")\n    filter_model = grid_filter_model_from_request(key="filter_model")\n    return jsonify({\n            # sort_model is a list[GridSortItem]\n            "sort_model[]": [model.dict() for model in sort_model],\n            # filter_model is GridFilterModel\n            "filter_model": filter_model.dict()\n    })\n\n\nif __name__ == "__main__":\n    app.run()\n```\n',
    'author': 'Kevin Kirsche',
    'author_email': 'kev.kirsche@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
