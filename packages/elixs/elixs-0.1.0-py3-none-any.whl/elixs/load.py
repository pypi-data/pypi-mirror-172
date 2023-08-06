#Copyright (C)2022  Elias Kremer, full license (GNU AGPLv3) in LICENSE.txt
from .errorhandlers import *

class ReadConfig:
    def __init__(self, configpath, file = "project.conf"):
        from os import path
        self.configpath = f'{configpath}/config/{file}'
        self.config = []

        if path.exists(self.configpath):
            configfile = open(self.configpath, "r")
            for line in configfile:
                x = line.strip()
                if x[:1] != "#" and x[:1] != "": self.config.append(x)
            configfile.close()
        else: raise LoadError(f'Config file not found at {self.configpath}')

    def getconfig(self, type = None):

        if type == "all" or type == None: return self.config

        elif type == "dsbcredentials":
            return {"username": self.config[0], "password": self.config[1]}

        elif type == "mySQL":
            return {"host": self.config[2], "username": self.config[3], "password": self.config[4], "dbname": self.config[5]}

        elif type == "logmode":
            return self.config[6]

        # elif type == "ci": #Controll Interface
        #     return {"port": int(self.config[10]),
        #             "password": self.config[11]}

        # elif type == "li": #Live Interface
        #     return {"port": int(self.config[12]),
        #             "password": self.config[13]}

        else: raise LoadError(f'Unknown argument "{str(type)}" for function getconfig()')

class mySQL:
    # configs is the ReadConfig object from above
    def __init__(self, configs):
        self.init(configs)

    def init(self, configs):
         import mysql.connector as sql
         self.InterfaceError = sql.errors.InterfaceError
         self.OperationalError = sql.errors.OperationalError

         credentials = configs.getconfig("mySQL")

         try: self.connection = sql.connect(host=credentials["host"],
                                            user=credentials["username"],
                                            passwd=credentials["password"])
         except Exception as er: raise mySQLError(er) from None

         self.cursor = self.connection.cursor()
         self.cursor.execute("SHOW DATABASES;")
         res = self.cursor.fetchall()
         res = [x for sublist in res for x in sublist]
         if not credentials["dbname"] in res: self.cursor.execute(f'CREATE DATABASE {credentials["dbname"]};')
         self.cursor.execute(f'use {credentials["dbname"]};')
         return

    def sendquery(self, query):
        try:
            self.cursor.execute(query)
        except self.OperationalError:
            try:
                self.close()
                self.init()
                self.cursor.execute(query)
            except self.OperationalError as er:
                self.crashreport = er
                res = False

        try:
            res = self.cursor.fetchall()
            self.multiline = res
            res = [x for sublist in res for x in sublist]
        except self.InterfaceError as er:
            self.crashreport = er
            self.multiline = None
            res = False

        return res

    def commit(self):
        self.connection.commit()

    def close(self):
        self.connection.commit()
        self.cursor.close()
        self.connection.close()

def version():
    return 4.5 #Generalized version of 4.1
