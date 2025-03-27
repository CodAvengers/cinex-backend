from routes.movies import movies_bp
from routes.series import series_bp
from routes.favorites import favorites_bp
import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Load environment variables
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
VIDSRC_BASE = os.getenv("VIDSRC_BASE")
VIDLINK_BASE = os.getenv("VIDLINK_BASE")

# Register blueprints
app.register_blueprint(movies_bp)
app.register_blueprint(series_bp)
app.register_blueprint(favorites_bp)
