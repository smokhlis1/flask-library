from flask import Flask 
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db as root_db, login_manager, ma
from flask_cors import CORS

from .site.routes import home
from .auth.routes import auth
from .api.routes import books


app = Flask(__name__)
CORS(app)

app.config.from_object(Config)

app.register_blueprint(home)
app.register_blueprint(auth)
app.register_blueprint(books)

root_db.init_app(app)
login_manager.init_app(app)
ma.init_app(app)
migrate = Migrate(app, root_db)