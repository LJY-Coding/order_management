from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_bcrypt import Bcrypt
from flask_app.models import users

bcrypt = Bcrypt(app)
# Login
@app.route('/')
def index():
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.clear()
    return redirect('/')

# Login
@app.route('/login', methods=['POST'])
def login():
    try: 
        user = users.Users.get_by_email({'email': request.form['email']})
        if not user:
            flash(u'Invalid Email/Password', 'login')
            return redirect('/')
        if not bcrypt.check_password_hash(user.password, request.form['password']):
            flash(u'Invalid Email/Password', 'login')
            return redirect('/')
    except: 
        flash(u'Invalid Email/Password', 'login')
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

# Register
@app.route('/register', methods=['POST'])
def register():
    if not users.Users.validate_user(request.form):
        return redirect('/')
    if request.form['password'] != request.form['confirm_pwd']:
        flash(u"Those passwords didn't match. Try again.", 'register')
        return redirect('/')
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'user_name': request.form['user_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user = users.Users.create_user(data)
    session['user_id'] = user
    return redirect('/dashboard')
