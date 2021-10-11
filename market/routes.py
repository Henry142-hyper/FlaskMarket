from market import app, db, login_manager
from market.models import User, Item
from market.form import PurchaseForm, Register, LoginForm, SellForm
from flask import redirect, url_for, render_template, flash, get_flashed_messages, request
from flask_login import login_user, logout_user, current_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods=["GET", "POST"])
@login_required
def market_page():
    # Purchasing and Selling Logic
    purchase_form = PurchaseForm()
    sell_form = SellForm()
    if request.method == "POST":
        purchase_item = request.form.get("purchase_item")
        p_item_obj = Item.query.filter_by(name=purchase_item).first()
        if p_item_obj:
            if current_user.can_buy(p_item_obj):
                p_item_obj.buy(current_user)
                flash(f"You have successfully purchased {purchase_item}", category="success")
            else:
                flash(f"You don't have enough money to purchase {purchase_item}", category="danger")
    
        sell_item = request.form.get("sell_item")
        s_item_obj = Item.query.filter_by(name=sell_item).first()
        if s_item_obj:
            if current_user.can_sell(s_item_obj):
                s_item_obj.sell(current_user)
                flash(f"You have successfully sold {sell_item} with {s_item_obj.price}$.", category="success")
            else:
                flash(f"Something went wrong! Please try again later.", category="danger")

        return redirect(url_for("market_page"))

    # Returning items and owned_items during GET method
    if request.method == "GET":
        owned_items = Item.query.filter_by(owner=current_user.id)
        item = Item.query.filter_by(owner=None)
        return render_template('market.html', items=item, purchase_form=purchase_form, 
                                owned_items=owned_items, sell_form=sell_form)

# Login
@app.route('/login', methods=["GET", "POST"])
def login_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        attempted_user = User.query.filter_by(username=login_form.username.data).first()
        if attempted_user and attempted_user.check_pwd(login_form.password.data):
            login_user(attempted_user)
            flash(f"You have logged in as {attempted_user.username}.", category="success")
            return redirect(url_for("market_page"))
        else:
            flash("Username or Password is incorrect. Please try again!", category="danger")

    return render_template('login.html', form=login_form)

# Register
@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = Register()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data, password_hash=form.password1.data)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash(f"You have successfully created an account. You are logged in as {user.username}.", category="success")
        return redirect(url_for('market_page'))
    
    if form.errors != {}:
        for error in form.errors.values():
            flash(f'There was an error creating the user: {error}', category='danger')
    
    return render_template('register.html', form=form)

# Logout
@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have successfully logged out!", category="info")
    return redirect(url_for('home_page'))


