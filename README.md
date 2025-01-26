# FastAPI CRUD Application

This is a FastAPI application that implements CRUD operations with PostgreSQL database integration.

![Application Architecture](https://github.com/majnikool/test-app-std/blob/main/test-app.jpg?raw=true)

## Features
- CRUD operations for items
- PostgreSQL database integration
- Environment variable configuration
- Logging
- Automatic database table creation
- Unit tests

## Setup for Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate 
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a test PostgreSQL instance:
```bash
# Create a Docker network (optional but good practice)
docker network create fastapi-net

# Run PostgreSQL container
docker run --name postgres-db \
  --network fastapi-net \
  -e POSTGRES_USER=myuser \
  -e POSTGRES_PASSWORD=mypassword \
  -e POSTGRES_DB=mydatabase \
  -p 5432:5432 \
  -d postgres:15

# Connect to PostgreSQL container
docker exec -it postgres-db bash

# Connect to PostgreSQL
psql -U myuser -d mydatabase
```

Useful Docker commands for troubleshooting:
```bash
# View container logs
docker logs postgres-db

# Stop the container
docker stop postgres-db

# Remove the container
docker rm postgres-db

# Remove everything and start fresh
docker stop postgres-db
docker rm postgres-db
docker volume prune  # Removes unused volumes
```

4. Configure environment variables:
   - Copy the `.env.example` file to `.env` and update the values according to your PostgreSQL setup.

5. Run the application:
```bash
uvicorn app.main:app --reload
```

The application also supports packaging as an RPM package which will be used in later steps by Ansible.

## Testing

### Manual Testing
```bash
# Create an item
curl -X POST "http://localhost:8000/items/" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Item","description":"Testing our FastAPI app"}'

# Get all items
curl "http://localhost:8000/items/"

# Get the item by ID (replace 1 with the ID from your create response)
curl "http://localhost:8000/items/1"

# Update the item
curl -X PUT "http://localhost:8000/items/1" \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Item","description":"This item has been updated"}'

# Delete the item
curl -X DELETE "http://localhost:8000/items/1"
```

### Automated Testing
```bash
# Run all tests
pytest -v

# Run only CRUD tests
pytest tests/test_crud.py

# Run a specific test
pytest tests/test_crud.py -k "test_partial_update_item"
```

## API Endpoints

- POST /items/ - Create a new item
- GET /items/ - Get all items
- GET /items/{item_id} - Get a specific item
- PUT /items/{item_id} - Update an item
- DELETE /items/{item_id} - Delete an item

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Automated Setup on AWS

### Terraform Section

1. Create an Access key and Secret access key from AWS UI

2. Use AWS CLI to configure credentials on your machine:
```bash
aws configure
```

3. Create an SSH key on your machine (if already created, copy from ~/.ssh).
   This key is referenced in `terraform/9-key-pairs.tf`. Update this file to point to the correct location if you are not using the default SSH key location on your machine.

4. Modify the region and zone values as needed by editing `terraform/0-locals.tf`

5. Fill in the correct AMI values under `terraform/8-instances.tf`. In this example, we are using Amazon Linux 2023. Example command to find the AMI:
```bash
aws ec2 describe-images \
    --filters "Name=name,Values=al2023-ami*" \
    --region us-east-2 \
    --query 'Images[*].[ImageId,Name]' \
    --output table
```

6. This example creates one VPC with one public and one private subnet. They can be modified by editing `terraform/2-vpc.tf` and `terraform/4-subnets.tf`.

   We are also creating a NAT Gateway in the public subnet to provide valid endpoints for VMs in the private subnet if they need to download anything from the web while not being directly exposed to the internet.

   An Internet Gateway is created to provide internet access. These can be modified by editing `terraform/3-igw.tf` and `terraform/5-nat.tf`.

   The example also creates one route table per subnet to create routes between subnets and between subnets and internet. These can be modified in `terraform/6-routes.tf`.

   The `7-security-groups.tf` manages firewall rules for instances. It only allows:
   - SSH and database access to the PostgreSQL DB VM from the FastAPI VM only
   - Public SSH and API access from the internet for the FastAPI VM

As the DB VM is located in the private subnet, we can't SSH to it directly from our machine and Ansible can't access it. To manage this, we have added our public key to the DB VM. To enable SSH access between the FastAPI VM (which we will use as a jump server in our Ansible setup to reach the DB VM) and the DB VM, we need to copy our private key to the FastAPI VM. This way, using the same SSH key from our local machine, the cloud servers can be accessed via SSH:
```bash
scp -i ~/.ssh/id_rsa ~/.ssh/id_rsa ec2-user@<fastapi-vm-ip>:/home/ec2-user/.ssh/id_rsa
```

### GitHub CI/CD

The repository uses GitHub CI for testing the code after each commit and creating an RPM release. To make a release:
```bash
git tag v0.1.0  
git push origin v0.1.0
```

### Ansible Section

1. Configure deployment settings in `group_vars/all.yml`:
   - Choose installation method: 'package' or 'source'
   - Update `public_vm_ip` and `private_vm_ip` with Terraform output

2. Run the playbook:
```bash
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml
```

After execution, Ansible will install and configure the services and run tests to make sure instances are working correctly.

Optional: Limit execution to specific VMs:
```bash
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml --limit fastapi
```

3. Run tests after installation:
```bash
ansible-playbook -i inventory.yml tests/test_installation.yml
```

4. Debugging commands:
```bash
systemctl status fastapi.service
journalctl -u fastapi.service -f
journalctl -u fastapi.service -n 100
```

5. For configuration changes:
   - Edit values in `group_vars/all.yml`
   - Rerun playbook with appropriate limit:
```bash
# For FastAPI changes only
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml --limit fastapi

# For DB changes only
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml --limit postgres

# For both services
ansible-playbook -i ansible/inventory.yml ansible/playbook.yml
```
```