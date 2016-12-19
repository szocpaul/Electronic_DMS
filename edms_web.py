import flask
from flask import Flask
import document as doclib
import uuid as uuid_lib
import datetime
import dateutil.parser
import database
import repository
import config
import werkzeug
import logging
from logging.handlers import RotatingFileHandler

app = Flask(__name__)

log_handler = RotatingFileHandler('logs/edms.log', maxBytes=1000000, backupCount=3)
log_handler.setLevel(logging.WARNING)
log_formatter = logging.Formatter("%(asctime)s - %(levelname)s\n%(message)s")
log_handler.setFormatter(log_formatter)
app.logger.addHandler(log_handler)


def get_db():
    configuration = config.parse('config.toml')
    db = database.get_instance(configuration)
    repo = repository.get_instance(configuration)
    return db, repo


@app.route("/")
def index():
    return flask.render_template("index.html")


@app.route("/search")
def search():
    """ flask.request.args.get:
        will parse the content of the query string. (the part in URL after the question mark)
        dateutil.parser.parse(to_raw).date():
        example: from (01-02-2013) to (2013, 1, 2)"""
    db, _ = get_db()

    users = [user for user in flask.request.args.get('users').split(' ') if user != '']
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

    results = db.search(users, from_date, to_date)
    search_users = ' '.join(users)

    if from_date == datetime.date.min:
        search_from = ''
    else:
        search_from = str(from_date)
    if to_date == datetime.date.max:
        search_to = ''
    else:
        search_to = str(to_date)

    return flask.render_template("search.html", results=results, search_users=search_users, search_from=search_from,
                                 search_to=search_to)


@app.route("/document/<uuid>")
def document(uuid):
    db, repo = get_db()
    try:
        uuid = uuid_lib.UUID(uuid)
    except ValueError:
        return "Invalid uuid"
    doc = db.load(uuid)
    if doc is None:
        return "Error not found"
    files = repo.get(uuid, basename_only=True)
    return flask.render_template("document.html", doc=doc, files=files)


@app.route("/upload/<uuid>", methods=['POST'])
def upload(uuid):
    _, repo = get_db()
    try:
        uuid = uuid_lib.UUID(uuid)
    except ValueError:
        return "not found upload uuid"  # TODO

    if 'document' not in flask.request.files:
        return "no upload"  # TODO
    file = flask.request.files['document']
    filename = werkzeug.secure_filename(file.filename)
    repo.save(uuid, file, filename)

    return flask.redirect(flask.url_for('edit', uuid=str(uuid)), code=303)


@app.route("/download/<uuid>/<file>")
def download(uuid, file):
    _, repo = get_db()
    try:
        uuid = uuid_lib.UUID(uuid)
    except ValueError:
        return "not found"  # TODO
    path = repo.get(uuid, file=file)
    if path is None:
        return "not found"  # TODO
    return flask.send_from_directory(repo.get_dir(uuid), file, as_attachment=True)


@app.route("/edit/<uuid>")
def edit(uuid):
    db, repo = get_db()
    try:
        uuid = uuid_lib.UUID(uuid)
    except ValueError:
        return "not found"  # TODO
    doc = db.load(uuid)
    if doc is None:
        return "not found"  # TODO
    files = repo.get(uuid, basename_only=True)

    return flask.render_template("edit.html", doc=doc, files=files)


@app.route("/save/<uuid>", methods=['POST'])
def save(uuid):
    db, repo = get_db()

    if uuid == 'new':
        doc = doclib.Document()
    else:
        try:
            uuid = uuid_lib.UUID(uuid)
        except ValueError:
            return "not found"  # TODO
        doc = db.load(uuid)
        if doc is None:
            return "not found"

    form = flask.request.form
    if 'title' in form and 'description' in form and 'date' in form:
        try:
            date = dateutil.parser.parse(form['date']).date()
        except ValueError:
            return "Invalid date"  # TODO
        doc.title = form['title']
        doc.document_date = date
        doc.author = form['author']
        doc.description = form['description']
        doc.state = form['state']
        doc.is_public = form['is_public']
        db.save(doc)
    if 'deluser' in form and 'user' in form:
        user = form['user']
        doc.remove_user(user)
        db.save(doc)
    if 'adduser' in form and 'user' in form:
        for user in form['user'].split():
            doc.add_user(user)
        db.save(doc)
    if 'delfile' in form and 'file' in form:
        file = form['file']
        repo.remove(uuid, file)

    return flask.redirect(flask.url_for('edit', uuid=doc.uuid), code=303)


@app.route("/delete/<uuid>", methods=['GET', 'POST'])
def delete(uuid):
    db, repo = get_db()
    try:
        uuid = uuid_lib.UUID(uuid)
    except ValueError:
        return "not found"  # TODO
    doc = db.load(uuid)
    if doc is None:
        return "not found"  # TODO

    if flask.request.method == 'POST' and 'yes' in flask.request.form:
        db.remove(doc)
        repo.remove_dir(doc.uuid)
        return flask.redirect(flask.url_for('index'), code=303)

    return flask.render_template("delete.html", doc=doc)


@app.route("/create")
def create():
    return flask.render_template("create.html")


@app.route("/repo_count")
def repo_count():
    db, _ = get_db()
    results = db.repo_count()
    return flask.render_template("search.html", results=results)


@app.route("/useroverview")
def useroverview():
    db, _ = get_db()
    users = db.user_count()
    return flask.render_template("useroverview.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)
