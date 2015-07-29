import cgi
import re
import os
import json

configfile = "/var/www/html/docent-learner/var/config/config.json"
textselectdir = "/var/www/html/docent-learner/textselect/"

def application(environ, start_response):
  status = '200 OK'
  response_headers = [('Content-type', 'text/html; charset=utf-8')]
  message = ""
  config = {}
  try:
    config_file = open(configfile, 'r')
    config_records = json.load(config_file)
    config_file.close()
    config = config_records
    #message += str(config) + "<br>"
  except Exception, error:
    message += "Config file error: " + str(error) + "<br>"

  form_data = cgi.FieldStorage(environ=environ, fp=environ['wsgi.input'])
  for key in form_data:
    value = form_data.getvalue(key)
    config[key] = value

  if(len(form_data) > 1):
    try:
      config_file = open(configfile, 'w')
      #config_file.write(unicode(json.dumps(config,ensure_ascii=False)))
      json.dump(config, config_file)
      config_file.close()
      message += "Configuration updated.<br>"
    except IOError as e:
      message += "Unable to write config file.<br> %s" % str(e)

  textselect_jsonfiles = [f for f in os.listdir(textselectdir) if re.match(r'.*\.json$', f,  re.IGNORECASE)]
  textselect_num_tagged = len(textselect_jsonfiles)
  imagequestions = ""
  tweetquestions = ""
  textinstructions = ""
  try:
    imagequestions = str(config['imagequestions'])
    tweetquestions = str(config['tweetquestions'])
    textinstructions = str(config['textinstructions'])
  except:
    message += "Configuration was incomplete.<br>"

  #message += str(config)

  html = "<html><title>Docent Learner Administration</title><h1>Docent Learner Administration</h1>"
  html += "<form action=\"/docent-learner/dl/admin/admin.py\" method=\"post\">"
  html += "<input type=\"hidden\" name=\"test\" value=\"bleh\">"
  html += """<hr><h2>Configure text select</h2>
    <a href='/docent-learner/dl/textselect.py'>Go to text select.</a><br>
    <br>
    <textarea rows='3' cols='100' name='textinstructions'>%s</textarea>
    <br><br>
    There are currently %s tagged examples.
    <br><br>
    <a href="/docent-learner/dl/admin/buildtextselectmodel.py">Build textselect model</a>
    """ % (textinstructions, str(textselect_num_tagged))

  html += """
    <br><br>
    <hr><h2>Configure the image tagger</h2>
    <a href='/docent-learner/dl/images.py'>Go to image tagger.</a><br>
    <br>
    Image Questions (in html form code)<br>
    <textarea rows='20' cols='100' name='imagequestions'>%s</textarea>

    """ % (imagequestions)

  html += """
    <br><br>
    Image Mode: <br>
    <input type="radio" name="imagemode" value="single" checked> Capture only one observation per image <br>
    <input type="radio" name="imagemode" value="multiple" disabled> Capture multiple observations silently <br>
    <input type="radio" name="imagemode" value="gamify" disabled> Capture multiple observations and gamify <br>
    """


  html += """
    <br><br>
    <hr><h2>Configure the tweet tagger</h2>
    <a href='/docent-learner/dl/tweets.py'>Go to tweet tagger.</a><br>
    <br>
    Tweet Questions (in html form code)<br>
    <textarea rows='20' cols='100' name='tweetquestions'>%s</textarea>

    """ % (tweetquestions)

  html += """
    <br><br>
    Tweet Mode: <br>
    <input type="radio" name="tweetmode" value="single" checked> Capture only one observation per image <br>
    <input type="radio" name="tweetmode" value="multiple" disabled> Capture multiple observations silently <br>
    <input type="radio" name="tweetmode" value="gamify" disabled> Capture multiple observations and gamify <br>
    """

  html += "<br><br><hr><input type=\"submit\" value=\"Save config\" style=\"width:200px; height:75px;\"><br>"
  html += "</form>"
  html += "<br><br>"
  html += message
  html += "</html>"
  start_response(status, response_headers)

  return [html]
