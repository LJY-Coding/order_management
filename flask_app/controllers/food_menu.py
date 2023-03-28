from flask_app import app
from flask import render_template, redirect, request, session, url_for, flash
from flask_bcrypt import Bcrypt
from flask_app.models import users, meals, orders

@app.route('/meals')
def food_menu():
    if 'user_id' in session:
        user = users.Users.get_by_id({ 'id': session['user_id']})
        all_meals = meals.Meals.get_all_meals()
        recent_orders = orders.Orders.get_recent_orders()
        sales_analysis = orders.Orders.sales_analysis()
        return render_template('food_menu.html', user = user, meals=all_meals, recent_orders=recent_orders, sales_analysis=sales_analysis)
    else:
        return redirect('/')

@app.route('/meals/new')
def new_meal():
    if 'user_id' in session:
        user = users.Users.get_by_id({ 'id': session['user_id']})
        menu_list = meals.Meals.menu_list()
        recent_orders = orders.Orders.get_recent_orders()
        sales_analysis = orders.Orders.sales_analysis()
        return render_template('menu_new.html', user = user, menu_list=menu_list, recent_orders=recent_orders, sales_analysis=sales_analysis)
    else:
        return redirect('/')

@app.route('/meals/add', methods=['POST'])
def add_meal():
    if 'user_id' not in session:
        return redirect('/')
    if not meals.Meals.validate_meal(request.form):
            return redirect('/meals/new')
    data = {
        'meal_group': request.form['meal_group'],
        'meal_name': request.form['meal_name'],
        'unit_price': request.form['unit_price'],
        'cost': request.form['cost']
    }
    meals.Meals.create_meal(data)
    return redirect('/meals')

# Edit a selected meal
@app.route('/meals/edit/<meal_id>')
def meals_edit(meal_id):
    if 'user_id' not in session:
        return redirect('/meals')
    this_meal =  meals.Meals.get_meal({'id': meal_id})
    user = users.Users.get_by_id({ 'id': session['user_id']})
    recent_orders = orders.Orders.get_recent_orders()
    sales_analysis = orders.Orders.sales_analysis()
    menu_list = meals.Meals.menu_list()
    return render_template('menu_update.html', user = user, meal=this_meal, menu_list=menu_list, recent_orders=recent_orders, sales_analysis=sales_analysis)

@app.route('/meals/update/<meal_id>', methods=['POST'])
def meals_update(meal_id):
    if 'user_id' not in session:
        return redirect('/')
    if not meals.Meals.validate_meal(request.form):
        return redirect(url_for('meals_edit', meal_id = meal_id))
    data = {
        'id': meal_id,
        'meal_group': request.form['meal_group'],
        'meal_name': request.form['meal_name'],
        'unit_price': request.form['unit_price'],
        'cost': request.form['cost']
    }
    meals.Meals.update_meal(data)
    return redirect('/meals')

# Delete a selected recipe
@app.route('/meals/delete/<meal_id>')
def meals_delete(meal_id):
    if 'user_id' not in session:
        return redirect('/')
    meals.Meals.destroy_meal({'id': meal_id})
    return redirect('/meals')

