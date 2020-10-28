#!/bin/sh
   tokenQuery=`curl -X POST https://app.debricked.com/api/login_check -d _username=nicolae.paladi@eit.lth.se -d _password=$1`
   sleep 1
   token=`echo $tokenQuery | sed  -e 's/{"token"://g' -e 's/}//g'`
   echo "Token is \n $token"
   apiQuery=`curl -X GET https://app.debricked.com/api/1.0/open/supported/dependency/files -H "Authorization: Bearer $token"`
   echo "Query result is: $apiQuery"

