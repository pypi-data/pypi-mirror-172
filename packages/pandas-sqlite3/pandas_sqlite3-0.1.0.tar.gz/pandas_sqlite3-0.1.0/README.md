
# Pandas Sqlite3

This project is to simplify the joining of pandas dataframes using Sqlite3. 
In the world of data science there are often two camps 1)Pandas and 2)SQL. 
We want to bring these worlds together by making it easier for those more 
familiar with SQL to manipulate Pandas dataframes within python. With Pandas Sqlite3
one can simply pass a list of Pandas dataframes, their names, and a Sqlite3 statement
to be executed. Enjoy :) 


## Authors

- [Hamilton Noel](https://www.github.com/noelham)



## Installation

Install my-project with pip

```bash
 pip install pandas_sqlite3
```
    
## Example Use


```python
import pandas as pd
from pandas_sqlite3.pandas_query import pandas_query

# create dataframes
sample_df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')

long_petal_df = sample_df.loc[sample_df['petal_length'] > 5].copy()

# write sql query
sql_query = """
                SELECT 
                        S.*
                FROM sample_df s
                JOIN long_petal_df USING ('sepal_length', 'sepal_width', 'petal_length', 'petal_width', 'species')
            """

# pass dataframes, their names, and SQL query to pandas_query function
final_df = pandas_query(dfs=[sample_df, long_petal_df], df_names=['sample_df', 'long_petal_df'], sql=sql_query)
```
## Contributing

Contributions are always welcome!

## License

[MIT](https://choosealicense.com/licenses/mit/)

## Acknowledgements

 - [Awesome Readme Templates](https://awesomeopensource.com/project/elangosundar/awesome-README-templates)
 - [Python Package to PyPI Using Poetry](https://towardsdatascience.com/how-to-effortlessly-publish-your-python-package-to-pypi-using-poetry-44b305362f9f)