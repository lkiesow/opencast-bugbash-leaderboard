import json
import sqlite3
import time

from flask import Flask, g, jsonify, request, redirect

__SQL_CREATE = '''
    CREATE TABLE IF NOT EXISTS leaderboard(
        date unsigned int NOT NULL,
        username varchar(255) NOT NULL,
        link varchar(255) NOT NULL,
        type varchar(255) NOT NULL,
        points unsigned int NOT NULL
    )'''
# unixepoch()

con = sqlite3.connect('leaderboard.db')
cur = con.cursor()
cur.execute(__SQL_CREATE)
con.close()

app = Flask(__name__)
app.json.sort_keys = False

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('leaderboard.db')
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def home():
    return redirect('/static/index.html', code=302)


@app.route('/add', methods=['POST'])
def add():
    data = request.json
    date = time.time()
    username = data.get('username')
    link = data.get('link')
    type_ = data.get('type')
    points = data.get('points')
    if not username or not link or not type_ or not points:
        return 'Required data is missing', 400

    db = get_db()
    data = (date, username, link, type_, points)
    db.cursor().execute('INSERT INTO leaderboard VALUES(?, ?, ?, ?, ?)', data)
    db.commit()
    return jsonify(data)

@app.route('/leaderboard')
def leaderboard():
    cur = get_db().cursor()
    data = cur.execute('''
        select username, sum(points) as sum_points
        from leaderboard
        group by username
        order by sum_points desc;''')
    data = {d[0]: d[1] for d in data}
    print(data)
    return jsonify(data)

@app.route('/data')
def data():
    cur = get_db().cursor()
    data = cur.execute('''
        select date, username, link, type, points
        from leaderboard
        order by date desc;''')
    data = [(d[0], d[1], d[2], d[3], d[4]) for d in data]
    print(data)
    return jsonify(data)


if __name__ == '__main__':
    app.run()
