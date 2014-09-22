import cgi
import cgitb; cgitb.enable()
import os
import random
import re
import tempfile

uploadsdir = "/var/www/html/uploads/"
docentlearnerdir = "/var/www/docent-learner/"

def application(environ, start_response):
  status = '200 OK'
  response_headers = [('Content-type', 'text/html')]

  temp_file = tempfile.TemporaryFile()
  temp_file.write(environ['wsgi.input'].read()) # or use buffered read()
  temp_file.seek(0)

  form = cgi.FieldStorage(environ=environ, fp=temp_file)
  data = ""
  for key in form:
    value = form.getvalue(key)
    data += "\"" + key + "\":\"" + value + "\","
  message = data

  try:
        fileitem = form['file']
  except KeyError:
        fileitem = None

  if fileitem and fileitem.file:
        fn = os.path.basename(fileitem.filename)
        with open(fn, 'wb') as f:
            data = fileitem.file.read(1024)
            while data:
                f.write(data)
                data = fileitem.file.read(1024)

            message = 'The file "' + fn + '" was uploaded successfully'

  else :
        message = 'please upload a file.'

  html = """<h2>Docent Learner Administration</h2>
   <form action="/docent-learner/admin.py" method="post">
    <input type="hidden" name="test" value="bleh">
    <input type="file" name="file">
    <input type="submit" value="Submit">
    </form>

  """
  html += message
  start_response(status, response_headers)
  return [html]
