from market import db, app, login_manager
from market import bcrypt
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    budget = db.Column(db.Integer(), nullable=False, default=1000)
    password = db.Column(db.String(1000), nullable=False)
    items = db.relationship("Item", backref=db.backref("owned_user", lazy=True))

    # Saving password as hash code using getter and setter
    @property
    def password_hash(self):
        return self.password

    @password_hash.setter
    def password_hash(self, plain_password):
        self.password = bcrypt.generate_password_hash(plain_password).decode("utf-8")

    # Check Hash Passwords
    def check_pwd(self, attempted_pwd):
        #attempted_hash_pwd = bcrypt.generate_password_hash(attempted_pwd)
        return bcrypt.check_password_hash(self.password, attempted_pwd)

    def __repr__(self):
        return f'User {self.id}'

    # Check if user have enough budget
    def can_buy(self, item):
        return self.budget >= item.price

    # Check if item is in user's property
    def can_sell(self, item):
        return item in self.items

class Item(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    barcode = db.Column(db.String(12), nullable=False)
    price = db.Column(db.Integer(), nullable=False)
    desc = db.Column(db.String(1000), nullable=False)
    owner = db.Column(db.Integer(), db.ForeignKey("user.id"))

    # Buy item
    def buy(self, user):
        self.owner = user.id
        user.budget -= self.price
        db.session.commit()

    # Sell item
    def sell(self, user):
        self.owner = None
        user.budget += self.price
        db.session.commit()
