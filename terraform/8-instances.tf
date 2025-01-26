resource "aws_instance" "fastapi_vm" {
  ami           = "ami-08970251d20e940b0" # Replace with a suitable AMI for FastAPI
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.public.id
  vpc_security_group_ids = [aws_security_group.fastapi_sg.id]
  key_name      = aws_key_pair.my_key.key_name

  user_data = <<-EOF
#!/bin/bash
mkdir -p /home/ec2-user/.ssh
chmod 700 /home/ec2-user/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDCBOWPN1c6nknwqs9OMvUKa2NTWCB9lRkd4ZIWOmTBiqxLz4siEdZuPGsg2h2aKiiwXUO3i+/y9hNjzPZKTZEPEnCBZ+/prZgxxoYfkTmjswYbMcoAdLUTnTjlqUZhKmkQ1iN8MHfz+zQ7QzxrwboycVNZYpBUYXmX4EWVzzo4nucPP8VsPCaHlvtMvAMM7WSIpcBDIQ58mm7wxLQxJzNs5N6HodRUve1nga5tF5SEtPoyO/YFFVd08Mg4mHLPWXE3dQs/JbG3V6ZAqMKJEp1IVRNmGI2xZ5uCNfVAcAtumOcvGcK/pYCAU8YGAtvtIF57OpChs877ClKwvRLKGck3" >> /home/ec2-user/.ssh/authorized_keys
chmod 600 /home/ec2-user/.ssh/authorized_keys
chown -R ec2-user:ec2-user /home/ec2-user/.ssh
EOF

  tags = {
    Name = "${local.env}-fastapi-vm"
  }
}

resource "aws_instance" "postgres_vm" {
  ami           = "ami-08970251d20e940b0" # Replace with a suitable AMI for PostgreSQL
  instance_type = "t3.micro"
  subnet_id     = aws_subnet.private.id
  vpc_security_group_ids = [aws_security_group.postgres_sg.id]
  key_name      = aws_key_pair.my_key.key_name

  user_data = <<-EOF
#!/bin/bash
mkdir -p /home/ec2-user/.ssh
chmod 700 /home/ec2-user/.ssh
echo "ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDCBOWPN1c6nknwqs9OMvUKa2NTWCB9lRkd4ZIWOmTBiqxLz4siEdZuPGsg2h2aKiiwXUO3i+/y9hNjzPZKTZEPEnCBZ+/prZgxxoYfkTmjswYbMcoAdLUTnTjlqUZhKmkQ1iN8MHfz+zQ7QzxrwboycVNZYpBUYXmX4EWVzzo4nucPP8VsPCaHlvtMvAMM7WSIpcBDIQ58mm7wxLQxJzNs5N6HodRUve1nga5tF5SEtPoyO/YFFVd08Mg4mHLPWXE3dQs/JbG3V6ZAqMKJEp1IVRNmGI2xZ5uCNfVAcAtumOcvGcK/pYCAU8YGAtvtIF57OpChs877ClKwvRLKGck3" >> /home/ec2-user/.ssh/authorized_keys
chmod 600 /home/ec2-user/.ssh/authorized_keys
chown -R ec2-user:ec2-user /home/ec2-user/.ssh
EOF

  tags = {
    Name = "${local.env}-postgres-vm"
  }
}
