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

questions = [["""In 1848, Charles Burton of New York City made the first baby carriage, but people strongly objected to the vehicles because they said the carriage operators hit too many pedestrians.  Still convinced that he had a good idea, Burton opened a factory in England.  He obtained orders for the baby carriages from Queen Isabella II of Spain, Queen Victoria of England, and the Pasha of Egypt.  The United States had to wait another ten years before it got a carriage factory, and the first year only 75 carriages were sold.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
Even after the success of baby carriages in England,<br> \
<br> \
<input type='hidden' name='question' value='1'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A4'>Charles Burton was a poor man.<br> \
<input type='radio' name='answer' value='B7'>Americans were still reluctant to buy baby carriages.<br> \
<input type='radio' name='answer' value='C9'>Americans purchased thousands of baby carriages.<br> \
<input type='radio' name='answer' value='D1'>the United States bought more carriages than any other country.<br> \
"""],["""In 1848, Charles Burton of New York City made the first baby carriage, but people strongly objected to the vehicles because they said the carriage operators hit too many pedestrians.  Still convinced that he had a good idea, Burton opened a factory in England.  He obtained orders for the baby carriages from Queen Isabella II of Spain, Queen Victoria of England, and the Pasha of Egypt.  The United States had to wait <b>another ten years before it got a carriage factory</b>, and the first year only 75 carriages were sold.
""","""  \
Please select response that best completes the following sentence:<br> \
<br> \
Even after the success of baby carriages in England,<br> \
<br> \
<input type='hidden' name='question' value='1'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A4'>Charles Burton was a poor man.<br> \
<input type='radio' name='answer' value='B7'>Americans were still reluctant to buy baby carriages.<br> \
<input type='radio' name='answer' value='C9'>Americans purchased thousands of baby carriages.<br> \
<input type='radio' name='answer' value='D1'>the United States bought more carriages than any other country.<br> \
"""],["""In the words of Thomas DeQuincey, "It is notorious that the memory strengthens as you lay burdens upon it."  If, like most people, you have trouble recalling the names of those you have just met, try this: the next time you are introduced, plan to remember the names.  Say to yourself, "I'll listen carefully; I'll repeat each person's name to be sure I've got it, and I will remember."  You'll discover how effective this technique is and probably recall those names for the rest of your life.
""",
""" \
Please select response that best completes the following sentence:<br> \
<br> \
The main idea of the paragraph maintains that the memory<br> \
<br> \
<input type='hidden' name='question' value='2'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A4'>always operates at peak efficiency.<br> \
<input type='radio' name='answer' value='B9'>breaks down under great strain.<br> \
<input type='radio' name='answer' value='C7'>improves if it is used often.<br> \
<input type='radio' name='answer' value='D1'>becomes unreliable if it tires.<br> \
"""],["""In the words of Thomas DeQuincey, "It is notorious that the <b>memory strengthens as you lay burdens upon it</b>."  If, like most people, you have trouble recalling the names of those you have just met, try this: the next time you are introduced, plan to remember the names.  Say to yourself, "I'll listen carefully; I'll repeat each person's name to be sure I've got it, and I will remember."  You'll discover how effective this technique is and probably recall those names for the rest of your life.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
The main idea of the paragraph maintains that the memory<br> \
<br> \
<input type='hidden' name='question' value='2'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A4'>always operates at peak efficiency.<br> \
<input type='radio' name='answer' value='B9'>breaks down under great strain.<br> \
<input type='radio' name='answer' value='C7'>improves if it is used often.<br> \
<input type='radio' name='answer' value='D1'>becomes unreliable if it tires.<br> \
"""],["""Unemployment was the overriding fact of life when Franklin D. Roosevelt became President of the United States on March 4, 1933.  An anomaly of the time was that the government did not systematically collect statistics of joblessness; actually it did not start doing so until 1940.  The Bureau of Labor Statistics later estimated that 12,830,000 persons were out of work in 1933, about one-fourth of a civilian labor force of over fifty-one million. <br> \
Roosevelt signed the Federal Emergency Relief Act (FERA) on May 12, 1933.  The President selected Harry L. Hopkins, who headed the New York relief program, to run FERA.  A gifted administrator, Hopkins quickly put the program into high gear.  He gathered a small staff in Washington and brought the state relief organizations into the FERA system.  While the agency tried to provide all the necessities, food came first. City dwellers usually got an allowance for fuel, and rent for one month was provided in case of eviction.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
This passage is primarily about \
<br> \
<input type='hidden' name='question' value='3'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A4'>unemployment in the 1930s.<br> \
<input type='radio' name='answer' value='B9'>the effect of unemployment on United States families.<br> \
<input type='radio' name='answer' value='C1'>President Franklin D. Roosevelt’s presidency.<br> \
<input type='radio' name='answer' value='D7'>President Roosevelt’s FERA program.<br> \
"""],["""Unemployment was the overriding fact of life when Franklin D. Roosevelt became President of the United States on March 4, 1933.  An anomaly of the time was that the government did not systematically collect statistics of joblessness; actually it did not start doing so until 1940.  The Bureau of Labor Statistics later estimated that 12,830,000 persons were out of work in 1933, about one-fourth of a civilian labor force of over fifty-one million. <br> \
<b>Roosevelt signed the Federal Emergency Relief Act (FERA)</b> on May 12, 1933.  The President selected Harry L. Hopkins, who headed the New York relief program, to run FERA.  A gifted administrator, Hopkins quickly put the program into high gear.  He gathered a small staff in Washington and brought the state relief organizations into the FERA system.  While the agency tried to provide all the necessities, food came first. City dwellers usually got an allowance for fuel, and rent for one month was provided in case of eviction.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
This passage is primarily about <br>\
<br> \
<input type='hidden' name='question' value='3'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A4'>unemployment in the 1930s.<br> \
<input type='radio' name='answer' value='B9'>the effect of unemployment on United States families.<br> \
<input type='radio' name='answer' value='C1'>President Franklin D. Roosevelt’s presidency.<br> \
<input type='radio' name='answer' value='D7'>President Roosevelt’s FERA program.<br> \
"""],["""It is said that a smile is universally understood.  And nothing triggers a smile more universally than a taste of sugar.  Nearly everyone loves sugar.  Infant studies indicate that humans are born with an innate love of sweets.  Based on statistics, a lot of people in Great Britain must be smiling, because on average, every man, woman and child in that country consumes ninety-five pounds of sugar each year.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
From this passage it seems safe to conclude that the English <br> \
<br> \
<input type='hidden' name='question' value='4'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A4'>do not know that too much sugar is unhealthy.<br> \
<input type='radio' name='answer' value='B9'>eat desserts at every meal.<br> \
<input type='radio' name='answer' value='C7'>are fonder of sweets than most people.<br> \
<input type='radio' name='answer' value='D5'>have more cavities than any other people.<br> \
"""],["""It is said that a smile is universally understood.  And nothing triggers a smile more universally than a taste of sugar.  Nearly everyone loves sugar.  Infant studies indicate that humans are born with an innate love of sweets.  Based on statistics, a lot of people in Great Britain must be smiling, because on average, <b>every man, woman and child in that country consumes ninety-five pounds of sugar</b> each year.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
From this passage it seems safe to conclude that the English <br> \
<br> \
<input type='hidden' name='question' value='4'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A4'>do not know that too much sugar is unhealthy.<br> \
<input type='radio' name='answer' value='B9'>eat desserts at every meal.<br> \
<input type='radio' name='answer' value='C7'>are fonder of sweets than most people.<br> \
<input type='radio' name='answer' value='D5'>have more cavities than any other people.<br> \
"""],["""With varying success, many women around the world today struggle for equal rights.  Historically, women have achieved greater equality with men during periods of social adversity.  Three of the following factors initiated the greatest number of improvements for women:  violent revolution, world war, and the rigors of pioneering in an undeveloped land.  In all three cases, the essential element that improved the status of women was a shortage of men, which required women to perform many of society’s vital tasks.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
We can conclude from the information in this passage that <br> \
<br> \
<input type='hidden' name='question' value='5'> \
<input type='hidden' name='bold' value='false'> \
<input type='radio' name='answer' value='A3'>women today are highly successful in winning equal rights.<br> \
<input type='radio' name='answer' value='B9'>only pioneer women have been considered equal to men.<br> \
<input type='radio' name='answer' value='C4'>historically, women have only achieved equality through force.<br> \
<input type='radio' name='answer' value='D7'>historically, the principle of equality alone has not been enough to secure women equal rights.<br> \
"""],["""With varying success, many women around the world today struggle for equal rights.  Historically, women have achieved greater equality with men during periods of social adversity.  Three of the following factors initiated the greatest number of improvements for women:  violent revolution, world war, and the rigors of pioneering in an undeveloped land.  In all three cases, <b>the essential element that improved the status of women was a shortage of men</b>, which required women to perform many of society’s vital tasks.
""",""" \
Please select response that best completes the following sentence:<br> \
<br> \
We can conclude from the information in this passage that <br> \
<br> \
<input type='hidden' name='question' value='5'> \
<input type='hidden' name='bold' value='true'> \
<input type='radio' name='answer' value='A3'>women today are highly successful in winning equal rights.<br> \
<input type='radio' name='answer' value='B9'>only pioneer women have been considered equal to men.<br> \
<input type='radio' name='answer' value='C4'>historically, women have only achieved equality through force.<br> \
<input type='radio' name='answer' value='D7'>historically, the principle of equality alone has not been enough to secure women equal rights.<br> \
"""]
]

