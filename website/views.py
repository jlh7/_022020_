from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import Exercises, Muscles, Schedules, Users, Plans,Weeks, E_Details
from . import db, write_log, send_mail
from random import randint
from datetime import datetime

views = Blueprint('views', __name__)

@views.route("/")
def index():
  return render_template('other/index.html', user=current_user, bar=True)

#!-------------------------------------------------------------------------------
@views.route('/home', methods=['GET','POST'])
def home():
  if not current_user.is_authenticated or not current_user.Status:
    flash("Hãy đăng nhập trước!",category='error')
    return redirect(url_for('auth.sign_in'))
  if not current_user.Hint_name or not current_user.Dob or not current_user.Gender:
    flash("Hãy nhập đầy đủ thông tin trước!",category='error')
    return redirect(url_for('views.acc_info'))
  if request.method == "POST":
    purpose = int(request.form.get('purpose'))
    return redirect(url_for("views.plan", purpose=purpose))
  return render_template('client/home.html', user=current_user)

#!-------------------------------------------------------------------------------
@views.route('/home/a')
def home1():
  flash(f'Đã sửa đổi gì? Cùng thử nghiệm nào!', category='success')
  return redirect(url_for("views.home"))

#!-------------------------------------------------------------------------------
@views.route('/home/0')
def home2():
  write_log(f">>> User ({current_user.User_name}) deleted the workout schedule!!!--")
  flash(f'Hãy tạo một lịch tập mới nào!', category='success')
  schedule = Schedules.query.filter_by(User_id=current_user.id).first()
  if schedule:
    week = Weeks.query.filter_by(Schedule_id = schedule.id).first()
    if week:
      day = Monday.query.filter_by(Week_id = week.id)
      if day:
        for _ in day:
          db.session.delete(_)
      day = Tuesday.query.filter_by(Week_id = week.id)
      if day:
        for _ in day:
          db.session.delete(_)
      day = Wednesday.query.filter_by(Week_id = week.id)
      if day:
        for _ in day:
          db.session.delete(_)
      day = Thursday.query.filter_by(Week_id = week.id)
      if day:
        for _ in day:
          db.session.delete(_)
      day = Friday.query.filter_by(Week_id = week.id)
      if day:
        for _ in day:
          db.session.delete(_)
      day = Saturday.query.filter_by(Week_id = week.id)
      if day:
        for _ in day:
          db.session.delete(_)
      day = Sunday.query.filter_by(Week_id = week.id)
      if day:
        for _ in day:
          db.session.delete(_)
      db.session.delete(week)
    db.session.delete(schedule)
    db.session.commit()
  return redirect(url_for("views.home"))

