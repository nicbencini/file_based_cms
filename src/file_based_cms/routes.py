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

from src.file_based_cms.utility import(
    get_data_path
)

import os
from pathlib import Path
from src.file_based_cms import app
from markdown import markdown


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
def save_file(file):


    file_path = os.path.join(g.data_dir, file)

    content = request.form['file_contents']
    with open(file_path, 'w') as file_document:
        file_document.write(content)

    flash(f"{file} has been updated.")

    return redirect(url_for('index'))

@app.route("/<file>/edit")
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
def new_file():
    
    return render_template('new_file.html')


@app.route("/new", methods=['POST'])
def create_file():


    new_file_name = request.form['file_name']

    if new_file_name in g.file_names:
        flash(f"'{new_file_name}' already exists.")
    elif not new_file_name.endswith('.txt') or not new_file_name.endswith('.md'):
        flash(f"Please enter a valid file extension '.txt' or '.md'")
    else:
        create_document(new_file_name)

    return redirect(url_for('index'))

@app.route("/<file>/delete")
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

    if username == "admin" and password == "secret":
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

def check_creds(username, password):
    if username == 'admin' and password == 'secret':
        return True
    return False

