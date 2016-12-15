import sqlite3
import document
import uuid as uuidlib
import datetime


class EdmsSqlite(object):
    def __init__(self, configuration):
        sqlite_config = configuration['sqlite']

        if "file" in sqlite_config:
            _file = sqlite_config['file']
        else:
            _file = "edms_sqlite.db"

        self.connect = sqlite3.connect(_file)

    def save(self, document):
        cursor = self.connect.cursor()
        if document.in_database:
            stmt = """UPDATE document SET
                name=:name,
                title=:title,
                creation_date=:creation_date,
                document_date=:document_date,
                author=:author,
                description=:description,
                state=:state
                is_public=:is_public
            """
        else:
            stmt = """INSERT INTO document VALUES
                (:uuid,
                :title,
                :creation_date,
                :document_date,
                :author,
                :description,
                :state,
                :is_public
            """
        sqlite_uuid = sqlite3.Binary(document.uuid.bytes)
        values = {
            "uuid": sqlite_uuid,
            "title": document.title,
            "creation_date": document.creation_date.isoformat(),
            "document_date": document.document_date.isoformat(),
            "author": document.author,
            "description": document.description,
            "state": document.state,
            "is_public": document.is_public
        }
        cursor.execute(stmt, values)
        self.connect.commit()

    def load(self, uuid=None, raw_uuid=None):
        cursor = self.connect.cursor()
        stmt = "SELECT title, creation_date, document_date, author, description, state, is_public FROM document WHERE uuid = :uuid"
        if raw_uuid is not None:
            uuid = uuidlib.UUID(bytes=raw_uuid)
        sqlite_uuid = sqlite3.Binary(uuid.bytes)
        cursor.execute(stmt, {"uuid": sqlite_uuid})
        result = cursor.fetchone()
        if result is None:
            return None

        return document.Document(
            uuid=uuid,
            title=result[0],
            creation_date=datetime.datetime.strptime(result[1], "%Y-%m-%d").date(),
            document_date=datetime.datetime.strptime(result[2], "%Y-%m-%d").date(),
            author=result[3],
            description=result[4],
            state=result[5],
            is_public=result[6],
            in_database=True
        )
