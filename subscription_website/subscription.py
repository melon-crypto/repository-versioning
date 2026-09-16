import sqlite3
from flask import Flask, render_template, request, redirect, url_for, session
app = Flask(__name__)
app.secret_key = 'tungtungtungsahur'
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
            session['user_id'] = user['id']
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


@app.route('/signup', methods=['get', 'post'])
def signup_page():
    if request.method == 'POST':
        new_user = request.form['username']
        new_pass = request.form['password']
        conn = sqlite3.connect('database_subscription_website.db')
        conn.execute(
            'insert into users (username, password) values (?, ?)',
            (new_user, new_pass)
        )
        conn.commit()
        conn.close()
        return render_template('login page.html')
        
    return render_template('sign up page.html')


@app.route('/subscriptions')
def subscriptions_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    conn = sqlite3.connect('database_subscription_website.db')
    conn.row_factory = sqlite3.Row
    
    user_subs = conn.execute(
       'select * from subscriptions where user_id = ?',
       (session['user_id'],)
   ).fetchall()
    
    all_db_ids = conn.execute('SELECT user_id FROM subscriptions').fetchall()
    raw_ids = [row['user_id'] for row in all_db_ids]

    conn.close()   
    return render_template('subscriptions.html', subscriptions=user_subs)


@app.route('/new-subscription', methods=['GET', 'POST'])
def new_subscription_page():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        sub_name = request.form['subname']
        
        
        sub_cost = request.form.get('subcost', 0.0) 
        sub_expiry = request.form['subexpiry']
        current_user = session['user_id']
        
        conn = sqlite3.connect('database_subscription_website.db')
        
        
        conn.execute(
            'INSERT INTO subscriptions (subscription_name, cost, expiry_date, user_id) VALUES (?, ?, ?, ?)',
            (sub_name, sub_cost, sub_expiry, current_user)
        )
        conn.commit()
        conn.close()
        
       
        return redirect(url_for('subscriptions_page'))

    return render_template('new subscription.html')
if __name__ == '__main__':
    app.run(debug=True)