demographics = """<br> \
<br> \
<hr width = 20><br> \
Now, please answer some questions about you.<br>\
<br> \
What is your sex?<br> \
<select name='sex'><br> \
<option value='NA'></option><br> \
<option value='Male'>Male</option><br> \
<option value='Female'>Female</option><br> \
</select><br> \
<br> \
In what year were you born? <input type='text' name='year_born'><br> \
<br> \
What is your marital status?<br> \
<select name='marital status'><br> \
<option value='NA'></option><br> \
<option value='Now married'>Now married</option><br> \
<option value='Widowed'>Widowed</option><br> \
<option value='Divorced'>Divorced</option><br> \
<option value='Separated'>Separated</option><br> \
<option value='Never married'>Never married</option><br> \
</select><br> \
<br> \
What is the highest degree or level of school you have completed?<br> \
If currently enrolled, mark the previous grade or highest degree received.<br> \
<select name='education'><br> \
<option value='NA'></option><br> \
<option value='No schooling completed'>No schooling completed</option><br> \
<option value='Nursery school to 8th grade'>Nursery school to 8th grade</option><br> \
<option value='9th, 10th or 11th grade'>9th, 10th or 11th grade</option><br> \
<option value='12th grade, no diploma'>12th grade, no diploma</option><br> \
<option value='High school graduate'>High school graduate - high school diploma or the equivalent (for example: GED)</option><br> \
<option value='Some college credit, but less than 1 year'>Some college credit, but less than 1 year</option><br> \
<option value='1 or more years of college, no degree'>1 or more years of college, no degree</option><br> \
<option value='Associate degree'>Associate degree (for example: AA, AS)</option><br> \
<option value='Bachelor's degree'>Bachelor's degree (for example: BA, AB, BS)</option><br> \
<option value='Master's degree'>Master's degree (for example: MA, MS, MEng, MEd, MSW, MBA)</option><br> \
<option value='Professional degree'>Professional degree (for example: MD, DDS, DVM, LLB, JD)</option><br> \
<option value='Doctorate degree'>Doctorate degree (for example: PhD, EdD)</option><br> \
</select><br> \
<br> \
What is your employment status?<br> \
<select name='employment'><br> \
<option value='NA'></option><br> \
<option value='Employed for wages'>Employed for wages</option><br> \
<option value='Self-employed'>Self-employed</option><br> \
<option value='Out of work and looking for work'>Out of work and looking for work</option><br> \
<option value='Out of work but not currently looking for work'>Out of work but not currently looking for work</option><br> \
<option value='A homemaker'>A homemaker</option><br> \
<option value='A student'>A student</option><br> \
<option value='Retired'>Retired</option><br> \
<option value='Unable to work'>Unable to work</option><br> \
</select><br> \
<br> \
What is your total household income?<br> \
<select name='household income'><br> \
<option value='NA'></option><br> \
<option value='Less than $10,000'>Less than $10,000</option><br> \
<option value='$10,000 to $19,999'>$10,000 to $19,999</option><br> \
<option value='$20,000 to $29,999'>$20,000 to $29,999</option><br> \
<option value='$30,000 to $39,999'>$30,000 to $39,999</option><br> \
<option value='$40,000 to $49,999'>$40,000 to $49,999</option><br> \
<option value='$50,000 to $59,999'>$50,000 to $59,999</option><br> \
<option value='$60,000 to $69,999'>$60,000 to $69,999</option><br> \
<option value='$70,000 to $79,999'>$70,000 to $79,999</option><br> \
<option value='$80,000 to $89,999'>$80,000 to $89,999</option><br> \
<option value='$90,000 to $99,999'>$90,000 to $99,999</option><br> \
<option value='$100,000 to $149,999'>$100,000 to $149,999</option><br> \
<option value='$150,000 or more'>$150,000 or more</option><br> \
</select><br> \
<br> \
Please specify your ethnicity.<br> \
<select name='ethnicity'><br> \
<option value='NA'></option><br> \
<option value='Hispanic or Latino'>Hispanic or Latino</option><br> \
<option value='American Indian or Alaska Native'>American Indian or Alaska Native</option><br> \
<option value='Asian'>Asian</option><br> \
<option value='Black or African American'>Black or African American</option><br> \
<option value='Native Hawaiian or Other Pacific Islander'>Native Hawaiian or Other Pacific Islander</option><br> \
<option value='White'>White</option><br> \
<option value='Other'>Other</option><br> \
</select><br> \
<br> \
What is your primary language (i.e., the language you speak most of the time)?<br> \
<select name='language'><br> \
<option value='NA'></option><br> \
<option value='Rather not say'>Rather not say</option><br> \
<option value='Chinese'>Chinese</option><br> \
<option value='Japanese'>Japanese</option><br> \
<option value='Russian'>Russian</option><br> \
<option value='English'>English</option><br> \
<option value='French'>French</option><br> \
<option value='German'>German</option><br> \
<option value='Spanish'>Spanish</option><br> \
<option value='Danish'>Danish</option><br> \
<option value='Dutch'>Dutch</option><br> \
<option value='Italian'>Italian</option><br> \
<option value='Greek'>Greek</option><br> \
<option value='Portuguese'>Portuguese</option><br> \
<option value='Hebrew'>Hebrew</option><br> \
<option value='Norwegian'>Norwegian</option><br> \
<option value='Swedish'>Swedish</option><br> \
<option value='Korean'>Korean</option><br> \
<option value='Other'>Other</option><br> \
</select><br> \
<br> \
Where are you located?<br> \
<select name='location'><br> \
<option value='NA'></option><br> \
<option value='Africa'>Africa</option><br> \
<option value='Antarctica'>Antarctica</option><br> \
<option value='Asia'>Asia</option><br> \
<option value='Oceania'>Oceania (Australia, New Zealand, etc.)</option><br> \
<option value='Europe'>Europe</option><br> \
<option value='USA'>USA</option><br> \
<option value='Canada'>Canada</option><br> \
<option value='Mexico'>Mexico</option><br> \
<option value='Central America'>Central America</option><br> \
<option value='South America'>South America</option><br> \
<option value='Middle East'>Middle East</option><br> \
<option value='West Indies'>West Indies</option><br> \
</select><br> \
"""

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
      random_question_i = random.randint(0,len(questions)-1)
      content =  questions[random_question_i][0]
      random_question = questions[random_question_i][1]

      form = """
      <script>
      questionHtml = "<form action=''/docent-learner/dl/boldtext.py' method='post'> \
      <input type='hidden' name='user_agent_id' id='user_agent_id' value=''> \
      <input type='hidden' name='session_id' id='session_id' value=''> \
      %s \
      %s \
      <br><input type='submit' value='Submit'> \
      </form> \
      "
      </script>
      """ % (random_question, demographics)

      content_display = """
      <br><center><table class='imagetable' cellpadding='60'><tr><td id='question_area'>
      """ + content + """
      </td></tr></table><br><br></center>"""

      html = html_header + "<table class='rounded'><tr><td>" + content_display + "</td></tr><tr><td id='button_area'><button type='button' onclick='text_is_read()'>Click here after reading the text</button></td></tr></table>"

      html += docentlearner

      html += form + "<script src='/docent-learner/static/boldtext.js'></script></body></html>"

  return [html]
