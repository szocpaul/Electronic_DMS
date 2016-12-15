import json
import documents
import uuid as uuidlib
import repository
import config
import dateutil.parser

with open() as _file:
    docs = json.load(_file)
    for data in docs:
        doc = documents.Document(
            uuid=uuidlib.UUID(data['uuid']),
            title=data['name'],
            creation_date=dateutil.parser.parse(data['creation_date']).date(),
            document_date=dateutil.parser.parse(data['document_date']).date(),
            author=data['author'],
            description=data['description'],
            state=data['state'],
            is_public=data['is_public'])

