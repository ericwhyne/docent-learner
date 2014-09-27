#!/bin/bash
imagedir="/var/www/html/docent-learner/images/"
outfilename=`date +"%Y-%m-%d"`-image-tags.json
echo "[" > $outfilename
cat $imagedir*.json | while read a; do echo $imagedir$a, >> $outfilename; done
#sed -i '1s/^/\[/' $outfilename
sed -i '$s/,$/\n\]/' $outfilename
echo "Filename: $outfilename"
