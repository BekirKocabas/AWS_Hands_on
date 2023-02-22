import boto3
ec2 = boto3.resource('ec2')

# create a new EC2 instance
instances = ec2.create_instances(
     ImageId='ami-0dfcb1ef8550277af', # linux2 ami id
     MinCount=1,
     MaxCount=1,
     InstanceType='t2.micro',
     KeyName='firstkey' # put your keypair without .pem
 )