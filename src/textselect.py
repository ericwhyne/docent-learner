import cgi
import os
import random
import re

#TODO: Enforce html entity encoding to mitigate XSS attacks

textselectdir = "/var/www/html/textselect/"
docentlearnerdir = "/var/www/docent-learner/"

html_header = """
<html>
<title>Doccent Learner</title>
<link rel="stylesheet" type="text/css" href="/static/style.css">
<script>
var t = '';
function gText(e) {
    t = (document.all) ? document.selection.createRange().text : document.getSelection();
    document.getElementById('input').value = t;
    document.getElementById('show_input').innerHTML = t;
}
document.onmouseup = gText;
if (!document.all) document.captureEvents(Event.MOUSEUP);
</script>
"""

def random_text_file():
  files = [f for f in os.listdir(textselectdir) if re.match(r'.*\.(txt|text)$', f,  re.IGNORECASE)]
  jsonfiles = [f for f in os.listdir(textselectdir) if re.match(r'.*\.json$', f,  re.IGNORECASE)]
  jsonfiles = [jf.replace('.json', '') for jf in jsonfiles]
  unprocessed_files = list(set(files) - set(jsonfiles))
  if len(unprocessed_files) == 0:
    return ("", len(unprocessed_files))
  filename = random.choice(unprocessed_files)
  return (filename, len(unprocessed_files))

def application(environ, start_response):
  status = '200 OK'
  response_headers = [('Content-type', 'text/html')]
  start_response(status, response_headers)
  (currentfilename,files_left) = random_text_file()
  if currentfilename == "":
    return ["<html>All the content has been tagged!</html>"]
  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])

  while currentfilename == form_data.getvalue('tagged_text_filename') and files_left > 1:
    (currentfilename,files_left) = random_text_file()

  text_file = open(textselectdir + currentfilename, 'r')
  text_to_tag = text_file.read()
  form = """
    Please highlight the subject of the text.<br>
    <br>
    <form action="/docent-learner/textselect.py" method="post">
    <input type="hidden" name="tagged_text_filename" value="%s">
    <input type="hidden" name="selected_text" id='input'>
    Notes:<textarea name="notes" cols="40" rows="5"></textarea><br>
    <br><br>
    <center><input type="image" src="/static/submit.png" alt="Submit" width="100" height="100"></center>
    </form>
    <br> Random text file shown is:<br>  %s<br>
  """ % (currentfilename, currentfilename)
  data = "{ "
  for key in form_data:
    value = form_data.getvalue(key)
    data += "\"" + key + "\":\"" + value + "\","
  data = data[:-1]
  data += "}\n"
  textdisplay = "<table border=2 cellpadding=40><tr><td>" + text_to_tag + "</td></tr><tr><td><center>Selected text: <div id='show_input'></div></center></td></tr></table>"
  html = ""
  if (files_left == 1 and len(form_data) > 1) or currentfilename == "" :
    html = html_header + "All the text has been tagged!</html>"
  else:
    html = html_header + "<table><tr><td>" + form + "</td><td>" + textdisplay + "</td></tr></table</html>"

  if len(form_data) > 1:
    datafilename = form_data.getvalue('tagged_text_filename') + ".json"
    outfile = open(textselectdir + datafilename, "a")
    outfile.write(data)

  return [html]
