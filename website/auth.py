from flask import Blueprint,render_template,request,flash,redirect,url_for
from .moodels import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user
auth=Blueprint('auth',__name__)

@auth.route('/login',methods=["GET","POST"])
def login():
    password1=request.form.get("password1")
    email=request.form.get("email")
    user=User.query.filter_by(email=email).first()
    if user:
        if check_password_hash(user.password,password1):
            flash("You are logged in your account",category="sucess")
            login_user(user,remember=True)
            return redirect(url_for('views.home'))
        else:
            flash("Incorect password",category="error")
            return render_template("login.html",user=current_user)
    else:
        flash("Nu exista un cont cu acest email",category="error")
        return render_template("login.html",user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign-up",methods=['GET','POST'])
def sign_up():
    if request.method=="POST":
        pass1=request.form.get('password1')
        pass2=request.form.get('password2')
        firstName=request.form.get('firstName')
        email=request.form.get('email')
        user=User.query.filter_by(email=email).first()
        if user:
            flash("The email is already used,try other email",category="error")
        elif len(email)<5:
            flash("Emailul trebuie sa contine cel putin 5 caractere!",category="error")
        elif(len(firstName)<3):
            flash("Numele trebuie sa aiba cel putin 3 caractere!",category="error")
        elif(pass1!=pass2):
            flash("Parolele sunt diferite!",category="error")
        elif(len(pass1)<5):
            flash("Parola este prea scurta!",category="error")
        else:
            db.create_all()
            new_user=User(first_name=firstName,email=email,password=generate_password_hash(pass1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            flash("Contul a fost inregistrat cu succes !",category="success")
            return render_template("home.html",user=current_user)#render
    return render_template("signup.html",user=current_user)