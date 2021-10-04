from market import db, app
from market import bcrypt

class User(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(1000), nullable=False)

    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self, plain_password):
        self.password = bcrypt.generate_password_hash(plain_password)

    def __repr__(self):
        return f'User {self.id}'

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(12), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
