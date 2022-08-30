from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from datetime import datetime, timedelta
import smtplib

def write_log(s):
  with open('logs.txt', mode='a') as log:
    if s != "\n" and s != "":
      log.writelines(f">>>{datetime.now()}:\t{s}\n")
    elif s == "\n":
      log.writelines("\n")
    else:
      log.writelines(">>>" + "-"*100 + "\n")
    log.closed

def send_mail():
  write_log("Export file \"Logs.txt\" to default mail!")
  log = open('logs.txt', mode="r")
  s = log.read()
  print(s)
  gid_s = "work4heal@gmail.com"
  pwd = "W$Hadmin"
  gid_r = "7lhtuan@gmail.com"
  
  connect = smtplib.SMTP_SSL("smtp.gmail.com", 465)
  connect.login(gid_s,pwd)
  connect.sendmail(gid_s,gid_r, s)
  
  log.close()

DB_NAME = "w4h.db"
app = Flask(__name__)
app.config['SECRET_KEY'] = 'ahihihi hihihaha'
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///data/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] =  timedelta(minutes=31)
db = SQLAlchemy(app)

def create_app():
  from .views import views
  from .auth import auth

  app.register_blueprint(views, url_prefix='/')
  app.register_blueprint(auth, url_prefix='/')

  create_database(app)
  from .models import Users
  
  login_manager = LoginManager(app)
  login_manager.login_view = 'auth.sign_in'
  @login_manager.user_loader
  def load_user(id):
    return Users.query.get(int(id))
  
  return app

from .values import import_V

def create_database(app):
  if not path.exists(f"./data/{DB_NAME}"):
    db.create_all(app=app)
    import_V()