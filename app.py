from wsgiref.util import request_uri
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from werkzeug.utils import secure_filename
# import SQLAlchemy
from flask_sqlalchemy import SQLAlchemy
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float, DateTime, Enum
import enum

# model
Base = declarative_base()
#Base.query = session.query_property()

# Conversation State model
class ConversationState(str, enum.Enum):
    deploy = "deploy"
    wait = "wait"
    notadmitted = "notadmitted"

# Conversation model
class Conversation(Base):
    """
    Conversation model
    """
    __tablename__ = 'conversations'
    id = Column('id', Integer, primary_key = True)
    name = Column('name', String(200))
    filename = Column("filename", String(200))
    botstatus = Column('botsatus', Integer)
    owner = Column('owner', String(100))
    url = Column('url', String(200))

app=Flask(__name__)
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'txt', 'md', 'lu', 'qna'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# set the secret key.  keep this really secret:
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# file uploaded
@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        print(file.filename)
        print(request.url)
        print(allowed_file(file.filename))
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if not allowed_file(file.filename):
            flash('Not allowed file extention')
            return redirect(request.url)
        if file:
            print("save")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return 'file uploaded successfully'
    return render_template('upload_fail.html')
@app.route("/manage")
def manage():
    return render_template("manage.html")

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    # run host 0.0.0.0

    app.run(debug=True,host='0.0.0.0',)


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/conversation.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)
Samples_Metadata = Base.classes.sample_metadata
Samples = Base.classes.samples

