import os
import sys
import json
import base64
import sqlite3
from PIL import Image
from playwright.sync_api import sync_playwright

print("=== INICIANDO CONSTRUCCIÓN CATÁLOGO FLUIDO 1080p SYNTRA ===")

# Paths
BASE_DIR = r"C:\Users\UNK\Desktop\EXPORT IA\SYNTRA GROUP"
DB_PATH = os.path.join(BASE_DIR, "crm", "syntra_crm.db")
ASSETS_DIR = os.path.join(BASE_DIR, "syntraweb", "assets", "img", "catalog_assets")
BRAIN_DIR = r"C:\Users\UNK\.gemini\antigravity\brain\1fbe410f-c733-4b9d-841e-cf76d3274e44"
SCRATCH_DIR = os.path.join(BRAIN_DIR, "scratch")
HTML_OUT = os.path.join(SCRATCH_DIR, "catalogo_1080p_master.html")
PDF_OUT = os.path.join(BASE_DIR, "crm", "static", "catalogo.pdf")
PDF_OUT_FULL = os.path.join(BASE_DIR, "crm", "static", "catalogo_syntra_supply.pdf")
SYNTRAWEB_PDF = os.path.join(BASE_DIR, "syntraweb", "catalogo.pdf")
SYNTRAWEB_PDF_FULL = os.path.join(BASE_DIR, "syntraweb", "catalogo_syntra_supply.pdf")

# Connect DB
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("SELECT category, material_type, name, color, pvp_usd, pvp_cash_usd, current_stock FROM products ORDER BY category, material_type, color")
all_products = c.fetchall()
conn.close()

products_by_material = {}
for p in all_products:
    cat, mat, name, color, pvp, cash, stock = p
    if mat not in products_by_material:
        products_by_material[mat] = []
    products_by_material[mat].append({
        'category': cat,
        'material_type': mat,
        'name': name,
        'color': color,
        'pvp_usd': pvp,
        'pvp_cash_usd': cash,
        'current_stock': stock
    })

print(f"Productos cargados desde DB: {len(all_products)} SKUs en {len(products_by_material)} categorías")

