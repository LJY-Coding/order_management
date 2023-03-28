from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re

PRICE_REGEX = re.compile(r'\d+.?\d+')
class Meals:
    db = 'foodie'
    def __init__(self, data):
        self.id = data['id']
        self.meal_group = data['meal_group']
        self.meal_name = data['meal_name']
        self.unit_price = data['unit_price']
        self.cost = data['cost']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.is_deleted = data['is_deleted']

    @classmethod
    def create_meal(cls, data):
        query = "INSERT INTO meals (meal_group, meal_name, unit_price, cost) VALUE (%(meal_group)s, %(meal_name)s, %(unit_price)s, %(cost)s)"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results
    
    @classmethod
    def get_meal(cls, data):
        query = "SELECT * FROM meals WHERE id = %(id)s AND is_deleted = 0;"
        results = connectToMySQL(cls.db).query_db(query, data)
        if not results:
            return False
        this_meal = cls(results[0])
        return this_meal

    @classmethod
    def get_all_meals(cls):
        query = "SELECT * FROM meals WHERE is_deleted = 0"
        results = connectToMySQL(cls.db).query_db(query)
        meals = []
        for item in results:
            meals.append(cls(item))
        return meals

    @classmethod
    def update_meal(cls, data):
        query = "UPDATE meals SET meal_group=%(meal_group)s, meal_name=%(meal_name)s, unit_price=%(unit_price)s, \
            cost=%(cost)s WHERE id = %(id)s"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @classmethod
    def destroy_meal(cls, data):
        query = "UPDATE meals SET is_deleted = 1 WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        return results

    @staticmethod
    def menu_list():
        menu_list = ['Ace Meal', 'Super Meal', 'Happy Meal', 'Big Meal']
        return menu_list
    
    @staticmethod
    def validate_meal(data):
        is_valid = True
        if not PRICE_REGEX.match(data['cost']):
            flash(u'Invalid cost!', 'meal_info')
            is_valid = False
        if not PRICE_REGEX.match(data['unit_price']):
            flash(u'Invalid unit price!', 'meal_info')
            is_valid = False
        if len(data['meal_name']) < 2:
            flash(u'Invalid meal name!', 'meal_info')
            is_valid = False
        return is_valid