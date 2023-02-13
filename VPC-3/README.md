# Hands-on VPC-03 : 
  Purpose of the this hands-on training is to create VPC peering ,connecting resources from different VPCs and creating S3 VPC endpoint. 

# Learning Outcomes
- Creating VPC peering between two VPCs (Default and Custom one)
- Creating a  S3 VPC Endpoint.

# Outline: 

## Part 1 - Prep 

## Part 2 - Creating VPC peering between two VPCs (Default and Custom one)

## Part 3- Creating a  S3 VPC Endpoint.



## Part 1 - Prep---> Launching Instances and creating an NatGateway

- Launch 3 Instances. 
  
  - First instance will be private  in "bekir-az1a-private-subnet" of "bekir-vpc-a",
  - Second instance will be public for bastion host in  "bekir-az1b-public-subnet" of "bekir-vpc-a"
  - Third one will be public as "Windows" instance in "default VPC "


  - Warning !!!!  Since the private EC2 needs internet connectivity to set user data, we first need NAT Gateway.

### A. Since the private EC2 instance needs internet connectivity to set user data, first create NAT Gateway

- Click Create Nat Gateway button in left hand pane on VPC menu

- click Create NAT Gateway.

```bash
Name                      : bekir-nat-gateway

Subnet                    : bekir-az1a-public-subnet

Elastic IP allocation ID  : Allocate Elastic IP
```
- click "Create Nat Gateway" button

### B. Modify Route Table of Private Instance's Subnet

- Go to VPC console on left hand menu and select Route Table tab

- Select "bekir-private-rt" ---> Routes ----> Edit Rule ---> Add Route
```
Destination     : 0.0.0.0/0
Target ----> Nat Gateway ----> bekir-nat-gateway
```
- click save changes

WARNING!!! ---> Be sure that NAT Gateway is in active status. Since the private EC2 needs internet connectivity to set user data, NAT Gateway must be ready.

### C. Configure Public Windows instance in Default VPC.

```text
AMI             : Microsoft Windows Server 2019 Base
Instance Type   : t2.micro
Network         : Default VPC
Subnet          : Default Public Subnet
Security Group  : 
    Sec.Group Name : WindowsSG
    Rules          : RDP --- > 3389 ---> Anywhere
Tag             :
    Key         : Name
    Value       : Public-Windows

PS: For MAC, "Microsoft Remote Desktop" program should be installed on the computer.
```

### D. Configure Private instance in 'bekir-az1a-private-subnet' of 'bekir-vpc-a'.

```text
AMI             : Amazon Linux 2
Instance Type   : t2.micro
Network         : bekir-vpc-a 
Subnet          : bekir-az1a-private-subnet
user data       : 

#!/bin/bash

yum update -y
amazon-linux-extras install nginx1.12
cd /usr/share/nginx/html
chmod o+w /usr/share/nginx/html
rm index.html
wget https://raw.githubusercontent.com/awsdevopsteam/route-53/master/index.html
wget https://raw.githubusercontent.com/awsdevopsteam/route-53/master/ken.jpg
systemctl enable nginx
systemctl start nginx

Security Group    : 
    Sec.Group Name : PrivateSG
    Rules          : SSH  ---> 22 ---> Anywhere
                     HTTP ---> 80 ---> Anywhere
                     All ICMP IPv4 ---> Anywhere
    
Tag             :
    Key         : Name
    Value       : Private-Instance
```

### E. Configure Public Instance (Bastion Host) in "bekir-az1b-public-subnet" of "bekir-vpc-a"

```text
AMI             : Amazon Linux 2
Instance Type   : t2.micro
Network         : bekir-vpc-a
Subnet          : bekir-az1b-public-subnet
Security Group    : 
    Sec.Group Name : PublicSG
    Rules          : SSH --- > 22 ---> Anywhere
Tag             :
    Key         : Name
    Value       : Public-Instance (Bastion Host)
```

# Part 1 - Creating VPC peering between two VPCs (Default and Custom one)

## STEP 1: Connecting to Window instance

- Go to instance named 'Public-Windows' and hit the connect button ----> Download Remote Desktop File

- Decrypt your ".pem key" using "Get Password" button
  - Push "Get Password" button
  - Select your pem key using "Choose File" button ----> Push "Decrypt Password" button
  - copy your Password and paste it "Windows Remote Desktop" program as a "administrator password"

- Open the internet explorer of windows machine and paste the private IP of EC2 named 'Private-Instance'

- It is not able to connect to the website 


## STEP 2: Setting up Peering


- Go to 'Peering connections' menu on the left hand side pane of VPC

- Push "Create Peering Connection" button

