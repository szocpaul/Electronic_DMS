import sqlite3
import document
import uuid as uuid_lib
import datetime


class EdmsSqlite(object):
    def __init__(self, configuration):
        sqlite_config = configuration['sqlite']

        if "file" in sqlite_config:
            _file = sqlite_config['file']
        else:
            _file = "edms_sqlite.db"

        self.connect = sqlite3.connect(_file)

    def save(self, _document):
        cursor = self.connect.cursor()
        if _document.in_database:
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
        sqlite_uuid = sqlite3.Binary(_document.uuid.bytes)
        values = {
            "uuid": sqlite_uuid,
            "title": _document.title,
            "creation_date": _document.creation_date.isoformat(),
            "document_date": _document.document_date.isoformat(),
            "author": _document.author,
            "description": _document.description,
            "state": _document.state,
            "is_public": _document.is_public
        }
        cursor.execute(stmt, values)

        cursor.execute("DELETE FROM tag WHERE uuid=:uuid", {"uuid": sqlite_uuid})

        def tag_gen():
            for t in _document.tags:
                yield (sqlite_uuid, t)

        cursor.executemany("INSERT INTO tag VALUES (:uuid, :tag)", tag_gen())
        self.connect.commit()

    def load(self, uuid=None, raw_uuid=None):
        cursor = self.connect.cursor()
        stmt = "SELECT title, creation_date, document_date, author, description, state, is_public FROM document WHERE uuid = :uuid"
        if raw_uuid is not None:
            uuid = uuid_lib.UUID(bytes=raw_uuid)
        sqlite_uuid = sqlite3.Binary(uuid.bytes)
        cursor.execute(stmt, {"uuid": sqlite_uuid})
        result = cursor.fetchone()
        if result is None:
            return None

        stmt = "SELECT tag FROM tag WHERE uuid=:uuid"
        cursor.execute(stmt, {"uuid": sqlite_uuid})
        tags = set([t[0] for t in cursor.fetchall()])

        return document.Document(
            uuid=uuid,
            title=result[0],
            creation_date=datetime.datetime.strptime(result[1], "%Y-%m-%d").date(),
            document_date=datetime.datetime.strptime(result[2], "%Y-%m-%d").date(),
            author=result[3],
            description=result[4],
            state=result[5],
            is_public=result[6],
            tags=tags,
            in_database=True
        )

    def search(self, tags, from_date, to_date):
        cursor = self.connect.cursor()
        stmt = """SELECT uuid FROM document WHERE document_date >= ?
            AND document_date <= ?
            AND uuid IN(
            SELECT uuid FROM tag where tag in (""" + ",".join("?" * len(tags)) + """)
            GROUP BY uuid
            HAVING COUNT(tag) = ?)
        """

        values = [from_date.isoformat(), to_date.isoformat()]
        if len(tags) > 0:
            values = values + tags + [len(tags)]
        cursor.execute(stmt, values)
        return [self.load(raw_uuid=r[0]) for r in cursor.fetchall()]

    def tag_count(self):
        cursor = self.connect.cursor()
        stmt = "SELECT tag, COUNT(uuid) FROM tag GROUP BY tag"
        cursor.execute(stmt)
        return [{'title': r[0], 'count': r[1]} for r in cursor.fetchall()]

    def tag_less(self):
        cursor = self.connect.cursor()
        stmt = "SELECT uuid FROM document WHERE uuid NOT IN (SELECT uuid FROM tag)"
        cursor.execute(stmt)
        return [self.load(raw_uuid=r[0]) for r in cursor.fetchall()]

    def remove(self, doc):
        cursor = self.connect.cursor()
        sqlite_uuid = sqlite3.Binary(doc.uuid.bytes)
        cursor.execute("DELETE FROM document WHERE uuid = ?", sqlite_uuid)
        cursor.execute("DELETE FROM tag WHERE uuid = ?", sqlite_uuid)
        self.connect.commit()

    def update_db(self):
        self.ensure_not_empty()
        cursor = self.connect.cursor()
        cursor.execute("SELECT value FROM config WHERE key = 'version'")
        result = cursor.fetchone()
        self.update_from_version(int(result[0]))

    def update_from_version(self, old_version):
        cursor = self.connect.cursor()
        if old_version < 1:
            cursor.execute("""
            CREATE TABLE document(
                uuid BLOB PRIMARY KEY,
                title TEXT,
                creation_date INT,
                document_date INT,
                author TEXT,
                description TEXT,
                state TEXT,
                is_public TEXT
            """)
            cursor.execute("CREATE TABLE tag(uuid BLOB, tag TEXT, PRIMARY KEY (uuid, tag))")
        if old_version < 2:
            cursor.executescript("""
                BEGIN TRANSACTION;
                ALTER TABLE document RENAME TO document_old;
                CREATE TABLE document(uuid BLOB PRIMARY KEY, title TEXT, creation_date INT, document_date INT, author TEXT, description TEXT, state TEXT, is_public TEXT);
                INSERT INTO document(uuid, title, creation_date, document_date, author, description, state, is_public) SELECT uuid, title, creation_date, document_date, author, description, state, is_public FROM document_old;
                DROP TABLE document_old;
                COMMIT;""")
            self.connect.commit()

            cursor2 = self.connect.cursor()
            cursor.execute("SELECT uuid, creation_date, document_date FROM document")
            while True:
                result = cursor.fetchone()
                if result is None:
                    break
                uuid_lob = result[0]
                creation_date = datetime.date.fromtimestamp(int(result[1])).isoformat()
                document_date = datetime.date.fromtimestamp(int(result[2])).isoformat()
                cursor2.execute("UPDATE document SET creation_date = ?, document_date = ? WHERE uuid = ?", (creation_date, document_date, uuid_lob))
        cursor.execute("UPDATE config SET value = '2' WHERE key = 'version'")
        self.connect.commit()

    def ensure_not_empty(self):
        cursor = self.connect.cursor()
        try:
            stmt = "SELECT * FROM config"
            cursor.execute(stmt)
            # result = cursor.fetchone()
        except sqlite3.OperationalError:
            stmt = "CREATE TABLE config(key Text PRIMARY KEY, value TEXT)"
            cursor.execute(stmt)
            stmt2 = "INSERT INTO config VALUES ('version', '0')"
            cursor.execute(stmt2)
