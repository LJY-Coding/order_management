from ..config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import orders
import re


EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PHONE_REGEX = re.compile(r'[0-9]')
ZIP_REGEX = re.compile(r'\d{5}')
NAME_REGEX = re.compile(r'^\d{10}+')
class Customers:
    db = 'foodie'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.contact = data['contact']
        self.address = data['address']
        self.city = data['city']
        self.state = data['state']
        self.zip = data['zip']
        self.status = data['status']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.is_deleted = data['is_deleted']


    @classmethod
    def create_customer(cls, data):
        query = "INSERT INTO customers (first_name, last_name, email, \
            contact, address, city, state, zip) VALUE (%(first_name)s, %(last_name)s, %(email)s, \
            %(contact)s, %(address)s, %(city)s, %(state)s, %(zip)s)"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)
        return results
    
    @classmethod
    def get_customer(cls, data):
        query = "SELECT * FROM customers WHERE id = %(id)s AND is_deleted = 0;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        this_customer = cls(results[0])
        return this_customer
    
    @classmethod
    def get_all_customers(cls):
        query = "SELECT * FROM customers WHERE is_deleted = 0"
        results = connectToMySQL(cls.db).query_db(query)
        customers = []
        for item in results:
            customers.append(cls(item))
        return customers
    
    @classmethod
    def update_customer(cls, data):
        query = "UPDATE customers SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, \
            contact=%(contact)s, city=%(city)s, state=%(state)s, zip=%(zip)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def destroy_customer(cls, data):
        query = "UPDATE customers SET is_deleted = 1 WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @staticmethod
    def state_list():
        state_list = ['MA', 'NY', 'MO', 'LA', 'TX']
        return state_list
    
    @classmethod
    def get_customer_orders(cls):
        query = "SELECT COUNT(customer_id) AS orders, customer_id FROM orders GROUP BY customer_id;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        return results
    
    @classmethod
    def update_status(cls, data):
        query = "UPDATE customers SET status=%(status)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @staticmethod
    def validate_customer(data):
        is_valid = True
        if len(data['first_name']) < 2 or len(data['last_name']) < 2:
            flash(u'Must enter a valid name', 'customer_info')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash(u'Invalid email address!', 'customer_info')
            is_valid = False
        if len(data['address']) < 2:
            flash(u'Invalid address!', 'customer_info')
            is_valid = False
        if len(data['city']) < 2:
            flash(u'Invalid city!', 'customer_info')
            is_valid = False
        if not ZIP_REGEX.match(data['zip']):
            flash(u'Invalid zip code!', 'customer_info')
            is_valid = False
        if not PHONE_REGEX.match(data['contact']):
            flash(u'Invalid contact, expected to be 10 digits phone number!', 'customer_info')
            is_valid = False
        return is_valid