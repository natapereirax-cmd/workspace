#FUNÇÕES BACKEND DE MANIPULAÇÃO DE DADOS DA TABELA CATEGORIA

import mysql.connector

import os
from dotenv import load_dotenv
load_dotenv()


def create_category(name, user_id):
    conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
    )

    cursor = conn.cursor()

    query = "INSERT INTO categories (name, user_id) VALUES (%s, %s)"
    values = (name, user_id)

    try:
        cursor.execute(query, values)
        conn.commit()
        return True
    except:
        return False
    finally:
        cursor.close()
        conn.close()


def delete_category(category_id: int, user_id: int) -> bool:
    conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()

    query = "DELETE FROM categories WHERE id = %s AND user_id = %s"

    cursor.execute(query, (category_id, user_id,))

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False

    conn.commit()

    cursor.close()
    conn.close()

    return True

def load_categories(user_id):
    conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
    )

    cursor = conn.cursor()

    query = "SELECT id, name FROM categories WHERE user_id = %s"
    
    cursor.execute(query, (user_id,))

    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results 

def count_categories(user_id: int) -> int:
    conn = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
    )
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM categories WHERE user_id = %s"
    cursor.execute(query, (user_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else 0
