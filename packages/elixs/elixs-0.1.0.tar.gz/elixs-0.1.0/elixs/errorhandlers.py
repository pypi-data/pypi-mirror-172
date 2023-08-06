class LoadError(Exception):
    pass

class mySQLError(Exception):
    pass

class httpError(Exception):
    pass

def version():
    return 1.0
