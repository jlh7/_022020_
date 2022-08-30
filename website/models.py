from . import db,app
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin, current_user
from flask import url_for,redirect
from flask_admin import Admin, AdminIndexView, expose
from flask import redirect,url_for,flash

#======================================================================================================================#TODO_Bảng người dùng:
class Users(db.Model, UserMixin):

#!_Xác định tên bảng và khoá chính
  __tablename__ = "Users"
  id = db.Column(db.Integer, primary_key = True) 

#?_: Các thông tin đăng nhập của người dùng:
  Admin     = db.Column(db.Boolean, nullable=False,default=False)
  Dev       = db.Column(db.Boolean, nullable=False,default=False)
  User_name = db.Column(db.Text, unique = True, nullable=False)    #?_Tên đăng nhập
  Password  = db.Column(db.Text, nullable=False)                   #?_Mật khẩu
  Email     = db.Column(db.Text, unique = True, nullable=False)  #?_Thư điện tử
  Status    = db.Column(db.Boolean, nullable=False, default=False)                    #?_Trạng thái hoạt động
  
#?_: Các thông tin tổng quan về người dùng
  Hint_name = db.Column(db.Text)             #?_Tên hiển thị
  Gender    = db.Column(db.Text)                #?_Giới tính
  Dob       = db.Column(db.Text)                   #?_Sinh nhật
  
#?_: Thông tin thêm về người dùng
  Note      = db.Column(db.Text)                #?_Ghi chú
  
#?_: Các bảng liên kết với bảng Người dùng
  Schedule = db.relationship('Schedules')
  Plan     = db.relationship('Plans')

#*_: Các chức năng dữ liệu bảng
  def __repr__(self):
    return f" | {self.Status} | {self.User_name} | {self.Password} | {self.Email} | {self.Hint_name} | {self.Gender} | {self.Dob} | {self.Note} | "
  
  def add_new(self,new_user_name, new_pwd, new_email):
    self.Password  = new_pwd
    self.Email     = new_email
    self.User_name = new_user_name
    
  
  def change_main(self, new_pwd, new_email):
    self.Password = new_pwd
    self.Email    = new_email
  
  def info(self, new_hint_name, new_gender, new_dob, new_note):
    self.Hint_name = new_hint_name
    self.Gender    = new_gender
    self.Dob       = new_dob
    self.Note      = new_note

class User_View(ModelView):
  def is_accessible(self):
    if current_user.is_authenticated:
      return current_user.Dev
    return False
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for("auth.sign_in"))
  
  
  can_export = True
  can_view_details = True
  can_create = False
  can_delete = False
  can_edit = False
  page_size = 10
  column_list = ('id', 'User_name','Status')
  column_labels = dict(id='STT', User_name='Tên tài khoản', Status="Trạng thái")
  create_template = 'admin/users/create.html'
  list_template = 'admin/users/list.html'

#======================================================================================================================#TODO_Bảng lên kế hoạch tập luyện cho người dùng
class Plans(db.Model):

#!_Xác định tên bảng và khoá chính
  __tablename__ = "Plans"
  id = db.Column(db.Integer, primary_key = True) 
  
#?_: Thông tin để xác định độ khó bài tập
  Weight  = db.Column(db.Integer)        
  Height  = db.Column(db.Integer)           
  Push_up = db.Column(db.Integer)        
  Squat   = db.Column(db.Integer)           
  Crunch  = db.Column(db.Integer)   

#?_: Thông tin để xác định phương hướng tập
  Level   = db.Column(db.Integer)                   
  
#?_: Thông tin ban đầu để xác định hướng lên kế hoạch 
  Purpose = db.Column(db.Integer)              
  
#?_: Các bảng liên kết với bảng Kế hoạch
  Schedule = db.relationship('Schedules')
  User_id  = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)

#*_: Các chức năng dữ liệu bảng
  def __repr__ (self):
    return f" | {self.Weight} | {self.height} | {self.push_up} | {self.squat} | {self.crunch} | {self.purpose} | {self.level} | "



