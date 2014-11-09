import cgi
import re
import json
import threading
import subprocess

configfile = "/var/www/html/docent-learner/var/config/config.json"
lockfile = "/var/www/html/docent-learner/var/textselect-modelbuild.lock"

def read_lock():
  try:
    lock_file = open(lockfile,'r')
    lock = lock_file.read();
    lock_file.close()
  except Exception, error:
    print "Lock file error: " + str(error)
  return str(lock)

def write_lock(val):
  try:
    lock_file = open(lockfile,'w')
    lock_file.write(val);
    lock_file.close()
  except Exception, error:
    return "Lock file error: " + str(error)
  return "Starting build"

def build_process():
  predict_command = "/var/www/docent-learner/admin/textselect-build-model-script.sh"
  out = subprocess.check_output(predict_command.split(' '))

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

  # Read lock file
  lock = read_lock()

  if re.match('^1.*', lock): # If file is locked, show status
    message += "Build is in progress"
    # Javascript read lock file, if closed show animated icon, otherwise show animated icon
    # Javascript read status and print in window

  elif re.match('^0.*', lock): # if file is unlocked, spawn build and reload page
    message += write_lock('1')
    p = threading.Thread(target=build_process)
    p.start()

  html = "<html><title>Docent Learner Administration</title><h1>Docent Learner building text select model</h1>"

  html += "<pre id='status'></pre>"

#TODO: This is terribly broken and I'm tired so it's just getting worse. I quit for the night.
  html += """
  <script>

  var req = new XMLHttpRequest();
  req.onreadystatechange = displayupdate();
  req.open('GET', '/docent-learner/var/textselect-model-build-status.txt');
  req.send();

  document.getElementById('status').textContent = req.responseText;

  </script>
  """

  html += "<br>Lock file contents:" + str(lock)
  html += message
  html += "</html>"
  start_response(status, response_headers)

  return [html]
