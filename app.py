from flask import Flask, render_template, request, session, redirect
import db
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv
import re

load_dotenv()

app=Flask(__name__)
app.secret_key = 'secret_key'

DB_USER = os.getenv("DB_USERNAME")
DB_PASS = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db_orm=SQLAlchemy(app)

class User (db_orm.Model):
    __tablename__ = 'users'
    id=db_orm.Column(db_orm.Integer, primary_key=True)
    username = db_orm.Column(db_orm.String(80),unique=True, nullable=False)
    password = db_orm.Column(db_orm.String(200),nullable=False)
    role = db_orm.Column(db_orm.String(50))
    

def validate_search_input(user_input):
    if not user_input:
        return user_input
    pattern = re.compile(r'^[a-zA-Z0-9\s\-äöüÄÖÜß]+$')
    if not pattern.match(user_input):
        raise ValueError("Ungültige Zeichen in der Sucheingabe")
    return user_input    

@app.route('/')
def index():
    return render_template('willkommen.html')


@app.route('/search', methods=['GET'])
def search():
    try:
        search_query = validate_search_input(request.args.get('q', ''))
    except ValueError:
        return "Ungültige Eingabe", 400
    

    if search_query:
        products = db.search(search_query)
    else:
        # Wenn nichts gesucht wird, zeige alle Produkte an
        products = db.get_all_products()

    return render_template('search.html', products=products, query=search_query)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '')
        passwort = request.form.get('password', '')
        #user = db.login(username, passwort)
        user= User.query.filter_by(username=username, password=passwort).first()
        if user:
            # Nutzerdaten in der Session speichern
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role

            products = db.get_all_products()
            return render_template('login.html', success=True, user=user, products=products)
        else:
            return render_template('login.html', success=False, error="Falscher Benutzername oder Passwort.")
    return render_template('login.html')

@app.route('/order', methods=['GET'])
def order_page():
    name = request.args.get('name', '')
    return render_template('order.html', name=name)

@app.route('/orders', methods=['GET'])
def view_orders():
    # Wenn niemand eingeloggt ist, zurück zum Login schicken
    if 'user_id' not in session:
        return redirect('/login')

    role = session.get('role')
    user_id = session.get('user_id')
    if role == 'admin':
        orders = db.get_all_orders()
    else:
        orders = db.get_user_orders(user_id)

    return render_template('orders.html', orders=orders, role=role)

@app.route('/checkout', methods= ['POST'])
def checkout():
    name = request.form.get('name')
    notes = request.form.get('notes', '')
    user_id = session.get('user_id', 1)
    
    db.order(name,notes,user_id)
    return f"<h3>Bestellung erfolgreich!</h3><p>Du hast '{name}' bestellt.</p><a href='/search'>Zurück zum Shop</a>"



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
