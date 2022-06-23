from winreg import QueryInfoKey
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
        if order['quantity'] < 1:
            isValid = False
            flash("Please change the quantity of sandwiches to at least one.", "order")
        return isValid

    @classmethod
    def newOrder(cls, data):
        query = 'INSERT INTO orders ( method, size, bread, meat, toppings, quantity, createdAt, updatedAt, user_id ) VALUES ( %(method)s, %(size)s, %(bread)s, %(meat)s, %(toppings)s, %(quantity)s, NOW(), NOW(), %(user_id)s);'
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def updateOrder(cls, data):
        query = 'UPDATE orders SET method = %(method)s, size = %(size)s, bread = %(bread)s, meat = %(meat)s, toppings = %(toppings)s, quantity = %(quantity)s, updatedAT = NOW() WHERE id = %(id)s;'

    @classmethod
    def getAllUserOrders(cls, data):
        query = 'SELECT * from orders where user_id=%(user_id)s order by id desc;'
        results = connectToMySQL(cls.db).query_db(query, data)
        orders = []
        for order in results:
            orders.append(cls(order))
        return orders

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

    @classmethod
    def unfavoritedOrders(cls,data):
        query = "SELECT * FROM orders WHERE orders.id NOT IN ( SELECT order_id FROM favorites WHERE user_id = %(id)s );"
        results = connectToMySQL('orders').query_db(query,data)
        orders = []
        for row in results:
            orders.append(cls(row))
        print(orders)
        return orders

