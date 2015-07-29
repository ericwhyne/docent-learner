# -*- coding: utf-8 -*-
import cgi
import os
import random
import re
import json
import string
import pprint

filesdir = "/var/www/html/docent-learner/boldtext/"
docentlearnerdir = "/var/www/docent-learner/dl/"

length_of_key = 6

html_header = """
<html>
<title>Docent Learner</title>
<link rel="stylesheet" type="text/css" href="/docent-learner/static/style.css">
"""

questions = [
["""
<div class=\"squaredOne\"><label><input type=\"checkbox\" name=\"option1\" value=\"true\">This is option one</label></div><br>
<div class=\"squaredOne\"><label><input type=\"checkbox\" name=\"something_else\" value=\"true\">something else</label></div><br>
""",
"""
Paragraph text here with <b>bold text</b>
"""],
["""
<div class=\"squaredOne\"><label><input type=\"checkbox\" name=\"is_suicidal\" value=\"true\">This is option one</label></div><br>
<div class=\"squaredOne\"><label><input type=\"checkbox\" name=\"something_else\" value=\"true\">something else</label></div><br>
""",
"""
Another paragraph text here with <b>bold text</b>
"""]
]

def application(environ, start_response):
  status = '200 OK'
  response_headers = [('Content-type', 'text/html')]
  start_response(status, response_headers)
  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])

  data = "{ "
  for key in form_data:
    value = form_data.getvalue(key)
    data += "\"" + key + "\":\"" + value + "\","
  data = data[:-1]
  data += "}\n"
  html = ""
  if len(form_data) > 1:
      last_random_key = form_data.getvalue('random_key')
      datafilename =  last_random_key + ".json"
      outfile = open(filesdir + datafilename, "a")
      outfile.write(data)
      html = html_header + "<table class='rounded'><tr><td width=\"300\">Thanks!<br><br>Here's your code for Mechanical Turk:<br> <h1>" + last_random_key + "</h1></td></tr></table>"

  else:
      random_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length_of_key))
      random_question = questions[0][0]

      form = """
      Please help tag this tweet.<br><br>
      <form action="/docent-learner/dl/boldtext.py" method="post">
      <input type="hidden" name="random_key" value="%s">
      %s
      <input type="submit" value="Submit">
      </form>
      """ % (random_key, random_question)

      content =  questions[0][1]

      content_display = "<br><center><table class='imagetable' cellpadding='60'><tr><td>" + content + "</td></tr></table><br><br></center>"

      html = html_header + "<table class='rounded'><tr><td width=\"300\">" + form + "</td><td>" + content_display + "</td></tr></table>"

      html += """
            <table cellpadding='10'>
            <tr>
            <td><h5>Docent-learner | <a href='/docent-learner/dl/admin/admin.py'>Admin</a> this instance. | This tool is open source, get help or help make it better on <a href='https://github.com/ericwhyne/docent-learner'>github</a>.</h5></td>
            </tr>
            </table>
            """

  html += "</html>"

  return [html]
