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
  form = "<form action=\"/docent-learner/dl/admin.py\" method=\"post\">"
  form += "<input type=\"hidden\" name=\"test\" value=\"bleh\">"
  form += "<textarea name='imagequestions'>" + imagequestions + "</textarea>"
  form += "<input type=\"submit\" value=\"Save\"><br>"
  form += "</form>"
  html += form
  html += "<br><br>" + message
  html += "</html>" 
  start_response(status, response_headers)

  return [html]
