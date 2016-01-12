import os
import subprocess
import tempfile
import logging
import urllib
from flask import Flask, request, redirect, url_for, abort, send_file
from werkzeug import secure_filename

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = set(['pdf'])

app = Flask(__name__)
app.config.from_pyfile('config.py')

logging.getLogger().setLevel(logging.INFO)

@app.route('/')
def hello_world():
    return 'Hello World!'

def run_pdftohtmlex(url, first_page="1", last_page = None):
    # Cache to temp file:
    in_f  = tempfile.NamedTemporaryFile(suffix=".pdf", delete=False)
    urllib.urlretrieve(url, in_f.name)
    # TODO Check file exists etc.
    out_f  = tempfile.NamedTemporaryFile(suffix=".html", delete=False)
    out_d, out_name = os.path.split(out_f.name)
    # run process
    if last_page:
        cmd = ['pdf2htmlEX', '--first-page', first_page,'--last-page', last_page, '--dest-dir', "%s/" % out_d, in_f.name, out_name]
    else:
        cmd = ['pdf2htmlEX', '--dest-dir', "%s/" % out_d, in_f.name, out_name]
    logging.debug("Running: %s" % cmd )
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    if( out ):
      logging.debug("pdf2htmlEX STDOUT %s" % out)
    if( err ):
      logging.debug("pdf2htmlEX STDERR: %s" % err)
    # return the file
    return out_f.name


@app.route('/convert')
def convert():
    url = request.args.get('url')
    if not url:
        return abort(400)
    first_page = request.args.get('first_page')
    last_page = request.args.get('last_page')
    # Process it:
    logging.debug('URL is: %s' % url)
    if last_page:
        if not first_page:
            first_page = "1"
        result = run_pdftohtmlex(url, first_page, last_page)
    else:
        result = run_pdftohtmlex(url)
    return send_file(result,attachment_filename="testing.html",
                     as_attachment=False)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')

