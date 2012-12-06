import os, sys, sqlite3

DB_NAME = 'mayb.db'
SQL_PATH = '../../../sql/mayb.sql'

class SQLite3(object):
    
    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '__instance__'):
            try:
                d = os.path.dirname(os.path.abspath(__file__))
                cls.__instance__ = sqlite3.connect(os.path.join(d, '../../', DB_NAME), timeout = 5000)
            except:
                print 'Error connecting to database.'
                raise
        return cls.__instance__

def setup():
    d = os.path.dirname(os.path.abspath(__file__))
    db = SQLite3()
    for statement in open(os.path.join(d, SQL_PATH)).read().split(';'):
        db.execute(statement)

def main():
    print SQLite3()

if __name__ == '__main__': main()