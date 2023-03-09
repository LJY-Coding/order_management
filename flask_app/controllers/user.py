from flask_app import app
from flask import Flask, render_template

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/customers')
def customers():
    return render_template('customers.html')

@app.route('/orders')
def orders():
    return render_template('orders.html')

@app.route('/forms')
def forms():
    return render_template('forms.html')

@app.route('/analytics')
def analytics():
    return render_template('analytics.html')