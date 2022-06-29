from crypt import methods
from flask_app import app
from flask import render_template, redirect, session, request
from flask_app.models.order import Order
from flask_app.models.user import User


# Editing an order

@app.route('/order/edit/<int:id>')
def editOrder(id):
    if 'user_id' not in session:
        return redirect('/logout')
    
    data = {
        'user_id': session['user_id']
    }

    order_data = {
        'id': id
    }
    order = Order.getOneOrder(order_data)
    user = User.getOne(data)
    return render_template('editOrder.html', order = order, user=user)


@app.route('/order/update', methods = ['POST'])
def updateOrder():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Order.validate_order(request.form):
        return redirect('/checkout')
    order_data = {
        'id' : request.form['id'],
        'method' : request.form['method'],
        'size' : request.form['size'],
        'bread' : request.form['bread'],
        'meat' : request.form['meat'],
        'toppings' : request.form['toppings'],
        'quantity' : request.form['quantity'],
    }
    Order.updateOrder(order_data)
    return redirect('/checkout')

# Checkout Page

@app.route('/order/checkout/<int:id>')
def checkout(id):
    if 'user_id' not in session:
        return redirect ('/logout')
    order_data = {
        'id' : id
    }
    user_data = {
        'user_id': session['user_id']
    }    
    order = Order.getOneOrder(order_data)
    user = User.getOne(user_data)
    return render_template('checkout.html', order = order, user = user)

# Order Confirmation Page

@app.route('/checkout/confirmation/<int:id>')
def confirmation(id):
    if 'user_id' not in session:
        return redirect ('/logout')
    order_data = {
        'id' : id
    }
    user_data = {
        'user_id': session['user_id']
    }    
    order = Order.getOneOrder(order_data)
    user = User.getOne(user_data)
    return render_template('confirmation.html', order = order, user = user) 


# Creating a new order!

@app.route('/order/new')
def newOrder():
    if 'user_id' not in session: 
        return redirect ('/logout')
    data = {
        'id': session['user_id']
    }
    return render_template('newOrder.html', user=User.getOne(data))


@app.route('/order/submit', methods = ['POST'])
def submitOrder():
    isValid = Order.validate_order(request.form)
    if not isValid:
        return redirect('/order/new')
    newOrder = {
        'method' : request.form['method'],
        'size' : request.form['size'],
        'bread' : request.form['bread'],
        'meat' : request.form['meat'],
        'toppings' : request.form['toppings'],
        'quantity' : request.form['quantity'],
        'user_id' : session['user_id']       
    }
    Order.newOrder(newOrder)
    return redirect('/checkout')

# if the user deletes their order at checkout (or deletes it from their favorites?)

@app.route('/order/delete/<int:id>')
def startOverOrder(id):
    if 'user_id' not in session:
        return redirect('/logout')
    order_data = {
        'id': id
    }
    Order.deleteOrder(order_data)
    return redirect('/dashboard')