#!/bin/bash

aws dynamodb create-table \
	--table-name Thread \
	--attribute-definitions AttributeName=ForumName,AttributeType=S AttributeName=Subject,AttributeType=S \
	--key-schema AttributeName=ForumName,KeyType=HASH AttributeName=Subject,KeyType=RANGE \
	--provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

