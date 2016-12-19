import datetime
import json
import config
import repository
import database


def main():
    db, _ = get_db()
    docs = db.search([], datetime.date.min, datetime.date.max)
    res = []
    for doc in docs:
        res.append({
            "uuid": str(doc.uuid),
            "title": doc.title,
            "creation_date": str(doc.creation_date),
            "document_date": str(doc.document_date),
            "author": doc.author,
            "description": doc.description,
            "state": doc.state,
            "is_public": doc.is_public,
            "tags": list(doc.tags)
        })
    print(json.dumps(res))


def get_db():
    configuration = config.parse('config.toml')
    db = database.get_instance(configuration)
    repo = repository.get_instance(configuration)
    return db, repo

main()
