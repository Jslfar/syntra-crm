import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "syntra_crm.db")

# Las 117 líneas exactas agrupadas comercialmente o por SKU con el factor de importación real de Syntra
# En el modelo de Syntra:
# Multiplicador Almacén = Costo FOB * 1.48 (flete marítimo, nacionalización y aduanas)
# Total unidades físicas = 1,750 unidades

PROFORMA_GROUPS = [
    # Filamentos Básicos
    ("Filamentos Basicos", "PETG Basic 1kg (17 colores Kingroon)", 170, 3.20, 4.74, 16.00, 70.4),
    ("Filamentos Basicos", "PLA Basic 1kg (200 und - 12 colores: Blanco 50, Negro 30, Rojo 30, etc.)", 200, 5.20, 7.70, 18.00, 57.2),
    ("Filamentos Basicos", "PLA+ 1kg Alta Resistencia (7 colores: Azul 20, Amarillo, etc.)", 80, 5.90, 8.74, 20.00, 56.3),
    
    # Filamentos Silk
    ("Filamentos Silk", "PLA Silk Gold Oro 1kg (150 und - Top Ventas)", 150, 5.70, 8.44, 22.00, 61.6),
    ("Filamentos Silk", "PLA Silk Solidos y Metalicos 1kg (110 und - Plata 20, Bronce, Negro, etc.)", 110, 5.70, 8.44, 22.00, 61.6),
    ("Filamentos Silk", "PLA Silk Dual-Color Bicolor 1kg (7 combinaciones)", 70, 6.00, 8.88, 24.00, 63.0),
    ("Filamentos Silk", "PLA Silk Tri-Color Tricolor 1kg (8 combinaciones)", 80, 5.90, 8.74, 24.00, 63.6),
    ("Filamentos Silk", "PLA Silk Rainbow Gradientes 1kg (4 combinaciones)", 40, 6.20, 9.18, 24.00, 61.8),
    
    # Filamentos Especiales & Técnicos
    ("Filamentos Especiales", "PLA Marble Efecto Marmol 1kg", 10, 7.00, 10.36, 24.00, 56.8),
    ("Filamentos Especiales", "PLA Matte Mate (Rojo / Piel) 1kg", 20, 4.60, 6.81, 19.00, 64.2),
    ("Filamentos Especiales", "PETG Matte Mate (Negro / Blanco) 1kg", 20, 3.90, 5.77, 18.00, 67.9),
    ("Tecnicos & Flexibles", "TPU 95A Flexible 1kg (10 colores Kingroon)", 120, 6.80, 10.07, 26.00, 61.3),
    ("Tecnicos & Flexibles", "ASA Basic Resistente UV 1kg (Blanco / Gris / Negro)", 30, 6.60, 9.77, 28.00, 65.1),
    ("Tecnicos & Flexibles", "PETG-CF Fibra de Carbono 1kg", 10, 7.50, 11.11, 38.00, 70.8),
    ("Tecnicos & Flexibles", "PLA-CF Fibra de Carbono 1kg", 10, 7.50, 11.11, 38.00, 70.8),
    
    # Camas Magnéticas Bambu Lab & H2D (140 placas)
    ("Camas Magneticas", "Placa PEI Doble Cara Texturizada A1 Mini (184x184)", 20, 2.50, 3.70, 16.00, 76.9),
    ("Camas Magneticas", "Placa Diamante + PEO A1 Mini (184x184)", 20, 2.80, 4.15, 18.00, 76.9),
    ("Camas Magneticas", "Placa Gold PEI Doble Cara Bambu X1/P1/A1 (257x257)", 20, 3.30, 4.89, 28.00, 82.5),
    ("Camas Magneticas", "Placa Diamante + Carbono Bambu X1/P1/A1 (257x257)", 10, 4.30, 6.37, 30.00, 78.8),
    ("Camas Magneticas", "Placa Doble Cara PEI Film Bambu X1/P1/A1 (257x257)", 10, 6.50, 9.62, 32.00, 69.9),
    ("Camas Magneticas", "Placa Topre Chameleon PEO+PEI Bambu (257x257)", 10, 4.80, 7.11, 32.00, 77.8),
    ("Camas Magneticas", "Placa Diamante + PEO Grande Bambu X1/P1/A1 (257x257)", 10, 4.80, 7.11, 32.00, 77.8),
    ("Camas Magneticas", "Placa Cold-Stamping Serigrafiada Bambu (256x256)", 10, 6.50, 9.62, 34.00, 71.7),
    ("Camas Magneticas", "Placas H2D 355x346 (Carbon PET / PEO / PEI 3 modelos)", 30, 6.50, 9.62, 42.00, 77.1),
    
    # Hotends & Boquillas Bambu Lab & H2D (280 hotends)
    ("Hotends & Boquillas", "Hotend Inox Bambu A1 / A1 Mini (0.2 a 0.8mm)", 80, 2.60, 3.85, 18.00, 78.6),
    ("Hotends & Boquillas", "Hotend Hardened Bambu A1 / A1 Mini (0.2 a 0.8mm)", 80, 2.60, 3.85, 22.00, 82.5),
    ("Hotends & Boquillas", "Hotend Laton Brass Heatsink A1 Hardened 0.4", 10, 5.20, 7.70, 28.00, 72.5),
    ("Hotends & Boquillas", "Hotend H2D Standard Hardened (0.2 a 0.8mm)", 80, 3.00, 4.44, 24.00, 81.5),
    ("Hotends & Boquillas", "Hotend H2D High-Flow Integrado (0.4 a 0.8mm)", 30, 5.20, 7.70, 32.00, 75.9),
    
    # Repuestos & Accesorios (210 repuestos)
    ("Repuestos & Accesorios", "Engranajes Extrusor Bambu X1/P1 Hardened Helical", 10, 6.70, 9.92, 24.00, 58.7),
    ("Repuestos & Accesorios", "Wipers Boquilla Silicona Bambu A1 Mini (Set x3)", 50, 0.25, 0.37, 4.00, 90.8),
    ("Repuestos & Accesorios", "Wipers Boquilla Silicona Bambu A1 (Set x3)", 50, 0.25, 0.37, 4.00, 90.8),
    ("Repuestos & Accesorios", "Fundas Silicona Termica Bambu H2D", 100, 0.15, 0.22, 2.50, 91.2)
]

def update_db():
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    
    # Preservar ventas si hubiera, pero reemplazar productos con la proforma exacta
    cur.execute("DELETE FROM products")
    
    total_qty = 0
    total_fob = 0.0
    
    for cat, name, qty, fob, cost_wh, pvp, margin in PROFORMA_GROUPS:
        profit_unit = pvp - cost_wh
        cur.execute("""
        INSERT INTO products (category, name, initial_stock, current_stock, cost_warehouse, pvp_usd, margin_pct, net_profit_unit)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (cat, name, qty, qty, cost_wh, pvp, margin, profit_unit))
        total_qty += qty
        total_fob += qty * fob
        
    conn.commit()
    conn.close()
    print(f"[+] Base de datos actualizada con la Proforma Oficial:")
    print(f"    - Unidades Físicas Exactas: {total_qty}")
    print(f"    - Costo FOB Fábrica Total: ${total_fob:.2f}")

if __name__ == "__main__":
    update_db()
