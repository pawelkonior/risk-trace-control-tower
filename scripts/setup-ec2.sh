#!/usr/bin/env bash
# EC2 bootstrap — run once on fresh Ubuntu 24.04
# Usage: curl -sL https://raw.githubusercontent.com/.../scripts/setup-ec2.sh | sudo bash
set -euo pipefail

DOMAIN="${1:?Usage: $0 <yourdomain.com>}"
RWA_DIR=/opt/rwa

echo "==> Installing Docker"
apt-get update -q
apt-get install -y -q \
    ca-certificates curl gnupg nginx certbot python3-certbot-nginx \
    awscli jq unzip

install -m 0755 -d /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg \
    | gpg --dearmor -o /etc/apt/keyrings/docker.gpg
echo \
    "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] \
    https://download.docker.com/linux/ubuntu $(. /etc/os-release && echo "$VERSION_CODENAME") stable" \
    > /etc/apt/sources.list.d/docker.list
apt-get update -q
apt-get install -y -q docker-ce docker-ce-cli containerd.io docker-compose-plugin

systemctl enable docker
usermod -aG docker ubuntu

echo "==> Creating /opt/rwa"
mkdir -p "${RWA_DIR}"

echo "==> Writing .env template (fill in values)"
cat > "${RWA_DIR}/.env" <<'EOF'
# --- Fill these in ---
REGISTRY=ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com
IMAGE_TAG=latest
POSTGRES_USER=rwa
POSTGRES_PASSWORD=CHANGE_ME_STRONG_PASSWORD
DOMAIN=YOUR_DOMAIN
EOF

echo "==> Copying docker-compose.prod.yml"
# Assumes repo is cloned or files copied here
if [ -f "/tmp/docker-compose.prod.yml" ]; then
    cp /tmp/docker-compose.prod.yml "${RWA_DIR}/docker-compose.prod.yml"
fi

echo "==> Configuring nginx"
sed "s/YOUR_DOMAIN/${DOMAIN}/g" /tmp/rwa.conf > /etc/nginx/sites-available/rwa
ln -sf /etc/nginx/sites-available/rwa /etc/nginx/sites-enabled/rwa
rm -f /etc/nginx/sites-enabled/default
nginx -t && systemctl reload nginx

echo "==> Obtaining Let's Encrypt certificate"
certbot --nginx -d "${DOMAIN}" --non-interactive --agree-tos \
    --email "admin@${DOMAIN}" --redirect

echo "==> Setting up certbot auto-renewal"
systemctl enable certbot.timer
systemctl start certbot.timer

echo "==> Setting up ECR login cron (IAM instance profile required)"
cat > /usr/local/bin/ecr-login.sh <<'SCRIPT'
#!/bin/bash
REGION=$(curl -s http://169.254.169.254/latest/meta-data/placement/region)
REGISTRY=$(grep REGISTRY /opt/rwa/.env | cut -d= -f2)
aws ecr get-login-password --region "${REGION}" \
    | docker login --username AWS --password-stdin "${REGISTRY}"
SCRIPT
chmod +x /usr/local/bin/ecr-login.sh

# ECR token expires every 12h
echo "0 */11 * * * root /usr/local/bin/ecr-login.sh" > /etc/cron.d/ecr-login

echo ""
echo "==> Setup complete. Next steps:"
echo "    1. Fill in /opt/rwa/.env (REGISTRY, POSTGRES_PASSWORD, DOMAIN)"
echo "    2. Copy docker-compose.prod.yml to /opt/rwa/"
echo "    3. Run: cd /opt/rwa && docker compose -f docker-compose.prod.yml up -d"
echo "    4. Set GitHub Secrets (see docs)"
