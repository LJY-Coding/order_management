from ..config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import users, customers, meals
from datetime import datetime
import re

class Orders:
    db = 'foodie'
    def __init__(self, data):
        self.id = data['id']
        self.meal_id = data['meal_id']
        self.customer_id = data['customer_id']
        self.order_source = data['order_source']
        self.order_date = data['order_date']
        self.status = data['status']
        self.quantity = data['quantity']
        self.total_price = data['total_price']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.customer = None
        self.user = None
        self.meal = None
        self.duration = {'seconds': 0, 'minutes': 0, 'hours': 0}

    @classmethod
    def create_order(cls, data):
        query = "INSERT INTO orders (id, meal_id, customer_id, order_source, order_date, \
            status, quantity, total_price, user_id) VALUE (%(id)s, %(meal_id)s, %(customer_id)s, %(order_source)s, \
            %(order_date)s, %(status)s, %(quantity)s, %(total_price)s, %(user_id)s)"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def get_all_orders(cls):
        query = "SELECT * FROM orders LEFT JOIN customers ON orders.customer_id = customers.id \
            LEFT JOIN users ON orders.user_id = users.id LEFT JOIN meals ON orders.meal_id = meals.id;"
        results = connectToMySQL(cls.db).query_db(query)
        orders = []
        for item in results:
            this_order = cls(item)
            data1= {
                'id': item['customer_id'],
                'first_name': item['first_name'],
                'last_name': item['last_name'],
                'email': item['email'],
                'contact': item['contact'],
                'address': item['address'],
                'city': item['city'],
                'state': item['state'],
                'zip': item['zip'],
                'status': item['status'],
                'created_at': item['customers.created_at'],
                'updated_at': item['customers.updated_at'],
                'is_deleted': item['customers.is_deleted']
            }
            this_order.customer = customers.Customers(data1)

            data2 = {
                'id': item['user_id'],
                'user_name': item['user_name'],
                'email': item['users.email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at'],
                'is_deleted': item['users.is_deleted']
            }
            this_order.user = users.Users(data2)

            data3 = {
                'id': item['meal_id'],
                'meal_group': item['meal_group'],
                'meal_name': item['meal_name'],
                'unit_price': item['unit_price'],
                'cost': item['cost'],
                'created_at': item['meals.created_at'],
                'updated_at': item['meals.updated_at'],
                'is_deleted': item['meals.is_deleted']
            }
            this_order.meal = meals.Meals(data3)
            orders.append(this_order)
        return orders

    @classmethod
    def get_order(cls, data):
        query = "SELECT * FROM orders LEFT JOIN customers ON orders.customer_id = customers.id \
            LEFT JOIN users ON orders.user_id = users.id LEFT JOIN meals ON orders.meal_id = meals.id WHERE orders.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        result = results[0]
        this_order = cls(results[0])
        data1= {
            'id': result['customer_id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
            'contact': result['contact'],
            'address': result['address'],
            'city': result['city'],
            'state': result['state'],
            'zip': result['zip'],
            'status': result['status'],
            'created_at': result['customers.created_at'],
            'updated_at': result['customers.updated_at'],
            'is_deleted': result['customers.is_deleted']
        }
        this_order.customer = customers.Customers(data1)

        data2 = {
            'id': result['user_id'],
            'user_name': result['user_name'],
            'email': result['users.email'],
            'password': result['password'],
            'created_at': result['users.created_at'],
            'updated_at': result['users.updated_at'],
            'is_deleted': result['users.is_deleted']
        }
        this_order.user = users.Users(data2)

        data3 = {
            'id': result['meal_id'],
            'meal_group': result['meal_group'],
            'meal_name': result['meal_name'],
            'unit_price': result['unit_price'],
            'cost': result['cost'],
            'created_at': result['meals.created_at'],
            'updated_at': result['meals.updated_at'],
            'is_deleted': result['meals.is_deleted']
        }
        this_order.meal = meals.Meals(data3)
        return this_order
    
    @classmethod
    def update_order(cls, data):
        query = "UPDATE orders SET meal_id=%(meal_id)s, customer_id=%(customer_id)s, order_source=%(order_source)s, \
            order_date=%(order_date)s, status=%(status)s, quantity=%(quantity)s, total_price=%(total_price)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def destroy_order(cls, data):
        query = "DELETE FROM orders WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def generate_order_id(cls, order_date):
        date_obj = datetime.strptime(order_date, "%Y-%m-%d")
        order_date_str = date_obj.strftime('%Y%m%d')
        query1 = f"SELECT COUNT(*) AS COUNT FROM orders WHERE order_date = '{order_date_str}'"
        results = connectToMySQL(cls.db).query_db(query1)
        order_count = results[0]['COUNT']
        order_id = f"{order_date_str}{order_count+1:04d}"

        # Check if the order_id already exists in the database
        query2 = f"SELECT COUNT(*) AS COUNT FROM orders WHERE id = '{order_id}'"
        results2 = connectToMySQL(cls.db).query_db(query2)
        order_id_count = results2[0]['COUNT']
        # If the order_id already exists, generate a new one recursively
        if order_id_count > 0:
            order_id = int(order_id) + 1

        return order_id
    
    @staticmethod
    def source_status():
        ss_list = { 'source_list' : ['Online', 'In Store'], 'status_list': ['Open', 'Complete']}
        return ss_list
    
    @classmethod
    def orders_oneday_analysis(cls):
        # Total Sales, Orders and revenue within the last 24 hrs
        query = "SELECT COUNT(o.order_id) AS total_orders, SUM(o.order_quantity) AS total_meals_sold, SUM(o.total_price) AS total_sales, SUM(o.total_cost) AS total_cost, SUM(o.total_price)-SUM(o.total_cost) AS total_revenue FROM ( \
                SELECT orders.id AS order_id, orders.quantity AS order_quantity, orders.total_price AS total_price, SUM(meals.cost*orders.quantity) AS total_cost FROM orders \
                LEFT JOIN meals ON orders.meal_id = meals.id WHERE orders.order_date >= DATE_SUB(NOW(), INTERVAL 1 DAY) GROUP BY orders.id ) AS o;"
        last_24hr = connectToMySQL(cls.db).query_db(query)
        results = last_24hr[0]        
        return results
    
    @classmethod
    def sales_analysis(cls):
        # Total new customers comparing to last 2 days categoriezed by order_source
        query = "SELECT COUNT(DISTINCT(id)) AS customer, order_source FROM orders WHERE orders.order_date >= DATE_SUB(NOW(), INTERVAL 1 DAY) GROUP BY order_source;"
        results = connectToMySQL(cls.db).query_db(query)

        query2 = "SELECT COUNT(DISTINCT(id)) AS customer, order_source FROM orders WHERE orders.order_date BETWEEN DATE_SUB(NOW(), INTERVAL 2 DAY) AND DATE_SUB(NOW(), INTERVAL 1 DAY) GROUP BY order_source;"
        results2 = connectToMySQL(cls.db).query_db(query2)

        # Total new customers comparing to last 2 days
        query3 = "SELECT COUNT(DISTINCT(id)) AS new_customer FROM orders WHERE orders.order_date >= DATE_SUB(NOW(), INTERVAL 1 DAY) GROUP BY DATE(order_date);"
        results3 = connectToMySQL(cls.db).query_db(query3)

        query4 = "SELECT COUNT(DISTINCT(id)) AS new_customer FROM orders WHERE orders.order_date BETWEEN DATE_SUB(NOW(), INTERVAL 2 DAY) AND DATE_SUB(NOW(), INTERVAL 1 DAY) GROUP BY DATE(order_date);"
        results4 = connectToMySQL(cls.db).query_db(query4)

        def sources_count(results):
            in_store = 0
            online = 0
            for item in results:
                if item['order_source'] == "In Store":
                    in_store = item['customer']
                elif item['order_source'] == "Online":
                    online = item['customer']
            return in_store, online
        
        def compare(data_24, data_48):
            if data_48 != 0:
                data_percent = round(((data_24 - data_48) / data_48) * 100, 2)
            else:
                data_percent = 100
            return data_percent

        in_store_24, online_24 = sources_count(results)
        in_store_48, online_48 = sources_count(results2)
        instore_percent = compare(in_store_24, in_store_48)
        online_percent = compare(online_24, online_48)
        try: 
            new_cust_24 = results3[0]['new_customer']
            new_cust_48 = results4[0]['new_customer']
        except:
            new_cust_24 = 0
            new_cust_48 = 0
        new_cust_percent = compare(new_cust_24, new_cust_48)
        analysis = {'online': online_24, 'online_per': online_percent, 'instore': in_store_24, 'instore_per': instore_percent, 'new_customer': new_cust_24, 'new_cust_per': new_cust_percent}
        # analysis = [{'cat': 'Online Orders', 'data_24': online_24, 'data_per': online_percent}, {'cat': 'In Store Orders', 'data_24': in_store_24, 'data_per': instore_percent}, {'cat': 'New Customers', 'data_24': new_cust_24, 'data_per': new_cust_percent}]
        return analysis

    @classmethod
    def get_recent_orders(cls):
        query = "SELECT *, TIMEDIFF(NOW(), orders.created_at) AS duration FROM orders LEFT JOIN meals ON orders.meal_id = meals.id \
            LEFT JOIN users ON orders.user_id = users.id WHERE orders.order_date >= DATE_SUB(NOW(), INTERVAL 1 DAY);"
        results = connectToMySQL(cls.db).query_db(query)
        recent_orders = []
        for item in results:
            this_order = cls(item)
            data = {
                'id': item['user_id'],
                'user_name': item['user_name'],
                'email': item['email'],
                'password': item['password'],
                'created_at': item['users.created_at'],
                'updated_at': item['users.updated_at'],
                'is_deleted': item['users.is_deleted']
            }
            this_order.user = users.Users(data)

            data2 = {
                'id': item['meal_id'],
                'meal_group': item['meal_group'],
                'meal_name': item['meal_name'],
                'unit_price': item['unit_price'],
                'cost': item['cost'],
                'created_at': item['meals.created_at'],
                'updated_at': item['meals.updated_at'],
                'is_deleted': item['meals.is_deleted']
            }
            this_order.meal = meals.Meals(data2)
            hours, minutes, seconds = str(item['duration']).split(":")
            this_order.duration['seconds'] = int(seconds)
            this_order.duration['minutes'] = int(minutes)
            this_order.duration['hours'] = int(hours)
            recent_orders.append(this_order)
        return recent_orders
    
    @staticmethod
    def validate_order(data):
        is_valid = True
        if not data['order_source'] or data['order_source'] == "Choose...":
            flash(u'Must select an order source', 'order_info')
            is_valid = False
        if not data['customer_id'] or data['customer_id'] == "Choose...":
            flash(u'Must select a customer', 'order_info')
            is_valid = False
        if not data['meal_id']:
            flash(u'Must select a meal', 'order_info')
            is_valid = False
        if not data['order_date']:
            flash(u'Must select an order date', 'order_info')
            is_valid = False
        if not data['quantity']:
            flash(u'Must enter a quantity', 'order_info')
            is_valid = False
        return is_valid