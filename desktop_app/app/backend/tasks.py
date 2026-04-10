#FUNÇÕES BACKEND DE MANIPULAÇÃO DE DADOS DA TABELA TAREFAS

import mysql.connector
import os
from dotenv import load_dotenv
load_dotenv()

def create_task(name, description, priority, due_date, user_id, category_id):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )

    cursor = conn.cursor()

    query = "INSERT INTO tasks(name, description, priority, due_date, user_id, category_id) VALUES(%s, %s, %s, %s, %s, %s)"
    values = (name, description, priority, due_date, user_id, category_id)

    cursor.execute(query, values)
    conn.commit()

    add_activity(user_id, f"Task '{name}' created")

    cursor.close()
    conn.close()
    return True


def delete_task(task_id: int, user_id: int, category_id: int) -> bool:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = "DELETE FROM tasks WHERE id = %s AND user_id = %s AND category_id = %s"

    cursor.execute(query, (task_id, user_id, category_id,))

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False

    conn.commit()

    cursor.close()
    conn.close()

    return True

def mark_completed(id: int, user_id: int) -> bool:

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        UPDATE tasks
        SET status = 'completed', completed_at = NOW()
        WHERE id = %s AND user_id = %s
        """
    
    values = (id, user_id)
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        conn.close()
        return False
    
    conn.commit()
    conn.close()
    return True

def mark_pending(id: int, user_id: int) -> bool:

    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
            UPDATE tasks
            SET status = 'pending',
                completed_at = NULL
            WHERE id = %s AND user_id = %s
    """

    values = (id, user_id)
    cursor.execute(query, values)

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False
    
    conn.commit()
    conn.close()

    return True

def count_tasks(user_id: int) -> int:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = "SELECT COUNT(*) FROM tasks WHERE user_id = %s"
    cursor.execute(query, (user_id,))

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else 0

def count_completed_status(user_id: int) -> int:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()
    query = """
        SELECT COUNT(*) 
        FROM tasks 
        WHERE user_id = %s AND status = 'completed'
    """
    
    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else 0

def count_pending_tasks(user_id: int) -> int:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        SELECT COUNT(*) 
        FROM tasks 
        WHERE user_id = %s
          AND status = 'pending'
          AND due_date >= CURDATE()
    """

    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else 0

def count_overdue_tasks(user_id: int) -> int:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        SELECT COUNT(*) 
        FROM tasks 
        WHERE user_id = %s
          AND status = 'pending'
          AND due_date < CURDATE()
    """

    cursor.execute(query, (user_id,))
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result[0] if result else 0

def get_weekly_completed_tasks(user_id: int) -> list[int]:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        SELECT DAYOFWEEK(completed_at) - 1 AS weekday,
            COUNT(*)
        FROM tasks
        WHERE user_id = %s
            AND completed_at IS NOT NULL
            AND completed_at >= DATE_SUB(CURDATE(), INTERVAL 6 DAY)
            AND completed_at <= CURDATE()
        GROUP BY weekday
    """

    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    week_data = [0] * 7

    for weekday, count in results:
        week_data[int(weekday)] = count

    return week_data

def category_statistics(user_id):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        SELECT 
            c.name,
            COALESCE(SUM(CASE WHEN t.status = 'completed' THEN 1 ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN t.status = 'pending' AND t.due_date >= CURDATE() THEN 1 ELSE 0 END), 0),
            COALESCE(SUM(CASE WHEN t.status = 'pending' AND t.due_date < CURDATE() THEN 1 ELSE 0 END), 0)
        FROM categories c
        LEFT JOIN tasks t ON t.category_id = c.id
        WHERE c.user_id = %s
        GROUP BY c.id
    """

    cursor.execute(query, (user_id,))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

import mysql.connector

def get_upcoming_deadlines(user_id: int, limit: int = 5):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        SELECT name, due_date, priority
        FROM tasks
        WHERE user_id = %s
          AND status = 'pending'
          AND due_date >= CURDATE()
        ORDER BY due_date ASC
        LIMIT %s
    """

    cursor.execute(query, (user_id, limit))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def add_activity(user_id: int, message: str):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        INSERT INTO activity (user_id, message) 
        VALUES (%s, %s)
    """

    cursor.execute(query, (user_id, message))
    conn.commit()

    cursor.close()
    conn.close()

def get_recent_activity(user_id: int, limit: int = 10):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        SELECT message, created_at
        FROM activity
        WHERE user_id = %s
        ORDER BY created_at DESC
        LIMIT %s
    """

    cursor.execute(query, (user_id, limit))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results

def get_tasks_by_category( user_id: int, category_id: int):
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        SELECT id, name, status, due_date, priority
        FROM tasks
        WHERE user_id = %s
          AND category_id = %s
        ORDER BY due_date ASC
    """

    cursor.execute(query, (user_id, category_id))
    results = cursor.fetchall()

    cursor.close()
    conn.close()

    return results


def complete_task(task_id: int, user_id: int, category_id: int) -> bool:
    conn = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME")
        )
    cursor = conn.cursor()

    query = """
        UPDATE tasks
        SET status = 'completed',
            completed_at = NOW()
        WHERE id = %s AND user_id = %s AND category_id = %s
    """

    cursor.execute(query, (task_id, user_id, category_id,))

    if cursor.rowcount == 0:
        cursor.close()
        conn.close()
        return False

    conn.commit()

    cursor.close()
    conn.close()

    return True