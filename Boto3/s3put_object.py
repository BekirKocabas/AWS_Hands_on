import boto3

#use amazon s3
s3 = boto3.resource('s3')

#upload a new file
data = open('test.jpg', 'rb')
s3.Bucket('bekirs-boto3-bucket').put_object(Key='test.jpg', Body=data)
