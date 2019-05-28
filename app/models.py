from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def check_password_hash(self, password):
        return check_password_hash(self.password_hash, password)

    def set_password(self, password):
        password = generate_password_hash(password)
        self.password_hash = password

    def avatar(self, size):
        return 'http://www.gravatar.com/avatar/' + md5(self.email.encode("utf8")).hexdigest() + '?d=mm&s=' + str(size)

    def __repr__(self):
        return '<User %r>' % (self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))
