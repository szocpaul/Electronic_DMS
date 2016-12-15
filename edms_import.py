import json
import document
import uuid as uuid_lib
import repository
import config
import dateutil.parser
import database


def main(file_name):
    db, _ = get_db()

    with open(file_name) as _file:
        docs = json.load(_file)
        for data in docs:
            doc = document.Document(
                uuid=uuid_lib.UUID(data['uuid']),
                title=data['name'],
                creation_date=dateutil.parser.parse(data['creation_date']).date(),
                document_date=dateutil.parser.parse(data['document_date']).date(),
                author=data['author'],
                description=data['description'],
                state=data['state'],
                is_public=data['is_public'])
            try:
                db.save(doc)
            except database.ExistError:
                print(str(doc.uuid) + " already exist")


def get_db():
    configuration = config.parse('config.toml')
    db = database.get_instance(configuration)
    repo = repository.get_instance(configuration)
    return db, repo
