#####################################
#
#    Web site brainfuck encrypion
#
#                 by
#
#          Code Monkey King
#
#####################################

# packages
from flask import *
import csv

# create app instance
app = Flask(__name__)

# create a route
@app.route('/')
def root():
    with open('lulu.csv') as f:
        # import data from CSV file
        data = [dict(item) for item in csv.DictReader(f)]
        
        # dynamic HTML content
        html = render_template_string('''
          <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.0/css/bootstrap.min.css">
          <div class="container mt-4">
            {% for item in data %}
              <div class="card mt-4">
                <div class="card-body">
                  <div class="row">
                    <div class="col-10">
                      <h3>{{item.title}}<h3>
                      <p><strong>{{item.price}}</strong><p>
                      <span>{{item.Content}}</span>
                      <span>{{item.Type}}</span>
                      <span>{{item.Brand}}</span>
                    </div>
                    <div class="col-2">
                      <img src="{{item.thumbnail_url}}">
                    </div>
                  </div>
                </div>
              </div>
            {% endfor %}
          </div>
        ''', data=data[0:6])
        
        # brainfuck decoder
        script = '''
          <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
          <script src="/static/jquery-3.4.0.js"></script>
        '''
    
        # encrypt content as brainfuck code
        html = ''.join(['+' * ascii + '.>' for ascii in [ord(char) for char in html]])
    
        # append content div
        html = '<div class="content">' + html + '</div>' + script
        
        return html

# main driver
if __name__ == '__main__':
    # start development server
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
