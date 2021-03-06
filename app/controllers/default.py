from app import app, db, lm
from flask import render_template, flash, redirect, url_for, request, jsonify, render_template
from flask_login import login_user, logout_user, current_user
from json import dumps

from app.models.tables import User, Link_a, Grupo, UserGrupo, Link_Group
from app.models.forms import LoginForm, RegisterForm, LinkForm, GoupForm

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


@app.route("/links/")
def links():
    if current_user.is_authenticated:
        link_1 = Link_a.query.all()
        return render_template('links.html', links=link_1)
    else:
        return render_template('index.html')

@app.route("/comunidade/")
def comunit():
    link_1 = Link_a.query.all()
    return render_template('link_comunit.html', links=link_1)


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
                result = 'Nao'
                #INSERT
                if form.public.data == True:
                    result = 'Sim'
                    print("public ", result)
                else:
                    result = 'Nao'
                    print("private ", result)
                i = Link_a(form.name.data, form.link.data, form.descricao.data, current_user.id, result)
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


@app.route("/user/<int:user_id>", methods=["GET", "POST"], endpoint='user')
def usuario(user_id):
    if current_user.is_authenticated:
        user_1 = User.query.get(user_id)
        link_1 = Link_a.query.all()
        return render_template('perfil.html', links=link_1, users=user_1)
    else:
        flash('Entre com uma conta para acessar o usuário')
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

            if form.public.data == True:
                result = 'Sim'
                print("public ", result)
            else:
                result = 'Nao'
                print("private ", result)

            link_1.public = result

            db.session.commit()
            link_1 = Link_a.query.all()
            return render_template('links.html', links=link_1)
        else:
            return render_template('edit_link.html', form=form, link_a=link_1)
    else:
        return render_template('links.html', links=link_1)


#Grupos

@app.route('/grupos/')
def grupos():
    if current_user.is_authenticated:
        grupos = Grupo.query.all()
        return render_template('groups.html', grupos=grupos)
    else:
        return render_template('index.html')

@app.route('/grupo/<int:code>/<int:id>')
def grupo(code, id):
    if current_user.is_authenticated:
        grupos = Grupo.query.get(id)
        return render_template('groups.html', grupos=grupos)
    else:
        link_1 = Link_a.query.all()
        return render_template('index.html')

@app.route("/grupos/register", methods=["GET", "POST"])
def grupos_register():
    if current_user.is_authenticated:
        form = GoupForm()
        grupo_g = Grupo.query.all()
        name = Grupo.query.filter_by(name=form.name.data).first()
        if form.is_submitted():
            if name == None:
                #INSERT
                id_g = Grupo.query.all()
                numb_g = 0
                for g in id_g:
                    if g.main_user == current_user.id:
                        numb_g += 1

                i = Grupo(form.name.data, form.descricao.data, current_user.id, form.public.data, ((current_user.id*31)+numb_g))
                db.session.add(i)
                db.session.commit()
                
                #Grupos_user
                if g.main_user == current_user.id:
                    i = UserGrupo((current_user.id*31)+numb_g, current_user.id)
                    db.session.add(i)
                    db.session.commit()

                flash("Grupo registrado")
            else:
                flash("Falha no registro")
            if name != None:
                flash("Este nome já está em uso")

        return render_template('register_group.html', form=form, links="")
    else:
        return render_template('index.html')


@app.route('/remove/grupo/<int:id>', methods=["GET", "POST"])
def remove_group(id):
    if current_user.is_authenticated:
        grupo_1 = Grupo.query.get(id)
        db.session.delete(grupo_1)
        db.session.commit()
        grupos = Grupo.query.all()
        return render_template('groups.html', grupos=grupos)
    else:
        return render_template('index.html')
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
