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
                 is_public="",
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
