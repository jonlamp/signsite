import sqlite3
import psycopg2, psycopg2.extras
import os


def get_db_connection(name):
    if 'DATABASE_URL' in os.environ:
        con = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
    else:
        con = psycopg2.connect(
            host = os.environ.get('PG_HOST'),
            dbname="simple_db", 
            user= os.environ.get('PG_USER'),
            password = os.environ.get('PG_PW')
        )
    return con

def get_totals():
    conn = get_db_connection('database.db')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    data = []
    query_sql = """
        SELECT star_sign As sign, personality as mbti, count(*) AS total 
        FROM responses
            INNER JOIN signs
            ON signs.id = responses.sign_id
            INNER JOIN personalities
            ON personalities.id = responses.personality_id
        GROUP BY star_sign, personality
        """
    cursor.execute(query_sql)
    rs = cursor.fetchall()
    for i in rs:
        data.append(dict(i))
    return data

def get_user_response(submission_id):
    conn = get_db_connection('database.db')
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    query_sql = """
        SELECT star_sign As sign, personality as mbti, selection
        FROM responses
            INNER JOIN signs
            ON signs.id = responses.sign_id
            INNER JOIN personalities
            ON personalities.id = responses.personality_id
        WHERE responses.id = """ + str(submission_id)
    cursor.execute(query_sql)
    rs = cursor.fetchall()
    return rs[0]

def get_user_data_dict(submission_id):
    data = get_totals()
    user_response = get_user_response(submission_id)
    result = {
        "user_response": user_response,
        "data": data
    }
    return result
