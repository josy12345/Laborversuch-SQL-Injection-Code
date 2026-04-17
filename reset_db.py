import mysql.connector
import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_USERNAME = os.getenv("DB_USERNAME")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

def reset_database():
    print ("Datenbank wird zurück gesetzt...")

    try:
        conn = mysql.connector.connect(
            host=DB_HOST,
            user=DB_USERNAME,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Verbunden mit Datenbank.")
        cursor = conn.cursor()

        cursor.execute("DROP TABLE IF EXISTS products;")
        cursor.execute("DROP TABLE IF EXISTS users;")
        cursor.execute("DROP TABLE IF EXISTS orders;")

        cursor.execute("""
        CREATE TABLE products(
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL,
            description TEXT
        );
        """)

        cursor.execute("""
        CREATE TABLE users(
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            role VARCHAR(50) DEFAULT 'user'
        );
        """)

        products_sql = "INSERT INTO products (name, price, description) VALUES (%s, %s, %s)"
        products_data = [
            ('Laptop', 999.99, 'Leistungsstarker Laptop für Studierende'),
            ('Smartphone', 499.00, 'Neustes Modell mit hochauflösender Kamera'),
            ('Tablet', 299.50, 'Perfekt für Notizen in der Vorlesung'),
            ('Kopfhörer', 149.99, 'Noise-Cancelling für ungestörtes Lernen'),
            ('USB-C Hub', 24.99, 'Erweitert deinen Laptop um wichtige Anschlüsse'),
            ('Mechanische Tastatur', 89.00, 'Für lange Programmier-Sessions'),
            ('Monitor 27 Zoll', 199.99, '4K Monitor für mehr Übersicht'),
            ('Ergonomische Maus', 39.50, 'Schont das Handgelenk bei langer Nutzung'),
            ('Smartwatch', 199.00, 'Behalte deine Nachrichten im Blick'),
            ('Powerbank 20000mAh', 35.00, 'Ausreichend Strom für lange Uni-Tage'),
            ('Webcam 1080p', 59.99, 'Für gestochen scharfe Online-Meetings'),
            ('WLAN-Router', 79.90, 'Schnelles Internet für die WG'),
            ('Netzwerkkabel 10m', 12.50, 'Für eine stabile Verbindung ohne Abbrüche'),
            ('Externe Festplatte 2TB', 65.00, 'Backups für die Bachelorarbeit'),
            ('USB-Stick 128GB', 15.99, 'Schneller Datentransfer für Präsentationen'),
            ('Grafikkarte RTX 4070', 649.00, 'Für Machine Learning und Gaming'),
            ('Kaffeemaschine', 45.00, 'Die wichtigste Hardware für Studierende'),
            ('HDMI-Kabel 2m', 9.99, 'Verbindet deinen Laptop mit Monitoren und Beamern'),
            ('Bluetooth-Lautsprecher', 45.00, 'Kompakter Sound für unterwegs'),
            ('Laptoptasche 15 Zoll', 29.99, 'Wasserabweisend und gut gepolstert')
        ]

        cursor.executemany(products_sql, products_data)

        users_sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        users_data = [
            ('max_mustermann', 'passwort1', 'user'),
            ('maria_musterfrau', 'passwort2', 'user'),
            ('student_01', 'klausur2026', 'user'),
            ('student_02', 'sommersemester!', 'user'),
            ('admin', 'super_geheimes_admin_passwort_123', 'admin'),
            ('dozent_schmidt', 'K0mpl3x3sP4ssw0rt!', 'user'),
            ('gast_account', 'gast1234', 'user'),
            ('josy', 'h4ckth3pl4n3t!', 'admin'),
            ('tutor_informatik', 'tut_pw_99', 'user'),
            ('praktikant_01', 'praxis2026', 'user')
        ]

        cursor.executemany(users_sql, users_data)

        
        cursor.execute("""
        CREATE TABLE orders ( 
             id INT AUTO_INCREMENT PRIMARY KEY,
             name VARCHAR(255) NOT NULL,
             price DECIMAL(10, 2) NOT NULL,
             user_id INT NOT NULL,
             notes TEXT
        );
        """)

        orders_sql = "INSERT INTO orders (name, price, user_id, notes) VALUES (%s, %s, %s, %s)"
        orders_data = [
            # user_id 3 ist max_mustermann
            ('Laptop', 999.99, 3, 'Bitte schnell liefern, mein alter PC ist kaputt.'),
            ('USB-C Hub', 24.99, 3, 'Bitte im selben Paket wie den Laptop verschicken.'),

            # user_id 4 ist maria_musterfrau
            ('Tablet', 299.50, 4, 'Wird für die Vorlesungen benötigt.'),

            # user_id 5 ist student_01
            ('Kopfhörer', 149.99, 5, 'Klingel ist defekt, bitte klopfen!'),

            # user_id 7 ist dozent_schmidt
            ('Kaffeemaschine', 45.00, 7, 'Lieferung an Büro C320, Fakultät Informatik.')
        ]
        cursor.executemany(orders_sql, orders_data)

        # Jetzt erst wird ALLES (Produkte, User und Bestellungen) fixiert
        conn.commit()
        print("Datenbank zurückgesetzt! Es sind 20 Produkte, 10 Nutzer und 5 Bestellungen angelegt.")
    except mysql.connector.Error as err:
        print(f"Fehler beim Zurücksetzen der Datenbank: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    reset_database()



