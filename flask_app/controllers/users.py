from flask_app import app 
from flask import render_template, redirect, session, request, flash 
from flask_app.models.user import User 
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/')
def index(): 
    return render_template('index.html') 


@app.route('/loginPage') 
def loginPage(): 
    return render_template('login.html')


@app.route('/registerPage')
def registerPage(): 
    return render_template('register.html') 



@app.route('/register', methods=['POST']) 
def register(): 
    isValid = User.validate(request.form) 
    if not isValid: 
        return redirect('/registerPage') 
    newUser = {
        'firstName': request.form['firstName'], 
        'lastName': request.form['lastName'], 
        "street": request.form['street'],
        "city": request.form['city'],
        "state": request.form['state'], 
        "zipcode": request.form['zipcode'],
        'email': request.form['email'], 
        'password': bcrypt.generate_password_hash(request.form['password'])  
    }

    id = User.save(newUser) 
    if not id: 
        flash('Something went wrong!') 
        return redirect('/registerPage') 
    session['user_id'] = id 
    return redirect('/dashboard')


@app.route('/login', methods=['POST']) 
def login(): 
    data = {
        'email': request.form['email']
    }
    user = User.getEmail(data) 
    if not user: 
        flash('That email is not in our database. Please register', "login")
        return redirect('/loginPage')
    if not bcrypt.check_password_hash(user.password, request.form['password']): 
            flash('Incorrect password', "login") 
            return redirect('/loginPage')    

    session['user_id'] = user.id 
    return redirect('/dashboard')


@app.route('/dashboard')
def dashboard(): 
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'id': session['user_id']
    }

    return render_template("dashboard.html", user=User.getOne(data))


@app.route('/account')
def accountPage():
    if 'user_id' not in session: 
        return redirect('/logout')

    userData = {
        "id": session['user_id']
    }
    return render_template('account.html', user=User.getOne(userData), allOrders=User.getUserOrders(userData)) 

@app.route('/update', methods=['POST']) 
def update():
    if 'user_id' not in session:
        return redirect('/logout')
    if not User.validate(request.form):
        return redirect('/account')
    data = {
        "firstName": request.form['firstName'],  
        "lastName": request.form['lastName'],
        "street": request.form['street'],
        "city": request.form['city'],
        "state": request.form['state'], 
        "zipcode": request.form['zipcode'],
        "id": request.form['id']
    }
    User.update(data)
    return redirect('/dashboard')



@app.route('/addFavorite', methods=['POST'])
def favorite():
    data = {
        'user_id': session['user_id'],
        'order_id': request.form['order_id']
    }
    User.favorite(data)
    return redirect("/account") 



@app.route('/removeFavorite', methods=['POST'])
def removeFavorite():
    data = {
        'order_id': request.form['order_id']
    }
    User.unfavorite(data)
    return redirect("/dashboard") 



@app.route('/logout') 
def logout(): 
    session.clear() 
    return redirect('/')














@app.route('/test')
def test(): 

    return render_template("account.html")
