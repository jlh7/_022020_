from . import write_log, db
from os import path
from .models import Users, Exercises,Muscles, Trains, E_Details
from werkzeug.security import generate_password_hash
import pandas as pd
import numpy as np
import openpyxl

data_import = []

user = [
  Users(
    User_name = "tester", 
    Password = generate_password_hash('tester123', method='sha256'),
    Email = '<Tester_ID>@gmail.com',
    Hint_name = "Người kiểm thử",
    Gender = "",
    Dob = "2000-09-09",
    Dev = False,
    Admin = False
  ),
  Users(
    User_name = "admin", 
    Password = generate_password_hash('admin123', method='sha256'),
    Email = '<Admin_ID>@gmail.com',
    Hint_name = "Người quản trị",
    Gender = "",
    Dob = "2000-09-09",
    Dev = True,
    Admin = True
  )
]

data_import.append(user)

if path.exists("./website/data/Muscles.xlsx"):
  tmp = []
  file = np.array(pd.read_excel("./website/data/Muscles.xlsx"))
  for f in file:
    tmp.append(
      Muscles(
        Name = f[0],
        Detail = f[1]
      )
    )
  data_import.append(tmp)

if path.exists("./website/data/Trainings.xlsx"):
  tmp = []
  file = np.array(pd.read_excel("./website/data/Trainings.xlsx"))
  for f in file:
    tmp.append(
      Trains(
        Detail = f[0]
      )
    )
  data_import.append(tmp)

if path.exists("./website/data/Exercises.xlsx"):
  tmp = []
  file = np.array(pd.read_excel("./website/data/Exercises.xlsx"))
  for f in file:
    tmp.append(
      Exercises(
        Name = f[0],
        Details = str(f[1]).replace(".", "\n")
      )
    )
  data_import.append(tmp)

if path.exists("./website/data/E_detail.xlsx"):
  tmp = []
  file = np.array(pd.read_excel("./website/data/E_detail.xlsx"))
  for f in file:
    tmp.append(
      E_Details(
        Exercise_id=int(f[0]),
        Train_id=int(f[1]),
        Muscle_id = int(f[2]),
        Level=int(f[3]),
        Purpose=int(f[4]),
        Set=int(f[5]),
        Rep=int(f[6]),
        Time=int(f[7])
      )
    )
  data_import.append(tmp)

def import_V():
  try:
    for _ in data_import:
      for i in _:
        db.session.add(i)
    db.session.commit()
  except:
    pass