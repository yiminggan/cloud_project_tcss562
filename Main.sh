#!/bin/bash

############################################################################################################
# There are four jpg file in my bucket can be tested: IMG_0135.jpg, IMG_0136.jpg, IMG_0137.jpg, IMG_0141.jpg
# In output json, box is syringe's location information in form: [x-axis, y-axis, width, height]; 
# profile is the time take to detect.
############################################################################################################

# Json input
json={"\"bucketname\"":\"test.bucket.562f19.yiming\"","\"filename\"":\"IMG_0135.jpg\""}
api="https://ioxr5fabfh.execute-api.us-east-2.amazonaws.com/first_deploy"

echo "Invoking Lambda function using API gateway"
time out_gateway=`curl -s -H "Content-Type: application/json" -X POST -d $json $api`
echo ""

echo "Output:"
echo $out_gateway | jq
echo ""
