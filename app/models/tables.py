from app import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(30))

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email

    def __repr__(self):
        return "<User %r>" % self.username


class Link_a(db.Model):
    __tablename__ = 'links'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    link = db.Column(db.Text)
    descricao = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    public = db.Column(db.String(5))

    user = db.relationship('User', foreign_keys=user_id)

    def __init__(self, name, link, descricao, user_id, public):
        self.name = name
        self.link = link
        self.descricao = descricao
        self.user_id = user_id
        self.public = public

    def __repr__(self):
        return "<Links %r>" % self.id

class Grupo(db.Model):
    __tablename__ = 'grupos'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    descricao = db.Column(db.String(100))
    main_user = db.Column(db.Integer, db.ForeignKey('users.id'))
    public = db.Column(db.Boolean)
    code = db.Column(db.Integer)

    def __init__(self, name, descricao, main_user, public, code):
        self.name = name
        self.descricao = descricao
        self.main_user = main_user
        self.public = public
        self.code = code

    def __repr__(self):
        return "<Goup %r>" % self.id

class UserGrupo(db.Model):
    __tablename__ = 'user_grupo'

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(db.Integer, db.ForeignKey('grupos.id')) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __init__(self, group_id, user_id):
        self.group_id = group_id
        self.user_id = user_id

    def __repr__(self):
        return "<Goup %r>" % self.id

class Link_Group(db.Model):
    __tablename__ = 'links_grupo'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    link = db.Column(db.Text)
    descricao = db.Column(db.String(100))
    group_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=group_id)

    def __init__(self, name, link, descricao, group_id):
        self.name = name
        self.link = link
        self.descricao = descricao
        self.group_id = group_id

    def __repr__(self):
        return "<Links por Grupo %r>" % self.id