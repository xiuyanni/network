#!/bin/bash

curl -i -X POST    -H "Content-Type:application/x-www-form-urlencoded"    -d "command=register"    -d "username=bob@gmail.com" -d "password=123"  'http://146.96.28.105:8080'
curl -i -X POST    -H "Content-Type:application/x-www-form-urlencoded"    -d "command=register"    -d "username=alice@gmail.com" -d "password=123"  'http://146.96.28.105:8080'
curl -i -X POST    -H "Content-Type:application/x-www-form-urlencoded"    -d "command=register"    -d "username=cherry@gmail.com" -d "password=123"  'http://146.96.28.105:8080'

curl -i -X POST    -H "Content-Type:application/x-www-form-urlencoded"    -d "command=addfriend"    -d "username1=alice@gmail.com" -d "username2=bob@gmail.com"  'http://146.96.28.105:8080'

curl -i -X POST    -H "Content-Type:application/x-www-form-urlencoded"    -d "command=addfriend"    -d "username1=alice@gmail.com" -d "username2=cherry@gmail.com"  'http://146.96.28.105:8080'

curl -i -X POST    -H "Content-Type:application/x-www-form-urlencoded"    -d "command=checkin"  -d "username=alice@gmail.com"  -d "latitude=876" -d "longtitude=987"  'http://146.96.28.105:8080'
curl -i -X POST    -H "Content-Type:application/x-www-form-urlencoded"    -d "command=checkin"  -d "username=bob@gmail.com"  -d "latitude=976" -d "longtitude=787"  'http://146.96.28.105:8080'
curl -i -X POST    -H "Content-Type:application/x-www-form-urlencoded"    -d "command=checkin"  -d "username=cherry@gmail.com"  -d "latitude=1276" -d "longtitude=689"  'http://146.96.28.105:8080'

