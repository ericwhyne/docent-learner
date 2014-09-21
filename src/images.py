import cgi
import os
import random
import re

imagesdir = "/var/www/html/images/"
docentlearnerdir = "/var/www/docent-learner/"

html_header = """
<html>
<title>Doccent Learner</title>
<link rel="stylesheet" type="text/css" href="/static/style.css">

"""


def random_image_file():
  files = [f for f in os.listdir(imagesdir) if re.match(r'.*\.(jpg|jpeg|png|gif)$', f,  re.IGNORECASE)]
  jsonfiles = [f for f in os.listdir(imagesdir) if re.match(r'.*\.json$', f,  re.IGNORECASE)]
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
  (imagefilename,files_left) = random_image_file()
  if imagefilename == "":
    return ["<html>All the images have been tagged!</html>"]
  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
  while imagefilename == form_data.getvalue('tagged_image') and files_left > 1:
    (imagefilename,files_left) = random_image_file()

  form_file = open('/var/www/html/var/config/image_questions.form', 'r')
  form_questions = form_file.read()
  form = """
    Please help tag this image.<br>
    <form action="/docent-learner/images.py" method="post">
    <input type="hidden" name="tagged_image" value="%s">
    %s
    <input type="submit" value="Submit">
    </form>
    <br> Random image file shown is:<br>  %s<br>
  """ % (imagefilename, form_questions, imagefilename)
  data = "{ "
  for key in form_data:
    value = form_data.getvalue(key)
    data += "\"" + key + "\":\"" + value + "\","
  data = data[:-1]
  data += "}\n"
  imagedisplay = "<br><center><image src='/images/" + imagefilename + "' height=400><br><br></center>"
  html = ""
  if (files_left == 1 and len(form_data) > 1) or imagefilename == "" :
    html = html_header + "All the Images have been tagged!</html>"
  else:
    html = html_header + "<table><tr><td>" + form + "</td><td>" + imagedisplay + "</td></tr></table</html>"

  if len(form_data) > 1:
    datafilename = form_data.getvalue('tagged_image') + ".json"
    outfile = open(imagesdir + datafilename, "a")
    outfile.write(data)

  return [html]
