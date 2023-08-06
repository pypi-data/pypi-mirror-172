# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pandas_sqlite3']

package_data = \
{'': ['*']}

install_requires = \
['pandas>=1.5.1,<2.0.0']

setup_kwargs = {
    'name': 'pandas-sqlite3',
    'version': '0.1.0',
    'description': '',
    'long_description': '\n# Pandas Sqlite3\n\nThis project is to simplify the joining of pandas dataframes using Sqlite3. \nIn the world of data science there are often two camps 1)Pandas and 2)SQL. \nWe want to bring these worlds together by making it easier for those more \nfamiliar with SQL to manipulate Pandas dataframes within python. With Pandas Sqlite3\none can simply pass a list of Pandas dataframes, their names, and a Sqlite3 statement\nto be executed. Enjoy :) \n\n\n## Authors\n\n- [Hamilton Noel](https://www.github.com/noelham)\n\n\n\n## Installation\n\nInstall my-project with pip\n\n```bash\n pip install pandas_sqlite3\n```\n    \n## Example Use\n\n\n```python\nimport pandas as pd\nfrom pandas_sqlite3.pandas_query import pandas_query\n\n# create dataframes\nsample_df = pd.read_csv(\'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv\')\n\nlong_petal_df = sample_df.loc[sample_df[\'petal_length\'] > 5].copy()\n\n# write sql query\nsql_query = """\n                SELECT \n                        S.*\n                FROM sample_df s\n                JOIN long_petal_df USING (\'sepal_length\', \'sepal_width\', \'petal_length\', \'petal_width\', \'species\')\n            """\n\n# pass dataframes, their names, and SQL query to pandas_query function\nfinal_df = pandas_query(dfs=[sample_df, long_petal_df], df_names=[\'sample_df\', \'long_petal_df\'], sql=sql_query)\n```\n## Contributing\n\nContributions are always welcome!\n\n## License\n\n[MIT](https://choosealicense.com/licenses/mit/)\n\n## Acknowledgements\n\n - [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)\n - [Python Package to PyPI Using Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f)',
    'author': 'hamilton',
    'author_email': 'hamilton@pattern.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8',
}


setup(**setup_kwargs)
