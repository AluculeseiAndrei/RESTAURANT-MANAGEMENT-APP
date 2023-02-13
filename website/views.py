from flask import Blueprint,render_template,redirect,url_for
from flask_login import login_user,login_required,logout_user,current_user
from flask import request,flash
from . import db
from .moodels import Table,User

views=Blueprint('views',__name__)  

@views.route('/',methods=["GET","POST"])
@login_required
def home():
        table = Table.query.filter_by(user_id=current_user.id).all()
        if request.method=="POST":
            tableName=request.form.get('tableName')
            if len(tableName) < 1:  
                flash("Numele pe care l-ati dat mesei este invalid !",category="error")
                return render_template('home.html',table=table, user = current_user)
            else:
                db.create_all()
                new_table = Table(name=tableName,user_id=current_user.id)
                db.session.add(new_table)
                db.session.commit()
                flash("Masa adaugata cu succes !",category="success")
                return redirect(url_for('views.home'))
        return render_template("home.html",table=table,user = current_user)