import sqlite3, json, os, re

def get_color_hex_dict():
    return {
        # Sólidos Básicos
        'Blanco (White)': '#F8F9FA',
        'Blanco Puro (White)': '#FFFFFF',
        'Blanco Mate (White)': '#F0F0F0',
        'Blanco Perlado (Pearl White)': 'linear-gradient(135deg, #FFFFFF, #E0E0E0)',
        'Blanco Traslúcido': 'rgba(255, 255, 255, 0.75)',
        'Negro (Black)': '#141414',
        'Negro Mate (Black)': '#1A1A1A',
        'Negro Seda (Black)': 'linear-gradient(135deg, #2B2B2B, #0D0D0D)',
        'Gris (Gray)': '#757575',
        'Gris Oscuro (Dark Gray)': '#37474F',
        'Rojo (Red)': '#D32F2F',
        'Rojo Mate (Red)': '#C62828',
        'Rojo Rubí (Red)': '#B71C1C',
        'Rojo Flúor (Fluorescent Red)': '#FF1744',
        'Azul (Blue)': '#1565C0',
        'Azul Cielo (Sky Blue)': '#42A5F5',
        'Azul Oscuro (Dark Blue)': '#0D47A1',
        'Azul Zafiro (Blue)': '#1E88E5',
        'Azul Flúor (Fluorescent Blue)': '#00E5FF',
        'Amarillo (Yellow)': '#FDD835',
        'Amarillo Flúor (Fluorescent Yellow)': '#FFFF00',
        'Verde (Green)': '#2E7D32',
        'Verde Esmeralda (Green)': '#00897B',
        'Naranja (Orange)': '#EF6C00',
        'Naranja Cobre (Orange)': '#D84315',
        'Mandarina Flúor (Tangerine)': '#FF6D00',
        'Rosado (Pink)': '#F06292',
        'Morado (Purple)': '#7B1FA2',
        'Púrpura Real (Purple)': '#6A1B9A',
        'Marrón (Brown)': '#5D4037',
        'Beige (Skin)': '#E0C9A6',
        'Tono Piel (Skin Tone)': '#DEB887',
        'Transparente (Transparent)': 'rgba(255, 255, 255, 0.4)',
        'Mármol Piedra (Marble)': 'radial-gradient(circle, #555 10%, #E0E0E0 11%, #E0E0E0 100%)',
        
        # Metálicos y Seda Sólido
        'Oro Imperial (Gold)': 'linear-gradient(135deg, #FFD700, #FFA000)',
        'Oro Viejo (Dark Gold)': 'linear-gradient(135deg, #CFB53B, #8C7823)',
        'Plata Seda (Silver)': 'linear-gradient(135deg, #E0E0E0, #9E9E9E)',
        'Plata Metálico (Silver)': 'linear-gradient(135deg, #ECEFF1, #B0BEC5)',
        'Plata Brillante (Silver Metallic)': 'linear-gradient(135deg, #FFFFFF, #B0BEC5)',
        'Bronce Seda (Bronze)': 'linear-gradient(135deg, #CD7F32, #8C5221)',
        'Cobre (Copper)': 'linear-gradient(135deg, #B87333, #6E3B11)',
        
        # Co-Extrusión Bicolor (Dual)
        'Azul/Verde (Blue-Green)': 'linear-gradient(135deg, #1565C0 50%, #2E7D32 50%)',
        'Azul/Morado (Blue-Purple)': 'linear-gradient(135deg, #1565C0 50%, #7B1FA2 50%)',
        'Rojo/Azul (Red-Blue)': 'linear-gradient(135deg, #D32F2F 50%, #1565C0 50%)',
        'Rojo/Negro (Red-Black)': 'linear-gradient(135deg, #D32F2F 50%, #141414 50%)',
        'Oro/Plata (Gold-Silver)': 'linear-gradient(135deg, #FFD700 50%, #B0BEC5 50%)',
        'Oro/Morado (Gold-Purple)': 'linear-gradient(135deg, #FFD700 50%, #7B1FA2 50%)',
        'Verde/Negro (Green-Black)': 'linear-gradient(135deg, #2E7D32 50%, #141414 50%)',

        # Co-Extrusión Tricolor (Tri)
        'Rojo/Amarillo/Azul': 'linear-gradient(135deg, #D32F2F 33%, #FDD835 33% 66%, #1565C0 66%)',
        'Azul/Verde/Naranja': 'linear-gradient(135deg, #1565C0 33%, #2E7D32 33% 66%, #EF6C00 66%)',
        'Oro/Plata/Cobre': 'linear-gradient(135deg, #FFD700 33%, #B0BEC5 33% 66%, #B87333 66%)',
        'Oro/Verde/Rosa': 'linear-gradient(135deg, #FFD700 33%, #2E7D32 33% 66%, #F06292 66%)',
        'Rojo/Oro/Azul': 'linear-gradient(135deg, #D32F2F 33%, #FFD700 33% 66%, #1565C0 66%)',
        'Rojo/Oro/Morado': 'linear-gradient(135deg, #D32F2F 33%, #FFD700 33% 66%, #7B1FA2 66%)',
        'Negro/Azul/Morado': 'linear-gradient(135deg, #141414 33%, #1565C0 33% 66%, #7B1FA2 66%)',
        'Verde/Morado/Cobre': 'linear-gradient(135deg, #2E7D32 33%, #7B1FA2 33% 66%, #B87333 66%)',

        # Rainbow & Gradientes
        'Macaron Gradient': 'linear-gradient(135deg, #FFB3BA, #FFDFBA, #FFFFBA, #BAFFC9, #BAE1FF)',
        'Pastel Gradient': 'linear-gradient(135deg, #B5EAD7, #C7CEEA, #FFDAC1, #FF9AA2)',
        'Rainbow Gradient': 'linear-gradient(135deg, #E53935, #FB8C00, #FDD835, #43A047, #1E88E5, #8E24AA)',
        'Ice Cream Gradient': 'linear-gradient(135deg, #F8BBD0, #E1BEE7, #D1C4E9, #C5CAE9, #BBDEFB)',

        # Camas Magnéticas
        'PEI Doble Cara 184x184': '#D4AF37',
        'Diamante / Carbon Fiber 257x257': 'radial-gradient(circle, #222 20%, #444 60%, #111 100%)',
        'PEI + PEI Film 257x257': '#E6C200',
        'PEO Chameleon + PEI 257x257': 'linear-gradient(135deg, #00E5FF, #7B1FA2)',
        'Gold PEI Sprayed 257x257': '#FFD700',
        'Diamante + PEO 184x184': '#37474F',
        'Diamante + PEO 257x257': '#263238',
        'Carbon Fiber PET + PEO 355x346': '#1C2833',
        'Doble Carbon PET 355x346': '#17202A',
        'Cold-Stamping 256x256': '#546E7A',
        'Doble PEI 355x346': '#C5A059',

        # Hotends Bambu A1 & H2D
        'Inox 0.2mm': '#CFD8DC',
        'Inox 0.4mm': '#B0BEC5',
        'Inox 0.6mm': '#90A4AE',
        'Inox 0.8mm': '#78909C',
        'Hardened Steel 0.2mm': '#455A64',
        'Hardened Steel 0.4mm': '#37474F',
        'Hardened Steel 0.6mm': '#263238',
        'Hardened Steel 0.8mm': '#1C2321',
        'Brass Heatsink 0.4mm': '#D4AF37',
        'H2D Hardened 0.2mm': '#3E2723',
        'H2D Hardened 0.4mm': '#2C3E50',
        'H2D Hardened 0.6mm': '#1A252F',
        'H2D Hardened 0.8mm': '#11171D',
        'High-Flow Hardened 0.4mm': '#E65100',
        'High-Flow Hardened 0.6mm': '#BF360C',
        'High-Flow Hardened 0.8mm': '#870000',

        # Accesorios
        'Hardened Helical Gear': '#5D6D7E',
        'Silicone Wiper A1 Mini (x3)': '#E0E0E0',
        'Silicone Wiper A1 (x3)': '#ECEFF1',
        'Silicone Sleeve H2D': '#2C3E50'
    }

