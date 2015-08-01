# -*- coding: utf-8 -*-
import cgi
import os
import random
import re
import json
import string
import pprint
import unicodedata


#TODO: Enforce html entity encoding to mitigate XSS attacks

filesdir = "/var/www/html/docent-learner/tweets/"
docentlearnerdir = "/var/www/docent-learner/dl/"
configfile = "/var/www/html/docent-learner/var/config/config.json"

html_header = """
<html>
<title>Docent Learner</title>
<link rel="stylesheet" type="text/css" href="/docent-learner/static/style.css">
<head>
</head>
<body>
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
  response_headers = [('Content-type', 'text/html; charset=utf-8')]
  start_response(status, response_headers)
  (filename,files_left) = random_file()
  if filename == "":
    return ["<html>All the content has been tagged!</html>"]
  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
  while filename == form_data.getvalue('tagged_file') and files_left > 1:
    (filename,files_left) = random_file()
  data = {}
  for key in form_data: # convert the FieldStorage to dict
      data[key] = form_data.getvalue(key)
  if len(form_data) > 1:
    datafilename = form_data.getvalue('tagged_file') + ".json"
    outfile = open(filesdir + datafilename, "a")
    data['ip'] = environ['REMOTE_ADDR']
    #outfile.write(str(pprint.pformat(data)))
    outfile.write(json.dumps(data))


  config_file = open(configfile, 'r')
  config = json.load(config_file)
  config_file.close()
  form_questions = str(config['tweetquestions'])

  content_file_contents = open(filesdir + filename,'r').read()
  content_dat = json.loads(content_file_contents)

  form = """
    Please help tag this tweet.<br><br>
    <form action="/docent-learner/dl/tweets.py" method="post">
    Your name: <input type='text' name='tagger_name' id='tagger_name' onblur='setname()'><br>
    <br>
    <br>
    <input type="hidden" name="tagged_file" value="%s">
    <input type="hidden" name="tweet_str_id" value="%s">
    <input type="hidden" name="user_agent_id" id="user_agent_id" value="">
    <input type="hidden" name="session_id" id="session_id" value="">
    %s
    <input type="submit" value="Submit">
    </form>
    <br> Random tweet shown is:<br>  %s<br>
  """ % (filename, content_dat['id_str'].encode('utf-8'), form_questions, filename)
#  data = "{"
#  for key in form_data:
#    value = form_data.getvalue(key)
#    data += "\"" + key + "\":\"" + value + "\","
#  data = data[:-1]
#  data += "}\n"

  #content = '<pre>' + str(pprint.pformat(content_dat)) + '</pre>'
  tweet = content_dat['text'].encode('utf-8')
  created_at = content_dat['created_at'].encode('utf-8')
  link = "<a href=\"https://twitter.com/" + content_dat['user']['screen_name'].encode('utf-8') + "/status/" + content_dat['id_str'].encode('utf-8') + "\">view on Twitter</a>"
  #content = unicodedata.normalize('NFKD', title).encode('ascii','ignore')

  content_display = "<br><center><table class='imagetable' cellpadding='60'><tr><td>" + tweet + "<br><br>Created at: " + created_at + "<br>" + link + "</td></tr></table><br><br></center>"

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

  html += "<script src='/docent-learner/static/metrics.js'></script></body></html>"

  return [html]
