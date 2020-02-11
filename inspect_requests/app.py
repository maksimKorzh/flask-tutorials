from flask import Flask, request, jsonify, render_template_string

app = Flask(__name__)

@app.route('/')
def root():
    template = '''
      <!DOCTYPE html>

      <html>
        <head>
          <title>Inspect HTTP requests</title>
          <!-- JQuery -->
          <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>

          <!-- Bootstrap -->
          <link rel="stylesheet" type="text/css" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">

        </head>
        <body>
          <div class="card">
            <div class="card-body">
              <div class="card">
                <div class="card-body">
                  <!-- Request info -->
                  <table class="table border">
                    <tbody id="request">
                      <tr class="bg-light">
                        <td><strong>REQUESTS</strong></td>
                        <td></td>
                      </tr>
                      <!-- Jquery dynamic HTML rendering -->
                    </tbody>
                  </table>
                  
                  <!-- Headers info -->
                  <table class="table border mt-4">
                    <tbody id="headers">
                      <tr class="bg-light">
                        <td><strong>HEADERS</strong></td>
                        <td></td>
                      </tr>
                      <!-- Jquery dynamic HTML rendering -->
                    </tbody>
                  </table>
                </div>
              </div>  
            </div>
          </div>
        </body>
        
        <script type="text/javascript">
          $.get('/api', (data) => {
            // append rows to request table
            $.each(data, (key, val) => {
              if (key != 'headers') {
                if (key == 'url')
                  row = '<tr><td><strong>' + key + ':</strong></td><td><a href="' + val + '">' + val + '</a></td></tr>'
                else
                  row = '<tr><td><strong>' + key + ':</strong></td><td>' + val + '</td></tr>'
                $('#request').append(row);
              }
            });
            
            // append rows to headers table
            $.each(data.headers, (key, val) => {
              row = '<tr><td><strong>' + key + ':</strong></td><td>' + val + '</td></tr>'
              $('#headers').append(row);
            });
          });
        </script>
      </html>
    '''

    return render_template_string(template)

@app.route('/api')
def api():
    if request.headers.getlist('X-Forwarded-For'):
        ip = request.headers.getlist('X-Forwarded-For')[0]
    else:
        ip = request.remote_addr

    data = {
        'ip': ip,
        'method': request.method,
        'url': request.url,
        'headers': dict(request.headers)
    }
    
    return jsonify(data) 


if __name__ == '__main__':
    app.run(debug=True, threaded=True)