class Plan_View(ModelView):
  def is_accessible(self):
    if current_user.is_authenticated:
      return current_user.Dev
    return False
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for("auth.logout"))
  
  can_export = True
  can_view_details = True
  can_create = False
  can_delete = False
  can_edit = False
  page_size = 10
  column_list = ('User_id', 'Level','Purpose')
  column_labels= dict(User_id = "Mã người dùng", Level = "Mức độ tập luyện", Purpose = "Mục đích tập luyện")
  create_template = 'admin/plans/create.html'
  list_template = 'admin/plans/list.html'

#======================================================================================================================#TODO_Bảng lịch tập
class Schedules(db.Model):

#!_Xác định tên bảng
  __tablename__ = "Schedules"
  id = db.Column(db.Integer,primary_key = True)

#?_: Các bảng liên kết với bảng Lịch tập
  User_id            = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
  Plan_id            = db.Column(db.Integer, db.ForeignKey('Plans.id'), nullable=False)
  Week               = db.relationship('Weeks')

#======================================================================================================================#TODO_Bảng tập luyện
class Trains(db.Model):

#!_Xác định tên bảng
  __tablename__ = "Trains"
  id = db.Column(db.Integer,primary_key = True)
  
#?_: Các thông tin về bài tập
  Detail = db.Column(db.Text, nullable=False)
  
#?_: Các thông tin về các bảng liên kết với bảng Vùng cơ
  Exercise_detail = db.relationship('E_Details')

class Trains_View(ModelView):
  def is_accessible(self):
    if current_user.is_authenticated:
      return current_user.Dev
    return False
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for("auth.logout"))
  
  can_export = True
  can_view_details = True
  can_edit = False
  can_create = False
  can_delete = False
  page_size = 10
  column_list = ('id', 'Detail')
  column_labels = dict(id = "Mã giai đoạn(STT)", Detail = "Giai đoạn")
  list_template = 'admin/trains/list.html'

#======================================================================================================================#TODO_Bảng vùng cơ
class Muscles(db.Model):

#!_Xác định tên bảng
  __tablename__ = "Muscles"
  id = db.Column(db.Integer,primary_key = True)
  
#?_: Các thông tin về bài tập
  Name = db.Column(db.Text, nullable=False)
  Detail = db.Column(db.Text, nullable=False)
  
#?_: Các thông tin về các bảng liên kết với bảng Vùng cơ
  E_detail = db.relationship('E_Details')

class Muscles_View(ModelView):
  def is_accessible(self):
    if current_user.is_authenticated:
      return current_user.Dev
    return False
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for("auth.logout"))
  
  can_export = True
  can_view_details = True
  can_edit = False
  can_create = False
  can_delete = False
  page_size = 10
  column_list = ('id', 'Detail')
  column_labels = dict(id = "Mã nhóm cơ(STT)", Detail = "Nhóm cơ")
  column_editable_list = ('Name','Detail')
  list_template = 'admin/muscles/list.html'

#======================================================================================================================#TODO_Bảng bài tập
class Exercises(db.Model):

#!_Xác định tên bảng
  __tablename__ = "Exercises"
  id = db.Column(db.Integer,primary_key = True)
  
#?_: Các thông tin về bài tập
  Name   = db.Column(db.Text, nullable=False)
  Details = db.Column(db.Text, nullable=False)
  
#?_: Các bảng liên kết với bảng Bài Tập
  Detail = db.relationship('E_Details')


class Exercise_View(ModelView):
  def is_accessible(self):
    if current_user.is_authenticated:
      return current_user.Dev
    return False
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for("auth.logout"))
  
  can_export = True
  can_view_details = True
  can_edit = False
  page_size = 10
  column_list = ('id', 'Name', 'Details')
  column_labels = dict(id = "Mã bài tập(STT)", Name="Tên bài tập", Details = "Chi tiết bài tập")
  column_editable_list = ('Name', 'Details')
  form_columns = ('Name', 'Details')
  create_template = 'admin/exercises/create.html'
  list_template = 'admin/exercises/list.html'


#======================================================================================================================#TODO_Bảng chi tiết bài tập
class E_Details(db.Model):

