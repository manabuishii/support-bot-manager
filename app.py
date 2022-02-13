# -*- coding: utf-8 -*-
"""Conversation bot."""
import enum
import os

from flask import Flask, redirect, render_template, request, session, url_for

# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Enum, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = "./uploads"
ALLOWED_EXTENSIONS = {"txt", "md", "lu", "qna"}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
# set the secret key.  keep this really secret:
app.secret_key = "A0Zr98j/3yX R~XHH!jmN]LWX/,?RT"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///conversation.sqlite?check_same_thread=False"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)
# enginestring = 'sqlite:///sample_db.sqlite3?check_same_thread=False'
# engine = sqlalchemy.create_engine(enginstring, echo=True)

# model
Base = declarative_base()


# Conversation State model
class ConversationState(str, enum.Enum):
    """Conversation State model."""

    deploy = "運用中"
    wait = "承認待ち"
    notadmitted = "非承認"


# Conversation model
class Conversation(Base):
    """Conversation model."""

    __tablename__ = "conversations"
    id = Column("id", Integer, primary_key=True)
    name = Column("name", String(200))
    filename = Column("filename", String(200))
    botstatus = Column("botsatus", Enum(ConversationState))
    owner = Column("owner", String(100))
    url = Column("url", String(200))


# Base = automap_base()
# Base.prepare(db.engine, reflect=True)
# Samples_Metadata = Base.classes.sample_metadata
# Samples = Base.classes.samples

dbsession = Session(autocommit=False, autoflush=True, bind=db.engine)

Base.metadata.create_all(bind=db.engine)


def allowed_file(filename):
    """Check extention is allowed."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# file uploaded
@app.route("/uploader", methods=["GET", "POST"])
def upload_file():
    """File upload."""
    global dbsession
    reason = "The fail reason is not defined"
    if request.method == "POST":
        # check if the post request has the file part
        if "file" not in request.files:
            reason = "No file part"
            return redirect(request.url)
        file = request.files["file"]
        print(file.filename)
        print(request.url)
        print(allowed_file(file.filename))
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == "":
            reason = "No selected file"
        elif not allowed_file(file.filename):
            reason = "[" + file.filename + "] has non-allowed file extention"
        elif file:
            print("save")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
            # get username from session
            username = "-"
            if "username" in session:
                username = session["username"]
            auth = request.authorization
            if auth is not None:
                username = auth.username
            # save to database
            conversation = Conversation(
                name=filename,
                filename=filename,
                botstatus=ConversationState.deploy,
                owner=username,
                url=request.url,
            )
            dbsession.add(conversation)
            dbsession.commit()
            # return 'file uploaded successfully'
            return redirect(url_for("manage"))
    return render_template("upload_fail.html", reason=reason)


@app.route("/manage")
def manage():
    """Manage all conversation."""
    result = dbsession.query(Conversation).all()
    files = []
    for conversation in result:
        print(conversation.id, conversation.filename)
        # count line number of conversation.filename
        count = 0
        with open(app.config["UPLOAD_FOLDER"] + "/" + conversation.filename, "r") as f:
            for _ in f:
                count = count + 1
        files.append(
            {
                "id": conversation.id,
                "filename": conversation.filename,
                "botstatus": conversation.botstatus,
                "owner": conversation.owner,
                "url": conversation.url,
                "count": count,
            }
        )
    return render_template("manage.html", files=files)


@app.route("/update", methods=["GET", "POST"])
def update():
    """Update conversation bot status."""
    global dbsession
    if request.method == "POST":
        # get id from request
        id = request.form["id"]
        # get botstatus from request
        botstatus = request.form["botstatus"]
        # update Conversation id
        print(id, botstatus)
        conversation = dbsession.query(Conversation).filter_by(id=id).first()
        conversation.botstatus = botstatus
        dbsession.commit()
    return redirect(url_for("manage"))
    # return render_template("detail.html", file = file)


@app.route("/detail/<int:id>")
def detail(id):
    """Detail page per entry."""
    file = dbsession.query(Conversation).filter_by(id=id).one()
    return render_template("detail.html", file=file)


@app.route("/")
def index():
    """Output index page."""
    return render_template("index.html")


if __name__ == "__main__":
    # run host 0.0.0.0
    # Base.metadata.create_all(bind=ENGINE)

    app.run(
        debug=True,
        host="0.0.0.0",
    )