# Helper to load image as base64
def get_img_base64(filename):
    path = os.path.join(ASSETS_DIR, filename)
    if not os.path.exists(path):
        return ""
    ext = os.path.splitext(filename)[1].lower()
    mime = "image/png" if ext == ".png" else "image/jpeg"
    with open(path, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("utf-8")
    return f"data:{mime};base64,{b64}"

# Images
img_logo = get_img_base64("bambu_pei_golden.jpg") # fallback
# Let's check logo in branding_8k
logo_path = os.path.join(BASE_DIR, "branding_8k", "logo_3d_glow.png")
if os.path.exists(logo_path):
    with open(logo_path, "rb") as f:
        img_logo = "data:image/png;base64," + base64.b64encode(f.read()).decode("utf-8")

img_silk_dual_dragon = get_img_base64("silk_dual_dragon.jpg")
img_plaplus_prints = get_img_base64("plaplus_prints.jpg")
img_tpu_shoe = get_img_base64("tpu_shoe_flex.jpg")
img_petg_prints = get_img_base64("petg_prints_showcase.jpg")
img_petg_toughness = get_img_base64("petg_toughness.jpg")
img_pacf_drone = get_img_base64("pacf_drone_parts.jpg")
img_bambu_hotend = get_img_base64("bambu_a1_hotend.jpg")
img_bambu_hardened = get_img_base64("bambu_hardened_hotend.jpg")
img_bambu_pei = get_img_base64("bambu_pei_golden.jpg")
img_bambu_peo = get_img_base64("bambu_peo_diamond.jpg")
img_h2d_pei = get_img_base64("bambu_h2d_pei.jpg")
img_pla_basic_spool = get_img_base64("pla_basic_spool.jpg")
img_plaplus_spool = get_img_base64("plaplus_spool.jpg")
img_petg_spool = get_img_base64("petg_spool.jpg")
img_silk_single_gold = get_img_base64("silk_single_gold.jpg")
img_silk_tri_showcase = get_img_base64("silk_tri_showcase.jpg")
img_tpu_spool = get_img_base64("tpu_spool.jpg")
img_pacf_spool = get_img_base64("pacf_spool.jpg")
img_matte_prints = get_img_base64("matte_prints.jpg")
img_qr = get_img_base64("whatsapp_qr.png")

# Color mapping helper
def get_base_hex(c):
    c = c.strip().lower()
    mapping = {
        'blanco': '#FFFFFF', 'white': '#FFFFFF', 'black': '#111827', 'negro': '#111827',
        'gris': '#94A3B8', 'silver': '#CBD5E1', 'plata': '#CBD5E1', 'space grey': '#4B5563',
        'rojo': '#EF4444', 'red': '#EF4444', 'azul': '#2563EB', 'blue': '#2563EB',
        'azul cielo': '#38BDF8', 'sky blue': '#38BDF8', 'azul cobalto': '#1D4ED8',
        'verde': '#10B981', 'green': '#10B981', 'verde manzana': '#84CC16',
        'verde militar': '#4D7C0F', 'amarillo': '#FACC15', 'yellow': '#FACC15',
        'naranja': '#F97316', 'orange': '#F97316', 'púrpura': '#8B5CF6', 'purple': '#8B5CF6',
        'magenta': '#D946EF', 'rosa': '#F472B6', 'pink': '#F472B6',
        'oro': '#EAB308', 'gold': '#EAB308', 'cobre': '#F97316', 'copper': '#F97316',
        'bronce': '#CD7F32', 'bronze': '#CD7F32', 'marrón': '#78350F', 'brown': '#78350F',
        'piel': '#FBCFE8', 'beige': '#FDE68A', 'cyan': '#06B6D4', 'turquesa': '#14B8A6'
    }
    for k, v in mapping.items():
        if k in c:
            return v
    return '#64748B'

def get_swatch_css(col_str):
    col_clean = col_str.split('(')[0].strip().lower()
    
    if 'cf' in col_clean or 'carbon' in col_clean or 'fibra de carbono' in col_clean:
        return 'background: repeating-linear-gradient(45deg, #181E29 0, #181E29 3px, #2A364F 3px, #2A364F 6px); border: 1px solid #4B5563;'
    if 'macaron' in col_clean:
        return 'background: linear-gradient(135deg, #FFB3BA, #FFDFBA, #FFFFBA, #BAFFC9, #BAE1FF);'
    if 'pastel' in col_clean:
        return 'background: linear-gradient(135deg, #FAD02C, #F49AC2, #B5EAD7, #C7CEEA);'
    if 'rainbow' in col_clean or 'ice cream' in col_clean or 'candy' in col_clean:
        return 'background: linear-gradient(135deg, #EF4444, #F59E0B, #10B981, #3B82F6, #8B5CF6);'
    if 'mármol' in col_clean or 'marble' in col_clean:
        return 'background: radial-gradient(circle, #CBD5E1 25%, #64748B 26%, #E2E8F0 50%, #475569 51%, #F8FAFC 85%); border: 1px solid #94A3B8;'
    if 'transparente' in col_clean or 'traslúcido' in col_clean:
        return 'background: #1E293B; border: 1.5px dashed #94A3B8;'

    if '/' in col_str:
        parts = col_str.split('(')[0].split('/')
        if len(parts) == 3:
            c1 = get_base_hex(parts[0])
            c2 = get_base_hex(parts[1])
            c3 = get_base_hex(parts[2])
            return f'background: linear-gradient(135deg, {c1} 0%, {c1} 33%, {c2} 33%, {c2} 66%, {c3} 66%, {c3} 100%);'
        elif len(parts) == 2:
            c1 = get_base_hex(parts[0])
            c2 = get_base_hex(parts[1])
            return f'background: linear-gradient(135deg, {c1} 0%, {c1} 50%, {c2} 50%, {c2} 100%);'

    hex_col = get_base_hex(col_clean)
    border = '#4B5563' if hex_col in ['#FFFFFF', '#F8FAFC', '#111827'] else 'transparent'
    return f'background-color: {hex_col}; border: 1px solid {border};'

def render_swatches(items, cols=3):
    html = f'<div style="display: grid; grid-template-columns: repeat({cols}, 1fr); gap: 6px;">'
    for it in items:
        style = get_swatch_css(it['color'])
        html += f'''
        <div style="background: #0E1420; border: 1px solid #1E2838; border-radius: 6px; padding: 5px 8px; display: flex; align-items: center; gap: 8px;">
          <div style="width: 14px; height: 14px; border-radius: 50%; {style} flex-shrink: 0;"></div>
          <div style="font-size: 10.5px; font-weight: 600; color: #E2E8F0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
            {it['color']}
          </div>
        </div>
        '''
    html += '</div>'
    return html

print("Generando HTML optimizado para 1080p exacto...")

# CSS styles for high-performance 1080p catalog
CSS_STYLES = '''
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  -webkit-font-smoothing: antialiased;
}
body {
  background-color: #05070A;
  color: #F8FAFC;
  font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
  margin: 0;
  padding: 0;
}
.page {
  width: 1080px;
  height: 1528px;
  background-color: #080B11;
  position: relative;
  overflow: hidden;
  padding: 36px 44px 28px 44px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  margin: 0 auto;
}
.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 1.5px solid #1E2838;
  padding-bottom: 12px;
}
.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}
.header-brand {
  font-size: 15px;
  font-weight: 900;
  letter-spacing: 0.12em;
  color: #FFFFFF;
}
.header-sub {
  font-size: 9.5px;
  font-weight: 600;
  letter-spacing: 0.15em;
  color: #94A3B8;
  text-transform: uppercase;
}
.header-badge {
  background: #111827;
  border: 1px solid #334155;
  color: #E2E8F0;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 0.1em;
  padding: 5px 12px;
  border-radius: 6px;
  text-transform: uppercase;
}

.page-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 16px 0;
}

.page-footer {
  border-top: 1.5px solid #1E2838;
  padding-top: 12px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 10px;
  font-weight: 600;
  color: #64748B;
  letter-spacing: 0.1em;
  text-transform: uppercase;
}
.footer-highlight {
  color: #94A3B8;
  font-weight: 700;
}

/* Reusable components */
.section-header {
  border-left: 4px solid #38BDF8;
  padding-left: 12px;
  margin-bottom: 12px;
}
.section-title {
  font-size: 19px;
  font-weight: 900;
  color: #FFFFFF;
  letter-spacing: 0.05em;
}
.section-desc {
  font-size: 11px;
  color: #94A3B8;
  margin-top: 2px;
}

.panel-card {
  background: #0D131F;
  border: 1.5px solid #1E2838;
  border-radius: 10px;
  padding: 14px 16px;
}

.card-title-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}
.card-main-title {
  font-size: 16px;
  font-weight: 800;
  color: #FFFFFF;
}
.price-tag {
  background: #162235;
  border: 1px solid #2563EB;
  color: #38BDF8;
  font-family: 'Consolas', monospace;
  font-size: 13px;
  font-weight: 700;
  padding: 4px 10px;
  border-radius: 6px;
}

.data-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 10.5px;
}
.data-table th {
  background: #111827;
  color: #94A3B8;
  font-weight: 700;
  text-align: left;
  padding: 8px 10px;
  border-bottom: 1.5px solid #1E2838;
  letter-spacing: 0.06em;
  text-transform: uppercase;
}
.data-table td {
  padding: 8px 10px;
  border-bottom: 1px solid #162030;
  color: #CBD5E1;
}
.data-table tr:nth-child(even) td {
  background: #0B101A;
}

.badge-tag {
  display: inline-block;
  background: #1E293B;
  color: #94A3B8;
  border: 1px solid #334155;
  font-size: 9px;
  font-weight: 700;
  padding: 2px 7px;
  border-radius: 4px;
}
'''
print("CSS Base compilado.")

# HTML generation functions for each page
def render_header(page_num, total_pages=9):
    return f'''
    <div class="page-header">
      <div class="header-left">
        <div style="width: 28px; height: 28px; border-radius: 6px; background: #1E293B; border: 1.5px solid #475569; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 14px; color: #38BDF8;">S</div>
        <div>
          <div class="header-brand">SYNTRA GROUP</div>
          <div class="header-sub">DIVISIÓN MANUFACTURA ADITIVA & CONSUMIBLES 3D</div>
        </div>
      </div>
      <div class="header-badge">EDICIÓN 2026 • CATÁLOGO MAESTRO</div>
    </div>
    '''

def render_footer(page_num, total_pages=9):
    return f'''
    <div class="page-footer">
      <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
      <div class="footer-highlight">ALMACÉN CENTRAL: LECHERÍA, ESTADO ANZOÁTEGUI</div>
      <div>PÁG. 0{page_num} / 0{total_pages}</div>
    </div>
    '''

# Build Page 1
def build_page_1():
    return f'''
    <div class="page" id="page-1">
      {render_header(1)}
      <div class="page-content">
        
        <!-- Hero Header -->
        <div style="display: flex; flex-direction: column; align-items: center; text-align: center; padding: 6px 0;">
          <img src="{img_logo}" style="width: 100px; height: 100px; border-radius: 20px; border: 2px solid #334155; margin-bottom: 12px; object-fit: cover;" />
          <h1 style="font-size: 40px; font-weight: 900; letter-spacing: 0.04em; color: #FFFFFF; margin-bottom: 4px;">
            SYNTRA SUPPLY
          </h1>
          <div style="font-size: 13px; font-weight: 700; color: #38BDF8; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 6px;">
            DISTRIBUIDOR AUTORIZADO KINGROON • ALMACÉN CENTRAL LECHERÍA
          </div>
          <p style="font-size: 12px; color: #94A3B8; max-width: 680px; line-height: 1.5;">
            El inventario físico más completo de filamentos de grado técnico, placas magnéticas y hotends de alto rendimiento en el oriente venezolano. Stock real verificado con despacho express inmediato.
          </p>
        </div>

        <!-- 3 Feature Photo Cards -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
          <div class="panel-card" style="padding: 0; overflow: hidden;">
            <img src="{img_silk_dual_dragon}" style="width: 100%; height: 210px; object-fit: cover; display: block;" />
            <div style="padding: 12px 14px;">
              <div style="font-size: 13.5px; font-weight: 800; color: #FFFFFF;">PLA Silk Bicolor Coaxial</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 3px;">Brillo metálico perlado y coextrusión continua.</div>
            </div>
          </div>
          <div class="panel-card" style="padding: 0; overflow: hidden;">
            <img src="{img_plaplus_prints}" style="width: 100%; height: 210px; object-fit: cover; display: block;" />
            <div style="padding: 12px 14px;">
              <div style="font-size: 13.5px; font-weight: 800; color: #FFFFFF;">PLA+ High Speed Pro</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 3px;">Precisión geométrica y tolerancia láser ±0.02mm.</div>
            </div>
          </div>
          <div class="panel-card" style="padding: 0; overflow: hidden;">
            <img src="{img_tpu_shoe}" style="width: 100%; height: 210px; object-fit: cover; display: block;" />
            <div style="padding: 12px 14px;">
              <div style="font-size: 13.5px; font-weight: 800; color: #FFFFFF;">TPU 95A Elastómero Flexible</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 3px;">450% de elongación y alta memoria elástica.</div>
            </div>
          </div>
        </div>

        <!-- Metrics Grid -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
          <div class="panel-card" style="text-align: center; padding: 14px 10px;">
            <div style="font-size: 24px; font-weight: 900; color: #FFFFFF;">1.750 UN</div>
            <div style="font-size: 9.5px; font-weight: 700; color: #38BDF8; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px;">Stock Físico Real</div>
          </div>
          <div class="panel-card" style="text-align: center; padding: 14px 10px;">
            <div style="font-size: 24px; font-weight: 900; color: #FFFFFF;">117 SKUs</div>
            <div style="font-size: 9.5px; font-weight: 700; color: #38BDF8; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px;">Variedad Inmediata</div>
          </div>
          <div class="panel-card" style="text-align: center; padding: 14px 10px;">
            <div style="font-size: 24px; font-weight: 900; color: #FFFFFF;">±0.02 mm</div>
            <div style="font-size: 9.5px; font-weight: 700; color: #38BDF8; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px;">Calibración Láser</div>
          </div>
          <div class="panel-card" style="text-align: center; padding: 14px 10px;">
            <div style="font-size: 24px; font-weight: 900; color: #FFFFFF;">15 - 30 MIN</div>
            <div style="font-size: 9.5px; font-weight: 700; color: #38BDF8; letter-spacing: 0.08em; text-transform: uppercase; margin-top: 2px;">Despacho Lechería</div>
          </div>
        </div>

        <!-- Navigation Index (8 sections) -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px; border-bottom: 1px solid #1E2838; padding-bottom: 8px;">
            <div style="font-size: 13px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.08em; text-transform: uppercase;">
              ÍNDICE EJECUTIVO DEL CATÁLOGO & ESTRUCTURA DE PRODUCTO
            </div>
            <div class="badge-tag">GUÍA DE SECCIONES</div>
          </div>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 9px 10px;">
              <div style="font-size: 10px; font-weight: 800; color: #38BDF8;">PÁG. 02 • INFRAESTRUCTURA</div>
              <div style="font-size: 9px; color: #94A3B8; margin-top: 2px;">Almacén Lechería vs pedidos foráneos y matriz de valor.</div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 9px 10px;">
              <div style="font-size: 10px; font-weight: 800; color: #38BDF8;">PÁG. 03 • PLA & PLA+</div>
              <div style="font-size: 9px; color: #94A3B8; margin-top: 2px;">19 colores en stock y guía de perfiles de laminación.</div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 9px 10px;">
              <div style="font-size: 10px; font-weight: 800; color: #38BDF8;">PÁG. 04 • PETG & MATTE</div>
              <div style="font-size: 9px; color: #94A3B8; margin-top: 2px;">22 SKUs mecánicos, hidrofóbicos y piedra mármol.</div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 9px 10px;">
              <div style="font-size: 10px; font-weight: 800; color: #38BDF8;">PÁG. 05 • SILK & BICOLOR</div>
              <div style="font-size: 9px; color: #94A3B8; margin-top: 2px;">18 colores de alto brillo y coextrusión dual.</div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 9px 10px;">
              <div style="font-size: 10px; font-weight: 800; color: #38BDF8;">PÁG. 06 • TRICOLOR & RAINBOW</div>
              <div style="font-size: 9px; color: #94A3B8; margin-top: 2px;">12 variantes artísticas y reglas de orientación.</div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 9px 10px;">
              <div style="font-size: 10px; font-weight: 800; color: #38BDF8;">PÁG. 07 • TPU, ASA & CF</div>
              <div style="font-size: 9px; color: #94A3B8; margin-top: 2px;">Polímeros industriales, flexibles y fibra de carbono.</div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 9px 10px;">
              <div style="font-size: 10px; font-weight: 800; color: #38BDF8;">PÁG. 08 • HARDWARE & CAMAS</div>
              <div style="font-size: 9px; color: #94A3B8; margin-top: 2px;">31 repuestos, camas magnéticas PEI y hotends.</div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 9px 10px;">
              <div style="font-size: 10px; font-weight: 800; color: #38BDF8;">PÁG. 09 • PACKS & PEDIDOS</div>
              <div style="font-size: 9px; color: #94A3B8; margin-top: 2px;">Modalidades de pago, precios mayoristas y WhatsApp.</div>
            </div>
          </div>
        </div>

        <!-- Banner Syntra Local -->
        <div class="panel-card" style="background: #0B111D; border-color: #2563EB; display: flex; justify-content: space-between; align-items: center; padding: 14px 20px;">
          <div>
            <div style="font-size: 14px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.04em;">
              TU TALLER 3D EN LECHERÍA, SIN INTERRUPCIONES NI FLETES COSTOSOS
            </div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 3px;">
              Retiro inmediato en almacén central o delivery express en Lechería, PLC y Barcelona. Envíos nacionales por MRW, Tealca y Zoom.
            </div>
          </div>
          <div style="background: #1D4ED8; color: #FFFFFF; font-size: 12px; font-weight: 800; padding: 8px 16px; border-radius: 6px; white-space: nowrap; letter-spacing: 0.05em;">
            WA: +58 422-3446675
          </div>
        </div>

      </div>
      {render_footer(1)}
    </div>
    '''

print("Función Page 1 definida.")

# Build Page 2
def build_page_2():
    return f'''
    <div class="page" id="page-2">
      {render_header(2)}
      <div class="page-content">
        
        <div class="section-header">
          <div class="section-title">01 / INFRAESTRUCTURA & RESPALDO LOCAL</div>
          <div class="section-desc">Por qué Syntra Group es el socio logístico estratégico de las granjas de impresión y creadores del oriente venezolano.</div>
        </div>

        <!-- 3 Pillars Grid -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
          <div class="panel-card" style="padding: 0; overflow: hidden;">
            <img src="{img_pla_basic_spool}" style="width: 100%; height: 160px; object-fit: cover; display: block;" />
            <div style="padding: 12px 14px;">
              <div style="font-size: 13.5px; font-weight: 800; color: #FFFFFF;">Stock Físico Inmediato</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 3px; line-height: 1.4;">
                1.750 rollos en almacén climatizado de Lechería. Retiras en 15 minutos o recibes el mismo día.
              </div>
            </div>
          </div>
          <div class="panel-card" style="padding: 0; overflow: hidden;">
            <img src="{img_bambu_hotend}" style="width: 100%; height: 160px; object-fit: cover; display: block;" />
            <div style="padding: 12px 14px;">
              <div style="font-size: 13.5px; font-weight: 800; color: #FFFFFF;">Respaldo de Repuestos</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 3px; line-height: 1.4;">
                Hotends, boquillas y camas PEI originales en stock. Tu taller nunca se detiene por falta de piezas.
              </div>
            </div>
          </div>
          <div class="panel-card" style="padding: 0; overflow: hidden;">
            <img src="{img_pacf_drone}" style="width: 100%; height: 160px; object-fit: cover; display: block;" />
            <div style="padding: 12px 14px;">
              <div style="font-size: 13.5px; font-weight: 800; color: #FFFFFF;">Asesoría Técnica Maker</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 3px; line-height: 1.4;">
                Ingenieros con experiencia real en impresión 3D para calibrar perfiles, temperaturas y retracción.
              </div>
            </div>
          </div>
        </div>

        <!-- Comparison Table -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
            <div style="font-size: 13.5px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              MATRIZ DE VALOR: SYNTRA LECHERÍA VS PROVEEDORES DE CARACAS
            </div>
            <div class="badge-tag">VENTAJA LOGÍSTICA REAL</div>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th style="width: 25%;">Variable Operativa</th>
                <th style="width: 40%; color: #38BDF8;">Syntra Supply (Almacén Lechería)</th>
                <th style="width: 35%;">Distribuidores Caracas / ML</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Disponibilidad de Entrega</td>
                <td style="color: #38BDF8; font-weight: 700;">Inmediata hoy mismo (15 a 30 min)</td>
                <td>3 a 5 días hábiles de espera</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Costo de Flete / Encomienda</td>
                <td style="color: #38BDF8; font-weight: 700;">$0.00 (Retiro gratis en Lechería)</td>
                <td>$5.00 a $12.00 adicionales por bobina</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Riesgo de Transporte Terrestre</td>
                <td style="color: #38BDF8; font-weight: 700;">Cero riesgo. Trato directo en mano</td>
                <td>Riesgo de extravío, golpes y cajas mojadas</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Métodos de Pago Aceptados</td>
                <td style="color: #38BDF8; font-weight: 700;">USDT Binance Pay, Efectivo $, Bs BCV, Zelle</td>
                <td>Restricciones cambiarias y recargos altos</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Garantía de Fábrica Directa</td>
                <td style="color: #38BDF8; font-weight: 700;">Cambio inmediato en tienda local</td>
                <td>Envíos de retorno costosos y semanas de espera</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Soporte Técnico Presencial</td>
                <td style="color: #38BDF8; font-weight: 700;">Personalizado por makers en persona</td>
                <td>Respuestas genéricas o bots de mensajería</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Quality Control Protocol -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 12px;">
            <div style="font-size: 13px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              PROTOCOLO DE CALIDAD & ALMACENAMIENTO INDUSTRIAL
            </div>
            <div class="badge-tag">ESTÁNDAR KINGROON OFICIAL</div>
          </div>
          <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 10px;">
              <div style="font-size: 11px; font-weight: 800; color: #38BDF8;">Sellado al Vacío</div>
              <div style="font-size: 9.5px; color: #94A3B8; margin-top: 3px; line-height: 1.35;">
                Empaque hermético aluminizado directo de fábrica para cero absorción de humedad.
              </div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 10px;">
              <div style="font-size: 11px; font-weight: 800; color: #38BDF8;">Desecante Activo</div>
              <div style="font-size: 9.5px; color: #94A3B8; margin-top: 3px; line-height: 1.35;">
                Cada bobina incluye bolsa de gel de sílice activa para preservar propiedades mecánicas.
              </div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 10px;">
              <div style="font-size: 11px; font-weight: 800; color: #38BDF8;">Bobinado CNC 100%</div>
              <div style="font-size: 9.5px; color: #94A3B8; margin-top: 3px; line-height: 1.35;">
                Bobinado robotizado capa por capa que garantiza cero cruces y cero paradas de extrusión.
              </div>
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 10px;">
              <div style="font-size: 11px; font-weight: 800; color: #38BDF8;">Láser Coaxial ±0.02</div>
              <div style="font-size: 9.5px; color: #94A3B8; margin-top: 3px; line-height: 1.35;">
                Medición continua de diámetro para flujo uniforme y capas superficiales perfectas.
              </div>
            </div>
          </div>
        </div>

        <!-- Logistics Coverage Banner -->
        <div class="panel-card" style="background: #0B111D; border-color: #2563EB; display: flex; justify-content: space-between; align-items: center; padding: 12px 18px;">
          <div style="font-size: 12px; color: #CBD5E1; line-height: 1.4;">
            <strong style="color: #FFFFFF;">COBERTURA LOGÍSTICA COMPLETA:</strong> Retiro en Almacén Lechería (15-30 min) • Delivery express en Lechería, Puerto La Cruz y Barcelona • Envíos a todo el país vía MRW, Tealca y Zoom con guías rastreables en tiempo real.
          </div>
          <div class="price-tag" style="white-space: nowrap; margin-left: 14px;">DESPACHO HOY MISMO</div>
        </div>

      </div>
      {render_footer(2)}
    </div>
    '''

# Build Page 3
def build_page_3():
    pla_basic_items = products_by_material.get('PLA Basic', [])
    plaplus_items = products_by_material.get('PLA+ Alta Resistencia', [])
    
    return f'''
    <div class="page" id="page-3">
      {render_header(3)}
      <div class="page-content">
        
        <div class="section-header">
          <div class="section-title">02 / FILAMENTOS BÁSICOS & ALTA VELOCIDAD</div>
          <div class="section-desc">Polímeros de alta estabilidad térmica y tolerancia geométrica para prototipado rápido, maquetas y producción continua.</div>
        </div>

        <!-- PLA Basic Panel -->
        <div class="panel-card">
          <div class="card-title-row">
            <div>
              <div class="card-main-title">PLA Basic Estándar Kingroon (12 Colores en Stock)</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 2px;">
                1.75mm • 1.0 kg neto • Densidad 1.24 g/cm³ • Temp Nozzle: 190 - 220 °C • Temp Cama: 50 - 60 °C
              </div>
            </div>
            <div class="price-tag">Ref. $20.00 BCV</div>
          </div>
          <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 12px;">
            <img src="{img_pla_basic_spool}" style="width: 130px; height: 110px; object-fit: cover; border-radius: 8px; border: 1px solid #1E293B;" />
            <div style="flex: 1; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
              Fabricado a base de almidón de maíz biodegradable. Mínima contracción térmica, excelente adhesión entre capas y acabado satinado uniforme. Ideal para piezas de exhibición, figuras, moldes y piezas arquitectónicas sin alabeo.
              <div style="margin-top: 6px; color: #38BDF8; font-weight: 700;">
                ★ Descuento directo en divisa limpia (Binance Pay USDT / Efectivo $) al consultar por WhatsApp.
              </div>
            </div>
          </div>
          {render_swatches(pla_basic_items, cols=3)}
        </div>

        <!-- PLA+ High Speed Panel -->
        <div class="panel-card">
          <div class="card-title-row">
            <div>
              <div class="card-main-title">PLA+ High Speed Pro (7 Colores en Stock)</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 2px;">
                1.75mm • 1.0 kg neto • Resistencia al impacto 5x • Velocidad hasta 500 mm/s • Temp Nozzle: 205 - 230 °C
              </div>
            </div>
            <div class="price-tag">Ref. $21.50 BCV</div>
          </div>
          <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 12px;">
            <img src="{img_plaplus_spool}" style="width: 130px; height: 105px; object-fit: cover; border-radius: 8px; border: 1px solid #1E293B;" />
            <div style="flex: 1; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
              Modificado con elastómeros técnicos para conferir hasta 5 veces mayor resistencia al impacto que el PLA estándar. Diseñado para impresoras de alta aceleración como Bambu Lab X1/P1/A1, Creality K1 y Voron.
            </div>
          </div>
          {render_swatches(plaplus_items, cols=3)}
        </div>

        <!-- Slicer Guide -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 12.5px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              GUÍA DE LAMINACIÓN RECOMENDADA (BAMBU STUDIO / ORCASLICER / CURA)
            </div>
            <div class="badge-tag">PARÁMETROS TESTEADOS</div>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Material</th>
                <th>Temp. Boquilla</th>
                <th>Temp. Cama (PEI)</th>
                <th>Caudal Volumétrico</th>
                <th>Ventilador de Capa</th>
                <th>Retracción Recomendada</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">PLA Basic</td>
                <td>200 - 215 °C</td>
                <td>50 - 55 °C</td>
                <td>18 - 22 mm³/s</td>
                <td>100% (desde capa 2)</td>
                <td>0.8 mm (Direct) / 4.5 mm (Bowden)</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">PLA+ High Speed</td>
                <td>215 - 230 °C</td>
                <td>55 - 60 °C</td>
                <td>22 - 28 mm³/s</td>
                <td>100% (desde capa 2)</td>
                <td>0.6 - 0.8 mm (Direct Drive)</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
      {render_footer(3)}
    </div>
    '''

print("Funciones Page 2 y 3 definidas.")

# Build Page 4
def build_page_4():
    petg_items = products_by_material.get('PETG Basic', [])
    pla_matte = products_by_material.get('PLA Matte', [])
    petg_matte = products_by_material.get('PETG Matte', [])
    pla_marble = products_by_material.get('PLA Marble', [])
    special_items = pla_matte + petg_matte + pla_marble
    
    return f'''
    <div class="page" id="page-4">
      {render_header(4)}
      <div class="page-content">
        
        <div class="section-header">
          <div class="section-title">03 / RESISTENCIA QUÍMICA & ACABADOS ESPECIALES</div>
          <div class="section-desc">Termoplásticos de ingeniería para exteriores y polímeros de textura mate antirreflejo y mármol mineral.</div>
        </div>

        <!-- PETG Basic Panel -->
        <div class="panel-card">
          <div class="card-title-row">
            <div>
              <div class="card-main-title">PETG Basic Grado Técnico (17 Colores en Stock)</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 2px;">
                1.75mm • 1.0 kg neto • Hidrofóbico • Temp Nozzle: 225 - 250 °C • Temp Cama: 70 - 80 °C
              </div>
            </div>
            <div class="price-tag">Ref. $19.50 BCV</div>
          </div>
          <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 10px;">
            <img src="{img_petg_spool}" style="width: 125px; height: 100px; object-fit: cover; border-radius: 8px; border: 1px solid #1E293B;" />
            <div style="flex: 1; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
              Combina la facilidad de impresión del PLA con la resistencia mecánica y térmica del ABS. No absorbe humedad con facilidad, resiste químicos corrosivos, aceites y exposición continua a luz solar exterior.
              <div style="margin-top: 4px; color: #38BDF8; font-weight: 700;">
                ★ Opción predilecta para soportes de taller, piezas mecánicas y carcasas de electrónica marina en Lechería.
              </div>
            </div>
          </div>
          {render_swatches(petg_items, cols=3)}
        </div>

        <!-- Special Filaments Panel -->
        <div class="panel-card">
          <div class="card-title-row">
            <div>
              <div class="card-main-title">Filamentos de Acabado Especial (Matte & Mármol Mineral)</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 2px;">
                5 Variantes estéticas para arquitectura, interiorismo y disimulo total de líneas de capa
              </div>
            </div>
            <div class="price-tag">Ref. $21.50 - $22.50 BCV</div>
          </div>
          <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 10px;">
            <img src="{img_matte_prints}" style="width: 125px; height: 95px; object-fit: cover; border-radius: 8px; border: 1px solid #1E293B;" />
            <div style="flex: 1; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
              <strong>PLA & PETG Matte:</strong> Textura micro-porosa antirreflejo de tacto cerámico suave.<br/>
              <strong>PLA Mármol Granito:</strong> Matriz mineral con motas oscuras que recrea piedra natural pulida.
            </div>
          </div>
          {render_swatches(special_items, cols=3)}
        </div>

        <!-- Mechanical Matrix Table -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 12.5px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              MATRIZ DE SELECCIÓN MECÁNICA Y TÉRMICA COMPARADA
            </div>
            <div class="badge-tag">GUÍA TÉCNICA</div>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Polímero</th>
                <th>Resistencia Mecánica</th>
                <th>Temp. Deflexión (HDT)</th>
                <th>Resistencia a Intemperie</th>
                <th>Acabado Superficial</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">PLA Basic</td>
                <td>Media (55 MPa)</td>
                <td>52 - 55 °C</td>
                <td>Baja (Exclusivo Interiores)</td>
                <td>Satinado estándar</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">PLA+ High Speed</td>
                <td>Alta (68 MPa)</td>
                <td>55 - 58 °C</td>
                <td>Media</td>
                <td>Semibrillante suave</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">PETG Basic</td>
                <td>Muy Alta (75 MPa)</td>
                <td>72 - 78 °C</td>
                <td>Alta (Apto Sol y Lluvia)</td>
                <td>Brillante / Translúcido</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">PLA / PETG Matte</td>
                <td>Media-Alta</td>
                <td>55 °C / 75 °C</td>
                <td>Media / Alta</td>
                <td>Mate Cerámico Antirreflejo</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">PLA Mármol</td>
                <td>Media (52 MPa)</td>
                <td>54 - 56 °C</td>
                <td>Baja</td>
                <td>Piedra Esculpida Granítica</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
      {render_footer(4)}
    </div>
    '''

# Build Page 5
def build_page_5():
    silk_solid = products_by_material.get('PLA Silk Sólido', [])
    silk_bi = products_by_material.get('PLA Silk Bicolor', [])
    
    return f'''
    <div class="page" id="page-5">
      {render_header(5)}
      <div class="page-content">
        
        <div class="section-header">
          <div class="section-title">04 / FILAMENTOS SILK ACABADO METÁLICO & COEXTRUSIÓN</div>
          <div class="section-desc">Efecto sedoso de alto reflejo especular y coextrusión bicromática continua para piezas de diseño y trofeos.</div>
        </div>

        <!-- Silk Solid Panel -->
        <div class="panel-card">
          <div class="card-title-row">
            <div>
              <div class="card-main-title">PLA Silk Sólido Brillo Metálico (11 Colores en Stock)</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 2px;">
                1.75mm • 1.0 kg neto • Reflejo espejo • Temp Nozzle: 205 - 225 °C • Temp Cama: 55 - 60 °C
              </div>
            </div>
            <div class="price-tag">Ref. $24.00 BCV</div>
          </div>
          <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 10px;">
            <img src="{img_silk_single_gold}" style="width: 130px; height: 105px; object-fit: cover; border-radius: 8px; border: 1px solid #1E293B;" />
            <div style="flex: 1; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
              Polímero adicionado con modificadores ópticos que multiplican la reflectividad lumínica, ocultando completamente las líneas de capa verticales. Perfecto para galardones, joyería, litofanias decorativas y réplicas de metales nobles.
              <div style="margin-top: 4px; color: #38BDF8; font-weight: 700;">
                ★ Oro Imperial Kingroon: El filamento más solicitado para reconocimientos institucionales y piezas de lujo.
              </div>
            </div>
          </div>
          {render_swatches(silk_solid, cols=3)}
        </div>

        <!-- Silk Bicolor Panel -->
        <div class="panel-card">
          <div class="card-title-row">
            <div>
              <div class="card-main-title">PLA Silk Bicolor Coaxial (7 Combinaciones Dual en Stock)</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 2px;">
                1.75mm • 1.0 kg neto • Coextrusión longitudinal 50/50 • Cambio cromático dinámico al rotar la pieza
              </div>
            </div>
            <div class="price-tag">Ref. $27.00 BCV</div>
          </div>
          <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 10px;">
            <img src="{img_silk_dual_dragon}" style="width: 130px; height: 105px; object-fit: cover; border-radius: 8px; border: 1px solid #1E293B;" />
            <div style="flex: 1; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
              Dos polímeros de distinto color extruidos en paralelo dentro del mismo filamento. Al imprimir, la pieza muestra un tono en una cara y otro en la cara opuesta, creando un efecto tornasol cinético impresionante al girar o cambiar de luz.
            </div>
          </div>
          {render_swatches(silk_bi, cols=3)}
        </div>

        <!-- Silk Printing Guide -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 12.5px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              GUÍA DE TALLER: CÓMO MAXIMIZAR EL BRILLO ESPEJO EN FILAMENTOS SILK
            </div>
            <div class="badge-tag">REGLA DE ACABADO</div>
          </div>
          <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; font-size: 10px; color: #CBD5E1;">
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 10px;">
              <div style="font-weight: 800; color: #38BDF8; margin-bottom: 3px;">1. Velocidad de Muro Exterior</div>
              Reducir la velocidad del perímetro exterior a <strong>40 - 60 mm/s</strong>. A menor velocidad, mayor es la orientación molecular reflectiva y más intenso el brillo de espejo.
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 10px;">
              <div style="font-weight: 800; color: #38BDF8; margin-bottom: 3px;">2. Temperatura de Boquilla</div>
              Imprimir a <strong>215 - 225 °C</strong> (5-10°C por encima del PLA regular). Una mayor temperatura funde mejor los modificadores sedosos y evita acabados mates lechosos.
            </div>
            <div style="background: #111723; border: 1px solid #1E293B; border-radius: 6px; padding: 10px;">
              <div style="font-weight: 800; color: #38BDF8; margin-bottom: 3px;">3. Orientación en Bicolor</div>
              Alinear la costura de capa (seam) en la parte trasera del modelo para que la división cromática bicromática quede perfectamente simétrica en los laterales frontal y posterior.
            </div>
          </div>
        </div>

      </div>
      {render_footer(5)}
    </div>
    '''

# Build Page 6
def build_page_6():
    silk_tri = products_by_material.get('PLA Silk Tricolor', [])
    silk_rainbow = products_by_material.get('PLA Silk Rainbow', [])
    
    return f'''
    <div class="page" id="page-6">
      {render_header(6)}
      <div class="page-content">
        
        <div class="section-header">
          <div class="section-title">05 / FILAMENTOS SILK TRICOLOR & RAINBOW GRADIENTE</div>
          <div class="section-desc">Efectos tridimensionales de 3 colores simultáneos y gradientes secuenciales cromáticos para obras de arte.</div>
        </div>

        <!-- Silk Tricolor Panel -->
        <div class="panel-card">
          <div class="card-title-row">
            <div>
              <div class="card-main-title">PLA Silk Tricolor Coextruido (8 Variantes en Stock)</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 2px;">
                1.75mm • 1.0 kg neto • 3 filamentos fundidos a 120° en un solo hilo • Cambio tricromático continuo
              </div>
            </div>
            <div class="price-tag">Ref. $27.00 BCV</div>
          </div>
          <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 10px;">
            <img src="{img_silk_tri_showcase}" style="width: 130px; height: 105px; object-fit: cover; border-radius: 8px; border: 1px solid #1E293B;" />
            <div style="flex: 1; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
              La máxima evolución de la tecnología de coextrusión Kingroon. Tres filamentos independientes fusionados a 120 grados dentro de una sola hebra. La pieza impresa ofrece una transición de 3 colores según el ángulo de observación y la posición de las fuentes de luz.
            </div>
          </div>
          {render_swatches(silk_tri, cols=3)}
        </div>

        <!-- Silk Rainbow Panel -->
        <div class="panel-card">
          <div class="card-title-row">
            <div>
              <div class="card-main-title">PLA Silk Rainbow Gradiente Longitudinal (4 Variantes en Stock)</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 2px;">
                1.75mm • 1.0 kg neto • Transición gradual por metros • Excelente para jarrones, esculturas y dragones
              </div>
            </div>
            <div class="price-tag">Ref. $27.00 BCV</div>
          </div>
          <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 10px;">
            <img src="{img_silk_single_gold}" style="width: 130px; height: 100px; object-fit: cover; border-radius: 8px; border: 1px solid #1E293B;" />
            <div style="flex: 1; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
              El color evoluciona suavemente a lo largo del filamento sin saltos bruscos. Variantes en stock: Pastel Rainbow (tonos suaves), Fast Rainbow (cambio cada 10-15 metros), Macaron Rainbow (tonos pastel cremosos) y Candy Rainbow (tonos frutales vibrantes).
            </div>
          </div>
          {render_swatches(silk_rainbow, cols=3)}
        </div>

        <!-- Tricolor vs Rainbow Comparison -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 12.5px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              COMPARATIVA DE APLICACIÓN: TRICOLOR COEXTRUIDO VS RAINBOW LONGITUDINAL
            </div>
            <div class="badge-tag">CRITERIO DE DISEÑO</div>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Factor</th>
                <th>Silk Tricolor Coextruido</th>
                <th>Silk Rainbow Gradiente</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Dirección del Cambio</td>
                <td>Radial (360° en el plano horizontal X/Y)</td>
                <td>Vertical (progresivo a lo largo de la altura Z)</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Tamaño Mínimo de Pieza</td>
                <td>Visible desde piezas pequeñas (10 gramos en adelante)</td>
                <td>Requiere modelos de medianos a grandes (> 120-150 gramos)</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Uso Recomendado</td>
                <td>Miniaturas, bustos, dragones articulados, trofeos</td>
                <td>Jarrones en modo espiral (vase mode), lámparas, arte decorativo</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Patrón de Relleno Óptimo</td>
                <td>Gyroid al 10% - 15% para soporte uniforme</td>
                <td>Lineal o Gyroid al 10%</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
      {render_footer(6)}
    </div>
    '''

print("Funciones Page 4, 5 y 6 definidas.")

# Build Page 7
def build_page_7():
    tpu_items = products_by_material.get('TPU 95A Flexible', [])
    asa_items = products_by_material.get('ASA Basic Solar UV', [])
    petg_cf = products_by_material.get('PETG-CF Fibra de Carbono', [])
    pla_cf = products_by_material.get('PLA-CF Fibra de Carbono', [])
    cf_items = petg_cf + pla_cf
    
    return f'''
    <div class="page" id="page-7">
      {render_header(7)}
      <div class="page-content">
        
        <div class="section-header">
          <div class="section-title">06 / POLÍMEROS INDUSTRIALES, FLEXIBLES & COMPUESTOS</div>
          <div class="section-desc">Materiales técnicos de ingeniería para amortiguación, intemperie solar severa y rigidez aeroespacial.</div>
        </div>

        <!-- TPU 95A Panel -->
        <div class="panel-card">
          <div class="card-title-row">
            <div>
              <div class="card-main-title">TPU 95A Poliuretano Termoplástico Flexible (10 Colores en Stock)</div>
              <div style="font-size: 10.5px; color: #94A3B8; margin-top: 2px;">
                1.75mm • 1.0 kg neto • Dureza Shore 95A • 450% de elongación • Temp Nozzle: 215 - 235 °C • Temp Cama: 40 - 55 °C
              </div>
            </div>
            <div class="price-tag">Ref. $28.50 BCV</div>
          </div>
          <div style="display: flex; gap: 14px; align-items: center; margin-bottom: 10px;">
            <img src="{img_tpu_shoe}" style="width: 130px; height: 100px; object-fit: cover; border-radius: 8px; border: 1px solid #1E293B;" />
            <div style="flex: 1; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
              Elastómero de alta resiliencia con excelente memoria de retorno elástico y resistencia extrema al desgaste por abrasión e impacto repetitivo. Apto para juntas de sellado, amortiguadores de vibración para drones, fundas protectoras, calzado y correas.
              <div style="margin-top: 4px; color: #38BDF8; font-weight: 700;">
                ★ 10 Colores disponibles en Lechería: Negro, Blanco, Rojo, Azul, Verde, Amarillo, Naranja, Púrpura, Gris y Transparente.
              </div>
            </div>
          </div>
          {render_swatches(tpu_items, cols=3)}
        </div>

        <!-- ASA & Carbon Fiber Dual Grid -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <!-- ASA Card -->
          <div class="panel-card">
            <div class="card-title-row">
              <div>
                <div class="card-main-title" style="font-size: 14.5px;">ASA Basic Solar UV (3 Colores)</div>
                <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">
                  1.75mm • 1.0 kg • Temp Nozzle: 240 - 260 °C • Temp Cama: 90 - 100 °C
                </div>
              </div>
              <div class="price-tag" style="font-size: 11px;">Ref. $28.50 BCV</div>
            </div>
            <div style="font-size: 10px; color: #CBD5E1; line-height: 1.4; margin-bottom: 8px;">
              Evolución directa del ABS con sustitución acrílica. Inmune a la radiación ultravioleta del sol venezolano (no amarillea ni se vuelve quebradizo). Ideal para accesorios náuticos en Lechería y piezas exteriores automotrices.
            </div>
            {render_swatches(asa_items, cols=2)}
          </div>

          <!-- Carbon Fiber Card -->
          <div class="panel-card">
            <div class="card-title-row">
              <div>
                <div class="card-main-title" style="font-size: 14.5px;">Fibra de Carbono (PETG-CF / PLA-CF)</div>
                <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">
                  1.75mm • 1.0 kg • Microfibras de carbono al 15% • Rigidez extrema
                </div>
              </div>
              <div class="price-tag" style="font-size: 11px;">Ref. $42.00 BCV</div>
            </div>
            <div style="font-size: 10px; color: #CBD5E1; line-height: 1.4; margin-bottom: 8px;">
              Reforzado con microfibras de carbono de módulo elástico ultra-alto. Cero deformación dimensional (alabeo), acabado mate antracita de nivel automotriz y gran tolerancia mecánica. Requiere boquilla de acero endurecido.
            </div>
            {render_swatches(cf_items, cols=2)}
          </div>
        </div>

        <!-- Industrial Parameters Table -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 12.5px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              PROTOCOLO TÉCNICO DE EXTRUSIÓN PARA POLÍMEROS AVANZADOS
            </div>
            <div class="badge-tag">MANDATORIO EN TALLER</div>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Polímero</th>
                <th>Tipo de Boquilla</th>
                <th>Temp. Extrusión</th>
                <th>Temp. Cama</th>
                <th>Tratamiento de Secado</th>
                <th>Entorno de Impresión</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">TPU 95A Flexible</td>
                <td>Latón o Acero (0.4mm)</td>
                <td>220 - 235 °C</td>
                <td>40 - 50 °C</td>
                <td>Secado a 55 °C por 6h si hay humedad</td>
                <td>Extrusor directo obligatorio, velocidad 25-40 mm/s</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">ASA Solar UV</td>
                <td>Latón o Acero (0.4mm)</td>
                <td>245 - 260 °C</td>
                <td>95 - 105 °C</td>
                <td>Secado a 70 °C por 4h previo uso</td>
                <td>Cámara cerrada obligatoria (cero corrientes de aire)</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Fibra de Carbono (CF)</td>
                <td style="color: #38BDF8; font-weight: 700;">Acero Endurecido (0.4 - 0.6mm)</td>
                <td>240 - 265 °C</td>
                <td>70 - 80 °C</td>
                <td>Secado a 65 °C por 8h</td>
                <td>Baja retracción, boquilla resistente a la abrasión</td>
              </tr>
            </tbody>
          </table>
        </div>

      </div>
      {render_footer(7)}
    </div>
    '''

# Build Page 8
def build_page_8():
    return f'''
    <div class="page" id="page-8">
      {render_header(8)}
      <div class="page-content">
        
        <div class="section-header">
          <div class="section-title">07 / HARDWARE, REPUESTOS & SUPERFICIES DE IMPRESIÓN</div>
          <div class="section-desc">Camas magnéticas flexibles de alta adherencia y hotends ensamblados para Bambu Lab y Kingroon con entrega inmediata en Lechería.</div>
        </div>

        <!-- 3 Hardware Photo Cards -->
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px;">
          <div class="panel-card" style="padding: 0; overflow: hidden;">
            <img src="{img_bambu_hardened}" style="width: 100%; height: 140px; object-fit: cover; display: block;" />
            <div style="padding: 10px 12px;">
              <div style="font-size: 13px; font-weight: 800; color: #FFFFFF;">Hotends Bambu Lab A1 / Mini</div>
              <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">Sistema de cambio rápido con clip magnético. 0.2 a 0.8mm.</div>
            </div>
          </div>
          <div class="panel-card" style="padding: 0; overflow: hidden;">
            <img src="{img_bambu_pei}" style="width: 100%; height: 140px; object-fit: cover; display: block;" />
            <div style="padding: 10px 12px;">
              <div style="font-size: 13px; font-weight: 800; color: #FFFFFF;">Placas PEI Texturizado Doble Cara</div>
              <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">Adhesión insuperable sin adhesivos y liberación automática al enfriar.</div>
            </div>
          </div>
          <div class="panel-card" style="padding: 0; overflow: hidden;">
            <img src="{img_bambu_peo}" style="width: 100%; height: 140px; object-fit: cover; display: block;" />
            <div style="padding: 10px 12px;">
              <div style="font-size: 13px; font-weight: 800; color: #FFFFFF;">Superficies PEO Diamante & PET</div>
              <div style="font-size: 10px; color: #94A3B8; margin-top: 2px;">Transfieren patrones prismáticos y textura de carbono a la base.</div>
            </div>
          </div>
        </div>

        <!-- Magnetic Beds Table -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 12.5px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              CAMAS MAGNÉTICAS FLEXIBLES DE RESORTE DE ACERO (11 MODELOS EN STOCK)
            </div>
            <div class="badge-tag">REPUESTOS ORIGINALES</div>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Plataforma Compatible</th>
                <th>Dimensiones</th>
                <th>Tipo de Superficie / Acabado</th>
                <th>Adherencia</th>
                <th>Ref. Lista BCV</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Bambu Lab A1 Mini</td>
                <td>180 x 180 mm</td>
                <td>PEI Texturizado Oro Doble Cara</td>
                <td style="color: #38BDF8;">Excelente (Sin pegamento)</td>
                <td style="font-weight: 700; color: #38BDF8;">$22.00</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Bambu Lab A1 Mini</td>
                <td>180 x 180 mm</td>
                <td>PEO Diamante Holográfico + Smooth</td>
                <td style="color: #38BDF8;">Patrón transferible</td>
                <td style="font-weight: 700; color: #38BDF8;">$24.00</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Bambu Lab X1 / P1 / A1</td>
                <td>257 x 257 mm</td>
                <td>PEI Texturizado Oro Doble Cara</td>
                <td style="color: #38BDF8;">Uso rudo para granja</td>
                <td style="font-weight: 700; color: #38BDF8;">$28.00</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Bambu Lab X1 / P1 / A1</td>
                <td>257 x 257 mm</td>
                <td>PEO Diamante + PET Carbon Texture</td>
                <td style="color: #38BDF8;">Doble textura estética</td>
                <td style="font-weight: 700; color: #38BDF8;">$32.00</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Kingroon H2D / Gran Formato</td>
                <td>310 x 310 mm</td>
                <td>PEI Texturizado Industrial Doble Cara</td>
                <td style="color: #38BDF8;">Máxima área de trabajo</td>
                <td style="font-weight: 700; color: #38BDF8;">$35.00</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- Hotends & Accessories Table -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 12.5px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              HOTENDS COMPLETOS, BOQUILLAS DE ALTO RENDIMIENTO & MANTENIMIENTO (20 SKUs)
            </div>
            <div class="badge-tag">REPUESTOS CRÍTICOS</div>
          </div>
          <table class="data-table">
            <thead>
              <tr>
                <th>Componente</th>
                <th>Compatibilidad</th>
                <th>Material de la Boquilla</th>
                <th>Diámetro</th>
                <th>Ref. Lista BCV</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Hotend Completo Ensamblado</td>
                <td>Bambu Lab A1 / A1 Mini</td>
                <td>Acero Endurecido (Hardened Steel)</td>
                <td>0.4 mm (Estándar antiabrasión)</td>
                <td style="font-weight: 700; color: #38BDF8;">$22.00</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Hotend Alta Precisión</td>
                <td>Bambu Lab A1 / A1 Mini</td>
                <td>Acero Endurecido / Latón</td>
                <td>0.2 mm (Miniaturas y joyería)</td>
                <td style="font-weight: 700; color: #38BDF8;">$22.00</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Hotend Gran Caudal (High Flow)</td>
                <td>Bambu Lab A1 / A1 Mini</td>
                <td>Acero Endurecido / Latón</td>
                <td>0.6 mm y 0.8 mm (Piezas masivas)</td>
                <td style="font-weight: 700; color: #38BDF8;">$22.00</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Bloque Calefactor Cerámico 300°C</td>
                <td>Kingroon H2D / KP3S Pro</td>
                <td>Calentador cerámico 360° + Bimetal</td>
                <td>Ensamblado rápido</td>
                <td style="font-weight: 700; color: #38BDF8;">$18.00</td>
              </tr>
              <tr>
                <td style="font-weight: 700; color: #FFFFFF;">Wipers Limpiadores de Boquilla</td>
                <td>Bambu Lab A1 / A1 Mini</td>
                <td>Silicona de alta temperatura</td>
                <td>Pack de repuesto oficial</td>
                <td style="font-weight: 700; color: #38BDF8;">$8.00</td>
              </tr>
            </tbody>
          </table>
        </div>

        <!-- PEI Maintenance Protocol -->
        <div class="panel-card" style="background: #0B111D; border-color: #2563EB; display: flex; justify-content: space-between; align-items: center; padding: 12px 18px;">
          <div style="font-size: 11px; color: #CBD5E1; line-height: 1.4;">
            <strong style="color: #FFFFFF;">PROTOCOLO DE MANTENIMIENTO PEI:</strong> Lavar cada 15 impresiones con agua tibia y jabón desengrasante neutro para disolver aceites corporales y recuperar adherencia al 100%. Entre impresiones, limpiar con paño de microfibra y alcohol isopropílico 99%.
          </div>
          <div class="badge-tag" style="background: #1E293B; color: #38BDF8; font-weight: 800; white-space: nowrap; margin-left: 14px;">
            MÁXIMA DURABILIDAD
          </div>
        </div>

      </div>
      {render_footer(8)}
    </div>
    '''

# Build Page 9
def build_page_9():
    return f'''
    <div class="page" id="page-9">
      {render_header(9)}
      <div class="page-content">
        
        <div class="section-header">
          <div class="section-title">08 / CONDICIONES COMERCIALES, PACKS & PEDIDOS DIRECTOS</div>
          <div class="section-desc">Atención personalizada y abastecimiento continuo para granjas de impresión, empresas de arquitectura y talleres de manufactura.</div>
        </div>

        <!-- 4 Payment Cards -->
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px;">
          <div class="panel-card" style="padding: 12px 14px;">
            <div style="font-size: 13.5px; font-weight: 900; color: #38BDF8; margin-bottom: 4px;">Binance Pay (USDT)</div>
            <div style="font-size: 10px; color: #CBD5E1; line-height: 1.4;">
              Confirmación automática 24/7 sin comisiones bancarias. <strong>Descuento directo exclusivo de contado</strong> frente al precio de lista.
            </div>
          </div>
          <div class="panel-card" style="padding: 12px 14px;">
            <div style="font-size: 13.5px; font-weight: 900; color: #38BDF8; margin-bottom: 4px;">Efectivo Divisas ($)</div>
            <div style="font-size: 10px; color: #CBD5E1; line-height: 1.4;">
              Billetes en buen estado para retiro presencial inmediato en nuestro almacén central de Lechería o contraentrega local.
            </div>
          </div>
          <div class="panel-card" style="padding: 12px 14px;">
            <div style="font-size: 13.5px; font-weight: 900; color: #38BDF8; margin-bottom: 4px;">Pago Móvil / VES</div>
            <div style="font-size: 10px; color: #CBD5E1; line-height: 1.4;">
              Transferencias en Bolívares calculadas a la tasa oficial del Banco Central de Venezuela (BCV) del día con facturación legal.
            </div>
          </div>
          <div class="panel-card" style="padding: 12px 14px;">
            <div style="font-size: 13.5px; font-weight: 900; color: #38BDF8; margin-bottom: 4px;">Zelle Corporativo</div>
            <div style="font-size: 10px; color: #CBD5E1; line-height: 1.4;">
              Aceptado para órdenes institucionales, empresas y packs mayoristas de granjas con confirmación directa.
            </div>
          </div>
        </div>

        <!-- 2 Wholesale Packs -->
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px;">
          <div class="panel-card" style="background: #0B111D; border-color: #2563EB;">
            <div class="card-title-row">
              <div class="card-main-title" style="color: #38BDF8;">PACK MAKER PRO (10 BOBINAS)</div>
              <div class="price-tag">TARIFA VOLUMEN</div>
            </div>
            <ul style="font-size: 10.5px; color: #CBD5E1; line-height: 1.5; padding-left: 18px; margin-top: 6px;">
              <li>Combinación libre de colores y materiales (PLA Basic, PLA+, PETG, Silk).</li>
              <li>Delivery gratuito en toda la zona metropolitana de Lechería, PLC y Barcelona.</li>
              <li>Asesoría técnica prioritaria para calibración de flujo y perfiles en tu impresora.</li>
            </ul>
          </div>
          <div class="panel-card" style="background: #0B111D; border-color: #2563EB;">
            <div class="card-title-row">
              <div class="card-main-title" style="color: #38BDF8;">PACK GRANJA INDUSTRIAL (20+ BOBINAS)</div>
              <div class="price-tag">PRECIO MAYORISTA</div>
            </div>
            <ul style="font-size: 10.5px; color: #CBD5E1; line-height: 1.5; padding-left: 18px; margin-top: 6px;">
              <li>Máximo descuento por volumen para líneas de manufactura en serie y servicios 3D.</li>
              <li>Reserva de lote garantizada en almacén para evitar roturas de stock en tu producción.</li>
              <li>Acceso con descuento a camas magnéticas PEI de repuesto y hotends ensamblados.</li>
            </ul>
          </div>
        </div>

        <!-- Logistics & Syntra Warranty Protocol -->
        <div class="panel-card">
          <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
            <div style="font-size: 12.5px; font-weight: 800; color: #FFFFFF; letter-spacing: 0.05em;">
              DESPACHO INMEDIATO, LOGÍSTICA & GARANTÍA DE SATISFACCIÓN
            </div>
            <div class="badge-tag">COMPROMISO SYNTRA</div>
          </div>
          <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px; font-size: 10.5px; color: #CBD5E1; line-height: 1.45;">
            <div>
              <strong style="color: #FFFFFF;">Logística de Despacho Inmediato:</strong><br/>
              • <strong>Retiro en Mano Lechería:</strong> Listo en 15 a 30 minutos tras confirmar orden.<br/>
              • <strong>Delivery Express Zona Norte:</strong> Lechería, Puerto La Cruz y Barcelona.<br/>
              • <strong>Envíos Nacionales:</strong> Salidas diarias por MRW, Tealca y Zoom con embalaje de alta resistencia contra impactos.
            </div>
            <div>
              <strong style="color: #FFFFFF;">Garantía Directa de Fábrica:</strong><br/>
              • Todos los filamentos se entregan con sellado al vacío y gel desecante activo.<br/>
              • Garantía de reemplazo inmediato en tienda local ante cualquier eventualidad de fabricación o defecto de bobinado.<br/>
              • Respaldo y soporte de perfiles por la comunidad oficial de Syntra Group.
            </div>
          </div>
        </div>

        <!-- Grand WhatsApp Banner -->
        <div class="panel-card" style="background: #0B111D; border-color: #38BDF8; padding: 18px 24px; display: flex; align-items: center; gap: 24px;">
          <img src="{img_qr}" style="width: 105px; height: 105px; border-radius: 8px; border: 2px solid #38BDF8; background: #FFFFFF; padding: 4px;" />
          <div style="flex: 1;">
            <div style="font-size: 12px; font-weight: 800; color: #38BDF8; letter-spacing: 0.15em; text-transform: uppercase;">
              CONTACTO DIRECTO & PEDIDOS WHATSAPP
            </div>
            <div style="font-size: 26px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.02em; margin-top: 2px;">
              +58 422-3446675
            </div>
            <div style="font-size: 11px; color: #94A3B8; margin-top: 4px; line-height: 1.4;">
              Escanea el código QR o haz clic en el enlace para contactar a nuestro equipo de ventas y soporte técnico. Cotizaciones inmediatas, consulta de colores en tiempo real y despacho express en Lechería.
            </div>
            <div style="margin-top: 10px;">
              <a href="https://wa.me/584223446675" style="display: inline-block; background: #25D366; color: #000000; font-size: 12px; font-weight: 800; padding: 8px 18px; border-radius: 6px; text-decoration: none; letter-spacing: 0.05em;">
                CHATEAR POR WHATSAPP AHORA
              </a>
            </div>
          </div>
        </div>

      </div>
      {render_footer(9)}
    </div>
    '''

print("Funciones Page 7, 8 y 9 definidas.")

# Compile full HTML document
full_html = f'''<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<title>Catálogo Maestro Syntra Supply 2026</title>
<style>
{CSS_STYLES}
</style>
</head>
<body>
{build_page_1()}
{build_page_2()}
{build_page_3()}
{build_page_4()}
{build_page_5()}
{build_page_6()}
{build_page_7()}
{build_page_8()}
{build_page_9()}
</body>
</html>'''

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"HTML guardado en {HTML_OUT} ({len(full_html)} chars)")

