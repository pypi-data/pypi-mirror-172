#Copyright (C)2022  Elias Kremer, full license (GNU AGPLv3) in LICENSE.txt
from .errorhandlers import *
from datetime import datetime, date
strptime = datetime.strptime

class MySQLLogger:
    def __init__(self, config_obj, path):
        from .load import ReadConfig, mySQL
        from .logger import Logger

        self.logging = Logger(config_obj = config_obj, path = path, short = "SQLL", name = "db.log")
        self.keyerrorlogging = Logger(config_obj = config_obj, path = path, name = "keyerror.log")
        self.mysql = mySQL(config_obj)
        self.stats = 0
        self.logging.append("DB ready...")

    def create_table(self, name = "people", col = [["name", "VARCHAR(10)"], ["age", "INTEGER"]]):
        if name == "currentdate": name = str(date.today()).replace("-","_")
        self.name = name
        self.col = col

        query = f'CREATE TABLE IF NOT EXISTS {name} ('
        for pair in col:
            query += f'{pair[0]} {pair[1]},'
        query = query[:-1] + ");"

        self.mysql.sendquery(query)
        self.logging.append(f'Created table {name}')
        return

    def write(self, beacon, col = "standart", name = "standart"):
        if col == "standart": col = self.col
        if name == "standart": name = self.name
        self.verify(beacon)
        try:
            query = f'INSERT INTO {name} VALUES ('
            for pair in col:
                if pair[1] == "DATETIME":
                    try: query += f'"{strptime(str(beacon[pair[0]]), "%d.%m.%Y %H:%M")}",'
                    except ValueError: query += f'"{strptime(str(beacon[pair[0]]), "%d.%m.%Y")}",'
                else:
                    query += f'"{str(beacon[pair[0]])}",'
            query = query[:-1] + ");"
        except KeyError as e:
            self.keyerrorlogging.append(e)
            return False
        except TypeError as e:
            self.keyerrorlogging.append(e)
            return False

        self.mysql.sendquery(query)
        self.mysql.commit()
        self.stats += 1
        return True

    def verify(self, beacon):
        import sys
        for key in beacon.keys():
            if '"' in beacon[key]: beacon[key] = beacon[key].replace('"', "\\\"")
        return True

    def close(self):
        self.mysql.commit()
        self.mysql.close()
        self.logging.append("Wrote " + str(self.stats) + " rows to MySQL.")
        self.logging.append("DB closed.")
        self.logging.close()
        return True

def version():
    return "sqllogger.py: 1.6"
