cat *.json | while read a; do echo $a, >> aggregate.json; done
sed -i '1s/^/[\n /' aggregate.json
sed -i '$s/,$/]/' aggregate.json
