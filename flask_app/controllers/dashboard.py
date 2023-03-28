from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_bcrypt import Bcrypt
from flask_app.models import users, orders

@app.route('/dashboard')
def dashboard():
    if 'user_id' in session:
        user = users.Users.get_by_id({ 'id': session['user_id']})
        oneday_analysis = orders.Orders.orders_oneday_analysis()
        recent_orders = orders.Orders.get_recent_orders()
        sales_analysis = orders.Orders.sales_analysis()
        return render_template('dashboard.html', user = user, recent_orders=recent_orders, oneday_analysis = oneday_analysis, sales_analysis=sales_analysis)
    else:
        return redirect('/')