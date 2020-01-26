from flask import Flask
from flask import render_template_string

app = Flask(__name__)

@app.route('/')
def root():
    template = '''
    <h1>Flask app</h1>
    
    {% if var == True %}
      {{val}}
    {% else %}
      Bad condition
    {% endif %}
    
    <script type="text/javascript">
    
    {% if var == True %}
       alert('{{val}}');
    {% else %}
       alert('Bad condition');
    {% endif %}
    
    </script>
    '''
    
    var = True
    val = 10
    
    return render_template_string(template, var=var, val=val)


if __name__ == '__main__':
    app.run(debug=True)
