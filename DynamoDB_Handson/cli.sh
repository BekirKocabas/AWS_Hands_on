#!/bin/bash

aws dynamodb create-table --table-name Reply --attribute-definitions AttributeName=Id,AttributeType=S AttributeName=ReplyDateTime,AttributeType=S  AttributeName=PostedBy,AttributeType=S AttributeName=Message,AttributeType=S 
--key-schema AttributeName=Id,KeyType=HASH AttributeName=ReplyDateTime,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=5 --global-secondary-indexes "[{ \"IndexName\": \"PostedBy-Message-Index\",\
"KeySchema\": [{\"AttributeName\":\"PostedBy\",\"KeyType\":\"HASH\"},{\"AttributeName\":\"Message\",\"KeyType\":\"RANGE\"}], \"ProvisionedThroughput\": {\"ReadCapacityUnits\": 10,\"WriteCapacityUnits\": 5}}]"  