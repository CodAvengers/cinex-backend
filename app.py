import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from extensions import db, migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

load_dotenv()

def create_app():
    
    app = Flask(__name__)
    #db configuration
    db_config = {
        'POSTGRES_USER': os.getenv('POSTGRES_USER'),
        'POSTGRES_PASSWORD': os.getenv('POSTGRES_PASSWORD'),
        'POSTGRES_HOST': os.getenv('POSTGRES_HOST'),
        'DB_PORT': os.getenv('DB_PORT'),
        'POSTGRES_DB': os.getenv('POSTGRES_DB')
    }

    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{db_config['POSTGRES_USER']}:{db_config['POSTGRES_PASSWORD']}"
        f"@{db_config['POSTGRES_HOST']}:{db_config['DB_PORT']}/{db_config['POSTGRES_DB']}"
    )

    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24) #set after how long should the access token expire

    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app,resources={r"/*": {"origins": "*", "allow_headers": "*", "expose_headers": "*"}},supports_credentials=True)
    jwt = JWTManager(app)

    #importing the bp inside the function to avoid circular imports


    #register the blueprints


app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))  # Get port from environment, default to 5000
    app.run(debug=True, host='0.0.0.0', port=port)