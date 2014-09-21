import cgi
import os
import random
import re

imagesdir = "/var/www/html/images/"
docentlearnerdir = "/var/www/docent-learner/"

def application(environ, start_response):
  status = '200 OK'
  response_headers = [('Content-type', 'text/html')]

  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
  for key in form_data:
    value = form_data.getvalue(key)
    data += "\"" + key + "\":\"" + value + "\","

  html = "<h2>Docent Learner Content Administration</h2>"


  start_response(status, response_headers)
  return [html]
