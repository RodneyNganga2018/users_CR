from flask import Flask, render_template, request, redirect, session
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = 'damascusXIII'

@app.route('/users')
def new():
    mysql = connectToMySQL('users_cr')
    users = mysql.query_db('SELECT id,first_name,last_name,email,DATE_FORMAT(users.created_at, "%M %e, %Y") as created_at FROM users;')
    return render_template('index.html', all_users=users)

@app.route('/users/new')
def index():
    return render_template('new.html')

@app.route('/users/<userID>/edit')
def edit(userID):
    mysql = connectToMySQL('users_cr')
    edit = mysql.query_db('SELECT first_name,last_name,email FROM users;')
    return render_template('edit.html', user=edit, user_id=int(userID))

@app.route('/users/<userID>')
def user(userID):
    users = connectToMySQL('users_cr').query_db('SELECT id,first_name,last_name,email,DATE_FORMAT(users.created_at,"%M %e, %Y") as created_at,DATE_FORMAT(users.updated_at,"%M %e, %Y at %I:%i %p") as updated_at FROM users;')
    return render_template('show.html', all_users=users, user_id=int(userID))

@app.route('/create_user', methods=['POST'])
def new_user():
    mysql = connectToMySQL('users_cr')
    query = 'INSERT INTO users(first_name,last_name,email) VALUES (%(first_name)s,%(last_name)s,%(email)s);'
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    mysql.query_db(query,data)
    users = connectToMySQL('users_cr').query_db('SELECT id,first_name,last_name,email,DATE_FORMAT(users.created_at,"%M %e, %Y") as created_at,DATE_FORMAT(users.updated_at,"%M %e, %Y at %I:%i %p") as updated_at FROM users;')
    for user in users:
        if user['first_name'] == request.form['first_name']:
            session['new_user'] = user['id']

    return redirect('/users/'+str(session['new_user']))

@app.route('/update_user/<userID>', methods=['POST'])
def update_user(userID):
    mysql = connectToMySQL('users_cr')
    query = 'UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s, updated_at=NOW() WHERE id=%(user_id)s;'
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'user_id': userID
    }
    mysql.query_db(query,data)
    return redirect('/users/'+userID)

@app.route('/users/delete_user/<userID>')
def delete_user(userID):
    mysql = connectToMySQL('users_cr')
    query = 'DELETE FROM users WHERE id=%(user_id)s;'
    data = {
        'user_id': userID
    }
    mysql.query_db(query,data)
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)