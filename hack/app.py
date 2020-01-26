from flask import Flask
from flask import render_template
from flask import render_template_string
from flask import request
import urllib


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(error):
    template = '''
    <h1>Oops! This page doesn't exist!</h1>
    <h3>%s</h3>
    ''' % (urllib.parse.unquote(request.url))
    
    return render_template_string(template)

if __name__ == '__main__':
    app.run(debug=True)
