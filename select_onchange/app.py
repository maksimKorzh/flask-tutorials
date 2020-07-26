#########################################
#
#     Submit form on select option
#             change event
#
#                  by
#
#           Code Monkey King
#
#########################################

# packages
from flask import *

# create app instance
app = Flask(__name__)

# create UI route
@app.route('/')
def root():
    return render_template_string('''
      <h1 align="center">App to download files via clicking on items within option box</h1>
        <form method="POST" action="/download" align="center"> 
          <select name="select_file" onchange="this.form.submit()">
            <option>File1.csv</option>
            <option>File2.csv</option>
            <option>File3.csv</option>
          </select>
        </form>
    ''')

# create file download route
@app.route('/download', methods=['GET', 'POST'])
def download():
    return send_file(request.form.get('select_file'), as_attachment=True)

# main driver
if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
