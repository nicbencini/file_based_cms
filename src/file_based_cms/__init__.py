from flask import Flask
#from config import Config


app = Flask(__name__)
app.secret_key = 'secret1'

# Register blueprints or extensions here
from src.file_based_cms import routes


