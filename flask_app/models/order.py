from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Order:
    db = 'subDeliciousSchema'
    def __init__(self, data):
        self.id  = data['id']
        self.method  = data['method']
        self.size  = data['size']
        self.bread  = data['bread']
        self.meat  = data['meat']
        self.toppings  = data['toppings']
        self.quantity  = data['quantity']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.user_id = data['user_id']

    @staticmethod
    def validate_order(order):
        isValid = True
        if len(order['toppings']) < 1:
            isValid = False
            flash("Please select at least one topping.", "order")
        return isValid

    @classmethod
    def newOrder(cls, data):
        query = 'INSERT INTO orders ( method, size, bread, meat, toppings, quantity, createdAt, updatedAt, user_id ) VALUES ( %(method)s, %(size)s, %(bread)s, %(meat)s, %(toppings)s, %(quantity)s, NOW(), NOW(), %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def updateOrder(cls, data):
        query = 'UPDATE orders SET method = %(method)s, size = %(size)s, bread = %(bread)s, meat = %(meat)s, toppings = %(toppings)s, quantity = %(quantity)s, updatedAT = NOW() WHERE id = %(id)s;'


    @classmethod
    def getRecentOrder(cls, data):
        query = 'SELECT * FROM orders LEFT JOIN users on orders.user_id = users.id  where user_id = %(id)s ORDER BY orders.id desc;'
        results = connectToMySQL(cls.db).query_db(query, data)
        return cls(results[0])

    @classmethod
    def deleteOrder(cls, data):
        query = 'DELETE FROM orders WHERE id = %(id)s;'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def getOneOrder(cls, data):
        query = 'SELECT * from orders WHERE id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])
