from app import app, db, lm
from flask import render_template, flash, redirect, url_for, request, jsonify, render_template
from flask_login import login_user, logout_user, current_user
from json import dumps

from app.models.tables import User, Link_a
from app.models.forms import LoginForm, RegisterForm, LinkForm

@lm.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route("/index/<user>")
@app.route("/index")
@app.route("/")
def index():
    return render_template('index.html')

@app.route("/login/", methods=["GET", "POST"])
def login(): 
    form = LoginForm()
    if form.validate_on_submit():

        user = User.query.filter_by(username=form.username.data).first()

        if user and user.password == form.password.data:
            login_user(user)
            return redirect(url_for("links"))
        else:
            flash("Invalid Login.")

    return render_template('login.html', form=form)


@app.route("/logout/")
def logout():
    logout_user()
    flash("Logged out.")
    return redirect(url_for("index"))


#cadastrar
@app.route("/register/", methods=["GET", "POST"])
def register():
    form = RegisterForm()

    user_name = User.query.filter_by(username=form.username.data).first()
    name = User.query.filter_by(name=form.name.data).first()
    email = User.query.filter_by(email=form.email.data).first()

    if form.is_submitted():
        if user_name == None and email == None and name == None:
            #INSERT
            i = User(form.username.data, form.password.data, form.name.data, form.email.data)
            db.session.add(i)
            db.session.commit()

            flash("Registro feito")
            return render_template('index.html', form=form)
        else:
            flash("Falha no registro")
            if user_name != None:
                flash("Este nome de usuário já está em uso")
            if name != None:
                flash("Este nome já está em uso")
            if email != None:
                flash("Este e-mail já está em uso")
            return render_template('register.html', form=form)

    return render_template('register.html', form=form)


@app.route("/links")
def links():
    if current_user.is_authenticated:
        link_1 = Link_a.query.all()
        return render_template('links.html', links=link_1)
    else:
        return render_template('index.html')

@app.route("/links/register", methods=["GET", "POST"])
def links_register():
    if current_user.is_authenticated:
        form = LinkForm()
        name = Link_a.query.filter_by(name=form.name.data, user_id=current_user.id).first()
        link_1 = Link_a.query.filter_by(link=form.link.data, user_id=current_user.id).first()

        if name != None:
            if name.user_id != current_user.id:
                name = None
        if link_1 != None:
            if link_1.user_id != current_user.id:
                link_1 = None

        if form.is_submitted():
            if name == None and link_1 == None:
                #INSERT
                i = Link_a(form.name.data, form.link.data, form.descricao.data, current_user.id)
                db.session.add(i)
                db.session.commit()

                flash("Link registrado")
            else:
                flash("Falha no registro")
            if name != None:
                flash("Este nome já está em uso")
            if link_1 != None:
                flash("Este link já tem registo")

        return render_template('register_link.html', form=form, links="")
    else:
        return render_template('index.html')


@app.route('/remove/link/<int:id>', methods=["GET", "POST"])
def remove_link(id):
    if current_user.is_authenticated:
        link_1 = Link_a.query.get(id)
        db.session.delete(link_1)
        db.session.commit()
        link_1 = Link_a.query.all()
        return render_template('links.html', links=link_1)
    else:
        return render_template('index.html')

@app.route('/edit/link/<int:id>', methods=["GET", "POST"])
def edit_link(id):
    link_1 = Link_a.query.get(id)
    form = LinkForm()

    if current_user.is_authenticated:
        if request.method == 'POST':
            nome_tst = Link_a.query.filter_by(name=form.name.data, user_id=current_user.id).first()
            link_tst = Link_a.query.filter_by(link=form.link.data, user_id=current_user.id).first()

            link_1.name = form.name.data
            link_1.descricao = form.descricao.data
            link_1.link = form.link.data
            db.session.commit()
            link_1 = Link_a.query.all()
            return render_template('links.html', links=link_1)
        else:
            return render_template('edit_link.html', form=form, link_a=link_1)
    else:
        return render_template('links.html', links=link_1)



# -------------------------------------------------------TESTE------------------------------------------------
# @app.route("/teste/<info>")
# @app.route("/teste", defaults={"info":None})
# def teste(info):
#     r = User.query.filter_by(password="1234").first() #first() - retorna apenas o primeiro registro
#     print(r) #r.name - retorna paenas o atributo name
    
#     # r.name = "Teste"
#     # db.session.add(r) - edita o atributo
    
#     # db.session.delete(r) - deleta o registro

#     # INSERT
#     # i = User("DaniloABC", "12345", "Danilo Alves B", "daniloab786@gmail.com")
#     # db.session.add(i)
#     # db.session.commit()
#     return "OK"