#!-------------------------------------------------------------------------------
@views.route('/bmi', methods=['GET','POST'])
def BMI():
  if not current_user.is_authenticated or not current_user.Status:
    flash("Hãy đăng nhập trước!",category='error')
    return redirect(url_for('auth.sign_in'))
  if not current_user.Hint_name or not current_user.Dob or not current_user.Gender:
    flash("Hãy nhập đầy đủ thông tin trước!",category='error')
    return redirect(url_for('views.acc_info'))
  if request.method == 'POST':
    weight = int(request.form.get('weight'))
    height = int(request.form.get('height'))
    plan = Plans.query.filter_by(User_id=current_user.id).first()
    if plan:
      db.session.delete(plan)
    db.session.add(
      Plans(
        Weight = weight,
        Height = height,
        User_id = current_user.id
      )
    )
    db.session.commit()
    bmi = (weight/((height/100)**2))
    flash(f"Chỉ số BMI = {bmi}",category='success')
    if bmi <= 18.4:
      flash("Bạn bị thiếu cân, cần bổ sung thêm dinh dưỡng!\n(Nhưng nếu bạn có cơ hãy chăm sóc kỹ hơn nhé!)",category='success')
    elif bmi >= 18.5 and bmi <= 19.5:
      flash("Bạn đang gầy, cần chú trọng ăn uống nhé!\n(Nếu bạn có cơ thì... Suýt đẹp!)",category='success')
    elif bmi >= 19.6 and bmi <= 20.9:
      flash("Dáng bạn khá chuẩn!\n(Nếu bạn có cơ thì... Gần đẹp!)",category='success')
    elif bmi >= 21 and bmi <= 23:
      flash("Bạn đang bự lên!\n(Nếu bạn có cơ thì... Vừa đủ đẹp!)",category='success')
    elif bmi >= 23.1 and bmi <= 25:
      flash("Bạn sắp quá cỡ, hãy xem lại khẩu phần ăn!\n(Nếu bạn có cơ thì tập thêm nhé, Mlem rồi đấy!)",category='success')
    elif bmi >= 25.1 and bmi <= 29.9:
      flash("Bạn bị béo phì độ I, cần giảm cân!\n(Nếu bạn có cơ, hãy tập cardio nhiều hơn!)",category='success')
    elif bmi >= 30:
      flash("Bạn bị béo phì độ II!\n(Nếu bạn có cơ, hãy chú trọng chế độ dinh dưỡng nhé!)",category='success')
    write_log(f">>> User ({current_user.User_name}) has calculated BMI!!!--")
    return redirect(url_for("views.BMI"))
  return render_template('client/BMI.html', user=current_user, bar=True)

#!-------------------------------------------------------------------------------
@views.route('/healthy', methods=['GET','POST'])
def healthy():
  if not current_user.is_authenticated or not current_user.Status:
    flash("Hãy đăng nhập trước!",category='error')
    return redirect(url_for('auth.sign_in'))
  if not current_user.Hint_name or not current_user.Dob or not current_user.Gender:
    flash("Hãy nhập đầy đủ thông tin trước!",category='error')
    return redirect(url_for('views.acc_info'))
  if request.method == 'POST':
    weight = int(request.form.get('weight'))
    height = int(request.form.get('height'))
    push_up = int(request.form.get('push_up'))
    squat = int(request.form.get('squat'))
    crunch = int(request.form.get('crunch'))
    lv = int(((push_up + squat + crunch)/(weight / ((height/100) ** 2)))/2)
    plan = Plans.query.filter_by(User_id=current_user.id).first()
    if plan:
      db.session.delete(plan)
    db.session.add(
      Plans(
        Weight = weight,
        Height = height,
        Push_up = push_up,
        Squat = squat,
        Crunch = crunch,
        Level = lv,
        User_id = current_user.id
      )
    )
    db.session.commit()
    if lv == 0:
      flash(f"Chỉ số Healthy = {lv} -> Sức khoẻ ở mức Yếu!",category='success')
    elif lv == 1:
      flash(f"Chỉ số Healthy = {lv} -> Sức khoẻ ở mức Trung bình!",category='success')
    elif lv == 2:
      flash(f"Chỉ số Healthy = {lv} -> Sức khoẻ ở mức Khá!",category='success')
    elif lv == 3:
      flash(f"Chỉ số Healthy = {lv} -> Sức khoẻ ở mức Khá tốt!",category='success')
    elif lv == 4:
      flash(f"Chỉ số Healthy = {lv} -> Sức khoẻ ở mức Tốt!",category='success')
    elif lv == 5:
      flash(f"Chỉ số Healthy = {lv} -> Sức khoẻ ở mức Xuất sắc!",category='success')
    elif lv > 5:
      flash(f"Chỉ số Healthy = {lv} -> Sức khoẻ ở mức Quá Tốt!",category='success')
    write_log(f">>> User ({current_user.User_name}) has calculated HEALTHY!!!--")
    return redirect(url_for("views.healthy"))
  return render_template('client/healthy.html', user=current_user, bar=True)