def sync_crm_database_to_manifest():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.dirname(script_dir) if os.path.basename(script_dir) == 'crm' else script_dir
    db_path = os.path.join(root_dir, 'crm', 'syntra_crm.db')
    manifest_path = os.path.join(root_dir, 'syntraweb', 'lib', 'manifest.js')
    index_path = os.path.join(root_dir, 'syntraweb', 'index.html')

    if not os.path.exists(db_path):
        raise FileNotFoundError(f"No se encontró la base de datos en {db_path}")

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    cur.execute("""
        SELECT id, sku, name, category, color, material_type, initial_stock, current_stock, pvp_usd, pvp_cash_usd, cost_warehouse
        FROM products
        ORDER BY id;
    """)
    rows = cur.fetchall()
    conn.close()

    products_list = []
    for r in rows:
        pid, sku, name, crm_cat, color, mat, init_s, curr_s, pvp_bcv, pvp_cash, cost_w = r
        
        # Categoría para la web
        web_cat = 'filaments'
        crm_cat_lower = (crm_cat or '').lower()
        if 'camas' in crm_cat_lower or 'plates' in crm_cat_lower:
            web_cat = 'plates'
        elif 'hotend' in crm_cat_lower:
            web_cat = 'hotends'
        elif 'repuestos' in crm_cat_lower or 'accesorios' in crm_cat_lower:
            web_cat = 'accessories'
        else:
            web_cat = 'filaments'

        clean_color = color.strip() if color else 'Estándar'
        in_stock = int(curr_s or 0) > 0

        short_desc = f"Insumo original de precisión 3D Kingroon / Syntra Supply en Lechería. Stock físico: {curr_s} unidades."
        if 'CF' in name:
            short_desc = "Compuesto de alta rigidez reforzado con microfibra de carbono. Acabado mate industrial."
        elif 'Silk' in name or 'Seda' in name:
            short_desc = "Acabado brillante sedoso de alta pureza. Ideal para figuras y piezas estéticas."
        elif 'TPU' in name:
            short_desc = "Poliuretano termoplástico Shore 95A flexible con excelente memoria elástica."
        elif 'ASA' in name:
            short_desc = "Polímero de grado intemperie con alta resistencia UV solar y estabilidad térmica."
        elif 'PETG' in name:
            short_desc = "Polímero técnico resistente al impacto y humedad. Excelente fusión interlaminar."
        elif 'PLA' in name:
            short_desc = "Ácido poliláctico virgen de alta fluidez. Optimizado para impresión rápida y AMS."
        elif web_cat == 'plates':
            short_desc = "Placa de impresión magnética texturizada con adherencia superior y desmoldeo en frío."
        elif web_cat == 'hotends':
            short_desc = "Hotend de precisión intercambiable de alto rendimiento para flujo constante."

        products_list.append({
            "id": f"p_{pid:03d}",
            "sku": sku,
            "crm_id": pid,
            "category": web_cat,
            "name": name,
            "brand": "Syntra Supply" if web_cat in ['plates', 'accessories'] else "Kingroon",
            "badge": "Stock Lechería",
            "image": "assets/img/product_placeholder.svg",
            "shortDesc": short_desc,
            "color": clean_color,
            "inStock": in_stock,
            "price_bcv": float(pvp_bcv or 20.0),
            "price": float(pvp_bcv or 20.0),
            "material_type": mat or crm_cat,
            "stock_qty": int(curr_s or 0)
        })

    # Read existing TDS profiles from current manifest.js
    tds_block = ""
    if os.path.exists(manifest_path):
        with open(manifest_path, 'r', encoding='utf-8') as f:
            curr_manifest_text = f.read()
        idx_tds = curr_manifest_text.find('window.syntraTdsData =')
        if idx_tds != -1:
            tds_block = curr_manifest_text[idx_tds:].strip()

    swatches_dict = get_color_hex_dict()

    manifest_obj = {
        "brand": {
            "name": "Syntra Supply",
            "description": "Distribución Mayorista y Directa de Consumibles y Repuestos 3D en Lechería, Venezuela.",
            "warehouseLocation": "Calle Simón Rodríguez, Sector Morro II, Lechería, Estado Anzoátegui",
            "hours": "Lunes a Domingo: 6:00 AM – 11:00 PM (Despacho Continuo)",
            "phoneWhatsApp": "584223446675",
            "bcvRate": 896.12,
            "totalProducts": len(products_list),
            "totalPhysicalStock": sum(p['stock_qty'] for p in products_list)
        },
        "products": products_list
    }

    new_manifest_text = "window.__SYNTRA_SUPPLY__ = " + json.dumps(manifest_obj, indent=2, ensure_ascii=False) + ";\n\n"
    new_manifest_text += "window.colorSwatchHex = " + json.dumps(swatches_dict, indent=2, ensure_ascii=False) + ";\n\n"
    if tds_block:
        new_manifest_text += tds_block + "\n"

    with open(manifest_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write(new_manifest_text)

    # Actualizar index.html
    if os.path.exists(index_path):
        with open(index_path, 'r', encoding='utf-8') as f:
            index_content = f.read()

        index_content = re.sub(r'137 [íIÍ]tems', f'{len(products_list)} Ítems', index_content, flags=re.IGNORECASE)
        index_content = re.sub(r'137 consumibles', f'{len(products_list)} consumibles', index_content, flags=re.IGNORECASE)
        index_content = re.sub(r'137 Ítems Físicos', f'{len(products_list)} Ítems Físicos', index_content, flags=re.IGNORECASE)
        index_content = re.sub(r'Todos los 137 Ítems', f'Todos los {len(products_list)} Ítems', index_content, flags=re.IGNORECASE)
        index_content = re.sub(r'Todo el Stock \(137 Ítems\)', f'Todo el Stock ({len(products_list)} Ítems)', index_content, flags=re.IGNORECASE)
        index_content = re.sub(r'Mostrando 137 de 137', f'Mostrando {len(products_list)} de {len(products_list)}', index_content, flags=re.IGNORECASE)
        index_content = re.sub(r'Cargando 137 Ítems', f'Cargando {len(products_list)} Ítems', index_content, flags=re.IGNORECASE)
        index_content = re.sub(r'Stock Físico de 137 Consumibles', f'Stock Físico de {len(products_list)} Consumibles', index_content, flags=re.IGNORECASE)
        index_content = re.sub(r'1\.750 BOBINAS & 137 ÍTEMS', f'1.750 BOBINAS & {len(products_list)} ÍTEMS', index_content, flags=re.IGNORECASE)
        index_content = index_content.replace('?v=20261109_v6', '?v=20261109_v8')
        index_content = index_content.replace('?v=20261109_v7', '?v=20261109_v8')

        with open(index_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(index_content)

    return len(products_list), sum(p['stock_qty'] for p in products_list)

if __name__ == '__main__':
    cnt, stk = sync_crm_database_to_manifest()
    print(f"[EXITO] Sincronización finalizada: {cnt} productos con {stk} unidades físicas.")
