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
<body>
"""

questions = [
[""" \
Please select response that best completes the following sentence:<br> \
<br> \
Even after the success of baby carriages in England,<br> \
<br> \
<input type='hidden' name='question' value='Charles Burton of New York City'> \
<input type='radio' name='answer' value='54'>Charles Burton was a poor man.<br> \
<input type='radio' name='answer' value='75'>Americans were still reluctant to buy baby carriages.<br> \
<input type='radio' name='answer' value='89'>Americans purchased thousands of baby carriages.<br> \
<input type='radio' name='answer' value='41'>the United States bought more carriages than any other country.<br> \
""",
"""
In 1848, Charles Burton of New York City made the first baby carriage, but people strongly objected to the vehicles because they said the carriage operators hit too many pedestrians.  Still convinced that he had a good idea, Burton opened a factory in England.  He obtained orders for the baby carriages from Queen Isabella II of Spain, Queen Victoria of England, and the Pasha of Egypt.  The United States had to wait <b>another ten years before it got a carriage factory</b>, and the first year only 75 carriages were sold.
"""],
["""
<input type='hidden' name='question' value='Charles Burton of New York City'>
<input type='radio' name='answer' value='54'>Charles Burton was a poor man.<br>
<input type='radio' name='answer' value='75'>Americans were still reluctant to buy baby carriages.<br>
<input type='radio' name='answer' value='89'>Americans purchased thousands of baby carriages.<br>
<input type='radio' name='answer' value='41'>the United States bought more carriages than any other country.<br>
""",
"""
In 1848, Charles Burton of New York City made the first baby carriage, but people strongly objected to the vehicles because they said the carriage operators hit too many pedestrians.  Still convinced that he had a good idea, Burton opened a factory in England.  He obtained orders for the baby carriages from Queen Isabella II of Spain, Queen Victoria of England, and the Pasha of Egypt.  The United States had to wait <b>another ten years before it got a carriage factory</b>, and the first year only 75 carriages were sold.
"""]
]

def application(environ, start_response):
  status = '200 OK'
  response_headers = [('Content-type', 'text/html')]
  start_response(status, response_headers)
  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
  html = ""
  docentlearner = "<table cellpadding='10'><tr><td><h5><a href='https://github.com/ericwhyne/docent-learner'>Docent-learner</a></h5></td></tr></table>"
  data = {}
  for key in form_data: # convert the FieldStorage to dict
      data[key] = form_data.getvalue(key)
  if len(form_data) > 1:
      turk_random_key = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length_of_key))
      datafilename = turk_random_key + ".json"
      outfile = open(filesdir + datafilename, "a")
      data['ip'] = environ['REMOTE_ADDR']
      data['turk_random_key'] = turk_random_key
      #outfile.write(str(pprint.pformat(data)))
      outfile.write(json.dumps(data))

      html = html_header + "<table class='rounded'><tr><td width=\"400\">Thanks!<br><br>Here's your code for Mechanical Turk:<br> <h1>" + turk_random_key + "</h1></td></tr></table>" + docentlearner

  else:

      random_question = questions[0][0]
      content =  questions[0][1]

      form = """
      <script>
      questionHtml = "<form action=''/docent-learner/dl/boldtext.py' method='post'> \
      <input type='hidden' name='user_agent_id' id='user_agent_id' value=''> \
      <input type='hidden' name='session_id' id='session_id' value=''> \
      %s \
      <br><input type='submit' value='Submit'> \
      </form> \
      "
      </script>
      """ % (random_question)

      content_display = """
      <br><center><table class='imagetable' cellpadding='60'><tr><td id='question_area'>
      """ + content + """
      </td></tr></table><br><br></center>"""

      html = html_header + "<table class='rounded'><tr><td>" + content_display + "</td></tr><tr><td id='button_area'><button type='button' onclick='text_is_read()'>Click here after you've read the text</button></td></tr></table>"

      html += docentlearner

      html += form + "<script src='/docent-learner/static/boldtext.js'></script></body></html>"

  return [html]
