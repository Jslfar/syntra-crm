import os
import sys
import json
import sqlite3
import mimetypes
import re
import socket
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CRM_STATIC_DIR = os.path.join(BASE_DIR, "static")
STATIC_DIR = CRM_STATIC_DIR
DB_PATH = os.path.join(BASE_DIR, "syntra_crm.db")
ADMIN_PIN = os.environ.get("ADMIN_PIN", "2026")
STAFF_PIN = os.environ.get("STAFF_PIN", "1234")
ROOT_DIR = os.path.dirname(BASE_DIR)
WEB_DIR = os.path.join(ROOT_DIR, "syntraweb")
sys.path.append(os.path.join(ROOT_DIR, "whatsapp_bridge"))

def get_db():
    conn = sqlite3.connect(DB_PATH, timeout=15.0)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA busy_timeout=15000;")
    except Exception:
        pass
    return conn

def canonicalize_printer_model(raw_name):
    if not raw_name:
        return None
    lower = raw_name.strip().lower()

    # Familia Bambu Lab
    if 'bambu' in lower or 'x1' in lower or 'p1s' in lower or 'p1p' in lower or 'a1' in lower or 'a2' in lower or 'h2' in lower:
        if 'a2l' in lower or 'a2-l' in lower or 'a2 l' in lower:
            return 'Bambu Lab A2L'
        if 'a2' in lower:
            return 'Bambu Lab A2'
        if 'a1 mini' in lower or 'a1-mini' in lower or 'a1  mini' in lower:
            return 'Bambu Lab A1 Mini'
        if 'a1' in lower:
            return 'Bambu Lab A1'
        if 'p1s' in lower:
            return 'Bambu Lab P1S'
        if 'p1p' in lower:
            return 'Bambu Lab P1P'
        if 'x1e' in lower:
            return 'Bambu Lab X1E'
        if 'x1' in lower or 'carbon' in lower or 'x1c' in lower:
            return 'Bambu Lab X1-Carbon'
        if 'h2d' in lower or 'h2' in lower:
            return 'Bambu Lab H2D'
        return 'Bambu Lab'

    # Familia Creality (Ender, K1, K2, CR, Halot)
    if 'ender' in lower or 'creality' in lower or 'k1' in lower or 'k2' in lower or 'cr-10' in lower or 'cr10' in lower or 'cr-m4' in lower or 'halot' in lower:
        if 'k2 plus' in lower or 'k2-plus' in lower or 'k2' in lower:
            return 'Creality K2 Plus'
        if 'k1 max' in lower:
            return 'Creality K1 Max'
        if 'k1c' in lower:
            return 'Creality K1C'
        if 'k1 se' in lower:
            return 'Creality K1 SE'
        if 'k1' in lower:
            return 'Creality K1'
        if 'v3 plus' in lower:
            return 'Creality Ender 3 V3 Plus'
        if 'v3 ke' in lower:
            return 'Creality Ender 3 V3 KE'
        if 'v3 se' in lower:
            return 'Creality Ender 3 V3 SE'
        if 'v3' in lower:
            return 'Creality Ender 3 V3'
        if 'v2 neo' in lower:
            return 'Creality Ender 3 V2 Neo'
        if 'v2' in lower:
            return 'Creality Ender 3 V2'
        if 's1 pro' in lower:
            return 'Creality Ender 3 S1 Pro'
        if 's1 plus' in lower:
            return 'Creality Ender 3 S1 Plus'
        if 's1' in lower:
            return 'Creality Ender 3 S1'
        if 'ender 5 s1' in lower:
            return 'Creality Ender 5 S1'
        if 'ender 5 plus' in lower:
            return 'Creality Ender 5 Plus'
        if 'ender 5' in lower:
            return 'Creality Ender 5'
        if 'cr-10 se' in lower or 'cr10 se' in lower:
            return 'Creality CR-10 SE'
        if 'cr-10 smart' in lower or 'cr10 smart' in lower:
            return 'Creality CR-10 Smart'
        if 'cr-10' in lower or 'cr10' in lower:
            return 'Creality CR-10'
        if 'cr-m4' in lower or 'crm4' in lower:
            return 'Creality CR-M4'
        if 'halot' in lower:
            return 'Creality Halot Mage'
        if 'ender 3 pro' in lower:
            return 'Creality Ender 3 Pro'
        if 'ender 3 neo' in lower:
            return 'Creality Ender 3 Neo'
        if 'ender' in lower:
            return 'Creality Ender 3'
        return 'Creality'

    # Familia Elegoo
    if 'neptune' in lower or 'elegoo' in lower or 'centauri' in lower or 'saturn' in lower or 'mars' in lower:
        if 'centauri' in lower:
            return 'Elegoo Centauri Carbon'
        if 'saturn 4 ultra' in lower:
            return 'Elegoo Saturn 4 Ultra'
        if 'saturn 4' in lower:
            return 'Elegoo Saturn 4'
        if 'saturn' in lower:
            return 'Elegoo Saturn 3'
        if 'mars 5' in lower:
            return 'Elegoo Mars 5'
        if 'mars 4' in lower or 'mars' in lower:
            return 'Elegoo Mars 4'
        if '4 max' in lower:
            return 'Elegoo Neptune 4 Max'
        if '4 plus' in lower:
            return 'Elegoo Neptune 4 Plus'
        if '4 pro' in lower:
            return 'Elegoo Neptune 4 Pro'
        if '4' in lower:
            return 'Elegoo Neptune 4'
        if '3 plus' in lower:
            return 'Elegoo Neptune 3 Plus'
        if '3 pro' in lower:
            return 'Elegoo Neptune 3 Pro'
        if '3' in lower:
            return 'Elegoo Neptune 3'
        return 'Elegoo Neptune'

    # Familia Anycubic
    if 'anycubic' in lower or 'kobra' in lower or 'photon' in lower:
        if 'kobra 3' in lower:
            return 'Anycubic Kobra 3'
        if 'kobra 2 max' in lower:
            return 'Anycubic Kobra 2 Max'
        if 'kobra 2 plus' in lower:
            return 'Anycubic Kobra 2 Plus'
        if 'kobra 2 pro' in lower:
            return 'Anycubic Kobra 2 Pro'
        if 'kobra 2 neo' in lower:
            return 'Anycubic Kobra 2 Neo'
        if 'kobra 2' in lower:
            return 'Anycubic Kobra 2'
        if 'photon mono m5' in lower:
            return 'Anycubic Photon Mono M5s'
        if 'photon' in lower:
            return 'Anycubic Photon'
        if 'kobra' in lower:
            return 'Anycubic Kobra'
        return 'Anycubic'

    # Flashforge & Qidi
    if 'flashforge' in lower or 'adventurer' in lower:
        if '5m pro' in lower:
            return 'Flashforge Adventurer 5M Pro'
        return 'Flashforge Adventurer 5M'
    if 'qidi' in lower:
        if 'q1 pro' in lower or 'q1' in lower:
            return 'Qidi Q1 Pro'
        if 'x-max' in lower or 'xmax' in lower:
            return 'Qidi X-Max 3'
        if 'x-plus' in lower or 'xplus' in lower:
            return 'Qidi X-Plus 3'
        return 'Qidi Tech'

    # Sovol
    if 'sovol' in lower or 'sv08' in lower or 'sv07' in lower or 'sv06' in lower:
        if 'sv08' in lower:
            return 'Sovol SV08'
        if 'sv07 plus' in lower:
            return 'Sovol SV07 Plus'
        if 'sv07' in lower:
            return 'Sovol SV07'
        if 'sv06 plus' in lower:
            return 'Sovol SV06 Plus'
        if 'sv06' in lower:
            return 'Sovol SV06'
        return 'Sovol'

    # Artillery
    if 'artillery' in lower or 'sidewinder' in lower or 'genius' in lower:
        if 'x4 pro' in lower:
            return 'Artillery Sidewinder X4 Pro'
        if 'x4 plus' in lower:
            return 'Artillery Sidewinder X4 Plus'
        if 'x4' in lower:
            return 'Artillery Sidewinder X4'
        if 'x2' in lower:
            return 'Artillery Sidewinder X2'
        if 'genius pro' in lower:
            return 'Artillery Genius Pro'
        if 'genius' in lower:
            return 'Artillery Genius'
        return 'Artillery Sidewinder'

    # Kingroon
    if 'kingroon' in lower or 'kp3s' in lower or 'klp1' in lower:
        if 'kp3s pro v2' in lower:
            return 'Kingroon KP3S Pro V2'
        if 'kp3s pro' in lower:
            return 'Kingroon KP3S Pro'
        if 'klp1' in lower:
            return 'Kingroon KLP1'
        return 'Kingroon KP3S Pro'

    # Prusa & Voron
    if 'prusa' in lower:
        if 'mk4' in lower:
            return 'Prusa MK4'
        if 'xl' in lower:
            return 'Prusa XL'
        if 'mini' in lower:
            return 'Prusa MINI+'
        return 'Prusa MK3S+'
    if 'voron' in lower:
        if 'trident' in lower:
            return 'Voron Trident'
        if '0.2' in lower or 'v0' in lower:
            return 'Voron 0.2'
        return 'Voron 2.4'

    # Formateo capitalizado limpio para modelos personalizados
    words = raw_name.strip().split()
    return " ".join(w.capitalize() for w in words)

def extract_printer_counts_from_clients(cur):
    cur.execute("SELECT printer_model FROM clients WHERE printer_model IS NOT NULL AND printer_model != ''")
    printer_counts = {}
    for row in cur.fetchall():
        raw_val = row[0]
        if not raw_val:
            continue
        for item in re.split(r'[,;\n]+', raw_val):
            item = item.strip()
            if not item:
                continue
            qty = 1
            clean_name = item
            m_paren = re.search(r'\(x?(\d+)\)', item, re.IGNORECASE)
            if m_paren:
                qty = int(m_paren.group(1))
                clean_name = re.sub(r'\(x?\d+\)', '', item).strip()
            else:
                m_prefix = re.match(r'^(\d+)\s*x\s*(.*)$', item, re.IGNORECASE)
                if m_prefix:
                    qty = int(m_prefix.group(1))
                    clean_name = m_prefix.group(2).strip()
            
            canonical = canonicalize_printer_model(clean_name)
            if canonical:
                printer_counts[canonical] = printer_counts.get(canonical, 0) + qty
    
    sorted_list = sorted(printer_counts.items(), key=lambda x: x[1], reverse=True)[:12]
    return [{"model": k, "count": v} for k, v in sorted_list]

class SyntraCRMHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def address_string(self):
        # Desactivar resolucion DNS inversa lenta en Windows
        return self.client_address[0]

    def _send_json(self, data, status=200):
        payload = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(payload)

    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", "0")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Content-Length", "0")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/favicon.ico":
            self.send_response(204)
            self.send_header("Connection", "close")
            self.end_headers()
            return
        elif path == "/api/public/catalog":
            self.handle_get_public_catalog()
        elif path == "/api/bootstrap":
            self.handle_get_bootstrap()
        elif path == "/api/stats":
            self.handle_get_stats()
        elif path == "/api/products":
            self.handle_get_products()
        elif path == "/api/clients":
            self.handle_get_clients()
        elif path == "/api/sales":
            self.handle_get_sales()
        elif path == "/api/requests":
            self.handle_get_requests()
        elif path == "/api/state":
            self.handle_get_state()
        elif path == "/api/verify-reference":
            self.handle_get_verify_reference(parsed.query)
        elif path == "/api/suppliers":
            self.handle_get_suppliers()
        elif path == "/api/supplier-invoices":
            self.handle_get_supplier_invoices()
        elif path == "/api/inventory/kardex":
            self.handle_get_product_kardex(parsed.query)
        elif path == "/api/clients/statement":
            self.handle_get_client_statement(parsed.query)
        elif path == "/api/backup/download":
            self.handle_download_backup()
        elif path == "/api/affiliates":
            self.handle_get_affiliates()
        elif path == "/api/affiliates/payouts":
            self.handle_get_affiliate_payouts()
        elif path == "/api/affiliates/commissions":
            self.handle_get_affiliate_commissions()
        else:
            self.serve_static(path)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        path = parsed.path
        params = parse_qs(parsed.query)
        item_id = int(params.get("id", [0])[0]) if params.get("id") else None

        if path == "/api/sales":
            self.handle_delete_sale(item_id)
        elif path == "/api/clients":
            self.handle_delete_client(item_id)
        elif path == "/api/requests":
            self.handle_delete_request(item_id)
        elif path == "/api/suppliers":
            self.handle_delete_supplier(item_id)
        else:
            self._send_json({"error": "Ruta no encontrada"}, 404)

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        length = int(self.headers.get("Content-Length", 0))
        raw_bytes = self.rfile.read(length) if length > 0 else b""
        try:
            decoded = raw_bytes.decode("utf-8")
        except UnicodeDecodeError:
            decoded = raw_bytes.decode("latin-1", errors="replace")
        body = json.loads(decoded) if decoded else {}

        if path == "/api/auth/login":
            self.handle_post_auth_login(body)
        elif path == "/api/public/order":
            self.handle_post_public_order(body)
        elif path == "/api/sync-web":
            self.handle_sync_web()
        elif path == "/api/clients":
            self.handle_post_client(body)
        elif path == "/api/clients/delete":
            self.handle_delete_client(body.get("id"))
        elif path == "/api/sales":
            self.handle_post_sale(body)
        elif path == "/api/sales/delete":
            self.handle_delete_sale(body.get("id"))
        elif path == "/api/sales/reset":
            self.handle_reset_sales()
        elif path == "/api/sales/shipping":
            self.handle_post_sale_shipping(body)
        elif path == "/api/products":
            self.handle_post_product(body)
        elif path == "/api/requests":
            self.handle_post_request(body)
        elif path == "/api/requests/delete":
            self.handle_delete_request(body.get("id"))
        elif path == "/api/requests/status":
            self.handle_post_request_status(body)
        elif path == "/api/state":
            self.handle_post_state(body)
        elif path == "/api/whatsapp/sync":
            self.handle_whatsapp_sync()
        elif path == "/api/expenses":
            self.handle_post_expense(body)
        elif path == "/api/expenses/delete":
            self.handle_delete_expense(body.get("id"))
        elif path == "/api/sales/payment":
            self.handle_post_sale_payment(body)
        elif path == "/api/inventory/adjust":
            self.handle_post_inventory_adjust(body)
        elif path == "/api/suppliers":
            self.handle_post_supplier(body)
        elif path == "/api/suppliers/delete":
            self.handle_delete_supplier(body.get("id"))
        elif path == "/api/supplier-invoices":
            self.handle_post_supplier_invoice(body)
        elif path == "/api/supplier-invoices/delete":
            self.handle_delete_supplier_invoice(body.get("id"))
        elif path == "/api/supplier-payments":
            self.handle_post_supplier_payment(body)
        elif path == "/api/affiliates":
            self.handle_post_affiliate(body)
        elif path == "/api/affiliates/delete":
            self.handle_delete_affiliate(body.get("id"))
        elif path == "/api/affiliates/payout":
            self.handle_post_affiliate_payout(body)
        elif path == "/api/affiliates/payout/delete":
            self.handle_delete_affiliate_payout(body.get("id"))
        else:
            self._send_json({"error": "Ruta no encontrada"}, 404)

    def handle_post_auth_login(self, body):
        role = body.get("role", "staff")
        pin = str(body.get("pin", "")).strip()
        if role == "admin" and pin == ADMIN_PIN:
            self._send_json({
                "status": "ok", 
                "role": "admin", 
                "name": "Administrador General (Syntra Master)", 
                "can_delete": True, 
                "see_costs": True
            })
        elif role == "staff" and pin == STAFF_PIN:
            self._send_json({
                "status": "ok", 
                "role": "staff", 
                "name": "Personal de Ventas & Almacén", 
                "can_delete": False, 
                "see_costs": False
            })
        else:
            self._send_json({"status": "error", "error": "PIN de seguridad incorrecto"}, 401)

    def handle_get_bootstrap(self):
        conn = get_db()
        cur = conn.cursor()

        # 1. Stats
        cur.execute("SELECT COALESCE(SUM(total_price), 0), COALESCE(SUM(net_profit), 0), COUNT(*) FROM sales")
        total_rev, total_profit, sales_count = cur.fetchone()

        cur.execute("SELECT COUNT(*), COALESCE(SUM(current_stock), 0), COALESCE(SUM(current_stock * cost_warehouse), 0), COALESCE(SUM(current_stock * pvp_usd), 0), COALESCE(SUM(current_stock * COALESCE(pvp_cash_usd, pvp_usd)), 0) FROM products")
        prod_count, total_stock, inv_cost, inv_pvp, inv_pvp_cash = cur.fetchone()

        cur.execute("SELECT COUNT(*) FROM clients")
        client_count = cur.fetchone()[0]

        cur.execute("SELECT COUNT(*) FROM product_requests WHERE status != 'Atendido'")
        pending_requests_count = cur.fetchone()[0]

        printers = extract_printer_counts_from_clients(cur)

        cur.execute("SELECT materials_interest FROM clients WHERE materials_interest IS NOT NULL AND materials_interest != ''")
        mat_counts = {}
        for row in cur.fetchall():
            for m in [x.strip() for x in row[0].split(",")]:
                if m:
                    mat_counts[m] = mat_counts.get(m, 0) + 1
        materials = [{"material": k, "count": v} for k, v in sorted(mat_counts.items(), key=lambda x: x[1], reverse=True)[:6]]

        cur.execute("SELECT location, COUNT(*) as c FROM clients WHERE location IS NOT NULL AND location != '' GROUP BY location ORDER BY c DESC LIMIT 6")
        locations = [{"location": row[0], "count": row[1]} for row in cur.fetchall()]

        cur.execute("""
        SELECT s.*, c.name as client_name, c.phone as client_phone, c.location as client_location, c.printer_model as client_printer, p.name as product_name, a.name as affiliate_name, a.code as affiliate_code
        FROM sales s
        LEFT JOIN clients c ON s.client_id = c.id
        LEFT JOIN products p ON s.product_id = p.id
        LEFT JOIN affiliates a ON s.affiliate_id = a.id
        ORDER BY s.date DESC LIMIT 5
        """)
        recent_sales = [dict(row) for row in cur.fetchall()]

        # Gastos y Finanzas Operativas
        cur.execute("CREATE TABLE IF NOT EXISTS expenses (id INTEGER PRIMARY KEY AUTOINCREMENT, category TEXT, amount_usd REAL, amount_bs REAL, bcv_rate REAL, description TEXT, payment_method TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cur.execute("SELECT * FROM expenses ORDER BY date DESC")
        expenses = [dict(row) for row in cur.fetchall()]
        cur.execute("SELECT COALESCE(SUM(amount_usd), 0) FROM expenses")
        total_expenses = float(cur.fetchone()[0])

        # Cuentas por Cobrar (CxC / Ventas a Crédito)
        cur.execute("SELECT COALESCE(SUM(balance_due), 0), COUNT(*) FROM sales WHERE payment_status != 'PAGADO'")
        total_cxc, pending_credit_count = cur.fetchone()

        # Ajustes y Mermas de Inventario
        cur.execute("CREATE TABLE IF NOT EXISTS inventory_adjustments (id INTEGER PRIMARY KEY AUTOINCREMENT, product_id INTEGER, quantity INTEGER, reason TEXT, notes TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cur.execute("""
        SELECT a.*, p.name as product_name 
        FROM inventory_adjustments a 
        LEFT JOIN products p ON a.product_id = p.id 
        ORDER BY a.date DESC
        """)
        adjustments = [dict(row) for row in cur.fetchall()]

        # Historial de Abonos
        cur.execute("CREATE TABLE IF NOT EXISTS payment_records (id INTEGER PRIMARY KEY AUTOINCREMENT, sale_id INTEGER, amount_usd REAL, amount_bs REAL, payment_method TEXT, reference TEXT, notes TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cur.execute("""
        SELECT pr.*, s.client_id, c.name as client_name
        FROM payment_records pr
        LEFT JOIN sales s ON pr.sale_id = s.id
        LEFT JOIN clients c ON s.client_id = c.id
        ORDER BY pr.date DESC
        """)
        payments = [dict(row) for row in cur.fetchall()]

        # Cuentas por Pagar (CxP a Proveedores & Embarques)
        cur.execute("CREATE TABLE IF NOT EXISTS suppliers (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT, contact_name TEXT, phone TEXT, email TEXT, country TEXT, notes TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cur.execute("CREATE TABLE IF NOT EXISTS supplier_invoices (id INTEGER PRIMARY KEY AUTOINCREMENT, supplier_id INTEGER NOT NULL, invoice_number TEXT, description TEXT, total_amount_usd REAL NOT NULL, amount_paid REAL DEFAULT 0.0, balance_due REAL NOT NULL, due_date TEXT, payment_status TEXT DEFAULT 'PENDIENTE', category TEXT, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cur.execute("CREATE TABLE IF NOT EXISTS supplier_payments (id INTEGER PRIMARY KEY AUTOINCREMENT, invoice_id INTEGER NOT NULL, amount_usd REAL NOT NULL, amount_bs REAL, payment_method TEXT, reference TEXT, notes TEXT, date TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

        cur.execute("""
        SELECT si.*, s.name as supplier_name, s.category as supplier_category, s.country as supplier_country, s.phone as supplier_phone
        FROM supplier_invoices si
        LEFT JOIN suppliers s ON si.supplier_id = s.id
        ORDER BY si.created_at DESC
        """)
        supplier_invoices = [dict(row) for row in cur.fetchall()]

        cur.execute("SELECT * FROM suppliers ORDER BY name ASC")
        suppliers = [dict(row) for row in cur.fetchall()]

        cur.execute("SELECT * FROM supplier_payments ORDER BY date DESC")
        supplier_payments = [dict(row) for row in cur.fetchall()]

        cur.execute("SELECT COALESCE(SUM(balance_due), 0), COUNT(*) FROM supplier_invoices WHERE payment_status != 'PAGADO'")
        total_cxp, pending_supplier_count = cur.fetchone()

        # P&L Formal (Estado de Resultados Completo)
        cur.execute("""
        SELECT COALESCE(SUM(si.quantity * p.cost_warehouse), 0)
        FROM sale_items si
        LEFT JOIN products p ON si.product_id = p.id
        """)
        cogs = float(cur.fetchone()[0])
        if cogs == 0.0:
            cur.execute("""
            SELECT COALESCE(SUM(s.quantity * p.cost_warehouse), 0)
            FROM sales s
            LEFT JOIN products p ON s.product_id = p.id
            """)
            cogs = float(cur.fetchone()[0])
        gross_profit = total_rev - cogs
        gross_margin_pct = (gross_profit / total_rev * 100.0) if total_rev > 0 else 0.0

        cur.execute("""
        SELECT COALESCE(SUM(a.quantity * p.cost_warehouse), 0)
        FROM inventory_adjustments a
        LEFT JOIN products p ON a.product_id = p.id
        """)
        inventory_loss_usd = float(cur.fetchone()[0])

        real_operating_profit = gross_profit - total_expenses - inventory_loss_usd
        real_operating_margin_pct = (real_operating_profit / total_rev * 100.0) if total_rev > 0 else 0.0

        stats = {
            "total_revenue": total_rev,
            "total_profit": total_profit,
            "cogs": cogs,
            "gross_profit": gross_profit,
            "gross_margin_pct": gross_margin_pct,
            "total_expenses": total_expenses,
            "inventory_loss_usd": inventory_loss_usd,
            "real_net_profit": real_operating_profit,
            "real_margin_pct": real_operating_margin_pct,
            "total_cxc": total_cxc,
            "pending_credit_sales_count": pending_credit_count,
            "total_cxp": total_cxp,
            "pending_supplier_invoices_count": pending_supplier_count,
            "sales_count": sales_count,
            "total_stock": total_stock,
            "total_clients": client_count,
            "pending_requests_count": pending_requests_count,
            "inventory_cost_value": inv_cost,
            "inventory_pvp_value": inv_pvp,
            "inventory_pvp_cash_value": inv_pvp_cash,
            "inventory_pvp_cash_value": inv_pvp_cash,
            "printers_breakdown": printers,
            "materials_breakdown": materials,
            "locations_breakdown": locations,
            "recent_sales": recent_sales
        }

        # 2. Products
        cur.execute("SELECT * FROM products ORDER BY category, name")
        products = [dict(row) for row in cur.fetchall()]

        # 3. Clients
        cur.execute("""
        SELECT c.*, COALESCE(SUM(s.total_price), 0) as total_spent, COUNT(s.id) as purchases_count
        FROM clients c
        LEFT JOIN sales s ON c.id = s.client_id
        GROUP BY c.id
        ORDER BY c.created_at DESC
        """)
        clients = [dict(row) for row in cur.fetchall()]

        # 4. Sales
        cur.execute("""
        SELECT s.*, c.name as client_name, c.phone as client_phone, c.location as client_location, c.printer_model as client_printer, p.name as product_name, p.category as product_category, a.name as affiliate_name, a.code as affiliate_code
        FROM sales s
        LEFT JOIN clients c ON s.client_id = c.id
        LEFT JOIN products p ON s.product_id = p.id
        LEFT JOIN affiliates a ON s.affiliate_id = a.id
        ORDER BY s.date DESC
        """)
        sales = [dict(row) for row in cur.fetchall()]
        if sales:
            sale_ids = [s["id"] for s in sales]
            q_marks = ",".join("?" for _ in sale_ids)
            cur.execute(f"""
                SELECT si.*, p.name as product_name, p.category as product_category, p.color as product_color, p.sku as product_sku
                FROM sale_items si
                LEFT JOIN products p ON si.product_id = p.id
                WHERE si.sale_id IN ({q_marks})
            """, sale_ids)
            items_by_sale = {}
            for item_row in cur.fetchall():
                it = dict(item_row)
                items_by_sale.setdefault(it["sale_id"], []).append(it)
            for s in sales:
                s["items"] = items_by_sale.get(s["id"], [])
        else:
            for s in sales:
                s["items"] = []

        # 5. Requests
        cur.execute("""
        SELECT r.*, c.name as client_name_rel, c.phone as client_phone_rel
        FROM product_requests r
        LEFT JOIN clients c ON r.client_id = c.id
        ORDER BY 
            CASE r.priority 
                WHEN 'Alta' THEN 1 
                WHEN 'Media' THEN 2 
                ELSE 3 
            END,
            r.created_at DESC
        """)
        requests = [dict(row) for row in cur.fetchall()]

        # Affiliates & Payouts
        cur.execute("""
        SELECT a.*,
               COUNT(s.id) as sales_count,
               COALESCE(SUM(s.quantity), 0) as total_volume_units,
               COALESCE(SUM(s.total_price), 0) as total_sales_usd,
               COALESCE(SUM(s.commission_amount), 0) as total_commission_usd,
               COALESCE((SELECT SUM(ap.amount_usd) FROM affiliate_payouts ap WHERE ap.affiliate_id = a.id), 0) as total_payout_usd,
               (COALESCE(SUM(s.commission_amount), 0) - COALESCE((SELECT SUM(ap.amount_usd) FROM affiliate_payouts ap WHERE ap.affiliate_id = a.id), 0)) as balance_due
        FROM affiliates a
        LEFT JOIN sales s ON a.id = s.affiliate_id
        GROUP BY a.id
        ORDER BY total_sales_usd DESC, a.created_at DESC
        """)
        affiliates = [dict(row) for row in cur.fetchall()]

        cur.execute("""
        SELECT ap.*, a.name as affiliate_name, a.code as affiliate_code
        FROM affiliate_payouts ap
        LEFT JOIN affiliates a ON ap.affiliate_id = a.id
        ORDER BY ap.date DESC
        """)
        affiliate_payouts = [dict(row) for row in cur.fetchall()]

        # 6. State
        cur.execute("CREATE TABLE IF NOT EXISTS dashboard_state (id TEXT PRIMARY KEY, state_json TEXT, updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")
        cur.execute("SELECT state_json, updated_at FROM dashboard_state WHERE id = 'main'")
        state_row = cur.fetchone()
        state_data = {}
        if state_row and state_row["state_json"]:
            try:
                state_data = json.loads(state_row["state_json"])
            except:
                pass

        conn.close()

        self._send_json({
            "stats": stats,
            "products": products,
            "clients": clients,
            "sales": sales,
            "requests": requests,
            "expenses": expenses,
            "adjustments": adjustments,
            "payments": payments,
            "suppliers": suppliers,
            "supplier_invoices": supplier_invoices,
            "supplier_payments": supplier_payments,
            "affiliates": affiliates,
            "affiliate_payouts": affiliate_payouts,
            "state": state_data
        })

    def handle_get_stats(self):
        conn = get_db()
        cur = conn.cursor()

        # Ventas y ganancias
        cur.execute("SELECT COALESCE(SUM(total_price), 0), COALESCE(SUM(net_profit), 0), COUNT(*) FROM sales")
        total_rev, total_profit, sales_count = cur.fetchone()

        # Inventario
        cur.execute("SELECT COUNT(*), COALESCE(SUM(current_stock), 0), COALESCE(SUM(current_stock * cost_warehouse), 0), COALESCE(SUM(current_stock * pvp_usd), 0), COALESCE(SUM(current_stock * COALESCE(pvp_cash_usd, pvp_usd)), 0) FROM products")
        prod_count, total_stock, inv_cost, inv_pvp, inv_pvp_cash = cur.fetchone()

        # Clientes
        cur.execute("SELECT COUNT(*) FROM clients")
        client_count = cur.fetchone()[0]

        # Distribución de impresoras (normalizada y canónica)
        printers = extract_printer_counts_from_clients(cur)

        # Distribución de materiales
        cur.execute("SELECT materials_interest FROM clients WHERE materials_interest IS NOT NULL AND materials_interest != ''")
        mat_counts = {}
        for row in cur.fetchall():
            for m in [x.strip() for x in row[0].split(",")]:
                if m:
                    mat_counts[m] = mat_counts.get(m, 0) + 1
        materials = [{"material": k, "count": v} for k, v in sorted(mat_counts.items(), key=lambda x: x[1], reverse=True)[:6]]

        # Ciudades
        cur.execute("SELECT location, COUNT(*) as c FROM clients WHERE location IS NOT NULL AND location != '' GROUP BY location ORDER BY c DESC LIMIT 5")
        locations = [{"location": row[0], "count": row[1]} for row in cur.fetchall()]

        # Ventas recientes
        cur.execute("""
        SELECT s.id, c.name as client_name, p.name as product_name, s.quantity, s.total_price, s.net_profit, s.date 
        FROM sales s 
        LEFT JOIN clients c ON s.client_id = c.id 
        LEFT JOIN products p ON s.product_id = p.id 
        ORDER BY s.date DESC LIMIT 5
        """)
        recent_sales = [dict(row) for row in cur.fetchall()]

        # Solicitudes de nuevo stock (Wishlist / Radar)
        cur.execute("SELECT COUNT(*) FROM product_requests WHERE status NOT IN ('Stock Recibido', 'Descartado')")
        pending_requests_count = cur.fetchone()[0]

        conn.close()
        self._send_json({
            "total_revenue": total_rev,
            "total_profit": total_profit,
            "sales_count": sales_count,
            "total_stock": total_stock,
            "total_clients": client_count,
            "pending_requests_count": pending_requests_count,
            "inventory_cost_value": inv_cost,
            "inventory_pvp_value": inv_pvp,
            "inventory_pvp_cash_value": inv_pvp_cash,
            "inventory_pvp_cash_value": inv_pvp_cash,
            "printers_breakdown": printers,
            "materials_breakdown": materials,
            "locations_breakdown": locations,
            "recent_sales": recent_sales
        })

    def handle_get_products(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products ORDER BY category, name")
        products = [dict(row) for row in cur.fetchall()]
        conn.close()
        self._send_json(products)

    def handle_get_clients(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        SELECT c.*, 
               COALESCE(SUM(s.total_price), 0) as total_spent,
               COUNT(s.id) as purchases_count
        FROM clients c
        LEFT JOIN sales s ON c.id = s.client_id
        GROUP BY c.id
        ORDER BY c.created_at DESC
        """)
        clients = [dict(row) for row in cur.fetchall()]
        conn.close()
        self._send_json(clients)

    def handle_get_sales(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        SELECT s.*, c.name as client_name, c.phone as client_phone, c.location as client_location, c.printer_model as client_printer, p.name as product_name, p.category as product_category, a.name as affiliate_name, a.code as affiliate_code
        FROM sales s
        LEFT JOIN clients c ON s.client_id = c.id
        LEFT JOIN products p ON s.product_id = p.id
        LEFT JOIN affiliates a ON s.affiliate_id = a.id
        ORDER BY s.date DESC
        """)
        sales = [dict(row) for row in cur.fetchall()]
        if sales:
            sale_ids = [s["id"] for s in sales]
            q_marks = ",".join("?" for _ in sale_ids)
            cur.execute(f"""
                SELECT si.*, p.name as product_name, p.category as product_category, p.color as product_color, p.sku as product_sku
                FROM sale_items si
                LEFT JOIN products p ON si.product_id = p.id
                WHERE si.sale_id IN ({q_marks})
            """, sale_ids)
            items_by_sale = {}
            for item_row in cur.fetchall():
                it = dict(item_row)
                items_by_sale.setdefault(it["sale_id"], []).append(it)
            for s in sales:
                s["items"] = items_by_sale.get(s["id"], [])
        conn.close()
        self._send_json(sales)

    def handle_post_client(self, body):
        conn = get_db()
        cur = conn.cursor()
        raw_id = body.get("id")
        c_id = int(raw_id) if raw_id and str(raw_id).isdigit() else None
        name = body.get("name", "").strip()
        phone = body.get("phone", "").strip()
        location = body.get("location", "").strip()
        printer = body.get("printer_model", "").strip()
        materials = body.get("materials_interest", "").strip()
        status = body.get("lead_status", "Prospecto")
        pipeline = body.get("pipeline_stage", "Nuevo Prospecto")
        notes = body.get("notes", "").strip()

        if not name or not phone:
            self._send_json({"error": "Nombre y teléfono requeridos"}, 400)
            conn.close()
            return

        if c_id:
            cur.execute("""
            UPDATE clients SET name=?, phone=?, location=?, printer_model=?, materials_interest=?, lead_status=?, pipeline_stage=?, notes=?
            WHERE id=?
            """, (name, phone, location, printer, materials, status, pipeline, notes, c_id))
        else:
            cur.execute("""
            INSERT INTO clients (name, phone, location, printer_model, materials_interest, lead_status, pipeline_stage, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(phone) DO UPDATE SET
                name=excluded.name,
                location=excluded.location,
                printer_model=excluded.printer_model,
                materials_interest=excluded.materials_interest,
                lead_status=excluded.lead_status,
                pipeline_stage=excluded.pipeline_stage,
                notes=excluded.notes
            """, (name, phone, location, printer, materials, status, pipeline, notes))

        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Cliente guardado con éxito"})

    def handle_post_sale(self, body):
        conn = get_db()
        cur = conn.cursor()
        
        client_id = body.get("client_id")
        payment_method = body.get("payment_method", "Zelle / Divisas")
        delivery_method = body.get("delivery_method", "Retiro en Tienda / Local")
        tracking_number = body.get("tracking_number", "")
        shipping_carrier = body.get("shipping_carrier", "")
        if not shipping_carrier:
            if "MRW" in delivery_method: shipping_carrier = "MRW"
            elif "Tealca" in delivery_method: shipping_carrier = "Tealca"
            elif "Zoom" in delivery_method: shipping_carrier = "Zoom"
            elif "Delivery" in delivery_method: shipping_carrier = "Delivery Local"
            else: shipping_carrier = "Retiro en Almacén"
        shipping_status = body.get("shipping_status", "Preparando en Almacén")
        shipping_agency = body.get("shipping_agency", "")
        notes = body.get("notes", "")

        # Procesar lista de ítems (Multi-ítem o ítem simple)
        raw_items = body.get("items")
        cart_items = []
        if raw_items and isinstance(raw_items, list) and len(raw_items) > 0:
            for item in raw_items:
                pid = int(item.get("product_id", 0))
                qty = int(item.get("quantity", 1))
                if pid and qty > 0:
                    cart_items.append({"product_id": pid, "quantity": qty, "unit_price": item.get("unit_price")})
        else:
            single_pid = body.get("product_id")
            if single_pid:
                cart_items.append({
                    "product_id": int(single_pid),
                    "quantity": int(body.get("quantity", 1)),
                    "unit_price": body.get("unit_price")
                })

        if not cart_items:
            self._send_json({"error": "Debe seleccionar al menos un producto"}, 400)
            conn.close()
            return

        # Validar existencias de stock de todos los productos del carrito
        processed_items = []
        total_price = 0.0
        total_cost = 0.0
        total_qty = 0

        for it in cart_items:
            cur.execute("SELECT * FROM products WHERE id=?", (it["product_id"],))
            prod = cur.fetchone()
            if not prod:
                self._send_json({"error": f"Producto con ID {it['product_id']} no encontrado"}, 404)
                conn.close()
                return

            if prod["current_stock"] < it["quantity"]:
                self._send_json({"error": f"Stock insuficiente para '{prod['name']}'. Disponible: {prod['current_stock']}"}, 400)
                conn.close()
                return

            u_price = float(it["unit_price"] if (it["unit_price"] is not None and str(it["unit_price"]).strip() != "") else prod["pvp_usd"])
            u_cost = float(prod["cost_warehouse"])
            item_tot = round(u_price * it["quantity"], 2)
            item_cost_tot = round(u_cost * it["quantity"], 2)
            item_profit = round(item_tot - item_cost_tot, 2)

            total_price += item_tot
            total_cost += item_cost_tot
            total_qty += it["quantity"]

            processed_items.append({
                "product_id": it["product_id"],
                "quantity": it["quantity"],
                "unit_price": u_price,
                "unit_cost": u_cost,
                "total_price": item_tot,
                "net_profit": item_profit,
                "name": prod["name"]
            })

        total_price = round(total_price, 2)
        total_cost = round(total_cost, 2)

        # Parámetros de afiliado / comisión diferenciada pro-divisa
        raw_aff_id = body.get("affiliate_id")
        affiliate_id = int(raw_aff_id) if (raw_aff_id and str(raw_aff_id).strip() != "") else None
        
        commission_amount = float(body.get("commission_amount") or 0.0)
        if affiliate_id and commission_amount == 0.0:
            is_currency = not ("Pago Móvil" in payment_method or "Transferencia" in payment_method)
            rate = 1.50 if is_currency else 1.25
            commission_amount = round(rate * total_qty, 2)

        commission_status = "PENDIENTE" if (affiliate_id and commission_amount > 0) else "SIN_COMISION"

        # Ganancia neta retenida por Syntra (descontando la comisión del afiliado)
        net_profit = max(0.0, round((total_price - total_cost) - commission_amount, 2))

        # Parámetros de crédito y pago mixto
        payment_status = body.get("payment_status", "PAGADO")
        raw_paid = body.get("amount_paid")
        if payment_status == "PAGADO" and (raw_paid is None or raw_paid == ""):
            amount_paid = total_price
        else:
            amount_paid = round(float(raw_paid or 0), 2)

        balance_due = max(0.0, round(total_price - amount_paid, 2))
        if balance_due <= 0.01:
            payment_status = "PAGADO"
            balance_due = 0.0
        elif amount_paid > 0:
            payment_status = "PARCIAL"
        else:
            payment_status = "PENDIENTE"

        due_date = body.get("due_date", "")
        payment_details = body.get("payment_details", "")
        reference = body.get("reference", "")

        primary_product_id = processed_items[0]["product_id"]
        avg_unit_price = round(total_price / total_qty, 2) if total_qty > 0 else 0.0
        avg_unit_cost = round(total_cost / total_qty, 2) if total_qty > 0 else 0.0

        # 1. Registrar venta consolidada
        cur.execute("""
        INSERT INTO sales (client_id, product_id, quantity, unit_price, unit_cost, total_price, net_profit, payment_method, delivery_method, tracking_number, notes, payment_status, amount_paid, balance_due, due_date, payment_details, affiliate_id, commission_amount, commission_status, shipping_carrier, shipping_status, shipping_agency)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (client_id, primary_product_id, total_qty, avg_unit_price, avg_unit_cost, total_price, net_profit, payment_method, delivery_method, tracking_number, notes, payment_status, amount_paid, balance_due, due_date, payment_details, affiliate_id, commission_amount, commission_status, shipping_carrier, shipping_status, shipping_agency))
        sale_id = cur.lastrowid

        # 2. Registrar cada ítem en sale_items y descontar stock individual
        for pit in processed_items:
            cur.execute("""
            INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, unit_cost, total_price, net_profit)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (sale_id, pit["product_id"], pit["quantity"], pit["unit_price"], pit["unit_cost"], pit["total_price"], pit["net_profit"]))
            
            cur.execute("UPDATE products SET current_stock = current_stock - ? WHERE id=?", (pit["quantity"], pit["product_id"]))

        # 3. Registrar abono inicial en payment_records SOLO SI es a crédito con abono parcial
        # (Para ventas de contado completo, la venta misma es el ingreso contable y evita duplicidad en cierre de caja)
        if balance_due > 0 and amount_paid > 0:
            cur.execute("""
            INSERT INTO payment_records (sale_id, amount_usd, payment_method, reference, notes)
            VALUES (?, ?, ?, ?, ?)
            """, (sale_id, amount_paid, payment_method, reference, "Abono inicial de crédito al registrar venta"))

        # 4. Actualizar estado del cliente a Comprador y etapa de pipeline
        if client_id:
            cur.execute("SELECT COUNT(*) FROM sales WHERE client_id=?", (client_id,))
            sales_count = cur.fetchone()[0]
            lead_st = "Comprador Recurrente" if sales_count > 1 else "Cliente Activo"
            cur.execute("UPDATE clients SET lead_status=?, pipeline_stage='Cliente Concretado' WHERE id=?", (lead_st, client_id))

        conn.commit()
        conn.close()

        # Sincronización automática de inventario con catálogo web
        try:
            from sync_crm_to_web import sync_crm_database_to_manifest
            sync_crm_database_to_manifest()
        except Exception as _e_sync:
            print(f"[!] Sincronización Web tras venta: {_e_sync}")
        self._send_json({
            "status": "ok", 
            "message": f"Venta #{sale_id} registrada ({len(processed_items)} ítems, {total_qty} unds) e inventario descontado exitosamente",
            "sale_id": sale_id,
            "net_profit": net_profit,
            "total_price": total_price,
            "items_count": len(processed_items)
        })

    def handle_post_product(self, body):
        conn = get_db()
        cur = conn.cursor()
        p_id = body.get("id")
        name = body.get("name")
        category = body.get("category")
        stock_change = int(body.get("stock_change", 0))
        current_stock = body.get("current_stock")
        initial_stock = body.get("initial_stock")
        cost_warehouse = body.get("cost_warehouse")
        pvp_usd = body.get("pvp_usd")
        pvp_cash_usd = body.get("pvp_cash_usd")

        if p_id:
            cur.execute("SELECT * FROM products WHERE id=?", (p_id,))
            prod = cur.fetchone()
            if prod:
                n_name = name.strip() if name is not None else prod["name"]
                n_cat = category.strip() if category is not None else prod["category"]
                
                if current_stock is not None:
                    n_curr = int(current_stock)
                elif stock_change != 0:
                    n_curr = int(prod["current_stock"]) + stock_change
                else:
                    n_curr = int(prod["current_stock"])
                    
                n_init = int(initial_stock) if initial_stock is not None else int(prod["initial_stock"])
                n_cost = float(cost_warehouse) if cost_warehouse is not None else float(prod["cost_warehouse"])
                n_pvp = float(pvp_usd) if pvp_usd is not None else float(prod["pvp_usd"])
                n_pvp_cash = float(pvp_cash_usd) if pvp_cash_usd is not None else (float(prod["pvp_cash_usd"]) if ("pvp_cash_usd" in prod.keys() and prod["pvp_cash_usd"] is not None) else n_pvp)
                
                n_margin = round(((n_pvp_cash - n_cost) / n_pvp_cash) * 100, 1) if n_pvp_cash > 0 else 0.0
                n_profit = round(n_pvp_cash - n_cost, 2)
                
                min_stock = int(body.get("min_stock", prod["min_stock"] if "min_stock" in prod.keys() else 10))
                n_sku = str(body.get("sku", prod["sku"] if "sku" in prod.keys() else "")).strip()
                n_color = str(body.get("color", prod["color"] if "color" in prod.keys() else "")).strip()
                n_mat_type = str(body.get("material_type", prod["material_type"] if "material_type" in prod.keys() else "")).strip()
                cur.execute("""
                UPDATE products 
                SET name=?, category=?, current_stock=?, initial_stock=?, cost_warehouse=?, pvp_usd=?, pvp_cash_usd=?, margin_pct=?, net_profit_unit=?, min_stock=?, sku=?, color=?, material_type=?
                WHERE id=?
                """, (n_name, n_cat, n_curr, n_init, n_cost, n_pvp, n_pvp_cash, n_margin, n_profit, min_stock, n_sku, n_color, n_mat_type, p_id))
        else:
            n_name = (name or "Nuevo Material").strip()
            n_cat = (category or "Filamento").strip()
            n_curr = int(current_stock or 0)
            n_init = int(initial_stock or n_curr)
            n_cost = float(cost_warehouse or 0)
            n_pvp = float(pvp_usd or 0)
            n_pvp_cash = float(pvp_cash_usd or n_pvp)
            n_margin = round(((n_pvp_cash - n_cost) / n_pvp_cash) * 100, 1) if n_pvp_cash > 0 else 0.0
            n_profit = round(n_pvp_cash - n_cost, 2)
            min_stock = int(body.get("min_stock", 10))
            n_sku = str(body.get("sku", "")).strip()
            n_color = str(body.get("color", "")).strip()
            n_mat_type = str(body.get("material_type", "")).strip()
            cur.execute("""
            INSERT INTO products (name, category, initial_stock, current_stock, cost_warehouse, pvp_usd, pvp_cash_usd, margin_pct, net_profit_unit, min_stock, sku, color, material_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (n_name, n_cat, n_init, n_curr, n_cost, n_pvp, n_pvp_cash, n_margin, n_profit, min_stock, n_sku, n_color, n_mat_type))

        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Producto guardado exitosamente"})

    def handle_get_state(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS dashboard_state (
            id TEXT PRIMARY KEY,
            state_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        cur.execute("SELECT state_json, updated_at FROM dashboard_state WHERE id = 'main'")
        row = cur.fetchone()
        conn.close()
        if row and row["state_json"]:
            try:
                state_data = json.loads(row["state_json"])
                self._send_json({"status": "ok", "state": state_data, "updated_at": row["updated_at"]})
            except Exception as e:
                self._send_json({"status": "ok", "state": {}, "error": str(e)})
        else:
            self._send_json({"status": "ok", "state": {}, "updated_at": None})

    def handle_post_state(self, body):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS dashboard_state (
            id TEXT PRIMARY KEY,
            state_json TEXT,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Recuperar estado previo para fusión segura multi-sesión
        cur.execute("SELECT state_json FROM dashboard_state WHERE id = 'main'")
        row = cur.fetchone()
        merged_state = {}
        if row and row["state_json"]:
            try:
                merged_state = json.loads(row["state_json"])
            except Exception:
                merged_state = {}

        incoming = body.get("state", body)
        if isinstance(incoming, dict):
            # Fusión inteligente de claves sin sobreescribir datos de otras sesiones
            for k, v in incoming.items():
                if v is not None:
                    merged_state[k] = v
        else:
            merged_state = incoming

        state_str = json.dumps(merged_state, ensure_ascii=False)
        cur.execute("""
        INSERT INTO dashboard_state (id, state_json, updated_at)
        VALUES ('main', ?, datetime('now', 'localtime'))
        ON CONFLICT(id) DO UPDATE SET
            state_json = excluded.state_json,
            updated_at = excluded.updated_at
        """, (state_str,))
        conn.commit()
        cur.execute("SELECT updated_at FROM dashboard_state WHERE id = 'main'")
        r = cur.fetchone()
        updated_at = r[0] if r else ""
        conn.close()
        self._send_json({"status": "ok", "message": "Configuración y estado sincronizados exitosamente sin colisión", "updated_at": updated_at, "state": merged_state})

    def handle_get_requests(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        SELECT r.*, c.name as client_name_rel, c.phone as client_phone_rel
        FROM product_requests r
        LEFT JOIN clients c ON r.client_id = c.id
        ORDER BY 
            CASE r.priority 
                WHEN 'Alta' THEN 1 
                WHEN 'Media' THEN 2 
                ELSE 3 
            END,
            r.created_at DESC
        """)
        requests = [dict(row) for row in cur.fetchall()]
        
        # Resumen estadístico
        cur.execute("SELECT COUNT(*), COUNT(DISTINCT item_name), COALESCE(SUM(quantity), 0), COALESCE(SUM(quantity * estimated_price), 0) FROM product_requests WHERE status NOT IN ('Stock Recibido', 'Descartado')")
        tot_req, unique_items, tot_qty, est_investment = cur.fetchone()
        
        conn.close()
        self._send_json({
            "requests": requests,
            "summary": {
                "total_pending": tot_req,
                "unique_items": unique_items,
                "total_units_demanded": tot_qty,
                "estimated_volume_usd": est_investment
            }
        })

    def handle_post_request(self, body):
        conn = get_db()
        cur = conn.cursor()
        client_id = body.get("client_id")
        client_name = body.get("client_name", "").strip()
        client_phone = body.get("client_phone", "").strip()
        item_name = body.get("item_name", "").strip()
        category = body.get("category", "Filamentos Especiales")
        quantity = int(body.get("quantity", 1))
        est_price = float(body.get("estimated_price", 0.0))
        priority = body.get("priority", "Media")
        notes = body.get("notes", "").strip()
        
        if not item_name:
            self._send_json({"error": "Nombre del ítem/material requerido"}, 400)
            conn.close()
            return
            
        if client_id and (not client_name or not client_phone):
            cur.execute("SELECT name, phone FROM clients WHERE id=?", (client_id,))
            row = cur.fetchone()
            if row:
                if not client_name: client_name = row["name"]
                if not client_phone: client_phone = row["phone"]
                
        cur.execute("""
        INSERT INTO product_requests (client_id, client_name, client_phone, item_name, category, quantity, estimated_price, priority, status, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pendiente para Próximo Pedido', ?)
        """, (client_id, client_name or "Cliente General", client_phone or "", item_name, category, quantity, est_price, priority, notes))
        
        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Solicitud de stock registrada en el Radar"})

    def handle_post_request_status(self, body):
        conn = get_db()
        cur = conn.cursor()
        req_id = body.get("id")
        new_status = body.get("status")
        
        if not req_id or not new_status:
            self._send_json({"error": "ID y nuevo estado requeridos"}, 400)
            conn.close()
            return
            
        cur.execute("UPDATE product_requests SET status=? WHERE id=?", (new_status, req_id))
        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Estado de solicitud actualizado"})

    def handle_delete_sale(self, sale_id):
        if not sale_id:
            self._send_json({"error": "ID de venta requerido"}, 400)
            return
        conn = get_db()
        cur = conn.cursor()
        
        # 1. Reponer stock al inventario desde sale_items si existe, o desde sales
        cur.execute("SELECT product_id, quantity FROM sale_items WHERE sale_id=?", (sale_id,))
        items = cur.fetchall()
        total_restored = 0
        if items:
            for it in items:
                cur.execute("UPDATE products SET current_stock = current_stock + ? WHERE id=?", (it["quantity"], it["product_id"]))
                total_restored += it["quantity"]
        else:
            cur.execute("SELECT product_id, quantity FROM sales WHERE id=?", (sale_id,))
            row = cur.fetchone()
            if row and row["product_id"]:
                cur.execute("UPDATE products SET current_stock = current_stock + ? WHERE id=?", (row["quantity"], row["product_id"]))
                total_restored += row["quantity"]

        cur.execute("SELECT client_id FROM sales WHERE id=?", (sale_id,))
        s_row = cur.fetchone()
        client_id = s_row["client_id"] if s_row else None
        
        # 2. Eliminar venta y sus dependencias asociadas
        cur.execute("DELETE FROM sale_items WHERE sale_id=?", (sale_id,))
        cur.execute("DELETE FROM payment_records WHERE sale_id=?", (sale_id,))
        cur.execute("DELETE FROM sales WHERE id=?", (sale_id,))
        
        # 3. Recalcular estado del cliente
        if client_id:
            cur.execute("SELECT COUNT(*) FROM sales WHERE client_id=?", (client_id,))
            remaining = cur.fetchone()[0]
            if remaining == 0:
                cur.execute("UPDATE clients SET lead_status='Prospecto', pipeline_stage='Nuevo Prospecto' WHERE id=?", (client_id,))
            elif remaining == 1:
                cur.execute("UPDATE clients SET lead_status='Cliente Activo', pipeline_stage='Cliente Concretado' WHERE id=?", (client_id,))
                
        conn.commit()
        conn.close()

        # Sincronización automática de inventario con catálogo web
        try:
            from sync_crm_to_web import sync_crm_database_to_manifest
            sync_crm_database_to_manifest()
        except Exception as _e_sync:
            print(f"[!] Sincronización Web tras eliminar venta: {_e_sync}")

        self._send_json({"status": "ok", "message": f"Venta #{sale_id} eliminada y {total_restored} unidades restituidas al inventario."})

    def handle_reset_sales(self):
        """Limpia todas las ventas de prueba y restablece el stock a su totalidad (1,750 unidades)"""
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM sales")
        cur.execute("DELETE FROM sale_items")
        cur.execute("DELETE FROM payment_records")
        cur.execute("DELETE FROM affiliate_payouts")
        cur.execute("UPDATE products SET current_stock = initial_stock")
        cur.execute("UPDATE clients SET lead_status='Prospecto', pipeline_stage='Nuevo Prospecto'")
        cur.execute("DELETE FROM sqlite_sequence WHERE name IN ('sales', 'sale_items', 'payment_records', 'affiliate_payouts')")
        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Panel limpiado a cero y stock restablecido a 1,750 unidades."})

    def handle_post_sale_shipping(self, body):
        sale_id = body.get("sale_id")
        if not sale_id:
            self._send_json({"error": "ID de venta requerido"}, 400)
            return

        carrier = body.get("shipping_carrier", "MRW")
        status = body.get("shipping_status", "En Tránsito")
        agency = body.get("shipping_agency", "")
        tracking = body.get("tracking_number", "")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        UPDATE sales 
        SET shipping_carrier=?, shipping_status=?, shipping_agency=?, tracking_number=?
        WHERE id=?
        """, (carrier, status, agency, tracking, sale_id))

        conn.commit()
        conn.close()
        self._send_json({
            "status": "ok",
            "message": f"Despacho de Venta #{sale_id} actualizado: {carrier} ({status})"
        })

    def handle_delete_client(self, client_id):
        if not client_id:
            self._send_json({"error": "ID de cliente requerido"}, 400)
            return
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM sales WHERE client_id=?", (client_id,))
        cur.execute("DELETE FROM product_requests WHERE client_id=?", (client_id,))
        cur.execute("DELETE FROM clients WHERE id=?", (client_id,))
        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": f"Cliente #{client_id} eliminado exitosamente."})

    def handle_delete_request(self, request_id):
        if not request_id:
            self._send_json({"error": "ID de solicitud requerido"}, 400)
            return
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM product_requests WHERE id=?", (request_id,))
        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": f"Solicitud #{request_id} eliminada del Radar."})

    def handle_whatsapp_sync(self):
        """Escanea contactos reales directamente de WhatsApp Web (IndexedDB) y actualiza el CRM"""
        try:
            from whatsapp_agent import WhatsAppClient
            with WhatsAppClient(headless=True) as client:
                import time
                time.sleep(3)
                
                # Extraer contactos reales directamente del almacenamiento interno de WhatsApp Web
                contacts = client.page.evaluate("""async () => {
                    return new Promise((resolve) => {
                        const req = indexedDB.open('model-storage');
                        req.onsuccess = () => {
                            const db = req.result;
                            if (!db.objectStoreNames.contains('contact')) {
                                resolve([]);
                                return;
                            }
                            const tx = db.transaction('contact', 'readonly');
                            const store = tx.objectStore('contact');
                            const allReq = store.getAll();
                            allReq.onsuccess = () => {
                                const list = [];
                                for (let c of allReq.result) {
                                    const name = c.name || c.formattedTitle || c.notifyName || '';
                                    let phone = '';
                                    
                                    // El teléfono real suele estar en c.phone o en el ID
                                    if (c.phone && c.phone.includes('@c.us')) {
                                        phone = c.phone.replace('@c.us', '');
                                    } else if (c.id && c.id.includes('@s.whatsapp.net')) {
                                        phone = c.id.replace('@s.whatsapp.net', '');
                                    }
                                    
                                    if (name && phone && !name.includes('@syntra') && !name.includes('WhatsApp')) {
                                        list.push({ name, phone });
                                    }
                                }
                                resolve(list);
                            };
                            allReq.onerror = () => resolve([]);
                        };
                        req.onerror = () => resolve([]);
                    });
                }""")
                
                conn = get_db()
                cur = conn.cursor()
                synced = 0
                
                for c in contacts:
                    name = c.get('name', '').strip()
                    raw_phone = c.get('phone', '').strip()
                    if not name or not raw_phone:
                        continue
                        
                    # Formatear a formato internacional limpio: +58 414-7961014
                    formatted_phone = f"+{raw_phone}"
                    if len(raw_phone) == 12 and raw_phone.startswith("58"):
                        formatted_phone = f"+58 {raw_phone[2:5]}-{raw_phone[5:]}"
                    elif len(raw_phone) == 11 and raw_phone.startswith("58"):
                        formatted_phone = f"+58 {raw_phone[2:5]}-{raw_phone[5:]}"
                    elif len(raw_phone) > 10:
                        formatted_phone = f"+{raw_phone}"
                        
                    # Verificar si ya existe por nombre o teléfono
                    cur.execute("SELECT id, location, printer_model, materials_interest, lead_status, notes FROM clients WHERE name=? OR phone=?", (name, formatted_phone))
                    existing = cur.fetchone()
                    
                    if existing:
                        # Actualizar teléfono real si estaba incompleto o desactualizado
                        cur.execute("UPDATE clients SET phone=?, name=? WHERE id=?", (formatted_phone, name, existing['id']))
                        synced += 1
                    else:
                        cur.execute("""
                        INSERT INTO clients (name, phone, location, printer_model, materials_interest, lead_status, notes)
                        VALUES (?, ?, 'Lechería / Por definir', 'Por consultar', 'PLA / Insumos', 'Prospecto', 'Importado automáticamente desde WhatsApp')
                        """, (name, formatted_phone))
                        synced += 1
                        
                conn.commit()
                conn.close()
                self._send_json({"status": "ok", "synced_count": synced, "contacts": contacts})
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def serve_static(self, path):
        host = self.headers.get("Host", "").lower().split(":")[0]
        is_admin_host = host.startswith("admin.") or host.startswith("crm.")

        if is_admin_host:
            clean_path = path.lstrip("/")
            if not clean_path or clean_path == "index.html":
                filepath = os.path.join(CRM_STATIC_DIR, "index.html")
            else:
                filepath = os.path.join(CRM_STATIC_DIR, clean_path)
                if not os.path.exists(filepath):
                    filepath = os.path.join(CRM_STATIC_DIR, "index.html")
        else:
            if path == "/admin" or path.startswith("/admin/"):
                subpath = path[6:].lstrip("/")
                if not subpath or subpath == "index.html":
                    filepath = os.path.join(CRM_STATIC_DIR, "index.html")
                else:
                    filepath = os.path.join(CRM_STATIC_DIR, subpath)
                    if not os.path.exists(filepath):
                        filepath = os.path.join(CRM_STATIC_DIR, "index.html")
            else:
                clean_path = path.lstrip("/")
                if not clean_path or clean_path == "index.html":
                    filepath = os.path.join(WEB_DIR, "index.html")
                else:
                    filepath = os.path.join(WEB_DIR, clean_path)
                    if not os.path.exists(filepath) and os.path.exists(os.path.join(CRM_STATIC_DIR, clean_path)):
                        filepath = os.path.join(CRM_STATIC_DIR, clean_path)

        if os.path.exists(filepath) and os.path.isfile(filepath):
            if filepath.endswith(".js"):
                mime_type = "application/javascript; charset=utf-8"
            elif filepath.endswith(".css"):
                mime_type = "text/css; charset=utf-8"
            elif filepath.endswith(".html"):
                mime_type = "text/html; charset=utf-8"
            elif filepath.endswith(".svg"):
                mime_type = "image/svg+xml"
            else:
                mime_type, _ = mimetypes.guess_type(filepath)
                if not mime_type:
                    mime_type = "application/octet-stream"
                elif mime_type.startswith("text/") or mime_type == "application/javascript":
                    mime_type += "; charset=utf-8"

            with open(filepath, "rb") as f:
                content = f.read()

            self.send_response(200)
            self.send_header("Content-Type", mime_type)
            self.send_header("Content-Length", str(len(content)))
            self.send_header("Access-Control-Allow-Origin", "*")
            if filepath.endswith(".html"):
                self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
            elif filepath.endswith((".js", ".css")):
                self.send_header("Cache-Control", "no-cache, must-revalidate")
            else:
                self.send_header("Cache-Control", "public, max-age=86400")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(content)
        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.send_header("Content-Length", "13")
            self.send_header("Connection", "close")
            self.end_headers()
            self.wfile.write(b"404 Not Found")


    def handle_post_expense(self, body):
        conn = get_db()
        cur = conn.cursor()
        category = body.get("category", "General")
        amount_usd = float(body.get("amount_usd", 0))
        bcv_rate = float(body.get("bcv_rate", 53.50))
        amount_bs = float(body.get("amount_bs") or (amount_usd * bcv_rate))
        description = body.get("description", "").strip()
        payment_method = body.get("payment_method", "Zelle")
        custom_date = body.get("date")

        if amount_usd <= 0:
            conn.close()
            self._send_json({"error": "El monto del gasto debe ser mayor a 0"}, 400)
            return

        if custom_date:
            cur.execute("""
            INSERT INTO expenses (category, amount_usd, amount_bs, bcv_rate, description, payment_method, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (category, amount_usd, amount_bs, bcv_rate, description, payment_method, custom_date))
        else:
            cur.execute("""
            INSERT INTO expenses (category, amount_usd, amount_bs, bcv_rate, description, payment_method)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (category, amount_usd, amount_bs, bcv_rate, description, payment_method))

        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Gasto registrado exitosamente"})

    def handle_delete_expense(self, expense_id):
        if not expense_id:
            self._send_json({"error": "ID de gasto requerido"}, 400)
            return
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM expenses WHERE id=?", (expense_id,))
        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Gasto eliminado exitosamente"})

    def handle_post_sale_payment(self, body):
        conn = get_db()
        cur = conn.cursor()
        sale_id = body.get("sale_id")
        amount_usd = float(body.get("amount_usd", 0))
        bcv_rate = float(body.get("bcv_rate", 53.50))
        amount_bs = float(body.get("amount_bs") or (amount_usd * bcv_rate))
        payment_method = body.get("payment_method", "Pago Móvil")
        reference = body.get("reference", "").strip()
        notes = body.get("notes", "").strip()

        if not sale_id or amount_usd <= 0:
            conn.close()
            self._send_json({"error": "Venta y monto válido requeridos"}, 400)
            return

        cur.execute("SELECT total_price, amount_paid FROM sales WHERE id=?", (sale_id,))
        sale_row = cur.fetchone()
        if not sale_row:
            conn.close()
            self._send_json({"error": "Venta no encontrada"}, 404)
            return

        total_price = float(sale_row["total_price"])
        cur_paid = float(sale_row["amount_paid"] or 0)
        new_paid = cur_paid + amount_usd
        new_balance = max(0.0, total_price - new_paid)
        new_status = "PAGADO" if new_balance <= 0.01 else "PARCIAL"

        cur.execute("""
        INSERT INTO payment_records (sale_id, amount_usd, amount_bs, payment_method, reference, notes)
        VALUES (?, ?, ?, ?, ?, ?)
        """, (sale_id, amount_usd, amount_bs, payment_method, reference, notes))

        cur.execute("""
        UPDATE sales SET amount_paid=?, balance_due=?, payment_status=?
        WHERE id=?
        """, (new_paid, new_balance, new_status, sale_id))

        conn.commit()
        conn.close()
        self._send_json({
            "status": "ok", 
            "message": f"Abono de ${amount_usd:.2f} registrado. Saldo pendiente: ${new_balance:.2f}",
            "balance_due": new_balance,
            "payment_status": new_status
        })

    def handle_post_inventory_adjust(self, body):
        conn = get_db()
        cur = conn.cursor()
        product_id = body.get("product_id")
        qty = int(body.get("quantity", 1))
        reason = body.get("reason", "Uso Interno en Taller")
        notes = body.get("notes", "").strip()

        if not product_id or qty <= 0:
            conn.close()
            self._send_json({"error": "Producto y cantidad mayor a 0 requeridos"}, 400)
            return

        cur.execute("SELECT current_stock, name FROM products WHERE id=?", (product_id,))
        prod = cur.fetchone()
        if not prod:
            conn.close()
            self._send_json({"error": "Producto no encontrado"}, 404)
            return

        if prod["current_stock"] < qty:
            conn.close()
            self._send_json({"error": f"Stock insuficiente. Disponible: {prod['current_stock']}"}, 400)
            return

        # Descontar stock
        cur.execute("UPDATE products SET current_stock = current_stock - ? WHERE id=?", (qty, product_id))

        # Registrar ajuste / merma
        cur.execute("""
        INSERT INTO inventory_adjustments (product_id, quantity, reason, notes)
        VALUES (?, ?, ?, ?)
        """, (product_id, qty, reason, notes))

        conn.commit()
        conn.close()
        self._send_json({
            "status": "ok", 
            "message": f"Ajuste registrado exitosamente ({qty} unds descontadas por: {reason})"
        })


    def handle_get_verify_reference(self, query_string):
        params = parse_qs(query_string)
        ref = params.get("ref", [""])[0].strip()
        if not ref or len(ref) < 3:
            self._send_json({"duplicate": False})
            return
        conn = get_db()
        cur = conn.cursor()
        
        # 1. Check in client payment_records
        cur.execute("""
        SELECT pr.id, pr.amount_usd, pr.payment_method, pr.date, c.name 
        FROM payment_records pr 
        LEFT JOIN sales s ON pr.sale_id = s.id 
        LEFT JOIN clients c ON s.client_id = c.id 
        WHERE LOWER(pr.reference) = LOWER(?) LIMIT 1
        """, (ref,))
        match1 = cur.fetchone()
        if match1:
            conn.close()
            self._send_json({
                "duplicate": True,
                "type": "Abono / Cobranza de Cliente",
                "details": f"Registrada en cobro a {match1[4] or 'Cliente'} por ${match1[1]:.2f} ({match1[2]}) el {str(match1[3])[:10]}"
            })
            return

        # 2. Check in supplier_payments
        cur.execute("""
        SELECT sp.id, sp.amount_usd, sp.payment_method, sp.date, s.name 
        FROM supplier_payments sp 
        LEFT JOIN supplier_invoices si ON sp.invoice_id = si.id 
        LEFT JOIN suppliers s ON si.supplier_id = s.id 
        WHERE LOWER(sp.reference) = LOWER(?) LIMIT 1
        """, (ref,))
        match2 = cur.fetchone()
        if match2:
            conn.close()
            self._send_json({
                "duplicate": True,
                "type": "Pago a Proveedor",
                "details": f"Registrada en pago a {match2[4] or 'Proveedor'} por ${match2[1]:.2f} el {str(match2[3])[:10]}"
            })
            return

        # 3. Check in tracking_number / sale notes
        cur.execute("""
        SELECT id, total_price, client_id, date FROM sales WHERE LOWER(tracking_number) = LOWER(?) LIMIT 1
        """, (ref,))
        match3 = cur.fetchone()
        if match3:
            conn.close()
            self._send_json({
                "duplicate": True,
                "type": "Número de Guía / Venta",
                "details": f"Registrada como guía en Venta #{match3[0]} por ${match3[1]:.2f} el {str(match3[3])[:10]}"
            })
            return

        conn.close()
        self._send_json({"duplicate": False})

    def handle_get_suppliers(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM suppliers ORDER BY name ASC")
        suppliers = [dict(row) for row in cur.fetchall()]
        conn.close()
        self._send_json({"suppliers": suppliers})

    def handle_get_supplier_invoices(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        SELECT si.*, s.name as supplier_name, s.category as supplier_category, s.country as supplier_country
        FROM supplier_invoices si
        LEFT JOIN suppliers s ON si.supplier_id = s.id
        ORDER BY si.created_at DESC
        """)
        invoices = [dict(row) for row in cur.fetchall()]
        conn.close()
        self._send_json({"invoices": invoices})

    def handle_post_supplier(self, body):
        name = body.get("name")
        if not name:
            self._send_json({"error": "Nombre del proveedor es requerido"}, 400)
            return
        category = body.get("category", "General")
        contact_name = body.get("contact_name", "")
        phone = body.get("phone", "")
        email = body.get("email", "")
        country = body.get("country", "Venezuela")
        notes = body.get("notes", "")
        supplier_id = body.get("id")

        conn = get_db()
        cur = conn.cursor()
        if supplier_id:
            cur.execute("""
            UPDATE suppliers 
            SET name=?, category=?, contact_name=?, phone=?, email=?, country=?, notes=?
            WHERE id=?
            """, (name, category, contact_name, phone, email, country, notes, supplier_id))
        else:
            cur.execute("""
            INSERT INTO suppliers (name, category, contact_name, phone, email, country, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (name, category, contact_name, phone, email, country, notes))
            supplier_id = cur.lastrowid
        conn.commit()
        conn.close()
        self._send_json({"success": True, "id": supplier_id})

    def handle_delete_supplier(self, supplier_id):
        if not supplier_id:
            self._send_json({"error": "ID de proveedor requerido"}, 400)
            return
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM supplier_invoices WHERE supplier_id = ?", (supplier_id,))
        inv_count = cur.fetchone()[0]
        if inv_count > 0:
            conn.close()
            self._send_json({"error": f"No se puede eliminar este proveedor porque tiene {inv_count} factura(s)/embarque(s) asociadas. Elimina las facturas primero."}, 400)
            return
        cur.execute("DELETE FROM suppliers WHERE id = ?", (supplier_id,))
        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Proveedor eliminado exitosamente"})

    def handle_post_supplier_invoice(self, body):
        supplier_id = body.get("supplier_id")
        try:
            total_amount = float(body.get("total_amount_usd", 0))
        except (ValueError, TypeError):
            total_amount = 0.0

        if not supplier_id or total_amount <= 0:
            self._send_json({"error": "Proveedor y monto total positivo son requeridos"}, 400)
            return

        invoice_number = body.get("invoice_number", f"KR-INV-{int(time.time())}")
        description = body.get("description", "Orden de compra de insumos")
        try:
            amount_paid = float(body.get("amount_paid", 0.0))
        except (ValueError, TypeError):
            amount_paid = 0.0

        balance_due = max(0.0, total_amount - amount_paid)
        due_date = body.get("due_date", "")
        category = body.get("category", "Materia Prima 3D")
        status = "PAGADO" if balance_due <= 0.001 else ("PARCIAL" if amount_paid > 0 else "PENDIENTE")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        INSERT INTO supplier_invoices (supplier_id, invoice_number, description, total_amount_usd, amount_paid, balance_due, due_date, payment_status, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (supplier_id, invoice_number, description, total_amount, amount_paid, balance_due, due_date, status, category))
        invoice_id = cur.lastrowid

        if amount_paid > 0:
            pay_method = body.get("payment_method", "Transferencia Internacional")
            pay_ref = body.get("reference", "")
            cur.execute("""
            INSERT INTO supplier_payments (invoice_id, amount_usd, payment_method, reference, notes)
            VALUES (?, ?, ?, ?, ?)
            """, (invoice_id, amount_paid, pay_method, pay_ref, "Abono / Pago inicial registrado con factura"))

        conn.commit()
        conn.close()
        self._send_json({"success": True, "invoice_id": invoice_id})

    def handle_delete_supplier_invoice(self, invoice_id):
        if not invoice_id:
            self._send_json({"error": "ID es requerido"}, 400)
            return
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM supplier_payments WHERE invoice_id = ?", (invoice_id,))
        cur.execute("DELETE FROM supplier_invoices WHERE id = ?", (invoice_id,))
        conn.commit()
        conn.close()
        self._send_json({"success": True})

    def handle_post_supplier_payment(self, body):
        invoice_id = body.get("invoice_id")
        try:
            amount_usd = float(body.get("amount_usd", 0))
        except (ValueError, TypeError):
            amount_usd = 0.0

        if not invoice_id or amount_usd <= 0:
            self._send_json({"error": "ID de factura y monto válido requeridos"}, 400)
            return

        payment_method = body.get("payment_method", "Zelle")
        reference = body.get("reference", "")
        notes = body.get("notes", "")

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT total_amount_usd, amount_paid, balance_due FROM supplier_invoices WHERE id = ?", (invoice_id,))
        row = cur.fetchone()
        if not row:
            conn.close()
            self._send_json({"error": "Factura de proveedor no encontrada"}, 404)
            return
        tot, paid, bal = row
        new_paid = paid + amount_usd
        new_bal = max(0.0, tot - new_paid)
        new_status = "PAGADO" if new_bal <= 0.001 else "PARCIAL"

        cur.execute("""
        UPDATE supplier_invoices 
        SET amount_paid = ?, balance_due = ?, payment_status = ?
        WHERE id = ?
        """, (new_paid, new_bal, new_status, invoice_id))

        cur.execute("""
        INSERT INTO supplier_payments (invoice_id, amount_usd, payment_method, reference, notes)
        VALUES (?, ?, ?, ?, ?)
        """, (invoice_id, amount_usd, payment_method, reference, notes))

        conn.commit()
        conn.close()
        self._send_json({"success": True, "new_balance": new_bal, "status": new_status})


    def handle_get_product_kardex(self, query_string):
        params = parse_qs(query_string)
        prod_id = int(params.get("product_id", [0])[0]) if params.get("product_id") else None
        if not prod_id:
            self._send_json({"error": "product_id requerido"}, 400)
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM products WHERE id=?", (prod_id,))
        prod = cur.fetchone()
        if not prod:
            conn.close()
            self._send_json({"error": "Producto no encontrado"}, 404)
            return
        
        prod_data = dict(prod)
        init_stock = int(prod_data.get("initial_stock", 0))
        
        movements = []
        movements.append({
            "date": "2026-07-23 00:00:00",
            "type": "ENTRADA",
            "type_label": "Entrada Inicial / Embarque",
            "reference": "PROFORMA-KR-20260723",
            "description": "Carga inicial consolidada Shenzhen -> Guanta",
            "qty_in": init_stock,
            "qty_out": 0,
            "unit_cost": prod_data.get("cost_warehouse", 0.0)
        })

        cur.execute("""
        SELECT s.id, s.date, si.quantity, si.unit_price, si.total_price, c.name as client_name, s.delivery_method, s.tracking_number
        FROM sale_items si
        JOIN sales s ON si.sale_id = s.id
        LEFT JOIN clients c ON s.client_id = c.id
        WHERE si.product_id = ?
        ORDER BY s.date ASC
        """, (prod_id,))
        sale_records = cur.fetchall()
        if not sale_records:
            cur.execute("""
            SELECT s.id, s.date, s.quantity, s.unit_price, s.total_price, c.name as client_name, s.delivery_method, s.tracking_number
            FROM sales s
            LEFT JOIN clients c ON s.client_id = c.id
            WHERE s.product_id = ?
            ORDER BY s.date ASC
            """, (prod_id,))
            sale_records = cur.fetchall()
        for s in sale_records:
            movements.append({
                "date": s["date"],
                "type": "VENTA",
                "type_label": "Despacho / Venta",
                "reference": f"SYNTRA-VTA-{s['id']:04d}",
                "description": f"Cliente: {s['client_name'] or 'Mostrador'} ({s['delivery_method'] or 'Local'})",
                "qty_in": 0,
                "qty_out": s["quantity"],
                "unit_cost": s["unit_price"]
            })

        cur.execute("""
        SELECT a.id, a.date, a.quantity, a.reason, a.notes
        FROM inventory_adjustments a
        WHERE a.product_id = ?
        ORDER BY a.date ASC
        """, (prod_id,))
        for a in cur.fetchall():
            movements.append({
                "date": a["date"],
                "type": "MERMA",
                "type_label": "Merma / Ajuste",
                "reference": f"MERMA-{a['id']:04d}",
                "description": f"Motivo: {a['reason']} - {a['notes'] or ''}",
                "qty_in": 0,
                "qty_out": a["quantity"],
                "unit_cost": prod_data.get("cost_warehouse", 0.0)
            })

        movements.sort(key=lambda x: str(x["date"]))

        running = 0
        total_in = 0
        total_out = 0
        for m in movements:
            if m["qty_in"] > 0:
                running += m["qty_in"]
                total_in += m["qty_in"]
            if m["qty_out"] > 0:
                running -= m["qty_out"]
                total_out += m["qty_out"]
            m["balance_after"] = running

        conn.close()
        self._send_json({
            "product": prod_data,
            "total_in": total_in,
            "total_out": total_out,
            "current_balance": running,
            "movements": movements
        })

    def handle_get_client_statement(self, query_string):
        params = parse_qs(query_string)
        client_id = int(params.get("client_id", [0])[0]) if params.get("client_id") else None
        if not client_id:
            self._send_json({"error": "client_id requerido"}, 400)
            return

        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM clients WHERE id=?", (client_id,))
        client = cur.fetchone()
        if not client:
            conn.close()
            self._send_json({"error": "Cliente no encontrado"}, 404)
            return

        client_data = dict(client)

        cur.execute("""
        SELECT s.*, p.name as product_name, p.category as product_category
        FROM sales s
        LEFT JOIN products p ON s.product_id = p.id
        WHERE s.client_id = ?
        ORDER BY s.date DESC
        """, (client_id,))
        sales = [dict(r) for r in cur.fetchall()]

        cur.execute("""
        SELECT pr.*, s.id as sale_ref_id
        FROM payment_records pr
        JOIN sales s ON pr.sale_id = s.id
        WHERE s.client_id = ?
        ORDER BY pr.date DESC
        """, (client_id,))
        payments = [dict(r) for r in cur.fetchall()]

        total_spent = sum(float(s.get("total_price", 0.0)) for s in sales)
        total_paid = sum(float(s.get("amount_paid", s.get("total_price", 0.0))) for s in sales)
        total_balance = sum(float(s.get("balance_due", 0.0)) for s in sales if s.get("payment_status") != "PAGADO")

        conn.close()
        self._send_json({
            "client": client_data,
            "summary": {
                "total_sales_count": len(sales),
                "total_spent_usd": total_spent,
                "total_paid_usd": total_paid,
                "total_balance_due_usd": total_balance,
                "pending_invoices_count": len([s for s in sales if s.get("payment_status") != "PAGADO"])
            },
            "sales": sales,
            "payments": payments
        })

    def handle_download_backup(self):
        db_path = os.path.join(os.path.dirname(__file__), "syntra_crm.db")
        if not os.path.exists(db_path):
            self._send_json({"error": "Base de datos no encontrada"}, 404)
            return

        with open(db_path, "rb") as f:
            db_bytes = f.read()

        import datetime
        timestamp_str = datetime.datetime.now().strftime("%Y%m%d_%H%M")
        filename = f"syntra_crm_backup_{timestamp_str}.db"

        self.send_response(200)
        self.send_header("Content-Type", "application/x-sqlite3")
        self.send_header("Content-Disposition", f'attachment; filename="{filename}"')
        self.send_header("Content-Length", str(len(db_bytes)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Connection", "close")
        self.end_headers()
        self.wfile.write(db_bytes)


    # ================= AFFILIATE SYSTEM HANDLERS =================
    def handle_get_affiliates(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        SELECT a.*,
               COUNT(s.id) as sales_count,
               COALESCE(SUM(s.quantity), 0) as total_volume_units,
               COALESCE(SUM(s.total_price), 0) as total_sales_usd,
               COALESCE(SUM(s.commission_amount), 0) as total_commission_usd,
               COALESCE((SELECT SUM(ap.amount_usd) FROM affiliate_payouts ap WHERE ap.affiliate_id = a.id), 0) as total_payout_usd,
               (COALESCE(SUM(s.commission_amount), 0) - COALESCE((SELECT SUM(ap.amount_usd) FROM affiliate_payouts ap WHERE ap.affiliate_id = a.id), 0)) as balance_due
        FROM affiliates a
        LEFT JOIN sales s ON a.id = s.affiliate_id
        GROUP BY a.id
        ORDER BY total_sales_usd DESC, a.created_at DESC
        """)
        affiliates = [dict(row) for row in cur.fetchall()]
        conn.close()
        self._send_json(affiliates)

    def handle_get_affiliate_payouts(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        SELECT ap.*, a.name as affiliate_name, a.code as affiliate_code
        FROM affiliate_payouts ap
        LEFT JOIN affiliates a ON ap.affiliate_id = a.id
        ORDER BY ap.date DESC
        """)
        payouts = [dict(row) for row in cur.fetchall()]
        conn.close()
        self._send_json(payouts)

    def handle_get_affiliate_commissions(self):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("""
        SELECT s.id as sale_id, s.date, s.quantity, s.total_price, s.commission_amount, s.commission_status,
               c.name as client_name, p.name as product_name,
               a.id as affiliate_id, a.name as affiliate_name, a.code as affiliate_code
        FROM sales s
        JOIN affiliates a ON s.affiliate_id = a.id
        LEFT JOIN clients c ON s.client_id = c.id
        LEFT JOIN products p ON s.product_id = p.id
        ORDER BY s.date DESC
        """)
        commissions = [dict(row) for row in cur.fetchall()]
        conn.close()
        self._send_json(commissions)

    def handle_post_affiliate(self, body):
        conn = get_db()
        cur = conn.cursor()
        a_id = body.get("id")
        name = str(body.get("name", "")).strip()
        code = str(body.get("code", "")).strip().upper()
        phone = str(body.get("phone", "")).strip()
        email = str(body.get("email", "")).strip()
        location = str(body.get("location", "Lechería")).strip()
        comm_type = str(body.get("commission_type", "FIXED")).strip()
        try:
            comm_rate_cash = float(body.get("commission_rate_cash", body.get("commission_rate", 1.50)))
        except (ValueError, TypeError):
            comm_rate_cash = 1.50
        try:
            comm_rate_bcv = float(body.get("commission_rate_bcv", 1.25))
        except (ValueError, TypeError):
            comm_rate_bcv = 1.25
        comm_rate = comm_rate_cash

        payment_method = str(body.get("payment_method", "Binance USDT")).strip()
        payment_details = str(body.get("payment_details", "")).strip()
        status = str(body.get("status", "Activo")).strip()
        notes = str(body.get("notes", "")).strip()

        if not name or not code:
            conn.close()
            self._send_json({"error": "Nombre y Código de Afiliado son obligatorios"}, 400)
            return

        if a_id:
            try:
                cur.execute("""
                UPDATE affiliates
                SET name=?, code=?, phone=?, email=?, location=?, commission_type=?, commission_rate=?, commission_rate_cash=?, commission_rate_bcv=?, payment_method=?, payment_details=?, status=?, notes=?
                WHERE id=?
                """, (name, code, phone, email, location, comm_type, comm_rate, comm_rate_cash, comm_rate_bcv, payment_method, payment_details, status, notes, a_id))
            except sqlite3.IntegrityError:
                conn.close()
                self._send_json({"error": f"El código de promotor '{code}' ya está en uso. Elige uno diferente."}, 400)
                return
            except Exception as e:
                conn.close()
                self._send_json({"error": f"Error al actualizar afiliado: {str(e)}"}, 500)
                return
        else:
            try:
                cur.execute("""
                INSERT INTO affiliates (name, code, phone, email, location, commission_type, commission_rate, commission_rate_cash, commission_rate_bcv, payment_method, payment_details, status, notes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (name, code, phone, email, location, comm_type, comm_rate, comm_rate_cash, comm_rate_bcv, payment_method, payment_details, status, notes))
                a_id = cur.lastrowid
            except sqlite3.IntegrityError:
                conn.close()
                self._send_json({"error": f"El código de promotor '{code}' ya está en uso. Elige uno diferente."}, 400)
                return
            except Exception as e:
                conn.close()
                self._send_json({"error": f"Error al registrar afiliado: {str(e)}"}, 500)
                return

        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Afiliado guardado con éxito", "id": a_id})

    def handle_delete_affiliate(self, item_id):
        if not item_id:
            self._send_json({"error": "ID es requerido"}, 400)
            return
        conn = get_db()
        cur = conn.cursor()
        cur.execute("UPDATE sales SET affiliate_id=NULL WHERE affiliate_id=?", (item_id,))
        cur.execute("DELETE FROM affiliate_payouts WHERE affiliate_id=?", (item_id,))
        cur.execute("DELETE FROM affiliates WHERE id=?", (item_id,))
        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Afiliado y sus liquidaciones eliminadas"})

    def handle_post_affiliate_payout(self, body):
        conn = get_db()
        cur = conn.cursor()
        affiliate_id = body.get("affiliate_id")
        try:
            amount_usd = float(body.get("amount_usd", 0))
        except (ValueError, TypeError):
            amount_usd = 0.0

        amount_bs = float(body.get("amount_bs", 0))
        bcv_rate = float(body.get("bcv_rate", 896.12))
        payment_method = str(body.get("payment_method", "Binance USDT")).strip()
        reference = str(body.get("reference", "")).strip()
        notes = str(body.get("notes", "")).strip()

        if not affiliate_id or amount_usd <= 0:
            conn.close()
            self._send_json({"error": "Afiliado y monto válido requeridos"}, 400)
            return

        cur.execute("""
        INSERT INTO affiliate_payouts (affiliate_id, amount_usd, amount_bs, bcv_rate, payment_method, reference, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (affiliate_id, amount_usd, amount_bs, bcv_rate, payment_method, reference, notes))
        payout_id = cur.lastrowid

        # Marcar ventas del afiliado como liquidadas si el monto pagado cubre
        cur.execute("""
        UPDATE sales SET commission_status='LIQUIDADA'
        WHERE affiliate_id=? AND commission_status='PENDIENTE'
        """, (affiliate_id,))

        conn.commit()
        conn.close()
        self._send_json({
            "status": "ok",
            "message": f"Liquidación de comisión de ${amount_usd:.2f} registrada",
            "payout_id": payout_id
        })

    def handle_delete_affiliate_payout(self, payout_id):
        if not payout_id:
            self._send_json({"error": "ID es requerido"}, 400)
            return
        conn = get_db()
        cur = conn.cursor()
        cur.execute("DELETE FROM affiliate_payouts WHERE id=?", (payout_id,))
        conn.commit()
        conn.close()
        self._send_json({"status": "ok", "message": "Liquidación eliminada"})



    # =========================================================================
    # PUBLIC SYNC & WEB CATALOG ENDPOINTS (TIEMPO REAL)
    # =========================================================================
    def handle_get_public_catalog(self):
        try:
            conn = get_db()
            cur = conn.cursor()
            cur.execute("""
                SELECT id, sku, name, category, color, material_type, current_stock, pvp_usd
                FROM products
                ORDER BY id;
            """)
            products = [dict(row) for row in cur.fetchall()]
            conn.close()
            self._send_json({
                "status": "ok",
                "bcv_rate": 896.12,
                "total_products": len(products),
                "total_stock": sum(p.get("current_stock", 0) for p in products),
                "products": products
            })
        except Exception as e:
            self._send_json({"status": "error", "message": str(e)}, 500)

    def handle_post_public_order(self, body):
        try:
            conn = get_db()
            cur = conn.cursor()

            name = (body.get("client_name") or "Cliente Catálogo Web").strip()
            phone = (body.get("client_phone") or "").strip()
            city = (body.get("client_city") or "Lechería").strip()
            rif = (body.get("client_id") or "").strip()
            delivery = body.get("delivery_method", "Retiro en Almacén")
            payment = body.get("payment_method", "Pago Móvil (Tasa Oficial BCV)")
            items = body.get("items", [])

            # Buscar o crear cliente
            client_id = None
            if phone:
                cur.execute("SELECT id FROM clients WHERE phone=?", (phone,))
                r = cur.fetchone()
                if r:
                    client_id = r["id"]

            if not client_id:
                cur.execute("""
                    INSERT INTO clients (name, phone, location, lead_status, pipeline_stage, notes)
                    VALUES (?, ?, ?, 'Prospecto Web', 'Cotización Web', ?)
                """, (name, phone, city, f"Cédula/RIF: {rif} | Registrado automáticamente desde la web"))
                client_id = cur.lastrowid

            # Procesar ítems solicitados
            total_price = 0.0
            total_qty = 0
            order_items = []
            for it in items:
                sku = it.get("sku")
                qty = int(it.get("qty", 1))
                cur.execute("SELECT * FROM products WHERE sku=? OR id=?", (sku, it.get("crm_id") or 0))
                p = cur.fetchone()
                if p:
                    u_price = float(p["pvp_usd"] or 20.0)
                    u_cost = float(p["cost_warehouse"] or 10.0)
                    total_price += u_price * qty
                    total_qty += qty
                    order_items.append({
                        "product_id": p["id"],
                        "quantity": qty,
                        "unit_price": u_price,
                        "unit_cost": u_cost,
                        "total_price": u_price * qty,
                        "net_profit": (u_price - u_cost) * qty
                    })

            first_pid = order_items[0]["product_id"] if order_items else 1
            notes = f"Pedido Web | RIF: {rif} | Despacho: {delivery} | Pago: {payment}"

            # Registrar en tabla sales como COTIZACION WEB
            cur.execute("""
                INSERT INTO sales (client_id, product_id, quantity, unit_price, unit_cost, total_price, net_profit, payment_method, delivery_method, notes, payment_status, shipping_status)
                VALUES (?, ?, ?, ?, 0, ?, 0, ?, ?, ?, 'COTIZACION WEB', 'Pendiente Confirmar')
            """, (client_id, first_pid, total_qty, round(total_price / max(1, total_qty), 2), total_price, payment, delivery, notes))
            sale_id = cur.lastrowid

            for oi in order_items:
                cur.execute("""
                    INSERT INTO sale_items (sale_id, product_id, quantity, unit_price, unit_cost, total_price, net_profit)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (sale_id, oi["product_id"], oi["quantity"], oi["unit_price"], oi["unit_cost"], oi["total_price"], oi["net_profit"]))

            conn.commit()
            conn.close()

            self._send_json({
                "status": "ok",
                "sale_id": sale_id,
                "message": f"Orden #{sale_id} registrada en el CRM exitosamente."
            })
        except Exception as e:
            self._send_json({"status": "error", "message": str(e)}, 500)

    def handle_sync_web(self):
        try:
            from sync_crm_to_web import sync_crm_database_to_manifest
            count, stock = sync_crm_database_to_manifest()
            self._send_json({
                "status": "ok",
                "message": f"Catálogo web sincronizado con {count} productos y {stock} unidades físicas."
            })
        except Exception as e:
            self._send_json({"status": "error", "message": str(e)}, 500)

def get_local_ip():
    try:
        hostname = socket.gethostname()
        ips = socket.gethostbyname_ex(hostname)[2]
        for ip in ips:
            if not ip.startswith("127."):
                return ip
        return "127.0.0.1"
    except Exception:
        return "127.0.0.1"


def run(port=8500):
    os.makedirs(STATIC_DIR, exist_ok=True)
    server = ThreadingHTTPServer(("0.0.0.0", port), SyntraCRMHandler)
    local_ip = get_local_ip()
    print(f"[*] Panel Syntra CRM ejecutándose:")
    print(f"    - En esta PC:     http://localhost:{port}")
    print(f"    - En tu iPhone:   http://{local_ip}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    server.server_close()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", sys.argv[1] if len(sys.argv) > 1 else 8500))
    run(port)
