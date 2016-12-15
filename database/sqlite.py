import sqlite3
import documents
import uuid as uuidlib


class EdmsSqlite(object):
    def __init__(self, configuration):
        sqlite_config = configuration['sqlite']

        if "file" in sqlite_config:
            _file = sqlite_config['file']
        else:
            _file = "edms_sqlite.db"

        self.connect = sqlite3.connect(_file)




