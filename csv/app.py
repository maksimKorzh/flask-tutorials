from flask import Flask
from flask import render_template
from flask import request
import csv


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def root(): 
    if request.method == 'GET':
        return render_template('home.html')
    elif request.method == 'POST':
        results = []
        
        user_csv = request.form.get('user_csv').split('\n')
        reader = csv.DictReader(user_csv)
        
        for row in reader:
            results.append(dict(row))

        fieldnames = [key for key in results[0].keys()]

        return render_template('home.html', results=results, fieldnames=fieldnames, len=len)


if __name__ == '__main__':
    app.run(debug=True)
