from flask import Flask, render_template, request
import db

app=Flask(__name__)

@app.route('/')
def index():
    return render_template('willkommen.html')

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     username = request.form['username']
#     password = request.form['password']
#     if username == 'admin' and password == '1234':
#         return render_template('willkommen.html', username=username)
#     else:
#         return render_template('login.html', fehler='Falscher Benutzername oder Passwort!')

@app.route('/search', methods=['GET'])
def search():
    search_query = request.args.get('q', '')

    if search_query:
        products = db.search(search_query)
        return render_template('search.html', products=products, query=search_query)

    return render_template('search.html', products=[], query=" ")

    

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)