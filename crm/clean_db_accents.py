import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), "syntra_crm.db")
conn = sqlite3.connect(db_path)
cur = conn.cursor()

cur.execute("""
UPDATE clients 
SET location = 'Lechería / Anzoátegui',
    lead_status = 'En Cotización',
    notes = 'Interesado en separadores para farmacia'
WHERE name = 'Jesus Alfaro'
""")

cur.execute("""
UPDATE clients 
SET location = 'Barcelona / Anzoátegui',
    lead_status = 'Prospecto',
    notes = 'Consulta de stock para catálogo de regalos'
WHERE name = 'Andrea Mercedes'
""")

conn.commit()

cur.execute("SELECT id, name, phone, location, printer_model, lead_status, notes FROM clients")
for row in cur.fetchall():
    print(row)

conn.close()
print("[+] Clientes actualizados con acentos limpios.")
