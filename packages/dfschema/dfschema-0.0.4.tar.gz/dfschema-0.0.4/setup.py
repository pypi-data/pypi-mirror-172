# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dfschema', 'dfschema.core', 'dfschema.core.legacy']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.2.4,<2.0.0', 'pydantic>=1.9.1,<2.0.0']

extras_require = \
{'all': ['sqlalchemy>=1.0.0,<2.0.0', 'typer>=0.6.1,<0.7.0', 'PyYAML>=6.0,<7.0'],
 'cli': ['typer>=0.6.1,<0.7.0'],
 'sqlalchemy': ['sqlalchemy>=1.0.0,<2.0.0'],
 'yaml': ['PyYAML>=6.0,<7.0']}

entry_points = \
{'console_scripts': ['dfs = dfs.cli:app']}

setup_kwargs = {
    'name': 'dfschema',
    'version': '0.0.4',
    'description': 'lightweight pandas.DataFrame schema',
    'long_description': '# DFS (aka Dataframe_Schema)\n\n**DFS** is a lightweight validator for `pandas.DataFrame`. You can think of it as a `jsonschema` for dataframe. \n\nKey features:\n1. **Lightweight**: only dependent on `pandas`  and `pydantic` (which depends only on `typing_extensions`)\n2. **Explicit**: inspired by `JsonSchema`, all schemas are stored as json (or yaml) files and can be generated or changed on the fly.\n3. **Simple**: Easy to use, no need to change your workflow and dive into the implementation details. \n4. **Comprehensive**: Summarizes all errors in a single summary exception, checks for distributions, works on subsets of the dataframe \n5. **Rapid**: base schemas can be generated from given dataframe or sql query (using `pd.read_sql`).\n6. **Handy**: Supports command line interface (with `[cli]` extra).\n7. **Extendable**: Core idea is to validate *dataframes* of any type. While now supports only pandas, we\'ll add abstractions to run same checks on different types of dataframes (CuDF, Dask, SparkDF, etc )\n\n## QuickStart\n\n### 1. Validate DataFrame\n\nVia wrapper\n```python\nimport pandas as pd\nimport dfschema as dfs\n\n\ndf = pd.DataFrame({\n  "a": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],\n  "b": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\n})\n\nschema_pass = {\n  "shape": {"min_rows": 10}\n}\n\nschema_raise = {\n  "shape": {"min_rows": 20}\n}\n\n\ndfs.validate(df, schema_pass)  # won\'t raise any issues\ndfs.validate(df, schema_raise) # will Raise DataFrameSchemaError\n```\nAlternatively (v2 optional), you can use the root class, `DfSchema`:\n```python\ndfs.DfSchema.from_dict(schema_pass).validate(df)  # won\'t raise any issues\ndfs.DfSchema.from_dict(schema_raise).validate(df)  # will Raise DataFrameSchemaError\n```\n\n### 2. Generate Schema\n\n```python\ndfs.DfSchema.from_df(df)\n```\n### 3. Read and Write Schemas\n  \n```python\nschema = dfs.DfSchema.from_json(\'schema.json\')\nschema.to_yaml("schema.yaml")\n```\n\n### 4. Using CLI\n> Note: requires [cli] extra as relies on `Typer` and `click`\n\n#### Validate via CLI\n```shell\ndfschema validate --read_kwargs_json \'{delimiter="|"}\' FILEPATH SCHEMA_FILEPATH\n```\nSupports\n- csv\n- xlsx\n- parquet\n- feather\n\n#### Generate via CLI\n```shell\ndfs generate --format \'yaml\' DATA_PATH > schema.yaml\n```\n\n## Installation\n\nWIP\n\n## Alternatives\n- [TableScheme](https://pypi.org/project/tableschema/)\n- [GreatExpectations](https://greatexpectations.io/). Large and complex package with Html reports, Airflow Operator, connectors, etc. an work on out-of-memory data, SQL databases, parquet, etc\n- [Pandera](https://pandera.readthedocs.io/en/stable/) - awesome package, great and suitable for type hinting, compatible with `hypothesis`\n  - [great talk](https://www.youtube.com/watch?v=PI5UmKi14cM)\n- [Tensorflow validate](https://www.tensorflow.org/tfx/guide/tfdv)\n- [DTF expectations](https://github.com/calogica/dbt-expectations)\n\n## Changes\n- [[changelog]]\n\n## Roadmap\n- [ ] Add tutorial Notebook\n- [ ] Support tableschema\n- [ ] Support Modin models\n- [ ] Support SQLAlchemy ORM models\n- [ ] Built-in Airflow Operator?\n- [ ] Interactive CLI/jupyter for schema generation',
    'author': 'Philipp',
    'author_email': 'philippk@zillowgroup.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7.1,<4.0',
}


setup(**setup_kwargs)
