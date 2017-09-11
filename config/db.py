import sqlite3
from flask import g
import os
#from Flask_D01 import app

class DataBase(object):
    __shared_state = {}
    def __call__(self):
        self.__dict__ = self.__shared_state
        self._app = None
    
    def setApp(self, app):
        self._app = app
        self._app.config.update(dict(
            DATABASE = os.path.join(self._app.root_path, 'config/flaskr.db'),
            SECRET_KEY = 'development_key',
            USERNAME = 'admin',
            PASSWORD = 'default'
        ))
        self.init_db()
    
    def init_db(self):
        with self._app.app_context():
            db = self.get_db()
        with self._app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

    def get_db(self):
        db = getattr(g, 'db', None)
        if db is None:
            db = g.db = sqlite3.connect(self._app.config['DATABASE'])
            db.row_factory = sqlite3.Row
        return db

    def connect_db(self):
        return sqlite3.connect(self._app.config['DATABASE'])

    def query_db(self, query, args=(), one=False):
        db = self.get_db()
        cur = db.execute(query, args)
        rv = cur.fetchall()
        db.commit()
        cur.close()
        return (rv[0] if rv else None) if one else rv

    def insert(self, mydict):
        query = """
        INSERT INTO {0} ({1}) VALUES ({2})
        """
        d = dict(mydict) 
        table = d.pop('table')
        columns = ','.join(d.keys())
        placeholders = ','.join(['?'] * len(d))
        values = list(d.values())
        #print(query.format(table, columns, placeholders), values)
        self.query_db(query.format(table, columns, placeholders), values)
        query = "select * from "+table+" order by id desc limit 1;"
        return self.query_db(query)
    
    def select(self, mydict, where = None):
        query = """
        SELECT {0} FROM {1}{2}
        """
        d = dict(mydict) 
        table = d.pop('table')
        if(len(mydict['columns'])):
            columns = ','.join(d['columns'])
        else:
            columns = "*"
        if(where):
            str_where = " WHERE "
            str_where += ' AND '.join(["{}={}".format(k,v) for k,v in where.items()])
        else:
            str_where = ""
        print(query.format(columns, table, str_where))
        return self.query_db(query.format(columns, table, str_where))

    def update(self, mydict, where):
        query = """
        UPDATE {0} SET {1}{2}
        """
        d = dict(mydict) 
        table = d.pop('table')
        columns_values = ','.join(["{}={}".format(k,v) for k,v in d.items()])
        str_where = " WHERE "
        str_where += ' AND '.join(["{}={}".format(k,v) for k,v in where.items()])
        #print(query.format(table, columns_values, str_where))
        query = "select * from "+table+" where id = "+where['id']+";"
        return self.query_db(query)

    def delete(self, table, where):
        query = """
        DELETE FROM {0}{1}
        """
        str_where = " WHERE "
        str_where += ' AND '.join(["{}={}".format(k,v) for k,v in where.items()])
        print(query.format(table, str_where))
        return self.query_db(query.format(table, str_where))

 