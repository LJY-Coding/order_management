from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_bcrypt import Bcrypt
from flask_app.models import users, customers, meals
from flask_app.models.orders import Orders
from datetime import date


@app.route('/orders')
def orders():
    if 'user_id' in session:
        user = users.Users.get_by_id({ 'id': session['user_id']})
        all_orders = Orders.get_all_orders()
        recent_orders = Orders.get_recent_orders()
        sales_analysis = Orders.sales_analysis()
        return render_template('orders.html', user = user, orders = all_orders, recent_orders=recent_orders, sales_analysis=sales_analysis)
    else:
        return redirect('/')

@app.route('/orders/new')
def new_order():
    if 'user_id' in session:
        user = users.Users.get_by_id({ 'id': session['user_id']})
        all_customers = customers.Customers.get_all_customers()
        all_meals = meals.Meals.get_all_meals()
        recent_orders = Orders.get_recent_orders()
        sales_analysis = Orders.sales_analysis()
        return render_template('order_new.html', user = user, customers=all_customers, meals=all_meals, recent_orders=recent_orders, sales_analysis=sales_analysis)
    else:
        return redirect('/')

@app.route('/orders/add', methods=['POST'])
def add_order():
    if 'user_id' not in session:
        return redirect('/')
    if not Orders.validate_order(request.form):
        return redirect('/orders/new')
    meal = meals.Meals.get_meal({'id' : request.form['meal_id']})
    quantity = int(request.form['quantity'])
    price = meal.unit_price
    data = {
        'id': Orders.generate_order_id(request.form['order_date']),
        'meal_id': request.form['meal_id'],
        'customer_id': request.form['customer_id'],
        'order_source': request.form['order_source'],
        'order_date': request.form['order_date'],
        'status': request.form['status'],
        'quantity': quantity,
        'total_price': price*quantity,
        'user_id': session['user_id']
    }
    Orders.create_order(data)
    return redirect('/orders')

# Edit a selected customer
@app.route('/orders/edit/<order_id>')
def orders_edit(order_id):
    if 'user_id' not in session:
        return redirect('/orders')
    this_order =  Orders.get_order({'id': order_id})
    all_customers = customers.Customers.get_all_customers()
    recent_orders = Orders.get_recent_orders()
    sales_analysis = Orders.sales_analysis()
    all_meals = meals.Meals.get_all_meals()
    ss_list = Orders.source_status()
    user = users.Users.get_by_id({ 'id': session['user_id']})
    return render_template('order_update.html', user = user, order=this_order, customers=all_customers, meals=all_meals, ss_list = ss_list, recent_orders=recent_orders, sales_analysis=sales_analysis)

@app.route('/orders/update/<order_id>', methods=['POST'])
def orders_update(order_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Orders.validate_order(request.form):
        return redirect(url_for('orders_edit', order_id = order_id))
    meal = meals.Meals.get_meal({'id' : request.form['meal_id']})
    quantity = int(request.form['quantity'])
    price = meal.unit_price
    data = {
        'id': order_id,
        'meal_id': request.form['meal_id'],
        'customer_id': request.form['customer_id'],
        'order_source': request.form['order_source'],
        'order_date': request.form['order_date'],
        'status': request.form['status'],
        'quantity': quantity,
        'total_price': price*quantity,
        'user_id': session['user_id']
    }
    Orders.update_order(data)
    return redirect('/orders')

# Delete a selected recipe
@app.route('/orders/delete/<order_id>')
def orders_delete(order_id):
    if 'user_id' not in session:
        return redirect('/')
    Orders.destroy_order({'id': order_id})
    return redirect('/orders')