#!-------------------------------------------------------------------------------
@views.route("/plan/<purpose>", methods=['POST', 'GET'])
def plan(purpose):
  if not current_user.is_authenticated or not current_user.Status:
    flash("Hãy đăng nhập trước!",category='error')
    return redirect(url_for('auth.sign_in'))
  if not current_user.Hint_name or not current_user.Dob or not current_user.Gender:
    flash("Hãy nhập đầy đủ thông tin trước!",category='error')
    return redirect(url_for('views.acc_info'))
  if request.method == "POST":
    Can_nang = int(request.form.get('weight'))
    Chieu_cao = int(request.form.get('height'))
    push_up = int(request.form.get('push_up'))
    squat = int(request.form.get('squat'))
    crunch = int(request.form.get('crunch'))
    lv = int(((push_up + squat + crunch)/(Can_nang / ((Chieu_cao/100) ** 2)))/2)
    if lv > 5:
      lv = 5
    plan = Plans.query.filter_by(User_id=current_user.id).first()
    if plan:
      db.session.delete(plan)
    else:
      db.session.add(
        Plans(
          Purpose=purpose,
          Weight = Can_nang,
          Height = Chieu_cao,
          Push_up = push_up,
          Squat = squat,
          Crunch = crunch,
          Level = lv,
          User_id = current_user.id
        )
      )
      db.session.commit()
    write_log(f">>> User ({current_user.User_name}) has scheduled a workout!!!--")
    return redirect(url_for("views.schedule"))
  else:
    return render_template('client/plan.html', user=current_user, bar=True)
  
