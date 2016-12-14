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

    def add_author(self, author):
        return self.authors.add(author)

    def remove_author(self, author):
        return self.authors.remove(author)

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
    def files(self):
        return self._files

    @files.setter
    def files(self, value):
        self._files = value

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
    def doc_format(self):
        return self._doc_format

    @doc_format.setter
    def doc_format(self, value):
        self._doc_format = value

    def is_public(self):
        return self._is_public

    def make_public(self):
        self._is_public = True

    def make_private(self):
        self._is_public = False


class DocumentManager(object):
    """Manage documents"""

    def __init__(self):
        pass

    def add_document(self, document):
        pass

    def update_document(self, document_id, document):
        pass

    def remove_document(self, document_id):
        pass
