from flask import Flask
from flask_session import Session
from sqlalchemy.orm import sessionmaker
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
import datetime, os
from flask_sqlalchemy import SQLAlchemy

app = Flask("server")

basedir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(basedir, "instance", "base_datos.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
os.makedirs("instance", exist_ok=True)

#URL_BD = 'sqlite:///instance/base_datos.db'

#def crear_engine():
#    engine = db.engine
#    Session = sessionmaker(bind=engine)
#    return Session

app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_FILE_DIR"] = "./flask_session_cache"
app.config["SESSION_PERMANENT"] = False
app.config["PERMANENT_SESSION_LIFETIME"] = datetime.timedelta(minutes=5)

db = SQLAlchemy(app)
Session(app)
login_manager = LoginManager()
login_manager.init_app(app)
Bootstrap(app)