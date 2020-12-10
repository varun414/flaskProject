from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
import string, random, requests
from azure.storage.blob import BlockBlobService

app = Flask(__name__, instance_relative_config=True)
'''
app.config.from_pyfile('config.py')
account = app.config['ACCOUNT']   # Azure account name
key = app.config['STORAGE_KEY']      # Azure Storage account access key
container = app.config['CONTAINER'] # Container name
'''
account = 'fileuploadstoragebob'   # Azure account name
key = 'v4VDvHoBqcCjcuGru+gX/r7+v10i7kP7YpjIZup8TW8wG+fD0FdFgN3RFGj8dZkkp/FmZ4S7PFkCkg7Sjb2Mvw=='     # Azure Storage account access key
container = 'helloupload1' # Container name

blob_service = BlockBlobService(account_name=account, account_key=key)
'''
@app.route('/')
def hello_world():
    return 'Hello World!'
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        fileextension = filename.rsplit('.',1)[1]
        Randomfilename = id_generator()
        filename = Randomfilename + '.' + fileextension
        try:
            blob_service.create_blob_from_stream(container, filename, file)
        except Exception:
            print ('Exception=' + Exception)
            pass
        ref =  'http://'+ account + '.blob.core.windows.net/' + container + '/' + filename
        return '''
	    <!doctype html>
	    <title>File Link</title>
	    <h1>Uploaded File Link</h1>
	    <p>''' + ref + '''</p>
	    <img src="'''+ ref +'''">
	    '''
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form action="" method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''

def id_generator(size=32, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

if __name__ == '__main__':
    app.run()
