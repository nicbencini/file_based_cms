from flask import( 
    Flask,
    flash,
    g,
    render_template,
    redirect,
    request,
    session,
    url_for
)
import bcrypt

from src.file_based_cms.utility import(
    get_data_path
)

import os
from pathlib import Path
from src.file_based_cms import app
from markdown import markdown
from functools import wraps
import yaml

def valid_credentials(username, password):
    credentials = load_user_credentials()

    if username in credentials:
        stored_password = credentials[username].encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), stored_password)
    else:
        return False

def require_signed_in_user(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not check_creds():
            flash("You must be signed in to do that.")
            return redirect((url_for('signin')))
        
        return f(*args, **kwargs)
    
    return decorated_function

def load_user_credentials():
    filename = 'users.yml'
    root_dir = os.path.dirname(__file__)

    credentials_path = os.path.join(root_dir, filename)

    with open(credentials_path, 'r') as file:
        return yaml.safe_load(file)

@app.before_request
def load_file_names():

    #data_folder = Path("data/")
    root = get_data_path()
    data_dir = os.path.join(root, "data")

    g.root = root
    g.data_dir = data_dir
    g.file_names = os.listdir(data_dir)

@app.route('/')
def index():

    return render_template('index.html', file_names=g.file_names)


@app.route("/<file>")
def show_file(file):


    if file not in g.file_names:
        flash('The file could not be found.', 'warning')
        session.modified = True
        return redirect(url_for('index'))

    file_path = os.path.join(g.data_dir, file)

    with open(file_path) as f:
        file_data = f.readlines()

    if file.endswith('.md'):
        return markdown(''.join(file_data))

    return render_template('view_file.html', file_data=file_data)

@app.route("/<file>", methods=['POST'])
@require_signed_in_user
def save_file(file):


    file_path = os.path.join(g.data_dir, file)

    content = request.form['file_contents']
    with open(file_path, 'w') as file_document:
        file_document.write(content)

    flash(f"{file} has been updated.")

    return redirect(url_for('index'))

@app.route("/<file>/edit")
@require_signed_in_user
def edit_file(file):


    file_path = os.path.join(g.data_dir, file)
    
    if os.path.isfile(file_path):
        with open(file_path, 'r') as open_file:
            content = open_file.read()
        return render_template('edit_file.html', file=str(file), content=content)
    else:
        flash(f"{file} does not exist.")
        return redirect(url_for('index'))

@app.route("/new")
@require_signed_in_user
def new_file():
    
    return render_template('new_file.html')


@app.route("/new", methods=['POST'])
@require_signed_in_user
def create_file():


    new_file_name = request.form['file_name']

    if new_file_name in g.file_names:
        flash(f"'{new_file_name}' already exists.")
    elif not (new_file_name.endswith('.txt') or new_file_name.endswith('.md')):
        flash(f"Please enter a valid file extension '.txt' or '.md'")
    else:
        create_document(new_file_name)

    return redirect(url_for('index'))

@app.route("/<file>/delete")
@require_signed_in_user
def delete_file(file):

    file_path = os.path.join(g.data_dir, file)
    
    if os.path.isfile(file_path):
        os.remove(file_path)
        flash(f"'{file}' has been deleted.")
        return redirect(url_for('index'))
    else:
        flash(f"{file} does not exist.")
        return redirect(url_for('index'))

@app.route("/signin")
def signin():
    return render_template('signin.html')

@app.route("/signin", methods=['POST'])
def check_credentials():

    username = request.form['username']
    password = request.form['password']

    credentials = load_user_credentials()

    if valid_credentials(username, password):
        session['username'] = username
        flash("Welcome!")
        return redirect(url_for('index'))
    else:
        flash("Invalid credentials")
        return render_template('signin.html'), 422


@app.route("/signout")
def signout():

    session['username'] = ''
    session['password'] = ''

    return redirect(url_for('index'))
    
def create_document(name, content=""):
    with open(os.path.join(g.data_dir, name), 'w') as file:
        file.write(content)

def check_creds():

    credentials = load_user_credentials()

    if 'username' in session and session['username'] in credentials:
        return True
    
    return False



