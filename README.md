# 🚀 SYNTRA GROUP C.A. — CRM & ERP Almacén Lechería

Sistema integral de gestión de operaciones, inventario físico (1,750 unidades / 117 SKUs Kingroon), ventas duales Venezuela (BCV vs. USDT Binance Pay / Cash), notas de entrega, red de afiliados, arqueo de caja y control de acceso por roles.

---

## 🔐 1. CONTROL DE ACCESO & ROLES (RBAC)

El sistema cuenta con una pantalla de bloqueo y control de acceso por perfiles para permitir que futuros empleados o personal de almacén operen el sistema sin comprometer información confidencial ni borrar datos:

| Rol | PIN por Defecto | Permisos y Capacidades | Restricciones de Seguridad |
|---|---|---|---|
| **👑 Administrador (Syntra Master)** | `2026` | Control total, edición de productos, eliminación de órdenes/gastos/clientes, visualización de Costos Landed China FOB, P&L (Ganancias Netas), descarga de backups SQLite. | Ninguna. |
| **👤 Personal (Operador Almacén / Ventas)** | `1234` | Registrar nuevas ventas, emitir notas de entrega, cobrar en caja, registrar clientes, calcular cotizaciones 3D y duales, ver stock disponible físico. | 🚫 **No puede eliminar** ventas, clientes, proveedores ni gastos.<br>🚫 **No ve** costos de importación China FOB / Landed.<br>🚫 **No ve** márgenes de ganancia ni P&L.<br>🚫 **No puede** descargar la base de datos SQLite. |

> [!TIP]
> Puedes cambiar o bloquear la sesión en cualquier momento haciendo clic en la insignia de perfil en la esquina superior derecha (`👑 Admin` / `👤 Personal`).

---

## 📱 2. CÓMO USARLO EN TU IPHONE 17 PRO (COMO APP NATIVA)

El CRM está 100% optimizado para el **iPhone 17 Pro** (Super Retina XDR, Dynamic Island, gestos táctiles y modo pantalla completa PWA sin barras del navegador):

1. **Conéctate al mismo Wi-Fi** de tu oficina / casa en Lechería.
2. Abre **Safari** en tu iPhone y entra en:
   ```
   http://192.168.0.108:8500
   ```
3. Presiona el botón de **Compartir** en Safari (el ícono del cuadrado con flecha hacia arriba).
4. Selecciona **"Agregar a pantalla de inicio"** (Add to Home Screen).
5. Dale el nombre **"Syntra CRM"** y pulsa **Agregar**.

¡Listo! Se abrirá como una aplicación nativa independiente con su propio ícono, barra de estado oscura integrada y menú lateral deslizante táctil.

---

## 🌐 3. SUBIR A GITHUB & DESPLIEGUE EN LA NUBE

A diferencia del sitio web público (`syntraweb`, que es estático y corre en GitHub Pages), el CRM posee un **servidor Python** y una **base de datos SQLite real** (`crm/syntra_crm.db`), por lo que requiere un servidor en la nube para sincronización 24/7 desde la calle o fuera del Wi-Fi.

### Paso A: Subir el repositorio a GitHub
Abre la consola de comandos o PowerShell en esta carpeta y ejecuta:

```bash
# 1. Inicializar Git si aún no está inicializado
git init

# 2. Agregar los archivos al control de versiones
git add .

# 3. Guardar el primer commit del CRM
git commit -m "feat: Syntra CRM v2.0 - RBAC, iPhone 17 Pro, 1750 SKUs, Dual Pricing"

# 4. Cambiar a la rama principal
git branch -M main

# 5. Conectar con tu repositorio en GitHub (crea uno nuevo privado llamado 'syntra-crm' en github.com/new)
git remote add origin https://github.com/Jslfar/syntra-crm.git

# 6. Subir a GitHub
git push -u origin main
```

### Paso B: Desplegar en la Nube (1 Clic Gratis en Render o Railway)
Para tener una URL pública como `https://syntra-crm.onrender.com`:
1. Entra en [Render.com](https://render.com) e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **New +** ➔ **Web Service**.
3. Selecciona tu repositorio `syntra-crm`.
4. Render detectará automáticamente el archivo `render.yaml` y configurará:
   - **Environment:** Python 3
   - **Start Command:** `python crm/server.py`
   - **Persistent Disk:** Montado en SQLite para que las ventas y stock no se borren nunca.
5. Haz clic en **Deploy Web Service**. ¡En 2 minutos tendrás tu CRM online y accesible desde cualquier parte del mundo!

---

## ⚙️ 4. EJECUTAR LOCALMENTE EN TU COMPUTADORA

Si deseas correr el servidor en tu computadora:

```bash
# Iniciar el servidor en el puerto 8500
python crm/server.py 8500
```
- Acceso en tu PC: `http://localhost:8500`
- Acceso en tu red local (móvil/tablet): `http://192.168.0.108:8500`

---

## 🇻🇪 5. PARÁMETROS CRÍTICOS DE NEGOCIO (LECHERÍA, VENEZUELA)

- **Línea Oficial WhatsApp Syntra:** `+58 422-3446675` (`https://wa.me/584223446675`).
- **Modelo de Precios Duales:**
  - **PVP Lista Oficial BCV:** Para facturas y pagos en Bolívares (Pago Móvil / Transferencia VES).
  - **Contado en Divisas (USDT Binance Pay / Efectivo $):** Descuento real directo para captar moneda dura limpia sin fricción bancaria ni riesgo de devaluación.
- **Comisiones de Afiliados:**
  - **$1.50 USD / bobina** si el cliente paga en Divisa Limpia (USDT / Efectivo).
  - **$1.25 USD / bobina** si el cliente paga en Bolívares (VES BCV).
- **Inventario Activo:** 1,750 unidades físicas de fábrica Kingroon FOB Ningbo en almacén Lechería.
