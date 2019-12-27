from flask import Flask
from flask import render_template
import csv


app = Flask(__name__)

@app.route('/')
def root():
    data = []

    with open('London.csv', 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        for entry in reader:
            data.append(dict(entry))

    return render_template('home.html', data=data)


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
