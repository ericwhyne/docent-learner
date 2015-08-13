#!/bin/bash
cd /var/www/html/docent-learner/boldtext
echo ethnicity,employment,education,answer,location,maritalstatus,householdincome,bold,language,ip,year_born,question,turk_random_key,sex
cat *.json | jq '[.ethnicity, .employment, .education, .answer, .location, .maritalstatus, .householdincome, .bold, .language, .ip, .year_born, .question, .turk_random_key, .sex] | @csv' | sed 's/\\//g' | sed 's/^"//g' | sed 's/"$//g'
