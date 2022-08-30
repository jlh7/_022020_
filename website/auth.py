from flask import Blueprint, render_template, request, redirect, url_for, flash,session
from .models import Users
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, current_user
from . import db,  write_log

auth = Blueprint('auth', __name__)

@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
  if current_user.is_authenticated and current_user.Status:
    return redirect(url_for("views.home"))
  if request.method == "POST":
    uid = request.form.get('uid').lower()
    pwd = request.form.get('pwd')

    user = Users.query.filter_by(User_name=uid).first()
    text_uid = 0
		
    if user: 
      if check_password_hash(user.Password,pwd):
        login_user(user)
        user.Status = True
        session.permanent = True
        db.session.commit()
        if user.Dev == False:
          write_log(f">>> User ({user.User_name}) is logged!!--")
          flash('Đăng nhập thành công! Cùng trải nghiệm nào!', category='success')
        elif user.Dev == True:
          write_log(f">>> Admin ({current_user.User_name}) is logged!!--")
          flash(f'Chào nhà phát triển, {user.Hint_name}!', category='success')
        return redirect(url_for('views.home'))
      else:
        flash("Mật khẩu không đúng!",category='error')
        text_uid = 1
    else:
      flash("Tên đăng nhập không tồn tại!",category='error')
    if text_uid == 0:
      return render_template('client/sign_in.html',user = current_user, bar=True)
    else:
      text_uid = uid
      return render_template('client/sign_in.html',user = current_user, text_uid=text_uid, bar=True)
  else:
    return render_template("client/sign_in.html", user = current_user, bar=True)

@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
  if current_user.is_authenticated and current_user.Status:
    return redirect(url_for("views.home"))
  if request.method == "POST":
    email = request.form.get('email').lower()
    uid = request.form.get('uid').lower()
    pwd1 = request.form.get('pwd1')
    pwd2 = request.form.get('pwd2')

    user = Users.query.filter_by(User_name=uid).first()
    text_email=0
    text_uid = 0
  
    if user:
      flash("Tên đăng nhập đã tồn tại!",category='error')
      text_email = 1
    elif Users.query.filter_by(Email=email).first():
      flash("Email đã tồn tại!",category='error')
      text_uid = 1
    elif len(uid) < 3:
      flash("Tên tài khoản quá ngắn!",category='error')
      text_email = 1
    elif len(email) < 4:
      flash("Email quá ngắn!",category='error')
      text_uid = 1
    elif pwd1 != pwd2:
      flash("Mật khẩu không khớp!",category='error')
    elif len(pwd1) < 7:
      flash("Mật khẩu phải ít nhất 7 ký tự",category='error')
    else:
      new_user = Users(
        Admin = False,
        User_name=uid, 
        Email=email, 
        Password=generate_password_hash(pwd1, method='sha256')
      )
      db.session.add(new_user)
      db.session.commit()
      login_user(new_user)
      session.permanent = True
      write_log(f">>> User ({current_user.User_name}) is Registered!---")
      flash("Tạo tài khoản thành công! \nBây giờ bạn hãy điền các thông tin bên dưới nhé!", category='success')
      new_user.Status = True
      return redirect(url_for('views.acc_info'))
    if text_uid == 1 and text_email == 1:
      return render_template('client/sign_up.html',user = current_user, bar=True)
    elif text_email == 1 and text_uid == 0:
      text_email = email
      return render_template('client/sign_up.html',user = current_user, text_email=text_email, bar=True)
    elif text_uid == 1 and text_email == 0:
      text_uid = uid
      return render_template('client/sign_up.html',user = current_user, text_uid=text_uid, bar=True)
    else:
      text_uid = uid
      text_email = email
      return render_template('client/sign_up.html',user = current_user, text_uid=text_uid, text_email=text_email, bar=True)
  else:
    return render_template("client/sign_up.html", user = current_user, bar=True)


@auth.route('/logout')
def logout():
  if not current_user.is_authenticated:
    flash("Hãy đăng nhập trước!",category='error')
    return redirect(url_for('auth.sign_in'))
  current_user.Status=False
  db.session.commit()
  write_log(f">>> User ({current_user.User_name}) is Signed out!---")
  logout_user()
  return redirect(url_for('auth.sign_in'))