# Render via Playwright
print("Iniciando renderizado con Playwright a 1080p exacto...")
rendered_images = []

with sync_playwright() as p:
    browser = p.chromium.launch()
    # Viewport 1080 x 1528 exact
    page = browser.new_page(viewport={'width': 1080, 'height': 1528})
    page.goto(f"file:///{HTML_OUT.replace(os.sep, '/')}")
    page.wait_for_load_state("networkidle")
    
    for i in range(1, 10):
        img_file = os.path.join(SCRATCH_DIR, f"page_fluid_1080p_{i}.jpg")
        page_elem = page.locator(f"#page-{i}")
        page_elem.screenshot(path=img_file, type="jpeg", quality=86)
        rendered_images.append(img_file)
        print(f"  Capturada Página {i} a 1080x1528 -> {os.path.getsize(img_file)} bytes")
        
    browser.close()

# Measure bottom dead space with PIL
print("\n=== VERIFICACIÓN DE ESPACIO MUERTO POR PÁGINA ===")
for i, img_file in enumerate(rendered_images, start=1):
    im = Image.open(img_file).convert("RGB")
    W, H = im.size
    
    # Footer starts around Y=1470-1500
    # Let's find footer start Y
    footer_y = 0
    for y in range(H-60, H-10):
        for x in range(int(W*0.1), int(W*0.9), 15):
            r, g, b = im.getpixel((x, y))
            if r > 40 or g > 40 or b > 50:
                footer_y = y
                break
        if footer_y:
            break
            
    # Let's find last content row ABOVE footer_y - 20
    last_content_y = 0
    scan_limit = footer_y - 15 if footer_y else H - 65
    for y in range(scan_limit, 200, -1):
        row_has_content = False
        for x in range(int(W*0.1), int(W*0.9), 15):
            r, g, b = im.getpixel((x, y))
            if r > 40 or g > 40 or b > 50:
                row_has_content = True
                break
        if row_has_content:
            last_content_y = y
            break
            
    gap_px = (footer_y - last_content_y) if (footer_y and last_content_y) else 0
    gap_pct = (gap_px / H) * 100
    print(f"Página {i}: Último contenido Y={last_content_y}, Inicio Footer Y={footer_y}, Espacio vacío = {gap_px}px ({gap_pct:.1f}% de altura)")

