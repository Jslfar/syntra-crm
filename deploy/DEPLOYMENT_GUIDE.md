# GUÍA MAESTRA DE DESPLIEGUE: SYNTRA SUPPLY EN VPS Y DOMINIO PROPIO
### Presupuesto Total Anual: ~$55.00 – $60.00 USD (Ecosistema Web + CRM Unificado)

Esta guía explica paso a paso cómo activar el dominio `syntrasupply.com` y alojar conjuntamente la **Tienda Web Pública** y el **Panel Administrativo CRM** en un único servidor VPS de alta velocidad.

---

## 💰 1. DESGLOSE DEL PRESUPUESTO ($60/AÑO)

| Concepto | Proveedor Recomendado | Especificaciones | Costo Aproximado |
| :--- | :--- | :--- | :--- |
| **Dominio `.com`** | Spaceship / Namecheap / Cloudflare Registrar | `syntrasupply.com` (1 año con protección WHOIS gratuita) | ~$9.50 – $11.00 USD / año |
| **Servidor VPS Linux** | Hetzner Cloud (CX22) o Hostinger VPS 1 / Contabo | 2 vCPU, 4 GB RAM, 40 GB NVMe, 20 TB tráfico mensual | ~$3.80 – $4.10 USD / mes (~$45.00 – $49.00 USD / año) |
| **Certificados SSL HTTPS** | Let's Encrypt (Certbot) | Certificado wildcard o multidominio automático | **$0.00 (Gratis de por vida)** |
| **Base de Datos SQLite** | Integrada nativa en Python | 0 latencia, ultra rápida, WAL mode | **$0.00** |
| **TOTAL ANUAL** | — | **Ecosistema Completo Funcionando 24/7** | **~$55.00 – $60.00 USD** |

---

## 🌐 2. CONFIGURACIÓN DE REGISTROS DNS (EN TU REGISTRADOR DE DOMINIO)

Una vez que compres el dominio `syntrasupply.com`, ve al panel de gestión de DNS y agrega 3 registros tipo **A** apuntando a la dirección IP pública de tu VPS:

| Tipo | Nombre / Host | Valor / Destino | TTL |
| :---: | :---: | :---: | :---: |
| **A** | `@` (o en blanco) | `TU_IP_DEL_VPS` (ej: `159.69.123.45`) | Automático / 300 seg |
| **A** | `www` | `TU_IP_DEL_VPS` | Automático / 300 seg |
| **A** | `admin` | `TU_IP_DEL_VPS` | Automático / 300 seg |

> [!TIP]
> Con estos registros:
> - `https://syntrasupply.com` abrirá directamente el catálogo público web de consumibles y cotizaciones.
> - `https://admin.syntrasupply.com` (o `https://syntrasupply.com/admin`) abrirá tu CRM privado protegido con PIN.

---

## 🚀 3. INSTALACIÓN EN 1 CLIC EN EL VPS (PASO A PASO)

### Paso A: Conectarse al VPS por SSH
Abre una terminal en tu computadora (PowerShell en Windows o Terminal en Mac/Linux):
```bash
ssh root@TU_IP_DEL_VPS
```

### Paso B: Descargar y ejecutar el script automatizado
Copia y pega este comando en el VPS:
```bash
curl -sSL https://raw.githubusercontent.com/Jslfar/syntra-crm/main/deploy/setup_vps.sh | bash
```

*El script automáticamente actualizará el sistema, instalará Nginx, Python 3, Git, configurará el firewall UFW, clonará ambos repositorios (`syntra-crm` y `syntraweb`), activará el servicio como demonio `systemd` que reinicia solo ante cualquier fallo, y configurará el proxy inverso de Nginx.*

### Paso C: Generar los certificados de seguridad SSL (Candado Verde)
Ejecuta en el VPS:
```bash
certbot --nginx -d syntrasupply.com -d www.syntrasupply.com -d admin.syntrasupply.com
```
Ingresa tu correo para renovaciones automáticas y acepta los términos. ¡Listo! Tu web tendrá HTTPS grado A+.

---

## 🔄 4. CÓMO FUNCIONA LA SINCRONIZACIÓN EN TIEMPO REAL

1. **Catálogo y Stock Centralizado:**
   - La base de datos central es `syntra_crm.db` en el VPS.
   - Cada vez que en el CRM registras una venta, eliminas una orden o ajustas inventario, el servidor Python actualiza `syntraweb/lib/manifest.js` y sincroniza la tienda online instantáneamente (0 segundos de desfase).

2. **Órdenes Web Recibidas:**
   - Cuando un cliente confirma un carrito en la web, el cliente hace clic en "Confirmar Orden por WhatsApp" y en segundo plano se envía un `POST /api/public/order` al CRM.
   - En tu panel de pedidos del CRM aparecerá una cotización pendiente con el desglose del cliente, su RIF/CI, dirección y teléfono.

3. **Respaldos de Seguridad:**
   - Puedes descargar el backup completo de la base de datos con un clic desde el CRM en:
     `https://admin.syntrasupply.com` -> Botón "Descargar Respaldo SQLite" (o vía `/api/backup/download`).

---

## 🛠️ 5. COMANDOS ÚTILES PARA EL VPS

- **Ver el estado del servicio:**
  ```bash
  systemctl status syntra
  ```
- **Ver los logs en vivo:**
  ```bash
  journalctl -u syntra -f
  ```
- **Reiniciar el servicio:**
  ```bash
  systemctl restart syntra
  ```
- **Actualizar cambios tras un `git push`:**
  ```bash
  cd /var/www/syntra && git pull origin main
  cd /var/www/syntra/syntraweb && git pull origin main
  systemctl restart syntra
  ```
