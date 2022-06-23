from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app.models import order
from flask import flash 
import re 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User: 
    db = 'subDeliciousSchema'
    def __init__(self,data): 
        self.id = data['id']
        self.firstName = data['firstName']
        self.lastName = data['lastName']
        self.email = data['email']
        self.password = data['password']
        self.street = data['street']
        self.city = data['city']
        self.zipcode = data['zipcode']
        self.state = data['state']
        self.createdAt = data['createdAt']
        self.updatedAt = data['updatedAt']
        self.orders = []
        self.favorites = []


    @staticmethod
    def validate(user):
        isValid = True
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        results = connectToMySQL(User.db).query_db(query,user)
        print(results)
        if len(results) >= 1:
            isValid = False
            flash("That email is already taken!", "register")
        if not EMAIL_REGEX.match(user['email']):
            isValid = False
            flash("Invalid email format.", "register")
        if len(user['firstName']) < 2:
            isValid = False
            flash('First name must be at least 2 characters long.', "register")
        if len(user['lastName']) < 2:
            isValid = False
            flash('Last name must be at least 2 characters long.', "register")
        if len(user['password']) < 8:
            isValid = False
            flash('Password must be at least 8 characters long', "register")
        if user['password'] != user['confirm']:
            isValid = False
            flash('Passwords do not match', "register")
        if len(user['street']) < 1:
            isValid = False
            flash('Please provide street name.', "register")
        if len(user['city']) < 1:
            isValid = False
            flash('Please provide city.', "register")
        if len(user['zipcode']) < 5:
            isValid = False
            flash('Please provide zipcode.', "register")
        if len(user['state']) < 2:
            isValid = False
            flash('Please provide state.', "register")
        return isValid
    

    @classmethod 
    def getOne(cls, data):
        query = 'SELECT * FROM users WHERE id = %(id)s;' 
        results = connectToMySQL(cls.db).query_db(query, data) 
        if len(results) < 1: 
            return False 
        return cls(results[0]) 
        


    @classmethod
    def update(cls, data):
        query = "UPDATE users SET firstName=%(firstName)s, lastName=%(lastName)s, street=%(street)s, city=%(city)s, state=%(state)s, zipcode=%(zipcode)s, updatedAt=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)


    @classmethod 
    def getEmail(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;' 
        results = connectToMySQL(cls.db).query_db(query, data) 
        if len(results) < 1: 
            return False 
        return cls(results[0]) 
    
    @classmethod
    def save(cls, data ):
        query = "INSERT INTO users ( firstName , lastName , email , password, street, city, zipcode, state, createdAt, updatedAt ) VALUES ( %(firstName)s , %(lastName)s , %(email)s , %(password)s, %(street)s, %(city)s, %(zipcode)s, %(state)s,  NOW() , NOW() );"
        return connectToMySQL(cls.db).query_db( query, data )
    

    @classmethod
    def favorite(cls,data): 
        query = "INSERT INTO favorites (user_id, order_id) VALUES (%(user_id)s, %(order_id)s);"
        return connectToMySQL(cls.db).query_db( query, data ) 
    

    @classmethod
    def unfavorite(cls,data): 
        query = "DELETE FROM favorites WHERE order_id= %(order_id)s;"
        return connectToMySQL(cls.db).query_db( query, data )
    
    
    @classmethod
    def getUserFavorites(cls,data): 
        query = "SELECT * from orders LEFT join favorites on favorites.order_id = orders.id LEFT JOIN users on favorites.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db( query, data ) 
        user = cls(results[0])
        for row in results:
            orderData = {
                'id': row['orders.id'],
                'method': row['method'],
                'size': row['size'],
                'bread': row['bread'],
                'meat': row['meat'], 
                'toppings': row['toppings'],
                'quantity': row['quantity'],
                'user_id': row['user_id'],
                'createdAt': row['orders.createdAt'],
                'updatedAt': row['orders.updatedAt']
            }
            user.favorites.append( order.Order( orderData ) )
            user.orders.append(orderData["id"])
        return user
        
    @classmethod
    def unfavoritedOrders(cls,data):
        query = "SELECT * FROM orders WHERE orders.id NOT IN ( SELECT order_id FROM favorites WHERE user_id = %(id)s );"
        results = connectToMySQL('orders').query_db(query,data)
        orders = []
        for row in results:
            orders.append(cls(row))
        print(orders)
        return orders

    @classmethod 
    def getUserOrders(cls,data):
        query = "SELECT * FROM users LEFT JOIN orders ON users.id = orders.user_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])
        for row in results: 
            orderData = {
                'id': row['orders.id'],
                'method': row['method'],
                'size': row['size'],
                'bread': row['bread'],
                'meat': row['meat'], 
                'toppings': row['toppings'],
                'quantity': row['quantity'],
                'user_id': row['user_id'],
                'createdAt': row['orders.createdAt'],
                'updatedAt': row['orders.updatedAt']
            }
            user.orders.append(order.Order(orderData)) 
        return user 