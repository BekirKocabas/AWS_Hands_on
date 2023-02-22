import boto3
ec2 = boto3.resource('ec2')
ec2.Instance('i-03f1cc03ccc02c97d').stop() # put your instance id