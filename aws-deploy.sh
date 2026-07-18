#!/bin/bash

# AWS Deployment Script for Pentesting Ecommerce Django
# FOR AUTHORIZED SECURITY TESTING ONLY

set -e

echo "================================"
echo "AWS Ecommerce Django Deployment"
echo "FOR PENTESTING ONLY"
echo "================================"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
DOMAIN=${1:-"localhost"}
INSTANCE_IP=${2:-$(curl -s http://169.254.169.254/latest/meta-data/local-ipv4 2>/dev/null || echo "localhost")}

echo -e "${YELLOW}[*] Starting deployment...${NC}"
echo -e "${YELLOW}[*] Instance IP: $INSTANCE_IP${NC}"

# 1. Update system
echo -e "${YELLOW}[1] Updating system packages...${NC}"
sudo apt-get update
sudo apt-get upgrade -y
sudo apt-get install -y curl wget git htop

# 2. Install Docker
echo -e "${YELLOW}[2] Installing Docker...${NC}"
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
rm get-docker.sh

# 3. Install Docker Compose
echo -e "${YELLOW}[3] Installing Docker Compose...${NC}"
sudo apt-get install -y docker-compose-v2

# 4. Install nginx (optional, for testing)
echo -e "${YELLOW}[4] Installing nginx...${NC}"
sudo apt-get install -y nginx

# 5. Clone repository
echo -e "${YELLOW}[5] Cloning repository...${NC}"
cd /opt
if [ ! -d "ecommerce-django" ]; then
    # Update this with your actual repository
    # sudo git clone https://github.com/yourusername/ecommerce-django.git
    echo -e "${RED}[!] Please clone the repository manually${NC}"
    echo "sudo git clone <repository-url> /opt/ecommerce-django"
    exit 1
fi

cd ecommerce-django

# 6. Setup environment file
echo -e "${YELLOW}[6] Setting up environment...${NC}"
if [ ! -f ".env" ]; then
    cp .env.pentesting .env
    sed -i "s/localhost/$INSTANCE_IP/g" .env
    echo -e "${GREEN}[+] Created .env file${NC}"
else
    echo -e "${YELLOW}[!] .env file already exists${NC}"
fi

# 7. Build Docker images
echo -e "${YELLOW}[7] Building Docker images (this may take a few minutes)...${NC}"
docker-compose -f docker-compose.pentesting.yml build

# 8. Start containers
echo -e "${YELLOW}[8] Starting containers...${NC}"
docker-compose -f docker-compose.pentesting.yml up -d

# 9. Wait for services
echo -e "${YELLOW}[9] Waiting for services to start...${NC}"
sleep 10

# 10. Check services
echo -e "${YELLOW}[10] Checking services...${NC}"
docker-compose -f docker-compose.pentesting.yml ps

# 11. Setup firewall
echo -e "${YELLOW}[11] Configuring security groups...${NC}"
echo "Make sure your AWS Security Group allows:"
echo "  - Port 8000 (Django)"
echo "  - Port 5050 (pgAdmin)"
echo "  - Port 5432 (PostgreSQL)"
echo "  - Port 6379 (Redis)"
echo "  - Port 80 (HTTP)"

# 12. Display access information
echo -e "${GREEN}================================"
echo "Deployment Complete!"
echo "================================${NC}"
echo ""
echo -e "${GREEN}Access URLs:${NC}"
echo -e "  Django App:  ${GREEN}http://$INSTANCE_IP:8000${NC}"
echo -e "  Admin Panel: ${GREEN}http://$INSTANCE_IP:8000/admin${NC}"
echo -e "  pgAdmin:     ${GREEN}http://$INSTANCE_IP:5050${NC}"
echo ""
echo -e "${YELLOW}Default Credentials:${NC}"
echo "  Admin Username: admin"
echo "  Admin Password: admin123"
echo "  pgAdmin Email: admin@example.com"
echo "  pgAdmin Pass: admin123"
echo "  DB User: ecommerce_user"
echo "  DB Pass: ecommerce_pass"
echo ""
echo -e "${YELLOW}Debug Endpoints:${NC}"
echo "  SQL Injection:   /api/debug/sql-injection/"
echo "  Command Injection: /api/debug/cmd-injection/"
echo "  Path Traversal:  /api/debug/read-file/"
echo "  XXE:             /api/debug/xml-parser/"
echo "  System Info:     /api/debug/system-info/"
echo "  Weak Auth:       /api/debug/weak-auth/"
echo "  Get Logs:        /api/debug/get-logs/"
echo ""
echo -e "${RED}WARNING: This is FOR PENETRATION TESTING ONLY!${NC}"
echo -e "${RED}Do not expose this on the internet unless authorized!${NC}"
echo ""
echo "For detailed vulnerability information, see PENTESTING_GUIDE.md"