```text
Peering connection name tag : First Peering
VPC(Requester)              : Default VPC
Account                     : My Account
Region                      : This Region (us-east-1)
VPC (Accepter)              : bekir-vpc-a
```
- Hit "Create peering connection" button

- Select 'First Peering' ----> Action ---> Accept Request ----> Accept Request

- Go to route Tables and select default VPC's route table ----> Routes ----> Edit routes
```
Destination: paste "bekir-vpc-a" CIDR blok
Target ---> peering connection ---> select 'First Peering' ---> Save routes
```

- select bekir-private-rt's route table ----> Routes ----> Edit routes
```
Destination: paste "default VPC" CIDR blok
Target ---> peering connection ---> select 'First Peering' ---> Save routes
```
## STEP 3: Checking the "private web page" from the instance located in "different VPC" 

- Go to windows EC2 named 'Public-Windows', write the private IP address of the Private-Instance on browser and show the website with KEN.


WARNING!!! ---> Please do not terminate "NAT Gateway" and "Private-Instance" for next part.


# Part 3 - Create VPC Endpoint

## STEP 1: 

### A. Create S3 Bucket 

- Go to the S3 service on AWS console
- Create a bucket of `bekir-vpc-endpoint` with following properties, 

```text
Object Ownership            : ACLs disabled
Block all public access     : Checked
Versioning                  : Disabled
Server access logging       : Disabled
Tags                        : 0 Tags
Default encryption          : Disabled
Object lock                 : Disabled

```
- Upload 'Honda.png' file into the S3 bucket

### B. Create IAM role to reach S3 from "Private-Instance"

- Go to IAM Service from AWS console and select roles on left hand pane

- click create role
```
Trusted entity type: AWS Service
use case : EC2  
Use cases for other AWS services: s3 ---> Next : Permission
Permissions Policies: AmazonS3FullAccess ---> Next
Role Name : bekirS3FullAccessforEndpoint
Role description: bekir S3 Full Access for Endpoint
click create button
```
Go to EC2 service from AWS console

Select "Private-Instance" ---> Actions ---> Security ---> Modify IAM Role  select newly created IAM role named 'bekirS3FullAccessforEndpoint' ---> Apply

## STEP 2: Access S3 Bucket from Private-Instance

### A. Connect to the Bastion host

- Go to terminal and connect to the Bastion host named 'Public-Instance (Bastion Host)'

- Using Bastion host connect to the EC2 instance in "private subnet" named 'Private-Instance ' (using ssh agent or copying directly pem key into the EC2)

- Start the ssh-agent in the background

```bash
eval "$(ssh-agent)"
```
- Add your private key to the ssh agent on your computer `localhost`.

```bash
ssh-add ./[your pem file name]
```
- connect to the ec2 instance (Public-Instance (Bastion Host)) in bekir-az1b-public-subnet
```bash
ssh -A ec2-user@ec2-3-88-199-43.compute-1.amazonaws.com
```
### B.Connect to the Private Instance

- once logged into the bastion host connect to the private instance in the private subnet:
```bash
ssh ec2-user@[Your private EC2 private IP]
```
### C. Use CLI to verify connectivity

- list the bucket in S3 and content of S3 bucket named "aws s3 ls "bekir-vpc-endpoint" via following command

```
aws s3 ls
aws s3 ls bekir-vpc-endpoint
```

- go to NAT Gateways on VPC service

- select bekir-nat-gateways ---> Actions ---> Delete NAT Gateway

- Check the Elastic IP whether it is released or not . If not released it. 

- Go to the terminal and try to connect again S3 bucket via following command
```
aws s3 ls
```
- show that you are "not able to connect" to the s3 buckets list


## STEP 3: Create Endpoint

### A. Connect  to S3 via Endpoint

- go to the Endpoints menu on left hand pane in VPC

- click Create Endpoint
```text
Name             : bekir-s3-endpoint
Service Category : AWS services
Service Name     : com.amazonaws.us-east-1.s3
Service Type     : gateway
VPC              : bekir-vpc-a
```
- Create Endpoint

- Go to newly created S3 Endpoint>>> "Route tables" >>> "Manage route tables">>> select "bekir-private-rt"
- Go to private route table named ‘bekir-private-rt’ and show the endpoint rule that is automatically created by AWS

### B. Connect to S3 via Endpoint

- Go to terminal, list the buckets in S3 and content of S3 bucket named "bekir-vpc-endpoint" via following command
```bash
aws s3 ls
aws s3 ls bekir-vpc-endpoint
```

- copy the 'Honda.png' file from S3 bucket into the private EC2
```bash
aws s3 cp s3://bekir-vpc-endpoint/Honda.png .
```

**Don't forget to terminate the resources you've created!!!!!!!**










