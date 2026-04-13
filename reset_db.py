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
            ('Geheimes Admin-Handbuch', 0.00, 'Streng vertraulich: Nur für Administratoren sichtbar')
        ]

        cursor.executemany(products_sql, products_data)

        users_sql = "INSERT INTO users (username, password, role) VALUES (%s, %s, %s)"
        users_data = [
            ('admin', 'super_geheimes_admin_passwort_123', 'admin'),
            ('max_mustermann', 'passwort1', 'user'),
            ('maria_musterfrau', 'passwort2', 'user')
        ]

        cursor.executemany(users_sql, users_data)

        conn.commit()
        print("Datenbank zurückgesetzt! Es sind 3 Produkte und 3 Nutzer angelegt.")

        cursor.execute("""
        CREATE TABLE orders ( 
             id INT AUTO_INCREMENT PRIMARY KEY,
             name VARCHAR(255) NOT NULL,
             price DECIMAL(10, 2) NOT NULL,
             user_id INT NOT NULL,
             notes TEXT
        );
        """)

    except mysql.connector.Error as err:
        print(f"Fehler beim Zurücksetzen der Datenbank: {err}")

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

if __name__ == '__main__':
    reset_database()



