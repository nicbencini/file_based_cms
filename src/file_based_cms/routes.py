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

import os
from pathlib import Path
from src.file_based_cms import app
from markdown import markdown



@app.before_request
def load_file_names():

    data_folder = Path("data/")
    root = os.path.abspath(os.path.dirname(__file__))
    data_dir = os.path.join(root, "data")

    g.root = root
    g.data_dir = data_dir
    g.file_names = os.listdir(data_dir)

@app.route('/')
def index():

    file_names = [os.path.basename(path) for path in g.file_names]
    return render_template('index.html', file_names=file_names)


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

    content = request.form['content']
    with open(file_path, 'w') as file:
        file.write(content)

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
