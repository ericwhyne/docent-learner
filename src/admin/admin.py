import cgi
import re
import json

configfile = "/var/www/html/docent-learner/var/config/config.json"

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
    message += str(config) + "<br>"
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
      message += "Writing config file.<br>"
    except:
      message += "Unable to write config file.<br>"
  imagequestions = ""
  try: 
    imagequestions = str(config['imagequestions'])
  except:
    message += "Configuration was incomplete.<br>"

  message += str(config)

  html = "<html><h2>Docent Learner Administration</h2>"
  form = "<form action=\"/docent-learner/dl/admin/admin.py\" method=\"post\">"
  form += "<input type=\"hidden\" name=\"test\" value=\"bleh\">"
  
  form += """
    <br><br>
    Configure the <a href='/docent-learner/dl/images.py'>image tagger</a><br>
    <br>
    Image Questions<br>
    <textarea rows='20' cols='100' name='imagequestions'>%s</textarea>

    """ % (imagequestions)

  form += """
    <br><br>
    Image Mode: <br>
    <input type="radio" name="imagemode" value="single" checked> Capture only one observation per image <br>
    <input type="radio" name="imagemode" value="multiple"> Capture multiple observations silently <br>
    <input type="radio" name="imagemode" value="gamify"> Capture multiple observations and gamify <br>
    """

  form += "<br><br><input type=\"submit\" value=\"Save\"><br>"
  form += "</form>"
  html += form
  html += "<br><br>"
  html += "</html>" 
  start_response(status, response_headers)

  return [html]
