import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
current_logged_in_user = None
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        typed_user = request.form['username']
        typed_pass = request.form['password']
        conn = sqlite3.connect('database_subscription_website.db')
        conn.row_factory = sqlite3.Row
        user = conn.execute(
            'select * from users where username = ? AND password = ?', 
            (typed_user, typed_pass)
        ).fetchone()
        
        if user:
            conn.close()
            return render_template('loginresult.html', username=user['username'])
        else:
            db_count = conn.execute('SELECT COUNT(*) FROM users').fetchone()[0]
            conn.close()
            return f"failed, checked for user: '{typed_user}' password: '{typed_pass}' there are {db_count} users in database"
    return render_template('login page.html')

@app.route('/start')
def start_page():
    return render_template('start page.html')


@app.route('/signup')
def signup_page():
    return render_template('sign up page.html')


@app.route('/subscriptions')
def subscriptions_page():
    return render_template('subscriptions.html')


@app.route('/new-subscription')
def new_subscription_page():
    return render_template('new subscription.html')

if __name__ == '__main__':
    app.run(debug=True)
