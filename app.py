
from cms import create_app
from flask import( 
    Flask,
    render_template,
    url_for
)
import os
from pathlib import Path

app = create_app()
data_folder = Path("cms/data/")

@app.route('/')
def index():

    file_names = [name for name in os.listdir(data_folder)]
    return render_template('index.html', file_names=file_names)


if __name__ == "__main__":
    app.run(port=5003)

