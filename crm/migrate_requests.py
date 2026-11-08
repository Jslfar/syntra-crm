# -*- coding: utf-8 -*-
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "syntra_crm.db")

def migrate():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    cur.execute("""
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
    
    # Comprobar si ya hay registros
    cur.execute("SELECT COUNT(*) FROM product_requests")
    count = cur.fetchone()[0]
    
    if count == 0:
        cur.execute("""
        INSERT INTO product_requests (client_id, client_name, client_phone, item_name, category, quantity, estimated_price, priority, status, notes)
        VALUES 
        (1, 'Jesus Alfaro', '+58 414-7961014', 'Secador de Filamento (Filament Dryer Box)', 'Accesorios & Herramientas', 2, 45.00, 'Alta', 'Pendiente para Próximo Pedido', 'El clima húmedo de Lechería requiere secador para PETG y TPU'),
        (2, 'Andrea Mercedes', '+58 414-7931222', 'Filamento PLA Madera (Wood Grain)', 'Filamentos Especiales', 3, 26.00, 'Alta', 'Pendiente para Próximo Pedido', 'Para colección de macetas y portavasos decorativos'),
        (NULL, 'Taller Maker Anzoátegui', '+58 412-8889900', 'Resina UV Estándar Gris 1kg (SLA)', 'Resinas & SLA', 5, 28.00, 'Media', 'En Evaluación Kingroon', 'Preguntaron si Syntra traerá insumos para impresión de resina')
        """)
        print("[+] 3 solicitudes iniciales sembradas en el Radar de Demanda.")
        
    conn.commit()
    conn.close()
    print("[+] Tabla product_requests lista y migrada exitosamente.")

if __name__ == "__main__":
    migrate()
