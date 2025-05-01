
from flask import( 
    Flask,
    render_template,
    url_for
)
import os
from pathlib import Path

app = Flask(__name__)
data_folder = Path("cms/data/")
root = os.path.abspath(os.path.dirname(__file__))
data_dir = os.path.join(root, "cms", "data")

@app.route('/')
def index():

    
    
    files = [os.path.basename(path) for path in os.listdir(data_dir)]
    return render_template('index.html', file_names=files)


@app.route("/<file>")
def show_file(file):

    file_path = f'{data_dir}/{file}'

    with open(file_path) as f:
        file_data = f.readlines()

    return render_template('view_file.html', file_data=file_data)

if __name__ == "__main__":
    app.run(debug = True, port=5003)