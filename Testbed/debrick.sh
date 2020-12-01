#!/bin/sh
   tokenQuery=`curl -s -X POST https://app.debricked.com/api/login_check -d _username=nicolae.paladi@eit.lth.se -d _password=$1`
   sleep 1
   token=`echo $tokenQuery | sed s/'{"token":"'//g | sed s/'"}'//g`
   #echo "Token is \n $token"
   #apiQuery=`curl -X GET https://app.debricked.com/api/1.0/open/supported/dependency/files -H "Authorization: Bearer $token"`
   #echo "Query result is: $apiQuery"

   user=`curl -s -X GET https://app.debricked.com/api/1.0/open/zapier/user -H "accept: application/json" -H "Authorization: Bearer $token"` 
   echo "Vulnerability assessment for user: $user"
   
   repositories=`curl -s -X GET https://app.debricked.com/api/1.0/open/zapier/repositories -H "accept: application/json" -H "Authorization: Bearer $token"` 
   echo "Querying vulnerabilities for repositories: $repositories"

   vulnerabilities=`curl -s -X POST https://app.debricked.com/api/1.0/open/zapier/remediation/poll -H "accept: application/json" -H "Authorization: Bearer $token" -H "Content-Type: application/json" -d "{ \"repo\": [ 3036 ]}" `
   echo "The Following vulnerabilitis were found: $vulnerabilities"
