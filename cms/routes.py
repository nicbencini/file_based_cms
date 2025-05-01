from flask import render_template
from cms import create_app

app = create_app()

@app.route('/')
def index():
    return 'Hello'