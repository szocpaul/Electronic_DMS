import flask
from flask import Flask
import document
import edms_import
import uuid as uuid_lib
import repository
import datetime
import dateutil.parser
import database
import repository
import config

app = Flask(__name__)


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/search")
def search():
    """ flask.request.args.get:
        will parse the content of the query string. (the part in URL after the question mark)
        dateutil.parser.parse(to_raw).date():
        example: from (01-02-2013) to (2013, 1, 2)"""
    db, _ = edms_import.get_db()
    tags = [tag for tag in flask.request.args.get('tags').split(' ') if tag != '']
    to_raw = flask.request.args.get('to', '')
    from_raw = flask.request.args.get('from', '')

    to_date = datetime.date.max
    if to_raw != '':
        try:
            to_date = dateutil.parser.parse(to_raw).date()
        except ValueError:
            pass
    from_date = datetime.date.min
    if from_raw != '':
        try:
            from_date = dateutil.parser.parse(from_raw).date()
        except ValueError:
            pass

    result = db.search(tags, from_date, to_date)
    search_tags = ' '.join(tags)

    if from_date == datetime.date.min:
        search_from = ''
    else:
        search_from = str(from_date)
    if to_date == datetime.date.max:
        search_to = ''
    else:
        search_to = str(to_date)

    return flask.render_template("search.html", results=result, search_tags=search_tags, search_from=search_from,
                                 search_to=search_to)


@app.route("/document/<uuid>")
def document(uuid):
    db, repo = edms_import.get_db()
    try:
        uuid = uuid_lib.UUID(uuid)
    except ValueError:
        return "Invalid uuid"
    doc = db.load(uuid)
    if doc is None:
        return "Error not found"
    files = repo.get(uuid, basename_only=True)
    return flask.render_template("document.html", doc=doc, files=files)


if __name__ == "__main__":
    app.run()
