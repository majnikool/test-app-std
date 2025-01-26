output "fastapi_vm_public_ip" {
  value = aws_instance.fastapi_vm.public_ip
}

output "postgres_vm_private_ip" {
  value = aws_instance.postgres_vm.private_ip
}
