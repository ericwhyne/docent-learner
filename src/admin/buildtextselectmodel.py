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
  return ''

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

  if re.match('^1.*', lock): # If file is locked, do nothing but show status
    #TODO maybe do some error checking here.
    message += ""
  elif re.match('^0.*', lock): # If file is unlocked, spawn build
    message += write_lock('1')
    p = threading.Thread(target=build_process)
    p.start()

  html = """<html><title>Docent Learner Administration</title>
    <h1>Docent Learner - text select model build</h1>
    <a href="admin.py">Back to admin.</a><br>
    <a href="/docent-learner/dl/textselect.py">Text Select interface</a><br>
    <br>
    """

  html += "<div id='lock'></div><br><pre id='status'></pre>"

  html += """
  <script>
  var lock = '1';
  function statusListner(){
    if(this.readyState==4){
      document.getElementById('status').textContent = this.responseText;
      console.log("status request complete");
      if(lock == '1'){
        setTimeout(getStatus(), 1000);
      }
    }
  }
    function getStatus(){
    var req = new XMLHttpRequest();
    req.onreadystatechange = statusListner;
    req.open('GET', '/docent-learner/var/textselect-model-build-status.txt');
    req.send();
    console.log("status request sent");
  }
  function lockListner(){
    if(this.readyState==4){
      lock = this.responseText;
      if(lock == '1'){
        document.getElementById('lock').textContent = "The model is being built.";
      }else{
        document.getElementById('lock').textContent = "The model is complete.";
      }
      console.log("lock request complete");
      console.log(lock);
      if(lock == '1'){
        setTimeout(getLock(), 1000);
      }
    }
  }
  function getLock(){
    var req = new XMLHttpRequest();
    req.onreadystatechange = lockListner;
    req.open('GET', '/docent-learner/var/textselect-modelbuild.lock');
    req.send();
    console.log("lock request sent");
  }
  window.onload = getStatus();
  window.onload = getLock();

  </script>
  """
  html += message
  html += "</html>"
  start_response(status, response_headers)

  return [html]
