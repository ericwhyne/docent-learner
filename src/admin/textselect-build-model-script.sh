#!/bin/bash
outfile="/var/www/html/docent-learner/var/textselect-model-build-status.txt"
echo "" > $outfile
for i in `seq 1 10`;
do
  echo $i >> $outfile
  sleep 1
done

#Capture information about the model's performance
#Write meta-data about when model was built

#Unlock the interface
echo 0 > "/var/www/html/docent-learner/var/textselect-modelbuild.lock"
