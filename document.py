import uuid as uuid_lib
import datetime


class Document(object):
    """Document of the repository"""

    def __init__(self,
                 uuid=None,
                 title="",
                 creation_date=None,
                 document_date=None,
                 author="",
                 description="",
                 state="new",
                 is_public=True,
                 tags=set(),
                 in_database=False):
        if uuid is None:
            self.uuid = uuid_lib.uuid4()
        else:
            self.uuid = uuid
        self.title = title
        if creation_date is None:
            self.creation_date = datetime.date.today()
        else:
            self.creation_date = creation_date
        if document_date is None:
            self.document_date = datetime.date.today()
        else:
            self.document_date = document_date
        self.author = author
        self.description = description
        self.state = state
        self.is_public = is_public
        self.tags = tags
        self.in_database = in_database

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)
"""
        self._uuid = uuid
        self._title = title
        self._creation_date = creation_date
        self._document_date = document_date
        self._author = author
        self._description = description
        self._state = state
        self._is_public = is_public
        self._tags = tags
        self._in_database = in_database

    @property
    def document_date(self):
        return self._document_date

    @document_date.setter
    def document_date(self, value):
        if value is None:
            self._document_date = datetime.date.today()
        else:
            self._document_date = value

    @property
    def creation_date(self):
        return self._creation_date

    @creation_date.setter
    def creation_date(self, value):
        if value is None:
            self._creation_date = datetime.date.today()
        else:
            self._creation_date = value

    @property
    def uuid(self):
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        if value is None:
            self._uuid = uuid_lib.uuid4()
        else:
            self._uuid = value

    @property
    def authors(self):
        return self._author

    @authors.setter
    def authors(self, value):
        self._author = value

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
    def state(self):
        return self._state

    @state.setter
    def state(self, value):
        if value in ['new', 'pending', 'accepted', 'rejected']:
            self._state = value
        else:
            raise ValueError('The "{}" is an invalid document state!'.format(value))

    @property
    def is_public(self):
        return self._is_public

    @is_public.setter
    def is_public(self, value):
        self._is_public = value

    def make_public(self):
        self._is_public = True

    def make_private(self):
        self._is_public = False

    @property
    def in_database(self):
        return self._in_database

    @in_database.setter
    def in_database(self, value):
        self._in_database = value

    @property
    def tags(self):
        return self._tags

    @tags.setter
    def tags(self, value):
        self._tags = value

    def add_tag(self, tag):
        self.tags.add(tag)

    def remove_tag(self, tag):
        self.tags.remove(tag)
"""
