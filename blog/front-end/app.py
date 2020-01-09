from flask import Flask
from flask import request
from flask import render_template
from flask import redirect
import sqlite3


app = Flask(__name__)

@app.route('/')
def root():
    # Connect to db
    db = sqlite3.connect('posts.db')  
    cursor = db.cursor()
    
    # Get data from db
    cursor.execute('SELECT * FROM posts ORDER BY id DESC')
    posts = cursor.fetchall()
    
    # Close db connection
    db.close()
    
    return render_template('posts.html', posts=posts)

@app.route('/post/<_id>')
def post(_id):
    # Connect to db
    db = sqlite3.connect('posts.db')  
    cursor = db.cursor()
    
    # Get data from db
    cursor.execute('SELECT * FROM posts WHERE id=%s' % _id)
    post = cursor.fetchone()
    
    # Close db connection
    db.close()
    return render_template('post.html', post=post)

@app.route('/create')
def create():
    return render_template('create.html')

@app.route('/edit')
def edit():
    # Get request args
    title = request.args.get('title')
    post = request.args.get('post')
    _id = request.args.get('_id')

    return render_template('edit.html', title=title, post=post, _id=_id)


@app.route('/insert')
def insert():
    # Connect to db
    db = sqlite3.connect('posts.db')  
    cursor = db.cursor()
    
    # Get request args
    title = request.args.get('title')
    post = request.args.get('post')
    
    # Insert data into db
    cursor.execute('INSERT INTO posts(title, post) VALUES("%s", "%s")' % (title, post.replace('"', "'")))
    db.commit()
    
    # Close db connection
    db.close()
    return redirect('/')

@app.route('/update/<_id>')
def update(_id):
    # Connect to db
    db = sqlite3.connect('posts.db')  
    cursor = db.cursor()
    
    # Get request args
    title = request.args.get('title')
    post = request.args.get('post')
    
    # Update data in db
    cursor.execute('UPDATE posts SET title="%s", post="%s" WHERE id=%s' % (title, post.replace('"', "'"), _id))
    db.commit()
    
    # Close db connection
    db.close()
    return redirect('/')

@app.route('/delete/<_id>')
def delete(_id):
    # Connect to db
    db = sqlite3.connect('posts.db')  
    cursor = db.cursor()
    
    # Update data in db
    cursor.execute('DELETE FROM posts WHERE id=%s' % _id)
    db.commit()
    
    # Close db connection
    db.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
