# -*- coding: utf-8 -*-
import cgi
import os
import random
import re
import json
import string
import pprint

#TODO: Enforce html entity encoding to mitigate XSS attacks

filesdir = "/var/www/html/docent-learner/tweets/"
docentlearnerdir = "/var/www/docent-learner/dl/"
configfile = "/var/www/html/docent-learner/var/config/config.json"

html_header = """
<html>
<title>Docent Learner</title>
<link rel="stylesheet" type="text/css" href="/docent-learner/static/style.css">

"""

def random_file():
  files = [f for f in os.listdir(filesdir) if re.match(r'.*\.(twt|tweet)$', f,  re.IGNORECASE)]
  jsonfiles = [f for f in os.listdir(filesdir) if re.match(r'.*\.json$', f,  re.IGNORECASE)]
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
  (filename,files_left) = random_file()
  if filename == "":
    return ["<html>All the content has been tagged!</html>"]
  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
  while filename == form_data.getvalue('tagged_file') and files_left > 1:
    (filename,files_left) = random_file()


  config_file = open(configfile, 'r')
  config = json.load(config_file)
  config_file.close()
  form_questions = str(config['tweetquestions'])

  form = """
    Please help tag this tweet.<br><br>
    <form action="/docent-learner/dl/tweets.py" method="post">
    <input type="hidden" name="tagged_file" value="%s">
    %s
    <input type="submit" value="Submit">
    </form>
    <br> Random tweet shown is:<br>  %s<br>
  """ % (filename, form_questions, filename)
  data = "{ "
  for key in form_data:
    value = form_data.getvalue(key)
    data += "\"" + key + "\":\"" + value + "\","
  data = data[:-1]
  data += "}\n"

  content_file_contents = open(filesdir + filename,'r').read()
  content_dat = json.loads(content_file_contents)
  content = '<pre>' + str(pprint.pformat(content_dat)) + '</pre>'

  content_display = "<br><center><table class='imagetable' cellpadding='60'><tr><td>" + content + "</td></tr></table><br><br></center>"

  html = ""
  if (files_left == 1 and len(form_data) > 1) or filename == "" :
    html = html_header + "All the content has been tagged!</html>"
  else:
    html = html_header + "<table class='rounded'><tr><td width=\"300\">" + form + "</td><td>" + content_display + "</td></tr></table>"

  html += """
    <table cellpadding='10'>
      <tr>
        <td><h5>Docent-learner | <a href='/docent-learner/dl/admin/admin.py'>Admin</a> this instance. | This tool is open source, get help or help make it better on <a href='https://github.com/ericwhyne/docent-learner'>github</a>.</h5></td>
      </tr>
    </table>
  """


  html += "</html>"

  if len(form_data) > 1:
    datafilename = form_data.getvalue('tagged_file') + ".json"
    outfile = open(filesdir + datafilename, "a")
    outfile.write(data)

  return [html]
