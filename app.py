from cgi import test
from distutils.command.config import config
from os import curdir
from flask import Flask, redirect, render_template, request, jsonify
from scripts.utilities import *
import sqlite3


app=Flask(__name__)

def get_db_connection(name):
    conn = sqlite3.connect(name)
    conn.row_factory = sqlite3.Row
    return conn

#@app.route("/")
#def hello_world():
#    con = sqlite3.connect('database.db')
#    cursor = con.cursor()
#    return render_template('home.html')

#@app.route("/check")
@app.route("/")
def check_db():
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(cursor.fetchall())
    cursor.execute("SELECT * FROM signs")
    signs = cursor.fetchall()
    cursor.execute("SELECT * FROM personalities")
    personalities = cursor.fetchall()
    return render_template('home.html',signs=signs, personalities=personalities)

@app.route("/submit")
def submit_handler():
    print("running submit handler")
    sign = request.args.get("sign")
    personality = request.args.get("personality")
    selection = request.args.get("selection")
    #check variables before continuing
    test_vars = [sign, personality, selection]
    for tv in test_vars:
        if not tv.isnumeric():
            return render_template('error.html') #return error page if an input isn't numeric
    con = sqlite3.connect('database.db')
    cursor = con.cursor()
    cursor.execute("INSERT INTO responses ('sign_id','personality_id','selection') VALUES (" + sign + "," + personality + "," + selection+");")
    con.commit()
    id = cursor.lastrowid
    con.close()
    return redirect("/submitted/" + str(id))

@app.route("/submitted/<int:submission_id>")
def submitted(submission_id):
    print("running submitted")
    con = sqlite3.connect('database.db')
    con.row_factory = sqlite3.Row
    cursor = con.cursor()
    if not isinstance(submission_id, int): #make sure the submission id is an integer for security reasons
        return render_template('error.html')
    #grab the user's submission
    cursor.execute("SELECT * FROM responses WHERE id = " + str(submission_id))
    submission = dict(cursor.fetchone())
    #now match these up to their table values
    cursor.execute("SELECT * FROM signs WHERE id = " + str(submission['sign_id']))
    sign_dict = dict(cursor.fetchone())
    cursor.execute("SELECT * FROM personalities WHERE id = " + str(submission['personality_id']))
    personality_dict = dict(cursor.fetchone())
    submission['sign'] = sign_dict
    submission['personality'] = personality_dict
    #get counts of all grouped by sign, personality and selection
    sql = """
    SELECT star_sign, personality, selection, count(*) as total 
    FROM responses
    LEFT JOIN signs ON responses.sign_id = signs.id
    LEFT JOIN personalities ON responses.personality_id = personalities.id
    GROUP BY star_sign, personality, selection
    """
    cursor.execute(sql)
    signs = {}
    personalities = {}
    for r in cursor.fetchall():
        r = dict(r)
        #signs
        if r['star_sign'] in signs.keys():
            signs[r['star_sign']] += r['total']
        else:
            signs[r['star_sign']] = r['total']
        #personalities
        if r['personality'] in personalities.keys():
            personalities[r['personality']] += r['total']
        else:
            personalities[r['personality']] = r['total']
    
    response_sign = submission['sign']['star_sign']
    response_personality = submission['personality']['personality']
    response_selection = submission['selection']

    signs_total = 0
    for sign in signs.keys():
        signs_total += signs[sign]
    
    personalities_total = 0
    for p in personalities.keys():
        personalities_total += personalities[p] 
    
    response_sign_rate = round((signs[response_sign] / signs_total) * 100,1)
    response_sign_selection_rate = 0
    response_personality_rate = round((personalities[response_personality] / personalities_total) * 100,1)
    response_personality_selection_rate = 0

    user_data = get_user_data_dict(submission_id)

    return render_template(
        'results.html',
        response_sign = response_sign,
        response_personality = response_personality,
        response_selection = response_selection,
        response_sign_rate = response_sign_rate,
        response_sign_selection_rate = response_sign_selection_rate,
        response_personality_rate = response_personality_rate,
        response_personality_selection_rate = response_personality_selection_rate,
        user_data = user_data
    )

@app.route('/api/<int:submission_id>')
def api_call(submission_id):
    data = get_totals()
    user_response = get_user_response(submission_id)
    result = {
        "user_response": user_response,
        "data": data
    }
    return jsonify(result)