#!/usr/bin/python
import cgi
import subprocess
#import shlex
import os

textselectdir = "/var/www/html/docent-learner/textselect/"
docentlearnerdir = "/var/www/docent-learner/dl/"

def application(environ, start_response):
  status = '200 OK'
  response_headers = [('Content-type', 'text/html')]
  start_response(status, response_headers)
  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
  data = {}
  for key in form_data:
    value = form_data.getvalue(key)
    data[key] = value

  html = data['text']
  
  # http://127.0.0.1:8080/docent-learner/dl/textselect-tag.py?text=hello
  my_cmd = 'echo earth'
  p = subprocess.Popen(my_cmd, shell=True, stdout=subprocess.PIPE)
  out = p.stdout.read()

  html += str(out)

  return [html]
