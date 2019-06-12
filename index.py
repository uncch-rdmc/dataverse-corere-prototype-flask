from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_assets import Environment, Bundle
import os
from os import walk
import requests
from urllib.parse import urlparse
import base64
import urllib
import json
import time
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

from controller.google import app_google
from controller.github import app_github

OUTPUT = "temp/"

app = Flask(__name__)
app.secret_key = os.environ.get("FN_FLASK_SECRET_KEY", default=False)


### Register Blueprints 
app.register_blueprint(app_google)
app.register_blueprint(app_github)

assets = Environment(app)
assets.url = app.static_url_path
scss = Bundle('custom.scss', filters='pyscss', output='all.css')
assets.register('scss_all', scss)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', default='postgresql://localhost/core')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from config_loader import *
from models import Users, Catalog


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.commit()
        return instance


@app.route('/')
@app.route('/index')
def index():
    if 'username' in session:
        user = db.session.query(Users).filter_by(email=session['username']).first()
        if user:
            user.given_name = session['given_name']
            user.family_name = session['family_name']
            flash("Welcome back "+session['given_name'])
        else:
            user = Users(email=session['username'], given_name=session['given_name'], family_name = session['family_name'], role=1)
            flash(session['given_name']+", welcome to CORE2 Project ")

        db.session.add(user)
        db.session.commit()
        return render_template("index.html")
    else: 
        return render_template("login.html")


@app.route("/logs")
def logs():
    return render_template('logs.html')


@app.route('/deleteaccount')
def deleteaccount():
    if 'username' in session:
        deleted_user = session['username']
        user_tbl = db.session.query(Users).filter_by(email=session['username']).first()
        db.session.delete(user_tbl)
        db.session.commit()
        session.clear()
        flash("Account "+deleted_user+" has been succesfully deleted")
        return redirect("/", code=302)
    else:
        return redirect("/", code=302)

@app.route('/settings')
def settings():
    if 'username' in session:
        user_tbl = db.session.query(Users).all()
        print(user_tbl)
        return render_template('settings.html',user_tbl=user_tbl)
    else:
        return redirect("/", code=302)

@app.route('/logout')
def logout():
    session.clear()
    # [session.pop(key) for key in list(session.keys()) if key != '_flashes'] #for use in the future
    flash("You have succesfully logged out!")
    return redirect(url_for('index'))


@app.route('/create_import_init', methods = ['GET', 'POST'])
def create_import_init():
    if 'username' in session:
        if request.method == 'POST' and request.values.get('import'):
            if request.values.get('url') and request.values.get('persistID') and request.values.get('token') and \
                request.values.get('version'):
                    url = request.values.get('url')
                    key = request.values.get('token')

                    persistID = request.values.get('persistID')

                    fileIds = request.form.getlist('fileIds[]')
                    fileNames = request.form.getlist('fileNames[]')
                    

                    ## GET Metadata Blocks for dataset
                    META_URL = url+"/api/datasets/export?exporter=ddi&persistentId="+persistID
                    meta_download = requests.get(META_URL,allow_redirects=True)
                    meta_content = meta_download.content
                    open(OUTPUT+"/metadata.xml", 'wb').write(meta_content)

                    # Make Directory if it doesn't exist
                    if not os.path.exists(OUTPUT+"/"+session['username']):
                        os.mkdir(OUTPUT+"/"+session['username'])

                    ## Download files to a folder
                    for name,ids in zip(fileNames,fileIds):
                        FILE_Q = url+"/api/access/datafile/"+ids+"/?persistentId=doi:"+persistID+"&key="+key
                        r = requests.get(FILE_Q,allow_redirects=True)
                        
                        open(OUTPUT+"/"+session['username']+"/"+name, 'wb').write(r.content)
                    return "0"
            return "missing parameters"

    return request.values.get('files')
        


@app.route('/create')
def create_catalog():
    if 'username' in session:
        user = db.session.query(Users).filter_by(email=session['username']).first()
        userID = user.id
        new_catalog = Catalog(id=userID)
        db.session.add(new_catalog )
        return render_template("create.html")
    else:
        return redirect("/", code=302)


@app.route('/create_import')
def create_or_import():
    if 'username' in session:
        user = db.session.query(Users).filter_by(email=session['username']).first()
        userID = user.id
        new_catalog = Catalog(id=userID)
        db.session.add(new_catalog )
        return render_template("create_import.html")
    else:
        return redirect("/", code=302)


