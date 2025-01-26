resource "aws_key_pair" "my_key" {
  key_name   = "${local.env}-key"
  public_key = file("~/.ssh/id_rsa.pub") # Replace with your public key path
}