#!-------------------------------------------------------------------------------
from .models import Monday,Tuesday,Wednesday,Thursday,Friday,Saturday,Sunday
@views.route("/schedule", methods=['GET', 'POST'])
def schedule():
  if not current_user.is_authenticated or not current_user.Status:
    flash("Hãy đăng nhập trước!",category='error')
    return redirect(url_for('auth.sign_in'))
  pl = Plans.query.filter_by(User_id=current_user.id).first()
  if not pl:
      flash("Hãy tạo cho mình một kế hoạch tập luyện trước!",category='error')
      return redirect(url_for('views.home'))
  if not pl.Weight or not pl.Height or not pl.Push_up or not pl.Squat or not pl.Crunch or not pl.Purpose:
    flash("Hãy tạo cho mình một kế hoạch tập luyện trước!",category='error')
    return redirect(url_for('views.home'))
  schedule = Schedules.query.filter_by(User_id=current_user.id).first()
  if schedule:
    week = Weeks.query.filter_by(Schedule_id=schedule.id).first()
    if week:
      weeks = []
      count = 0
      day = datetime.today().isoweekday()
      #Todo_________________________________________________________CN
      Sun = Sunday.query.filter_by(Week_id = week.id)
      if Sun:
        tmp = []
        c = Sun.count()
        for _ in Sun:
          p = []
          
          d = E_Details.query.filter_by(id = _.E_Detail_id).first()
          if d:
            p.append(d.Rep)
            p.append(d.Set)
            p.append(d.Time)
          
          e = Exercises.query.filter_by(id = d.Exercise_id).first()
          if e:
            p.append(e.Name)
            p.append(e.Details)
          
          m = Muscles.query.filter_by(id = d.Muscle_id).first()
          if m:
            p.append(m.Name)
            p.append(m.Detail)
          
          if day == 0:
            p.append(True)
          else:
            p.append(False)
          
          if day > 0:
            p.append(False)
          else:
            p.append(True)
          
          tmp.append(p)
          
        Sun = tmp
        if c > count:
          count = c
      else:
        Sun = []
      weeks.append(Sun)
      #Todo_________________________________________________________T2
      Mon = Monday.query.filter_by(Week_id = week.id)
      if Mon:
        tmp = []
        for _ in Mon:
          p = []
          
          d = E_Details.query.filter_by(id = _.E_Detail_id).first()
          if d:
            p.append(d.Rep)
            p.append(d.Set)
            p.append(d.Time)
          
          e = Exercises.query.filter_by(id = d.Exercise_id).first()
          if e:
            p.append(e.Name)
            p.append(e.Details)
          
          m = Muscles.query.filter_by(id = d.Muscle_id).first()
          if m:
            p.append(m.Name)
            p.append(m.Detail)
          
          if day == 1:
            p.append(True)
          else:
            p.append(False)
          
          if day > 1:
            p.append(False)
          else:
            p.append(True)
          
          tmp.append(p)
        Mon = tmp
      else:
        Mon = []
      weeks.append(Mon)
      #Todo_________________________________________________________T3
      Tue = Tuesday.query.filter_by(Week_id = week.id)
      if Tue:
        tmp = []
        for _ in Tue:
          p = []
          
          d = E_Details.query.filter_by(id = _.E_Detail_id).first()
          if d:
            p.append(d.Rep)
            p.append(d.Set)
            p.append(d.Time)
          
          e = Exercises.query.filter_by(id = d.Exercise_id).first()
          if e:
            p.append(e.Name)
            p.append(e.Details)
          
          m = Muscles.query.filter_by(id = d.Muscle_id).first()
          if m:
            p.append(m.Name)
            p.append(m.Detail)
          
          if day == 2:
            p.append(True)
          else:
            p.append(False)
          
          if day > 2:
            p.append(False)
          else:
            p.append(True)
          
          tmp.append(p)
        Tue = tmp
      else:
        Tue = []
      weeks.append(Tue)
      #Todo_________________________________________________________T4
      Wed = Wednesday.query.filter_by(Week_id = week.id)
      if Wed:
        tmp = []
        for _ in Wed:
          p = []
          
          d = E_Details.query.filter_by(id = _.E_Detail_id).first()
          if d:
            p.append(d.Rep)
            p.append(d.Set)
            p.append(d.Time)
          
          e = Exercises.query.filter_by(id = d.Exercise_id).first()
          if e:
            p.append(e.Name)
            p.append(e.Details)
          
          m = Muscles.query.filter_by(id = d.Muscle_id).first()
          if m:
            p.append(m.Name)
            p.append(m.Detail)
          
          if day == 3:
            p.append(True)
          else:
            p.append(False)
          
          if day > 3:
            p.append(False)
          else:
            p.append(True)
          
          tmp.append(p)
        Wed = tmp
      else:
        Wed = []
      weeks.append(Wed)
      #Todo_________________________________________________________T5
      Thu = Thursday.query.filter_by(Week_id = week.id)
      if Thu:
        tmp = []
        for _ in Thu:
          p = []
          
          d = E_Details.query.filter_by(id = _.E_Detail_id).first()
          if d:
            p.append(d.Rep)
            p.append(d.Set)
            p.append(d.Time)
          
          e = Exercises.query.filter_by(id = d.Exercise_id).first()
          if e:
            p.append(e.Name)
            p.append(e.Details)
          
          m = Muscles.query.filter_by(id = d.Muscle_id).first()
          if m:
            p.append(m.Name)
            p.append(m.Detail)
          
          if day == 4:
            p.append(True)
          else:
            p.append(False)
          
          if day > 4:
            p.append(False)
          else:
            p.append(True)
          
          tmp.append(p)
        Thu = tmp
      else:
        Thu = []
      weeks.append(Thu)
      #Todo_________________________________________________________T6
      Fri = Friday.query.filter_by(Week_id = week.id)
      if Fri:
        tmp = []
        for _ in Fri:
          p = []
          
          d = E_Details.query.filter_by(id = _.E_Detail_id).first()
          if d:
            p.append(d.Rep)
            p.append(d.Set)
            p.append(d.Time)
          
          e = Exercises.query.filter_by(id = d.Exercise_id).first()
          if e:
            p.append(e.Name)
            p.append(e.Details)
          
          m = Muscles.query.filter_by(id = d.Muscle_id).first()
          if m:
            p.append(m.Name)
            p.append(m.Detail)
          
          if day == 5:
            p.append(True)
          else:
            p.append(False)
          
          if day > 5:
            p.append(False)
          else:
            p.append(True)
          
          tmp.append(p)
        Fri = tmp
      else:
        Fri = []
      weeks.append(Fri)
      #Todo_________________________________________________________T7
      Sat = Saturday.query.filter_by(Week_id = week.id)
      if Sat:
        tmp = []
        for _ in Sat:
          p = []
          
          d = E_Details.query.filter_by(id = _.E_Detail_id).first()
          if d:
            p.append(d.Rep)
            p.append(d.Set)
            p.append(d.Time)
          
          e = Exercises.query.filter_by(id = d.Exercise_id).first()
          if e:
            p.append(e.Name)
            p.append(e.Details)
          
          m = Muscles.query.filter_by(id = d.Muscle_id).first()
          if m:
            p.append(m.Name)
            p.append(m.Detail)
          
          if day == 6:
            p.append(True)
          else:
            p.append(False)
          
          if day > 6:
            p.append(False)
          else:
            p.append(True)
          
          tmp.append(p)
        Sat = tmp
      else:
        Sat = []
      weeks.append(Sat)
      
      write_log(f">>> User ({current_user.User_name}) is back in training!!!--")
      return render_template('client/schedule.html', 
        user=current_user, 
        week=weeks
      )
    else:
      db.session.delete(schedule)
  else:
    plan = Plans.query.filter_by(User_id=current_user.id).first()
    db.session.add(
      Schedules(
        User_id = plan.User_id,
        Plan_id = plan.id
      )
    )
    db.session.commit()
  
  schedule = Schedules.query.filter_by(User_id=current_user.id).first()
  if schedule:
    db.session.add(
      Weeks(
        Schedule_id = schedule.id
      )
    )
    db.session.commit()
    
    week = Weeks.query.filter_by(Schedule_id=schedule.id).first()
    w = []
    
    exercise_begin = E_Details.query.filter_by(Train_id=1)
    exercise_end   = E_Details.query.filter_by(Train_id=3)
    #Todo---------------------------------------------------------------------Mon
    exercise_main = E_Details.query.filter_by(Muscle_id=1,Purpose=plan.Purpose, Level=plan.Level)
    exercise_extra = E_Details.query.filter_by(Muscle_id=2,Purpose=plan.Purpose, Level=plan.Level)
    tmp = [
      Monday(
        Week_id = week.id,
        E_Detail_id = exercise_begin[0].id
      ),
      Monday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Monday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Monday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Monday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Monday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Monday(
        Week_id = week.id,
        E_Detail_id = exercise_end[0].id
      )
    ]
    w.append(tmp)
    
    #Todo---------------------------------------------------------------------Tue
    exercise_main = E_Details.query.filter_by(Muscle_id=3,Purpose=plan.Purpose, Level=plan.Level)
    exercise_extra = E_Details.query.filter_by(Muscle_id=2,Purpose=plan.Purpose, Level=plan.Level)
    tmp = [
      Tuesday(
        Week_id = week.id,
        E_Detail_id = exercise_begin[randint(1, exercise_begin.count()-1)].id
      ),
      Tuesday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Tuesday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Tuesday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Tuesday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Tuesday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Tuesday(
        Week_id = week.id,
        E_Detail_id = exercise_end[1].id
      ),
      Tuesday(
        Week_id = week.id,
        E_Detail_id = exercise_end[2].id
      )
    ]
    w.append(tmp)
    
    #Todo---------------------------------------------------------------------Wed
    exercise_main = E_Details.query.filter_by(Muscle_id=1,Purpose=plan.Purpose, Level=plan.Level)
    exercise_extra = E_Details.query.filter_by(Muscle_id=2,Purpose=plan.Purpose, Level=plan.Level)
    tmp = [
      Wednesday(
        Week_id = week.id,
        E_Detail_id = exercise_begin[randint(1, exercise_begin.count()-1)].id
      ),
      Wednesday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Wednesday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Wednesday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Wednesday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Wednesday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Wednesday(
        Week_id = week.id,
        E_Detail_id = exercise_end[1].id
      ),
      Wednesday(
        Week_id = week.id,
        E_Detail_id = exercise_end[2].id
      )
    ]
    w.append(tmp)
    
    #Todo---------------------------------------------------------------------Thu
    exercise_main = E_Details.query.filter_by(Muscle_id=3,Purpose=plan.Purpose, Level=plan.Level)
    exercise_extra = E_Details.query.filter_by(Muscle_id=2,Purpose=plan.Purpose, Level=plan.Level)
    tmp = [
      Thursday(
        Week_id = week.id,
        E_Detail_id = exercise_begin[0].id
      ),
      Thursday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Thursday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Thursday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Thursday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Thursday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Thursday(
        Week_id = week.id,
        E_Detail_id = exercise_end[0].id
      )
    ]
    w.append(tmp)
    
    #Todo---------------------------------------------------------------------Fri
    exercise_main = E_Details.query.filter_by(Muscle_id=1,Purpose=plan.Purpose, Level=plan.Level)
    exercise_extra = E_Details.query.filter_by(Muscle_id=2,Purpose=plan.Purpose, Level=plan.Level)
    tmp = [
      Friday(
        Week_id = week.id,
        E_Detail_id = exercise_begin[0].id
      ),
      Friday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Friday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Friday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Friday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Friday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Friday(
        Week_id = week.id,
        E_Detail_id = exercise_end[0].id
      )
    ]
    w.append(tmp)
    
    #Todo---------------------------------------------------------------------Sat
    exercise_main = E_Details.query.filter_by(Muscle_id=3,Purpose=plan.Purpose, Level=plan.Level)
    exercise_extra = E_Details.query.filter_by(Muscle_id=2,Purpose=plan.Purpose, Level=plan.Level)
    tmp = [
      Saturday(
        Week_id = week.id,
        E_Detail_id = exercise_begin[randint(1, exercise_main.count()-1)].id
      ),
      Saturday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Saturday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Saturday(
        Week_id = week.id,
        E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
      ),
      Saturday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Saturday(
        Week_id = week.id,
        E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
      ),
      Saturday(
        Week_id = week.id,
        E_Detail_id = exercise_end[1].id
      ),
      Saturday(
        Week_id = week.id,
        E_Detail_id = exercise_end[2].id
      )
    ]
    w.append(tmp)
    
    # #Todo---------------------------------------------------------------------Sun
    # exercise_main = E_Details.query.filter_by(Muscle_id=1,Purpose=plan.Purpose, Level=plan.Level)
    # exercise_extra = E_Details.query.filter_by(Muscle_id=2,Purpose=plan.Purpose, Level=plan.Level)
    # tmp = [
    #   Sunday(
    #     Week_id = week.id,
    #     E_Detail_id = exercise_begin[0].id
    #   ),
    #   Sunday(
    #     Week_id = week.id,
    #     E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
    #   ),
    #   Sunday(
    #     Week_id = week.id,
    #     E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
    #   ),
    #   Sunday(
    #     Week_id = week.id,
    #     E_Detail_id = exercise_main[randint(0, exercise_main.count()-1)].id
    #   ),
    #   Sunday(
    #     Week_id = week.id,
    #     E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
    #   ),
    #   Sunday(
    #     Week_id = week.id,
    #     E_Detail_id = exercise_extra[randint(0, exercise_extra.count()-1)].id
    #   ),
    #   Sunday(
    #     Week_id = week.id,
    #     E_Detail_id = exercise_end[0].id
    #   )
    # ]
    # w.append(tmp)
    
    for _ in w:
      for i in _:
        db.session.add(i)
    db.session.commit()
    write_log(f">>> User ({current_user.User_name}) have scheduled workouts!!!--")
    return redirect(url_for("views.schedule"))
  return render_template('client/schedule.html', user=current_user)

