import os
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from extensions import db, migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

load_dotenv()

def create_app():
    app = Flask(__name__)
    
    # Database configuration
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

    # JWT Configuration
    app.config['SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_secret_key')
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    
    # CORS Configuration
    CORS(app, resources={
        r"/*": {
            "origins": "*", 
            "allow_headers": "*", 
            "expose_headers": "*"
        }
    }, supports_credentials=True)
    
    jwt = JWTManager(app)

    # Import blueprints
    from routes.latest_series_and_movies import tmdb_routes
    from routes.top_rated import top_rated_routes
    from routes.popular_routes import popular_routes
    from routes.search_routes import search_routes
    from routes.authetication import user_bp  
    from routes.all_movies import all_movies
    from routes.trending_movies_and_series import trending_routes
    from routes.discover_filters_movies_and_series import discover_filters
    from routes.favorites import favorites_bp  
    from routes.movie_details import movie_details_bp
    from routes.watchlist_routes import watchlist_routes
    from routes.movies import movies_bp  

    # Register blueprints with URL prefixes
    app.register_blueprint(popular_routes, url_prefix='/')
    app.register_blueprint(top_rated_routes, url_prefix='/')
    app.register_blueprint(search_routes, url_prefix='/')
    app.register_blueprint(tmdb_routes, url_prefix='/')
    app.register_blueprint(user_bp)
    app.register_blueprint(all_movies, url_prefix='/')
    app.register_blueprint(trending_routes, url_prefix='/')
    app.register_blueprint(discover_filters, url_prefix='/')
    app.register_blueprint(favorites_bp)  
    app.register_blueprint(movie_details_bp) 
    app.register_blueprint(watchlist_routes)
    app.register_blueprint(movies_bp)

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)