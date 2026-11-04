# aws-three-tier-app

## Network architecture
![VPC resource map](docs/01-vpc-resource-map.png)

## 2. Compute (EC2, Nginx, pm2)
Private EC2 instance with no public IP, accessed through SSM Session Manager (no SSH keys, no open ports).

**IAM role (least privilege):** SSM and CloudWatch agent policies only.
![IAM role](docs/02-iam-role.png)

**Outbound internet through NAT gateway (app subnets only):**
![App route table](docs/03-app-route-nat.png)

**Instance in the private subnet, no public IP:**
![EC2 private](docs/04-ec2-private.png)

**Nginx reverse proxy to a Node app managed by pm2:**
![Nginx and pm2](docs/05-nginx-pm2.png)

## 3. Database (RDS MySQL)
Private RDS instance, reachable only from the app security group. Credentials are managed by AWS Secrets Manager and read at runtime through the instance role.

![RDS](docs/06-rds.png)
![RDS connection test](docs/07-rds-connect.png)

## 4. Load balancing and Auto Scaling
An Application Load Balancer in the public subnets forwards HTTP traffic to EC2 instances in the private app subnets. An Auto Scaling group keeps 2 instances running across two Availability Zones (min 2, max 3), scales on 50% average CPU, and replaces instances that fail the `/health` check.

**Target group: both targets healthy, one in each AZ:**
![Target group healthy](docs/08-target-group-healthy.png)

**ALB resource map (listener, target group, targets):**
![ALB resource map](docs/09-alb-resource-map.png)

**Request served through the ALB by a private instance:**
![ALB in browser](docs/10-alb-browser.png)

**Traffic distributed across both instances:**
![Load balancing](docs/11-alb-loadbalancing.png)

**Auto Scaling group with 2 instances in service:**
![Auto Scaling group](docs/12-asg.png)

