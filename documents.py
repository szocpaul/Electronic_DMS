import uuid as uuidlib
import datetime


class Document(object):
    """Document of the repository"""

    def __init__(self,
                 uuid=None,
                 title="",
                 creation_date=None,
                 document_date=None,
                 authors=set(),
                 description="",
                 in_database=False):

        """
        First version without property
        if uuid is None:
            self.uuid = uuidlib.uuid4()
        else:
            self.uuid = uuid
        self.title = title
        if creation_date is None:
            self.creation_date = datetime.date.today()
        else:
            self.document_date = creation_date
        if document_date is None:
            self.document_date = datetime.date.today()
        else:
            self.document_date = document_date
        self.authors = authors
        self.description = description
        self.in_database = in_database

    def add_authors(self, author):
        return self.authors.add(author)

    def remove_author(self, author):
        return self.authors.remove(author)
    """

    # With properties
        self._uuid = uuid
        self._title = title
        self._creation_date = creation_date
        self._document_date = document_date
        self._authors = authors
        self._description = description
        self._in_database = in_database

    @property
    def document_date(self):
        return self._document_date

    @document_date.setter
    def document_date(self, value):
        if value is None:
            self._document_date = datetime.date.today()
        else:
            self._document_date = self._document_date

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value):
        if value is None:
            self._creation_date = datetime.date.today()
        else:
            self._document_date = self._creation_date

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        if value is None:
            self._uuid = uuidlib.uuid4()
        else:
            self._uuid = value

    @property
    def authors(self):
        return self._authors

    @authors.setter
    def authors(self, value):
        self._authors = value

    def add_authors(self, author):
        return self._authors.add(author)

    def remove_author(self, author):
        return self._authors.remove(author)

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = value

    @property
    def in_database(self):
        return self._in_database

    @in_database.setter
    def in_database(self, value):
        self._in_database = value
