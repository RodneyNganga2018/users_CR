from flask import Flask, render_template, request, redirect
from mysqlconnection import connectToMySQL
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('new.html')

@app.route('/users')
def new():
    mysql = connectToMySQL('users_cr')
    users = mysql.query_db('SELECT id,first_name,last_name,email,DATE_FORMAT(users.created_at, "%M %e, %Y") as created_at FROM users;')
    print(users)

    return render_template('index.html', all_users=users)

@app.route('/create_user', methods=['POST'])
def new_user():
    print(request.form)
    mysql = connectToMySQL('users_cr')

    query = 'INSERT INTO users(first_name,last_name,email) VALUES (%(first_name)s,%(last_name)s,%(email)s);'
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email']
    }
    mysql.query_db(query,data)
    return redirect('/users')

if __name__ == '__main__':
    app.run(debug=True)