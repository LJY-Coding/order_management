from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_bcrypt import Bcrypt
from flask_app.models import users, orders
from flask_app.models.customers import Customers

@app.route('/customers')
def customers():
    if 'user_id' in session:
        user = users.Users.get_by_id({ 'id': session['user_id']})
        order_counts =Customers.get_customer_orders()
        for customer in order_counts:
            if customer['orders'] > 1:
                data = {
                    'id': customer['customer_id'],
                    'status': 1
                }
                Customers.update_status(data)
        recent_orders = orders.Orders.get_recent_orders()
        sales_analysis = orders.Orders.sales_analysis()
        all_customers = Customers.get_all_customers()
        return render_template('customers.html', user = user, customers = all_customers, order_counts = order_counts, recent_orders=recent_orders, sales_analysis=sales_analysis)
    else:
        return redirect('/')

@app.route('/customers/new')
def new_customer():
    if 'user_id' in session:
        user = users.Users.get_by_id({ 'id': session['user_id']})
        recent_orders = orders.Orders.get_recent_orders()
        sales_analysis = orders.Orders.sales_analysis()
        state_list = Customers.state_list()
        return render_template('customer_new.html', user = user, state_list=state_list, recent_orders=recent_orders, sales_analysis=sales_analysis)
    else:
        return redirect('/')

@app.route('/customers/add', methods=['POST'])
def add_customer():
    if 'user_id' not in session:
        return redirect('/')
    if not Customers.validate_customer(request.form):
            return redirect('/customers/new')
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'contact': request.form['contact'],
        'address': request.form['address'],
        'city': request.form['city'],
        'state': request.form['state'],
        'zip': request.form['zip'],
    }
    Customers.create_customer(data)
    return redirect('/customers')


# Edit a selected customer
@app.route('/customers/edit/<customer_id>')
def customers_edit(customer_id):
    if 'user_id' not in session:
        return redirect('/customers')
    this_customer =  Customers.get_customer({'id': customer_id})
    user = users.Users.get_by_id({ 'id': session['user_id']})
    recent_orders = orders.Orders.get_recent_orders()
    sales_analysis = orders.Orders.sales_analysis()
    state_list = Customers.state_list()
    return render_template('customer_update.html', user = user, customer=this_customer, state_list=state_list, recent_orders=recent_orders, sales_analysis=sales_analysis)

@app.route('/customers/update/<customer_id>', methods=['POST'])
def customers_update(customer_id):
    if 'user_id' not in session:
        return redirect('/')
    if not Customers.validate_customer(request.form):
        return redirect(url_for('customers_edit', customer_id = customer_id))
    data = {
        'id': customer_id,
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'contact': request.form['contact'],
        'address': request.form['address'],
        'city': request.form['city'],
        'state': request.form['state'],
        'zip': request.form['zip']
    }
    Customers.update_customer(data)
    return redirect('/customers')

# Delete a selected recipe
@app.route('/customers/delete/<customer_id>')
def customers_delete(customer_id):
    if 'user_id' not in session:
        return redirect('/')
    Customers.destroy_customer({'id': customer_id})
    return redirect('/customers')