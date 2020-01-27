from flask import Flask
from flask import session
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

app = Flask(__name__)

# config mysql
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'your_password'
app.config['MYSQL_DB'] = 'users'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.secret_key = '12345'

mysql = MySQL()
mysql.init_app(app)

@app.route('/')
def root():
    try:
        user = session['user']
        status = session['logged_in']
    except:
        user = 'guest'
        status = 'logged out'
    
    return '<strong>User: </strong><span>%s</span><br><strong>Status: </strong><span>%s</span>' % (user, status)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get form fields
        username = request.form['username']
        password_candidate = request.form['password']
        
        # create cursor
        cur = mysql.connection.cursor()
        
        # NEVER DO LIKE THIS
        #result = cur.execute("SELECT * FROM users WHERE user = '%s'" % username)
        
        # DO LIKE THIS INSTEAD
        result = cur.execute("SELECT * FROM users WHERE user = %s", [username])

        if result > 0:
            # get stored hash
            data = cur.fetchone()
            password = data['password']
            
            # compare password
            if sha256_crypt.verify(password_candidate, password):
                session['logged_in'] = True
                session['user'] = username

                return redirect(url_for('root'))
            else:
                error = "Invalid password!"
                return error
            
            # close connection
            cur.close()
        
        else:
            error = "Username not found!"
            return error
    
    return render_template('login.html')
    
# logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('root'))


if __name__ == '__main__':
    app.run(debug=True)
