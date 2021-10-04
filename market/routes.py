from market import app, db
from market.models import User, Item
from market.form import Register
from flask import redirect, url_for, render_template, flash, get_flashed_messages

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market')
def market_page():
    item = Item.query.all()
    return render_template('market.html', items=item)

@app.route('/login')
def login_page():

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = Register()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password1.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('market_page'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'There was an error creating the user: {error}', category='danger')
    
    return render_template('register.html', form=form)