#!_Xác định tên bảng
  __tablename__ = "E_Details"
  id = db.Column(db.Integer,primary_key = True)
  
#?_: Các thông tin chi tiết bài tập
  Level   = db.Column(db.Integer, nullable = False)
  Purpose = db.Column(db.Integer, nullable = False)
  Set     = db.Column(db.Integer, nullable = False)
  Rep     = db.Column(db.Integer, nullable = False)
  Time    = db.Column(db.Integer, nullable = False)
  
#?_: Các bảng liên kết với bảng Chi Tiết Bài Tập
  Mon = db.relationship('Monday')
  Tue = db.relationship('Tuesday')
  Wed = db.relationship('Wednesday')
  Thu = db.relationship('Thursday')
  Fri = db.relationship('Friday')
  Sat = db.relationship('Saturday')
  Sun = db.relationship('Sunday')
  Exercise_id = db.Column(db.Integer, db.ForeignKey('Exercises.id'), nullable=False)
  Train_id    = db.Column(db.Integer, db.ForeignKey('Trains.id'), nullable=False)
  Muscle_id   = db.Column(db.Integer, db.ForeignKey('Muscles.id'), nullable=False)


class E_Details_View(ModelView):
  def is_accessible(self):
    if current_user.is_authenticated:
      return current_user.Dev
    return False
  
  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for("auth.logout"))
  
  can_export = True
  can_view_details = True
  can_edit = False
  column_list = ('id','Muscle_id','Exercise_id','Train_id', 'Level', 'Purpose', 'Set', 'Rep', 'Time')
  column_editable_list = ('Level', 'Purpose', 'Set', 'Rep', 'Time')
  column_labels = dict(id = "STT",Muscle_id="Mã nhóm cơ(1-4)", Exercise_id = "Mã bài tập", Train_id = "Mã giai đoạn (1-3)", Level="Mức độ tập(1-5)", Purpose = "Mục đích tập (1-3)", Set = "Số hiệp", Rep = "Số nhịp", Time = "Thời gian (Phút)")
  form_columns = ('Muscle_id', 'Exercise_id', 'Train_id', 'Level', 'Purpose', 'Set', 'Rep', 'Time')
  page_size = 15
  create_template = 'admin/e_details/create.html'
  list_template = 'admin/e_details/list.html'


#======================================================================================================================#TODO_Bảng tuần tập
class Weeks(db.Model):

#!_Xác định tên bảng
  __tablename__ = "Weeks"
  id = db.Column(db.Integer,primary_key = True)

#?_: Các thông tin lên lịch tập
  Mon = db.relationship('Monday')
  Tue = db.relationship('Tuesday')
  Wed = db.relationship('Wednesday')
  Thu = db.relationship('Thursday')
  Fri = db.relationship('Friday')
  Sat = db.relationship('Saturday')
  Sun = db.relationship('Sunday')

#?_: Các bảng liên kết với bảng Lịch tập
  Schedule_id = db.Column(db.Integer, db.ForeignKey('Schedules.id'), nullable=False)

#======================================================================================================================#TODO_Bảng thứ 2
class Monday(db.Model):
  __tablename__ = "Monday"
  id = db.Column(db.Integer, primary_key = True)
  Week_id = db.Column(db.Integer,db.ForeignKey('Weeks.id'), nullable=False)
  E_Detail_id = db.Column(db.Integer,db.ForeignKey('E_Details.id'), nullable=False)
#======================================================================================================================#TODO_Bảng thứ 3
class Tuesday(db.Model):
  __tablename__ = "Tuesday"
  id = db.Column(db.Integer, primary_key = True)
  Week_id = db.Column(db.Integer,db.ForeignKey('Weeks.id'), nullable=False)
  E_Detail_id = db.Column(db.Integer,db.ForeignKey('E_Details.id'), nullable=False)

#======================================================================================================================#TODO_Bảng thứ 4
class Wednesday(db.Model):
  __tablename__ = "Wednesday"
  id = db.Column(db.Integer, primary_key = True)
  Week_id = db.Column(db.Integer,db.ForeignKey('Weeks.id'), nullable=False)
  E_Detail_id = db.Column(db.Integer,db.ForeignKey('E_Details.id'), nullable=False)

