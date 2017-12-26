from flask import Flask, request, render_template, g, session, redirect, url_for
from run import *
import os
import sqlite3
import pandas as pd
import webbrowser


app = Flask(__name__)
app.config['SECRET_KEY'] = 'half-life 3 confirmed'
app.config['DATABASE'] = os.path.join(app.root_path, 'player_data.db')


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    return conn


def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


# the to-be frontend
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        conn = get_db()
        value = str(request.form.get('choose'))
        result = None
        if value == 'match':
            result = query_db_match(conn)
        if value == 'today':
            result = query_db_today(conn)
        if value == 'week':
            result = query_db_week(conn)
        if value == 'month':
            result = query_db_month(conn)
        if value == 'lifetime':
            result = query_db_lifetime(conn)
        if result is None:
            return render_template('index.html')
        else:
            session['result'] = result
            return redirect(url_for('results'))
    else:
        return render_template('index.html')


@app.route('/results')
def results():
    # result = session['result']
    return render_template('results.html') # result=result


# backend POST request handler
@app.route('/GS', methods=['POST'])
def GSHandler():
    if request.is_json:
        payload = request.get_json()
        conn = get_db()
        if check_payload(payload):
            stats_df = parse_payload(payload)
            print(stats_df)
            print('\n')
            stats_df.to_sql("per_round_data", conn, if_exists="append", index=False)
            clean_db(conn)
            print(pd.read_sql('select * from per_round_data;', conn))

    return 'JSON Posted'


if __name__ == "__main__":
    # webbrowser.open_new('http://127.0.0.1:5000') # for deployment
    app.run(debug=True)
