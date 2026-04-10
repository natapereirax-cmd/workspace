#FUNÇÕES BACKEND DE MANIPULAÇÃO DE DADOS DA TABELA USUARIOS

import mysql.connector
import hashlib
import os
from dotenv import load_dotenv
load_dotenv()


def hash_password(password, salt):
    if isinstance(salt, str):
        salt = salt.encode()

    return hashlib.sha256(password.encode() + salt).hexdigest()


def get_user(email):
    try:
        conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )

        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE email = %s"
        cursor.execute(query, (email,))

        return cursor.fetchone()

    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def insert_user(firstname, lastname, username, email, password, salt):
    conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
    )

    cursor = conn.cursor()
    
    query = "INSERT INTO users (firstname, lastname, username, email, password, salt) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (firstname, lastname, username, email, password, salt)

    cursor.execute(query, values)
    conn.commit()

    cursor.close()
    conn.close()

def email_exists(email):
    conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
    )

    cursor = conn.cursor()
    cursor.execute(
        'SELECT 1 FROM users WHERE email = %s LIMIT 1', (email,)
    )
    result = cursor.fetchone() is not None

    cursor.close()
    conn.close()

    return result