#ENVIO DE DADOS DE SIGNUP PARA A TABELA DE USUARIOS

import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

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