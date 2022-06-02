import sqlite3

def get_db_connection(name):
    conn = sqlite3.connect(name)
    conn.row_factory = sqlite3.Row
    return conn

def get_totals():
    conn = get_db_connection('database.db')
    cursor = conn.cursor()
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
    c = cursor.execute(query_sql)
    rs = c.fetchall()
    for i in rs:
        data.append(dict(i))
    return data

def get_user_response(submission_id):
    conn = get_db_connection('database.db')
    cursor = conn.cursor()
    query_sql = """
        SELECT star_sign As sign, personality as mbti, selection
        FROM responses
            INNER JOIN signs
            ON signs.id = responses.sign_id
            INNER JOIN personalities
            ON personalities.id = responses.personality_id
        WHERE responses.id = """ + str(submission_id)
    c = cursor.execute(query_sql)
    rs = c.fetchall()
    return dict(rs[0])

def get_user_data_dict(submission_id):
    data = get_totals()
    user_response = get_user_response(submission_id)
    result = {
        "user_response": user_response,
        "data": data
    }
    return result