# Build unified PDF via PIL
print("\nCompilando PDF unificado a 1080p...")
pil_pages = [Image.open(img_path) for img_path in rendered_images]
pil_pages[0].save(
    PDF_OUT,
    "PDF",
    resolution=150.0,
    save_all=True,
    append_images=pil_pages[1:]
)
pdf_size = os.path.getsize(PDF_OUT)
print(f"PDF generado con éxito: {PDF_OUT} ({pdf_size} bytes, ~{round(pdf_size/1024/1024, 2)} MB)")

# Copy to static and syntraweb destinations
import shutil
shutil.copyfile(PDF_OUT, PDF_OUT_FULL)
shutil.copyfile(PDF_OUT, SYNTRAWEB_PDF)
shutil.copyfile(PDF_OUT, SYNTRAWEB_PDF_FULL)
print("PDF copiado a todas las rutas de distribución:")
print(f"  - {PDF_OUT}")
print(f"  - {PDF_OUT_FULL}")
print(f"  - {SYNTRAWEB_PDF}")
print(f"  - {SYNTRAWEB_PDF_FULL}")

# Save previews for user inspection
for i, img_path in enumerate(rendered_images, start=1):
    preview_path = os.path.join(BRAIN_DIR, f"catalog_1080p_p{i}.png")
    im = Image.open(img_path)
    im.save(preview_path, "PNG")

print("=== PROCESO COMPLETADO EXITOSAMENTE ===")
