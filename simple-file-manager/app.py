#
# Simple file manager with Python & Flask
#

# import packages
from flask import Flask
from flask import render_template_string
from flask import redirect
from flask import request
import os
import subprocess
import shutil

# create web app instance
app = Flask(__name__)

# handle root route
@app.route('/')
def root():
    return render_template_string('''
        <html>
          <head>
            <title>File manager</title>
          </head>
          <body>
            <div align="center">
              <h1>Local file system</h1>
              <p><strong>CWD: </strong>{{ current_working_directory }}</p>
            </div>
            
            
            <ul>
              <form action="/md">
                <input type="submit" value="New folder"/>
                <input name="folder" type="text" value="new_folder"/>
              </form>
              <li><a href="/cd?path=..">..</a></li>
              {% for item in file_list[0: -1] %}
                {% if '.' not in item%}
                  <li><strong><a href="/cd?path={{current_working_directory + '/' + item}}">{{item}}</a></strong><a href="/rm?dir={{item}}"> X</a></li>
                {% elif '.txt' in item or '.py' in item or '.json' in item %}
                  <li><strong><a href="/view?file={{current_working_directory + '/' + item}}">{{item}}</a></strong></li>
                {% else %}
                  <li>{{item}}</li>
                {% endif%}
              {% endfor %}
            </ul>
          </body>
        </html>
    ''', current_working_directory=os.getcwd(),
         file_list=subprocess.check_output('ls', shell=True).decode('utf-8').split('\n')) # use 'dir' command on Windows
    
# handle 'cd' command
@app.route('/cd')
def cd():
    # run 'level up' command
    os.chdir(request.args.get('path'))
    
    # redirect to file manager
    return redirect('/')

# handle 'make directory' command
@app.route('/md')
def md():
    # create new folder
    os.mkdir(request.args.get('folder'))
    
    # redirect to fole manager
    return redirect('/')

# handle 'make directory' command
@app.route('/rm')
def rm():
    # remove certain directory
    shutil.rmtree(os.getcwd() + '/' + request.args.get('dir'))
    
    # redirect to fole manager
    return redirect('/')
    
# view text files
@app.route('/view')
def view():
    # get the file content
    with open(request.args.get('file')) as f:
        return f.read().replace('\n', '<br>')

# run the HTTP server
if __name__ == '__main__':
    app.run(debug=True, threaded=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