@app.route('/upload')
def upload():
    return render_template("upload.html")

@app.route('/uploadfiles', methods=['GET', 'POST'])
def uploadfiles():
    if request.method == 'POST':
        f = request.files.get('file')
        f.save(os.path.join('./temp/', f.filename))

    return 'uploaded'


##BinderHub 
@app.route('/binder', methods=['GET','POST'])
def binder():
    myurl = request.args.get('url')
    return render_template('binder.html',myurl=myurl)


@app.route('/submit_review')
def submit_review():
    return ""

@app.route('/submit_odum')
def submit_odum():
    return ""

@app.route('/load', methods=['GET', 'POST'])
def load():
    myfiles = []

    for (dirpath, dirnames, filenames) in walk('./temp/'):
        for filename in filenames:
            if ".DS" not in filename:
                with open(dirpath+"/"+ filename, "rb") as f:
                    text = f.read().strip()

                    encoded = base64.b64encode(text).decode("utf-8")
                    z = {
                        "action": "create",
                        "file_path": filename,
                        "encoding": "base64",
                        "content": encoded
                    }
                    myfiles.append(z)

  

    runtime = {
        "action": "create",
        "file_path": "runtime.txt",
        "content": "r-2018-02-05"
    }
    myfiles.append(runtime)

    requirements = {
        "action": "create",
        "file_path": "requirements.txt",
        "content": """
        jupyterlab==0.35.6
        """
    }
    myfiles.append(requirements)

    gitignore = {
        "action": "create",
        "file_path": ".gitignore",
        "content": """.gitconfig
.yarn/
.npm/
.local/
.ipython/
.ipynb_checkpoints/
.bash_logout
.bashrc
.cache/
.conda/
.config/
.profile/
.profile
.jupyter/
        \r\n
        """
    }
    myfiles.append(gitignore)


    postBuild = {
        "action": "create",
        "file_path": "postBuild",
        "content": """#!/bin/bash

jupyter labextension install @lckr/jupyterlab_variableinspector
jupyter labextension install @jupyterlab/celltags
jupyter labextension install @andreyodum/core2
pip install jupyterlab-git
jupyter serverextension enable --py jupyterlab_git
rm -rf requirements.txt runtime.txt

git config --global user.email "{0}"
git config --global user.name "{1}"
git rm -r --cached .
git remote set-url origin {2}

\r\n
""".format(session['given_name'],session['given_name']+" "+session['family_name'], config["git_config_url"])
    }

    # jupyter labextension install @andreyodum/core2 
    myfiles.append(postBuild)


    #TEMPORARY
    GITLAB_URL = config["git_lab_url"]
    GITLAB_API = GITLAB_URL+"/"+config["git_api_version"]
    PRIVATE_TOKEN = "private_token="+config['git_private_token']
    headers = {'PRIVATE-TOKEN': ''+config['git_private_token']+'',
                'Content-Type': 'application/json'}


    username = session['username']
    
    requests.delete(GITLAB_API+"/projects/"+urllib.parse.quote("root/"+username, safe='')+"/?"+PRIVATE_TOKEN)
    while 1:
        r_project = requests.post(GITLAB_API+"/projects/?"+PRIVATE_TOKEN, data={"name": username, "visibility":"public"})
        if r_project.status_code == 201:
            break
        time.sleep(1)

    if r_project.status_code != 201:
        print(r_project.content)
        raise ValueError
       #return "ERROR" + str(r_project.status_code) + " CONENTE: "+str(r_project.content)
    
    gitlabid = str(json.loads(r_project.content)['id'])
    print("GITLABID" + gitlabid)


    r_put = requests.put(GITLAB_API+"projects/"+gitlabid+"/services/emails-on-push?&"+PRIVATE_TOKEN, 
        json={"recipients": config['receipients'], "disable_diffs": False, "send_from_committer_email": False
        }
        )

    r_commit = requests.post(GITLAB_API+"projects/"+gitlabid+"/repository/commits?&"+PRIVATE_TOKEN, 
        json={"branch": "master", "author_email": "admin@example.com", "author_name": "Administrator",
            "commit_message": "step2", "actions": myfiles
        }
        )

    print(r_commit.content)
    
    code = json.loads(r_commit.content)['id']
    return json.dumps({"status":"Success","Code":code,"URI": GITLAB_URL+"/root/"+username})


if __name__ == "__main__":
    app.run(debug=True)