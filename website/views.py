from flask import Blueprint,render_template,redirect,url_for
from flask_login import login_user,login_required,logout_user,current_user
from flask import request,flash
from . import db
from .moodels import Table,User

views=Blueprint('views',__name__)  
@views.route('/',methods=["GET","POST"])
@login_required
def home():
        price=[]
        product=[]
        buc=[]
        db.create_all()
        table = Table.query.filter_by(user_id=current_user.id).all()
        if request.method=="POST":
            tableName=request.form.get('tableName')
            products=request.form.get('Products')
            cp_prod=products.split(",")
            if len(tableName) < 1:  
                flash("Numele pe care l-ati dat mesei este invalid !",category="error")
                return render_template('home.html',table=table, user = current_user)
            if len(products)<3:
                flash("INTRODUCETI PRODUSE !",category="error")
                return render_template('home.html',table=table, user = current_user)
            if ',' not in products :
                flash("NU ATI RESPECTAT FORMATUL NUME_PRODUS,BUC,PRET!",category="error")
                return render_template('home.html',table=table, user = current_user)
            else:
                products=''
                for i in range(len(cp_prod)//3):
                    product.append(cp_prod[i*3])
                    buc.append(cp_prod[i*3+1].replace('buc',''))
                    price.append(cp_prod[i*3+2].replace('lei',''))
                    products +=str(product[i]) + ',' + str(buc[i]) + 'buc'+ ','+ str(price[i]) + 'lei' ','+'\n'
                s=0
                for i in range(len(price)):
                    a=int(buc[i].replace("buc",''))
                    b=float(price[i].replace("lei",''))
                    s=s+a*b
            new_table = Table(name=tableName,user_id=current_user.id,products=products,total=s)
            db.session.add(new_table)
            db.session.commit()
            flash("Masa adaugata cu succes !",category="success")
            return redirect(url_for('views.home'))
        return render_template("home.html",table=table,user = current_user)


@views.route('/delete/<int:id>',methods=["GET","POST"])
def delete(id):
        table_del=Table.query.get_or_404(id)
        try:
            db.session.delete(table_del)
            db.session.commit()
            flash("You deleted a table ",category="success")
            return redirect(url_for('views.home'))

        except:
            flash("Something went wrong...")
            return redirect(url_for('views.home'))


@views.route('/edit/<int:id>/<string:name>',methods=["GET","POST"])
@login_required
def edit(id,name):
        table = Table.query.filter_by(user_id=current_user.id, name=name).all()
        #if method==post1
            #stergem produsele care au fost platite si scadem suma(fara sa scadem de la admin)
        #if ...=post2
            #am introdus un produs gresit stergem din baza de date si scadem suma de la admin
        #if ....=post3:
            #adaugam produse la masa respectiva
        #if .....=post4
            #am terminat tot ce aveam de facut si ne intoarcem unde trebuie(url(for home))

            
        return render_template("edit.html",table=table)
    #returnam template basic
