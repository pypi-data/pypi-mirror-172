import pyodbc
import pymysql
from enum import Enum

from configuration import *
from logger import EasyPostLogger


def reloadconfig(func):  
    def wrap(*args, **kwargs):
        setglobals(globals())
        getglobals_new_globals = getglobals()
        globals().update(getglobals_new_globals)
        func_new_globals = func(*args,**kwargs)
        after_func_new_globals = getglobals()
        globals().update(after_func_new_globals)
        return func_new_globals
    return wrap

loadconfigwithfile = reloadconfig(loadconfigwithfile)
loadconfigwithjson = reloadconfig(loadconfigwithjson)

class SQLType(Enum):
    MSSQL = 0
    MYSQL = 1

class SQLConnection(Enum):
    # Odd numbers for MySQL, Even for MSSQL
    LOCALDB = 0
    PORTAL = 1
    PRINTDB = 2
    
    def type_select(self):
        if self.value % 2 == 1:
            return SQLType.MYSQL
        else:
            return SQLType.MSSQL
        
    @reloadconfig
    def select(self):
        return {
                    'host':globals()['C_DBHOST_' + self.name],
                    'user':globals()['C_DBUSER_' + self.name],
                    'password':globals()['C_DBPW_' + self.name],
                    'name':globals()['C_DBNAME_' + self.name],
                    'type': self.type_select()
                }

class SQLFactory():    
    @reloadconfig
    def __init__(self,sql_connection:SQLConnection = SQLConnection.PORTAL,connectiondata= None,logger = None, config_path=None):
        # setting selector
        loadconfigwithfile(config_path)
        self.sql_connection_selector = {
            SQLType.MYSQL : self.pymysql_connection,
            SQLType.MSSQL : self.pyodbc_connection
        }
        self.sql_connection = sql_connection
        self.connectiondata = connectiondata
        self.connection = None
        self.cursor = None
        self.app = None
        if not logger:
            self.logger = EasyPostLogger('SQLFactory')
        else:
            self.logger = logger
    @reloadconfig
    def pymysql_connection(self, name = None, app=None, retry=0, timeout=None, autocommit=None):
        try:
            self.connection = pymysql.connect(     host=self.connectiondata['host'],
                                        user = self.connectiondata['user'],
                                        password = self.connectiondata['password'],
                                        database = name if name else self.connectiondata['name'],
                                        charset='utf8mb4',
                                        cursorclass=pymysql.cursors.DictCursor,
                                        program_name=(app if app else 'DEFAULTAPP'),
                                        connect_timeout=(timeout if timeout else 10),
                                        autocommit= (autocommit if autocommit else False)
                                    )
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.pymysql_connection(name=name,retry=retry+1)
            else:
                raise ex
    
    @reloadconfig    
    def pyodbc_connection(self, name = None, app=None, retry=0, timeout=None, autocommit=None):
        try:
            self.connection = pyodbc.connect(      "APP=" + (app if app else 'DEFAULTAPP') + ";",
                                        driver='{SQL Server Native Client 11.0}',
                                        server=self.connectiondata['host'],
                                        user=self.connectiondata['user'],
                                        password=self.connectiondata['password'],
                                        database= name if name else self.connectiondata['name'],
                                        timeout=(timeout if timeout else 0),
                                        autocommit= (autocommit if autocommit else False)
                                )
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.pyodbc_connection(name=name,retry=retry+1)
            else:
                raise ex
            
    def executemany(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.executemany(*args,*kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.executemany(retry=retry+1)
            else:
                raise ex
               
    def rollback(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.rollback(*args,*kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.rollback(retry=retry+1)
            else:
                raise ex   
        
    def fetchone(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.fetchone(*args,*kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.fetchone(retry=retry+1)
            else:
                raise ex
       
        
    def fetchall(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.fetchall(*args,*kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.fetchall(retry=retry+1)
            else:
                raise ex
       
    def commit(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.commit(*args,**kwargs)
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.commit(retry=retry+1,*args,**kwargs)
            else:
                raise ex
             
    def execute(self, *args, retry=0, **kwargs):
        if not self.cursor:
            self.createCursor()
        try:
            return self.cursor.execute(*args,**kwargs)
        except Exception as ex:
            
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                return self.execute(retry=retry+1,*args,**kwargs)
            else:
                raise ex

    def createConnection(self):
        self.connectiondata = self.sql_connection.select()
        self.sql_connection_selector[self.connectiondata['type']]()
    
    @reloadconfig 
    def createCursor(self, retry = 0):
        if not self.connection:
            self.createConnection()
        try:
            self.cursor = self.connection.cursor()
        except Exception as ex:
            if retry < globals()['C_DEFAULT_RETRYS']:
                self.close_all()
                self.createCursor(retry=retry+1)
            else:
                raise ex

    def __enter__(self):
        #ttysetattr etc goes here before opening and returning the file object
        self.createCursor()
        return self
    
    def close_all(self):
        try:
            return self.cursor.close()
        except Exception as ex:
            self.logger.debug(ex)
        try:
            self.connection.close()
        except Exception as ex:
            self.logger.debug(ex)
            
    def __exit__(self, type, value, traceback):
        #Exception handling here
        self.close_all()

   
if __name__ == '__main__':
    with SQLFactory(SQLConnection.PORTAL) as con:
        con.execute("SELECT * FROM easypost_portal.afm_users where company = 7255;")
        data = con.fetchall()
        print(data)
    con2 = SQLFactory(SQLConnection.PRINTDB)
    con2.execute("SELECT * FROM [EasyPost].[dbo].[Companies] where id = 7255;")
    data = con2.fetchall()
    con2.close_all()