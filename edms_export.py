import datetime
import json
import edms_import


def main():
    db, _ = edms_import.get_db()
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
            "tags": list(doc.tags)
        })
    print(json.dumps(res))
