# elixs.dev Standart Library

[![Build Status](https://travis-ci.org/)](https://travis-ci.org/)

Librarys includes:
- Config File Loader
- MySQL interface
- Logger

The library is public on GitHub and Licensed under GNU AGPLv3.
Contact me via EMail: eliservices.server@gmail.com

# Installation
```sh
pip install elixs
```

# Usage
```python
import elixs

config_obj = ReadConfig("/path/to/dir", "project.conf")
conf_array = config_obj.getconfig("all")

sql = mySQL(config_obj)
tables = sql.sendquery("SHOW TABLES;")
sql.sendquery("CREATE TABLE firsttable;")
sql.commit()
sql.close()

sqll = MySQLLogger(config_obj, "/path/to/dir")
sqll.create_table("people", [["name", "VARCHAR(10)"], ["age", "INTEGER"]])
sqll.write(beacon)
sqll.close()
```