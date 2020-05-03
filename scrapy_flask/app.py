#
# Flask web app to run scrapy spider from web interface
#

# packages
from flask import Flask
from flask import render_template
from flask import request
import json
import subprocess

# create app instance
app = Flask(__name__)

# base route
@app.route('/')
def home():
    return render_template('scraper.html')
    
# run scraper route
@app.route('/run', methods=['POST'])
def run():
    # extract user input parameters
    category = request.form.get('category')
    
    # settings content
    settings = ''
    
    # open settings file
    with open('settings.json', 'r') as f:
        for line in f.read():
            settings += line
    
    # parse settings
    settings = json.loads(settings)
    
    # update settings
    settings['category'] = category
    
    # write scraper settings
    with open('settings.json', 'w') as f:
        f.write(json.dumps(settings, indent=4))
    
    # run scraper
    process = subprocess.Popen('python3 scraper.py', shell=True)
    process.wait()
    
    # output content
    output = ''
    
    # load scraper output
    with open('wellness.jsonl', 'r') as f:
        for line in f.read():
            output += line
    
    # parse content
    output = [json.loads(item + '\n}') for item in output.split('}\n')[0:-1]]
    
    return {'data': output}

# main driver
if __name__ == '__main__':
    # run app
    app.run(debug=True, threaded=True)
