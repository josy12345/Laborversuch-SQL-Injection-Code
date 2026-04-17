from flask import Flask, render_template, request, session, redirect
import db

app=Flask(__name__)
app.secret_key = 'secret_key'

@app.route('/')
def index():
    return render_template('willkommen.html')


@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('q', '')

    if search_query:
        # Wenn gesucht wird, nutze die Suchfunktion
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
        user = db.login(username, passwort)
        if user:
            # HIER: Nutzerdaten in der Session speichern
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']

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
    # Logik für die Rollenverteilung
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
