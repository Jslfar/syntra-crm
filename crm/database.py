import sqlite3
import os
import csv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "syntra_crm.db")
ROOT_DIR = os.path.dirname(BASE_DIR)
CSV_IMPORT_PATH = os.path.join(ROOT_DIR, "syntra_supply_google_sheets_import.csv")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    
    # 1. Tabla de Inventario / Productos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        name TEXT NOT NULL,
        initial_stock INTEGER NOT NULL,
        current_stock INTEGER NOT NULL,
        cost_warehouse REAL NOT NULL,
        pvp_usd REAL NOT NULL,
        margin_pct REAL,
        net_profit_unit REAL
    )
    """)
    
    # 2. Tabla de Clientes / Leads
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone TEXT UNIQUE NOT NULL,
        location TEXT,
        printer_model TEXT,
        materials_interest TEXT,
        lead_status TEXT DEFAULT 'Prospecto',
        pipeline_stage TEXT DEFAULT 'Nuevo Prospecto',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    # 3. Tabla de Ventas / Finanzas
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sales (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        unit_cost REAL NOT NULL,
        total_price REAL NOT NULL,
        net_profit REAL NOT NULL,
        payment_method TEXT DEFAULT 'Zelle / Divisa',
        delivery_method TEXT DEFAULT 'Retiro en Tienda / Local',
        tracking_number TEXT,
        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        notes TEXT,
        FOREIGN KEY (client_id) REFERENCES clients (id),
        FOREIGN KEY (product_id) REFERENCES products (id)
    )
    """)
    
    # 4. Tabla de Solicitudes de Nuevo Stock / Demanda Fuera de Catálogo (Wishlist)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_requests (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER,
        client_name TEXT NOT NULL,
        client_phone TEXT,
        item_name TEXT NOT NULL,
        category TEXT DEFAULT 'Filamentos Especiales',
        quantity INTEGER DEFAULT 1,
        estimated_price REAL DEFAULT 0.0,
        priority TEXT DEFAULT 'Media',
        status TEXT DEFAULT 'Pendiente para Próximo Pedido',
        notes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (client_id) REFERENCES clients (id)
    )
    """)
    
    # Sembrar inventario si está vacío
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0 and os.path.exists(CSV_IMPORT_PATH):
        seed_inventory(cursor)
        
    # Sembrar clientes iniciales de prueba / detectados si está vacío
    cursor.execute("SELECT COUNT(*) FROM clients")
    if cursor.fetchone()[0] == 0:
        cursor.execute("""
        INSERT INTO clients (name, phone, location, printer_model, materials_interest, lead_status, notes)
        VALUES 
        ('Jesus Alfaro', '+58 424-8193058', 'Lechería / Anzoátegui', 'Bambu Lab A1', 'PLA Blanco, PLA+', 'En Cotización', 'Interesado en separadores de farmacia'),
        ('Andrea Mercedes', '+58 412-1234567', 'Barcelona / Anzoátegui', 'Creality Ender 3 V3', 'PLA Silk Gold, PETG', 'Prospecto', 'Consulta de stock para catálogo de regalos'),
        ('Carlos Mendoza', '+58 414-9876543', 'Puerto La Cruz', 'Bambu Lab P1S', 'PLA-CF, Boquillas Hardened', 'Cliente Activo', 'Taller de prototipado 3D')
        """)
        
    conn.commit()
    conn.close()

def seed_inventory(cursor):
    print("[*] Sembrando base de datos inicial de inventario desde CSV de Syntra...")
    with open(CSV_IMPORT_PATH, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader, None)
        
        for row in reader:
            if not row or len(row) < 7:
                continue
            cat = row[0].strip()
            name = row[1].strip()
            if not name or cat.upper().startswith("TOTAL"):
                continue
                
            try:
                qty = int(float(row[2].replace(",", "").strip()))
                cost_wh = float(row[4].replace(",", "").strip())
                pvp = float(row[6].replace(",", "").strip())
                margin = float(row[7].replace("%", "").strip()) if len(row) > 7 else 0.0
                profit_unit = float(row[9].replace(",", "").strip()) if len(row) > 9 else (pvp - cost_wh)
                
                cursor.execute("""
                INSERT INTO products (category, name, initial_stock, current_stock, cost_warehouse, pvp_usd, margin_pct, net_profit_unit)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (cat, name, qty, qty, cost_wh, pvp, margin, profit_unit))
            except Exception as e:
                print(f"[-] Error parseando fila {row}: {e}")

if __name__ == "__main__":
    init_db()
    print("[+] Base de datos de Syntra CRM inicializada exitosamente.")
