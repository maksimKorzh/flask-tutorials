from flask import Flask
from flask import Response
from flask import request
from flask import jsonify
from flask import render_template
import json


app = Flask(__name__)

@app.route('/')
def root():
    return render_template('stats.html')

@app.route('/api/get')
def get():
    data = '['

    with open('api.json', 'r') as json_file:
        for line in json_file:
            data += line

    return jsonify({'data': json.loads(data[0:-1] + ']')})
    
@app.route('/api/post', methods=['POST'])
def post():
    response = Response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    
    stats = {
        'Agent': request.headers.get('User-Agent'),
        'Date': request.form.get('Date'),
        'Url': request.form.get('Url'),
    }
    
    if request.headers.getlist("X-Forwarded-For"):
       stats['Ip'] = request.headers.getlist("X-Forwarded-For")[0]
    else:
       stats['Ip'] = request.remote_addr
    
    if request.headers.get('Origin'):
        stats['Origin'] = request.headers.get('Origin')
    else:
        stats['Origin'] = 'N/A'

    with open('api.json', 'a') as json_file:
        json_file.write(json.dumps(stats, indent=2) + ',')

    return response
    

if __name__ == '__main__':
    app.run(debug=True, threaded=True)
