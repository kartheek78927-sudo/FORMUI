output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}

output "public_subnet_ids" {
  description = "IDs of the public subnets"
  value       = values(aws_subnet.public)[*].id
}

output "private_subnet_ids" {
  description = "IDs of the private subnets"
  value       = values(aws_subnet.private)[*].id
}

output "instance_public_ip" {
  description = "Public IP address of the test EC2 instance"
  value       = aws_instance.test.public_ip
}

output "instance_id" {
  description = "ID of the test EC2 instance"
  value       = aws_instance.test.id
}

output "nat_gateway_id" {
  description = "ID of the NAT Gateway"
  value       = aws_nat_gateway.nat.id
}