#======================================================================================================================#TODO_Bảng thứ 5
class Thursday(db.Model):
  __tablename__ = "Thursday"
  id = db.Column(db.Integer, primary_key = True)
  Week_id = db.Column(db.Integer,db.ForeignKey('Weeks.id'), nullable=False)
  E_Detail_id = db.Column(db.Integer,db.ForeignKey('E_Details.id'), nullable=False)

#======================================================================================================================#TODO_Bảng thứ 6
class Friday(db.Model):
  __tablename__ = "Friday"
  id = db.Column(db.Integer, primary_key = True)
  Week_id = db.Column(db.Integer,db.ForeignKey('Weeks.id'), nullable=False)
  E_Detail_id = db.Column(db.Integer,db.ForeignKey('E_Details.id'), nullable=False)

#======================================================================================================================#TODO_Bảng thứ 7
class Saturday(db.Model):
  __tablename__ = "Saturday"
  id = db.Column(db.Integer, primary_key = True)
  Week_id = db.Column(db.Integer,db.ForeignKey('Weeks.id'), nullable=False)
  E_Detail_id = db.Column(db.Integer,db.ForeignKey('E_Details.id'), nullable=False)

#======================================================================================================================#TODO_Bảng chủ nhật
class Sunday(db.Model):
  __tablename__ = "Sunday"
  id = db.Column(db.Integer, primary_key = True)
  Week_id = db.Column(db.Integer,db.ForeignKey('Weeks.id'), nullable=False)
  E_Detail_id = db.Column(db.Integer,db.ForeignKey('E_Details.id'), nullable=False)




class MyAdminIndexView(AdminIndexView):
  def is_accessible(self):
    if current_user.is_authenticated:
      return current_user.Dev
    return False
  
  def inaccessible_callback(self, name, **kwargs):
    if current_user.is_authenticated:
      flash("Bạn không phải quản trị viên! Hãy đăng nhập lại!", category="error")
    return redirect(url_for("auth.logout"))
  
  @expose('/')
  def index(self):
      return self.render('admin/index.html',
        u_count = Users.query.count(),
        us_count = Users.query.filter(Users.Status == True).count(),
        up_count = Plans.query.count(),
        usc_count = Schedules.query.count(),
        m_count = Muscles.query.count(),
        e_count = Exercises.query.count(),
        em1_count = E_Details.query.filter(E_Details.Muscle_id == 1,E_Details.Level == 3, E_Details.Purpose == 3).count(),
        em2_count = E_Details.query.filter(E_Details.Muscle_id == 2,E_Details.Level == 3, E_Details.Purpose == 3).count(),
        em3_count = E_Details.query.filter(E_Details.Muscle_id == 3,E_Details.Level == 3, E_Details.Purpose == 3).count(),
        em4_count = E_Details.query.filter(E_Details.Muscle_id == 4,E_Details.Level == 3).count(),
        et1_count = E_Details.query.filter(E_Details.Train_id == 1,E_Details.Level == 3).count(),
        et2_count = E_Details.query.filter(E_Details.Train_id == 2,E_Details.Level == 3, E_Details.Purpose == 3).count(),
        et3_count = E_Details.query.filter(E_Details.Train_id == 3,E_Details.Level == 3).count(),
        d_count = Users.query.filter(Users.Dev == True, Users.Admin ==False).count()
      )
  
My_admin = Admin(app, name="Workout for Healthy", index_view=MyAdminIndexView(name="Thống Kê"))


My_admin.add_view(User_View(Users, db.session, name="Người Dùng"))
My_admin.add_view(Plan_View(Plans, db.session, name="Kế Hoạch"))
My_admin.add_view(E_Details_View(E_Details, db.session, name="Chi Tiết Bài Tập"))
My_admin.add_view(Exercise_View(Exercises, db.session, name="Bài Tập"))
My_admin.add_view(Muscles_View(Muscles, db.session, name="Nhóm cơ"))
My_admin.add_view(Trains_View(Trains, db.session, name="Giai đoạn"))