from flask import Flask
from flask import render_template
from flask import request
from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

app = Flask(__name__)

@app.route('/')
def root():
    source = request.args.get('source')
    
    with Capturing() as output:
        try:
            exec(source, globals())
        except Exception as e:
            return render_template('code.html', output=e)
    
    return render_template('code.html', output='\n'.join(output))


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