#!-------------------------------------------------------------------------------
@views.route("/acc_info", methods=['GET', 'POST'])
def acc_info():
  if not current_user.is_authenticated or not current_user.Status:
    flash("Hãy đăng nhập trước!",category='error')
    return redirect(url_for('auth.sign_in'))
  if request.method == "POST":
    hint_name = request.form.get('hint_name')
    gender = request.form.get('Gender')
    dob = request.form.get('DOB')
    note = request.form.get('Note')
  
    current_user.info(new_hint_name=hint_name, new_gender=gender, new_dob=dob, new_note = note)
    db.session.commit()
    write_log(f">>> User ({current_user.User_name}) is Updated information!-!-")
    flash("Cập nhật thông tin thành công!", category="success")
    return render_template('client/acc_info.html',user = current_user)
  else:
    return render_template('client/acc_info.html',user=current_user)

#!-------------------------------------------------------------------------------
@views.route("/acc_scr", methods=['GET', 'POST'])
def acc_scr():
  if not current_user.is_authenticated or not current_user.Status:
    flash("Hãy đăng nhập trước!",category='error')
    return redirect(url_for('auth.sign_in'))
  if not current_user.Hint_name or not current_user.Dob or not current_user.Gender:
    flash("Hãy nhập đầy đủ thông tin trước!",category='error')
    return redirect(url_for('views.acc_info'))
  if request.method == "POST":
    mail = request.form.get('mail')
    pwd = request.form.get('pwd')
    pwd1 = request.form.get('pwd1')
    pwd2 = request.form.get('pwd2')
    g_log = request.form.get('g_log')
    error = None
    if current_user.Admin and g_log:
      error = 1
      flash("Xuất file Log thành công!", category="success")
      send_mail()
    else:
      if mail == current_user.Email and not pwd1:
          flash("Bạn chưa thay đổi gì cả!", category="error")
          error = 1
      else:
        ps = None
        if not pwd:
          flash("Bạn chưa nhập mật khẩu!", category="error")
          error = 1
        elif not check_password_hash(current_user.Password,pwd):
          flash("Mật khẩu cũ không đúng!", category="error")
          error = 1
        
        elif mail != current_user.Email:
          if len(mail) < 4:
            flash("Email quá ngắn!", category="error")
            error = 1
          elif Users.query.filter_by(Email=mail).first():
            flash("Email đã được sử dụng!", category="error")
            error = 1
        
        elif len(pwd1) < 7:
          flash("Mật khẩu phải có ít nhất 7 ký tự!", category="error")
          error = 1
          ps = 1
        elif not pwd2:
          flash("Bạn chưa nhập xác nhận mật khẩu!", category="error")
          error = 1
          ps = 1
        elif pwd1 != pwd2:
          flash("Mật khẩu không khớp!", category="error")
          error = 1
          ps = 1
        if ps != 1 and pwd1:
          pwd = pwd1
    
    if error != 1:
      current_user.change_main(
        new_pwd = generate_password_hash(pwd, method='sha256'), 
        new_email=mail
      )
      db.session.commit()
      write_log(f">>> User ({current_user.User_name}) is Security updated!-!!")
      
      flash("Cập nhật bảo mật thành công!", category="success")
      flash("Hãy đăng nhập lại để xác nhận!", category="success")
      
      return redirect(url_for('auth.logout'))
  return render_template('client/acc_scr.html', user=current_user)

#!-------------------------------------------------------------------------------
@views.route("/about")
def about():
  return render_template('other/about.html', user=current_user, bar=True )