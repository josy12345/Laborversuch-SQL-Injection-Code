import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Verbindung zur Datenbank wird hergestellt, indem die Konfiguration aus den Umgebungsvariablen verwendet werden (.env).
def get_db():
    conn = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USERNAME,
        password=DB_PASSWORD,
        database=DB_NAME,
    )
    return conn

# Funktion zur Produktsuche in der Datenbank. Nimmt den eingegebenen Suchbegriff entgegen.
def search(search_term):
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)
    query = f"SELECT * FROM products WHERE name LIKE '%{search_term}%';"
    print(f"[DEBUG] Generierte SQL-Query: {query}")
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Gibt alle Produkte aus der Datenbank zurück.
def get_all_products():
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)
    query = "SELECT * FROM products"
    cursor.execute(query)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results

# Überprüft die Anmeldedaten der nutzenden Person. Gleicht den übergebenen usernamen und passwort mit der Datenbank ab.
def login(username, password):
    conn = get_db()
    cursor = conn.cursor(dictionary=True, buffered=True)
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    print(f"[DEBUG] Generierte SQL-Query: {query}")
    cursor.execute(query)
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user

# Legt eine neue Bestellung für eine nutzende Person an. Ermittelt den aktuellen Preis des Produkts und speichert als Nächstes die Bestelldaten.
def order(name, notes, user_id=1):
    conn = get_db()
    cursor = conn.cursor(buffered=True)

    # Preis wird ausgelesen
    query = f"SELECT price FROM products WHERE name = '{name}'"
    print(f"Generierte SQL-Query: {query}")
    cursor.execute(query)
    result = cursor.fetchone()
    price = float(result[0]) if result else 0.00


    # Bestellung in die Datenbank eintragen
    query = f"INSERT INTO orders (name, price, user_id, notes) VALUES('{name}', {price}, {user_id}, '{notes}')"
    print(f"[DEBUG] Generierte SQL-Query: {query}")
    try:
        cursor.execute(query)

        # 2. Wir springen durch alle Ergebnisse, damit alle angehängten
        #    Befehle der SQL-Injection ausgeführt werden
        while cursor.nextset():
            pass

        conn.commit()
        success = True
    except Exception as e:
        print(f"Es ist ein Fehler bei der Bestellung aufgetreten: {e}")
        success = False
    cursor.close()
    conn.close()
    return success