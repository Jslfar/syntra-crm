import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "syntra_crm.db")
conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

commands = [
    "ALTER TABLE clients ADD COLUMN pipeline_stage TEXT DEFAULT 'Nuevo Prospecto'",
    "ALTER TABLE sales ADD COLUMN delivery_method TEXT DEFAULT 'Retiro en Tienda / Local'",
    "ALTER TABLE sales ADD COLUMN tracking_number TEXT"
]

for cmd in commands:
    try:
        cur.execute(cmd)
        print("[+] Migración exitosa:", cmd)
    except Exception as e:
        print("[*] Info:", e)

conn.commit()
conn.close()
