idLen = 8;
idChars = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';

userAgentId = '';
sessionId = '';

function randomString(length, chars) {
    var result = '';
    for (var i = length; i > 0; --i) result += chars[Math.round(Math.random() * (chars.length - 1))];
    return result;
}

function init_logger() {
  // Check if we have an active session. If not, give it an id.
  if (sessionStorage.getItem('session_id') == null) {
    sessionId = randomString(idLen, idChars);
    sessionStorage.setItem('session_id', sessionId);
  }else{
    sessionId = sessionStorage.getItem('session_id');
  }
  document.getElementById('session_id').value = sessionId;

  // Check if we've seen this user agent before. If not, give it an id.
  if (localStorage.getItem('user_agent_id') == null) {
    userAgentId = randomString(idLen, idChars);
    localStorage.setItem('user_agent_id', userAgentId);
  }else{
    userAgentId = localStorage.getItem('user_agent_id');
  }
  document.getElementById('user_agent_id').value = userAgentId;

  console.log('sessionId: ' + sessionId);
  console.log('userAgentId: ' + userAgentId);
}


function text_is_read() {
  // hide the button the user clicks after reading the text
  document.getElementById('button_area').innerHTML = "";
  document.getElementById('question_area').innerHTML = questionHtml;



  //init_logger();
}
