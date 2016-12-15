import sqlite3
import documents
import uuid as uuidlib


class EdmsSqlite(object):
    def __init__(self, configuration):
        sqlite_config = configuration['sqlite']

        if "_file" in sqlite_config:
            file = sqlite_config['_file']
        else:
            file = "edms_sqlite.db"

        self.connect = sqlite3.connect(file)




