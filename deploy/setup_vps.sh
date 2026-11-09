#!/bin/bash
# ==============================================================================
# SYNTRA GROUP - AUTOMATED VPS PROVISIONING SCRIPT
# Target OS: Ubuntu 22.04 LTS / 24.04 LTS / Debian 12
# Stack: Python 3 + SQLite + Nginx Reverse Proxy + Let's Encrypt SSL
# ==============================================================================

set -e

echo "=========================================================="
echo "  INICIANDO INSTALACIÓN DE SERVIDOR SYNTRA SUPPLY EN VPS  "
echo "=========================================================="

# 1. Update packages
echo "[1/6] Actualizando paquetes del sistema..."
apt-get update && apt-get upgrade -y
apt-get install -y python3 python3-pip python3-venv git nginx certbot python3-certbot-nginx ufw curl

# 2. Configure Firewall (UFW)
echo "[2/6] Configurando Firewall..."
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw --force enable

# 3. Create web directories
echo "[3/6] Preparando directorios en /var/www/syntra..."
mkdir -p /var/www/syntra
mkdir -p /var/www/certbot

# 4. Clone or pull repositories
echo "[4/6] Clonando repositorio de Syntra Group..."
if [ ! -d "/var/www/syntra/crm" ]; then
    git clone https://github.com/Jslfar/syntra-crm.git /var/www/syntra
else
    cd /var/www/syntra && git pull origin main
fi

# Clone syntraweb submodule/folder if not present
if [ ! -d "/var/www/syntra/syntraweb" ]; then
    git clone https://github.com/Jslfar/syntraweb.git /var/www/syntra/syntraweb
else
    cd /var/www/syntra/syntraweb && git pull origin main
fi

# Set permissions
chown -R www-data:www-data /var/www/syntra
chmod -R 755 /var/www/syntra

# 5. Configure Systemd Service
echo "[5/6] Instalando y activando servicio systemd syntra..."
cp /var/www/syntra/deploy/syntra.service /etc/systemd/system/syntra.service
systemctl daemon-reload
systemctl enable syntra
systemctl restart syntra

# 6. Configure Nginx
echo "[6/6] Configurando Nginx..."
cp /var/www/syntra/deploy/nginx-syntra.conf /etc/nginx/sites-available/syntrasupply.conf
ln -sf /etc/nginx/sites-available/syntrasupply.conf /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default
nginx -t
systemctl reload nginx

echo "=========================================================="
echo "  ¡INSTALACIÓN COMPLETADA CON ÉXITO!                      "
echo "  Para emitir los certificados SSL ejecuta:               "
echo "  certbot --nginx -d syntrasupply.com -d www.syntrasupply.com -d admin.syntrasupply.com"
echo "=========================================================="
