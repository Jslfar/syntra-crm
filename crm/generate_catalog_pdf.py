import os
import sqlite3
import base64
import asyncio
from playwright.async_api import async_playwright
from PIL import Image

def get_b64(path):
    if not os.path.exists(path):
        print(f"ERROR: File not found: {path}")
        return ""
    ext = os.path.splitext(path)[1].lower().replace('.', '')
    mime = 'image/jpeg' if ext in ['jpg', 'jpeg'] else 'image/png'
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    return f"data:{mime};base64,{data}"

ASSETS = r"c:\Users\UNK\Desktop\EXPORT IA\SYNTRA GROUP\syntraweb\assets\img"
CAT_ASSETS = os.path.join(ASSETS, "catalog_assets")

# Load real photography base64 (using the optimized assets)
img_logo_3d = get_b64(os.path.join(ASSETS, "syntralogo1.png"))
img_qr = get_b64(os.path.join(CAT_ASSETS, "whatsapp_qr.png"))

# Filament photos
img_pla_spool = get_b64(os.path.join(CAT_ASSETS, "pla_basic_spool.jpg"))
img_pla_prints = get_b64(os.path.join(CAT_ASSETS, "pla_basic_prints.jpg"))
img_pla_tolerance = get_b64(os.path.join(CAT_ASSETS, "pla_basic_tolerance.jpg"))

img_plaplus_spool = get_b64(os.path.join(CAT_ASSETS, "plaplus_spool.jpg"))
img_plaplus_prints = get_b64(os.path.join(CAT_ASSETS, "plaplus_prints.jpg"))
img_plaplus_tough = get_b64(os.path.join(CAT_ASSETS, "plaplus_toughness.jpg"))
img_plaplus_winding = get_b64(os.path.join(CAT_ASSETS, "plaplus_winding.jpg"))

img_petg_spool = get_b64(os.path.join(CAT_ASSETS, "petg_spool.jpg"))
img_petg_prints = get_b64(os.path.join(CAT_ASSETS, "petg_prints_showcase.jpg"))
img_petg_adhesion = get_b64(os.path.join(CAT_ASSETS, "petg_adhesion.jpg"))
img_petg_toughness = get_b64(os.path.join(CAT_ASSETS, "petg_toughness.jpg"))
img_matte_prints = get_b64(os.path.join(CAT_ASSETS, "matte_prints.jpg"))

img_silk_single_spool = get_b64(os.path.join(CAT_ASSETS, "silk_single_spool.jpg"))
img_silk_single_prints = get_b64(os.path.join(CAT_ASSETS, "silk_single_prints.jpg"))
img_silk_single_gold = get_b64(os.path.join(CAT_ASSETS, "silk_single_gold.jpg"))

img_silk_dual_spool = get_b64(os.path.join(CAT_ASSETS, "silk_dual_spool.jpg"))
img_silk_dual_dragon = get_b64(os.path.join(CAT_ASSETS, "silk_dual_dragon.jpg"))
img_silk_dual_vase = get_b64(os.path.join(CAT_ASSETS, "silk_dual_vase.jpg"))

img_silk_tri = get_b64(os.path.join(CAT_ASSETS, "silk_tri_showcase.jpg"))
img_silk_multi = get_b64(os.path.join(CAT_ASSETS, "silk_multi_prints.jpg"))

img_tpu_spool = get_b64(os.path.join(CAT_ASSETS, "tpu_spool.jpg"))
img_tpu_shoe = get_b64(os.path.join(CAT_ASSETS, "tpu_shoe_flex.jpg"))
img_tpu_models = get_b64(os.path.join(CAT_ASSETS, "tpu_models_test.jpg"))

img_pacf_spool = get_b64(os.path.join(CAT_ASSETS, "pacf_spool.jpg"))
img_pacf_drone = get_b64(os.path.join(CAT_ASSETS, "pacf_drone_parts.jpg"))
img_placf_spool = get_b64(os.path.join(CAT_ASSETS, "placf_spool_parts.jpg"))

# Hardware photos
img_bambu_hotend = get_b64(os.path.join(CAT_ASSETS, "bambu_a1_hotend.jpg"))
img_bambu_hardened = get_b64(os.path.join(CAT_ASSETS, "bambu_hardened_hotend.jpg"))
img_bambu_pei = get_b64(os.path.join(CAT_ASSETS, "bambu_pei_golden.jpg"))
img_bambu_peo = get_b64(os.path.join(CAT_ASSETS, "bambu_peo_diamond.jpg"))
img_bambu_h2d = get_b64(os.path.join(CAT_ASSETS, "bambu_h2d_pei.jpg"))

# Database products
conn = sqlite3.connect('crm/syntra_crm.db')
c = conn.cursor()
c.execute("SELECT id, category, name, material_type, color, sku, current_stock, pvp_usd, pvp_cash_usd FROM products ORDER BY id")
db_products = c.fetchall()

products_by_material = {}
for p in db_products:
    mat = p[3]
    products_by_material.setdefault(mat, []).append(p)

def get_base_hex(name):
    n = name.lower().strip()
    if 'blanco' in n or 'white' in n: return '#F8FAFC'
    if 'negro' in n or 'black' in n: return '#18181B'
    if 'gris oscuro' in n: return '#334155'
    if 'gris' in n or 'gray' in n: return '#64748B'
    if 'plata' in n or 'silver' in n: return '#C0C7D0'
    if 'oro viejo' in n or 'dark gold' in n: return '#B48A14'
    if 'oro' in n or 'gold' in n: return '#E5B80B'
    if 'cobre' in n or 'copper' in n: return '#C87533'
    if 'bronce' in n or 'bronze' in n: return '#CD7F32'
    if 'rojo flúor' in n: return '#FF2D55'
    if 'rojo' in n or 'red' in n: return '#EF4444'
    if 'azul cielo' in n or 'sky blue' in n: return '#38BDF8'
    if 'azul flúor' in n: return '#0091FF'
    if 'azul oscuro' in n or 'dark blue' in n: return '#1E3A8A'
    if 'azul' in n or 'blue' in n or 'zafiro' in n: return '#2563EB'
    if 'amarillo flúor' in n: return '#CCFF00'
    if 'amarillo' in n or 'yellow' in n: return '#EAB308'
    if 'verde esmeralda' in n: return '#059669'
    if 'verde' in n or 'green' in n: return '#10B981'
    if 'mandarina' in n or 'naranja' in n or 'orange' in n: return '#F97316'
    if 'rosado' in n or 'rosa' in n or 'pink' in n: return '#EC4899'
    if 'morado' in n or 'púrpura' in n or 'purple' in n: return '#9333EA'
    if 'marrón' in n or 'brown' in n or 'café' in n: return '#78350F'
    if 'piel' in n or 'skin' in n or 'beige' in n: return '#E2A97E'
    return '#94A3B8'

def get_color_style(col_str):
    col_clean = col_str.split('(')[0].strip().lower()
    
    if 'cf' in col_clean or 'carbon' in col_clean or 'fibra de carbono' in col_clean:
        return 'background: repeating-linear-gradient(45deg, #111 0, #111 2px, #333 2px, #333 4px); border: 1px solid rgba(255,255,255,0.4);'
    
    if 'macaron' in col_clean:
        return 'background: linear-gradient(135deg, #FFB3BA, #FFDFBA, #FFFFBA, #BAFFC9, #BAE1FF);'
    if 'pastel' in col_clean:
        return 'background: linear-gradient(135deg, #FAD02C, #F49AC2, #B5EAD7, #C7CEEA);'
    if 'rainbow' in col_clean or 'ice cream' in col_clean:
        return 'background: linear-gradient(135deg, #EF4444, #F59E0B, #10B981, #3B82F6, #8B5CF6);'
    
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
            
    if 'mármol' in col_clean or 'marble' in col_clean:
        return 'background: radial-gradient(circle, #CBD5E1 20%, #64748B 21%, #E2E8F0 40%, #475569 41%, #F8FAFC 80%); border: 1px solid rgba(255,255,255,0.4);'
        
    if 'transparente' in col_clean or 'traslúcido' in col_clean:
        return 'background: rgba(220, 235, 255, 0.25); border: 1.5px dashed rgba(255,255,255,0.6); box-shadow: inset 0 0 6px rgba(255,255,255,0.3);'
        
    hex_val = get_base_hex(col_clean)
    border = 'border: 1px solid rgba(255,255,255,0.5);' if hex_val in ['#FFFFFF', '#F8FAFC', '#18181B', '#000000', '#111113'] else 'border: 1px solid rgba(255,255,255,0.15);'
    return f'background: {hex_val}; {border}'

def render_swatch_grid(items, cols=4):
    html = f'<div class="swatches-grid grid-cols-{cols}">'
    for item in items:
        pid, cat, name, mat, col, sku, stock, pvp, pvp_cash = item
        clean_name = col.split('(')[0].strip()
        style = get_color_style(col)
        html += f'''
        <div class="swatch-card">
          <div class="swatch-dot" style="{style}"></div>
          <div class="swatch-content">
            <span class="swatch-title" title="{col}">{clean_name}</span>
            <div class="swatch-meta">
              <span class="swatch-sku">{sku}</span>
              <span class="swatch-stock">{stock} un</span>
            </div>
          </div>
        </div>'''
    html += '</div>'
    return html

css_styles = """
  /* 100% Native Vector System Fonts for Crisp Sharp PDF */

  @page {
    size: 210mm 297mm;
    margin: 0mm;
  }

  *, *::before, *::after {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }

  html, body {
    width: 210mm;
    margin: 0;
    padding: 0;
    background-color: #090A0F;
    color: #F1F5F9;
    font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif;
    -webkit-font-smoothing: antialiased;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }

  .page {
    width: 210mm;
    height: 297mm;
    max-height: 297mm;
    box-sizing: border-box;
    page-break-after: always;
    break-after: page;
    overflow: hidden;
    position: relative;
    display: flex;
    flex-direction: column;
    padding: 10mm 12mm 9mm 12mm;
    background-color: #090A0F;
    background-image: 
      radial-gradient(circle at 50% 0%, rgba(200, 210, 225, 0.08) 0%, transparent 60%),
      linear-gradient(rgba(200, 210, 225, 0.02) 1px, transparent 1px),
      linear-gradient(90deg, rgba(200, 210, 225, 0.02) 1px, transparent 1px);
    background-size: 100% 100%, 20px 20px, 20px 20px;
    gap: 10px;
  }

  /* Universal Header */
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(200, 210, 225, 0.14);
    padding-bottom: 6px;
    margin-bottom: 2px;
    flex-shrink: 0;
  }
  .header-brand {
    display: flex;
    align-items: center;
    gap: 10px;
  }
  .header-logo {
    width: 28px;
    height: 28px;
    border-radius: 6px;
    object-fit: contain;
  }
  .header-brand-title {
    font-family: 'Segoe UI', sans-serif;
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 0.08em;
    color: #FFFFFF;
  }
  .header-brand-sub {
    font-family: 'Segoe UI', sans-serif;
    font-size: 8px;
    font-weight: 700;
    color: #8F9AA9;
    letter-spacing: 0.12em;
    text-transform: uppercase;
  }
  .header-badge {
    background: rgba(200, 210, 225, 0.08);
    border: 1px solid rgba(200, 210, 225, 0.22);
    border-radius: 9999px;
    padding: 3.5px 12px;
    font-family: 'Consolas', monospace;
    font-size: 8.5px;
    font-weight: 700;
    color: #E2E8F0;
    letter-spacing: 0.05em;
  }

  /* Universal Footer */
  .page-footer {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-top: 1px solid rgba(200, 210, 225, 0.12);
    padding-top: 6px;
    font-size: 8px;
    color: #8F9AA9;
    flex-shrink: 0;
    margin-top: auto;
  }
  .page-footer strong {
    color: #C8D0DC;
  }

  /* Typography & Titles */
  .section-tag {
    font-family: 'Consolas', monospace;
    font-size: 8.5px;
    font-weight: 700;
    color: #C8D0DC;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 2px;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .section-tag::before {
    content: '';
    display: inline-block;
    width: 5px;
    height: 5px;
    background: #C8D0DC;
    border-radius: 1px;
  }
  .page-title {
    font-family: 'Segoe UI', sans-serif;
    font-size: 19px;
    font-weight: 800;
    letter-spacing: -0.01em;
    color: #FFFFFF;
    line-height: 1.15;
    margin-bottom: 2px;
  }
  .page-desc {
    font-size: 9.5px;
    color: #94A3B8;
    line-height: 1.35;
    margin-bottom: 1px;
  }

  /* Pricing Bar */
  .pricing-bar {
    display: flex;
    align-items: center;
    justify-content: space-between;
    background: linear-gradient(90deg, rgba(200, 210, 225, 0.12) 0%, rgba(14, 18, 26, 0.95) 100%);
    border: 1px solid rgba(200, 210, 225, 0.22);
    border-radius: 8px;
    padding: 7px 14px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.25);
  }
  .pricing-item {
    display: flex;
    align-items: baseline;
    gap: 8px;
  }
  .pricing-label {
    font-size: 9.5px;
    color: #8F9AA9;
    text-transform: uppercase;
    font-weight: 600;
    letter-spacing: 0.05em;
  }
  .pricing-amount {
    font-family: 'Segoe UI', sans-serif;
    font-size: 17px;
    font-weight: 900;
    color: #FFFFFF;
    letter-spacing: -0.02em;
  }
  .pricing-legal-note {
    font-size: 8px;
    color: #8F9AA9;
    line-height: 1.25;
    text-align: right;
    max-width: 250px;
  }
  .pricing-legal-note strong {
    color: #E2E8F0;
  }

  /* Galleries & Real Photos */
  .photo-gallery-2col {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 9px;
  }
  .photo-gallery-3col {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 9px;
  }
  .photo-gallery-4col {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr 1fr;
    gap: 8px;
  }
  .photo-card {
    background: #0E121A;
    border: 1px solid rgba(200, 210, 225, 0.16);
    border-radius: 8px;
    overflow: hidden;
    display: flex;
    flex-direction: column;
    position: relative;
    box-shadow: 0 4px 14px rgba(0,0,0,0.3);
  }
  .photo-card img {
    width: 100%;
    height: 145px;
    object-fit: cover;
    display: block;
    border-bottom: 1px solid rgba(200, 210, 225, 0.10);
  }
  .photo-card-body {
    padding: 6px 9px;
    display: flex;
    flex-direction: column;
    gap: 1.5px;
  }
  .photo-card-title {
    font-family: 'Segoe UI', sans-serif;
    font-size: 9.5px;
    font-weight: 700;
    color: #FFFFFF;
  }
  .photo-card-caption {
    font-size: 7.8px;
    color: #8F9AA9;
    line-height: 1.25;
  }

  /* Swatches Grid */
  .swatches-container {
    background: #0E121A;
    border: 1px solid rgba(200, 210, 225, 0.14);
    border-radius: 8px;
    padding: 8px 11px;
  }
  .swatches-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 6px;
    border-bottom: 1px solid rgba(200, 210, 225, 0.08);
    padding-bottom: 4px;
  }
  .swatches-header-title {
    font-family: 'Segoe UI', sans-serif;
    font-size: 9.8px;
    font-weight: 800;
    color: #FFFFFF;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .swatches-header-badge {
    font-size: 8px;
    color: #C8D0DC;
    font-family: 'Consolas', monospace;
  }
  .swatches-grid {
    display: grid;
    gap: 6px;
  }
  .grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
  .grid-cols-4 { grid-template-columns: repeat(4, 1fr); }
  .grid-cols-5 { grid-template-columns: repeat(5, 1fr); }

  .swatch-card {
    background: #141923;
    border: 1px solid rgba(200, 210, 225, 0.12);
    border-radius: 6px;
    padding: 7px 9px;
    display: flex;
    align-items: center;
    gap: 8px;
  }
  .swatch-dot {
    width: 16px;
    height: 16px;
    border-radius: 50%;
    flex-shrink: 0;
    box-shadow: 0 1px 3px rgba(0,0,0,0.5);
  }
  .swatch-content {
    display: flex;
    flex-direction: column;
    overflow: hidden;
    width: 100%;
  }
  .swatch-title {
    font-size: 9px;
    font-weight: 700;
    color: #F8FAFC;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    line-height: 1.2;
  }
  .swatch-meta {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 2px;
  }
  .swatch-sku {
    font-family: 'Consolas', monospace;
    font-size: 7.2px;
    color: #8F9AA9;
  }
  .swatch-stock {
    font-family: 'Consolas', monospace;
    font-size: 7.5px;
    font-weight: 700;
    color: #FFFFFF;
    background: rgba(200, 210, 225, 0.15);
    padding: 1.5px 5px;
    border-radius: 3px;
  }

  /* Technical Specs Banner */
  .tech-specs-bar {
    background: #0E121A;
    border: 1px solid rgba(200, 210, 225, 0.12);
    border-radius: 7px;
    padding: 7px 11px;
    display: grid;
    grid-template-columns: repeat(5, 1fr);
    gap: 6px;
    text-align: center;
  }
  .spec-item {
    display: flex;
    flex-direction: column;
    gap: 1.5px;
  }
  .spec-label {
    font-size: 7px;
    font-weight: 700;
    color: #8F9AA9;
    text-transform: uppercase;
    letter-spacing: 0.08em;
  }
  .spec-value {
    font-family: 'Consolas', monospace;
    font-size: 9px;
    font-weight: 700;
    color: #E2E8F0;
  }

  /* Technical Guide Panel */
  .tech-guide-panel {
    background: #0E121A;
    border: 1px solid rgba(200, 210, 225, 0.14);
    border-radius: 8px;
    padding: 8px 11px;
    display: flex;
    flex-direction: column;
    gap: 5px;
  }
  .tech-guide-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid rgba(200, 210, 225, 0.08);
    padding-bottom: 4px;
  }
  .tech-guide-title {
    font-family: 'Segoe UI', sans-serif;
    font-size: 9px;
    font-weight: 800;
    color: #FFFFFF;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    display: flex;
    align-items: center;
    gap: 6px;
  }
  .tech-guide-tag {
    font-family: 'Consolas', monospace;
    font-size: 7.8px;
    color: #C8D0DC;
  }
  .tech-guide-grid-3 {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 7px;
  }
  .tech-guide-grid-2 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 7px;
  }
  .tech-guide-grid-4 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 7px;
  }
  .guide-card {
    background: #141923;
    border: 1px solid rgba(200, 210, 225, 0.10);
    border-radius: 6px;
    padding: 7px 9px;
    display: flex;
    flex-direction: column;
    gap: 2.5px;
  }
  .guide-card-title {
    font-family: 'Segoe UI', sans-serif;
    font-size: 8.5px;
    font-weight: 700;
    color: #FFFFFF;
  }
  .guide-card-desc {
    font-size: 7.5px;
    color: #94A3B8;
    line-height: 1.35;
  }

  /* Hardware Table */
  .hardware-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 8.2px;
    background: #0E121A;
    border: 1px solid rgba(200, 210, 225, 0.14);
    border-radius: 7px;
    overflow: hidden;
  }
  .hardware-table th {
    background: #141923;
    padding: 6px 9px;
    text-align: left;
    font-family: 'Segoe UI', sans-serif;
    font-size: 7.8px;
    font-weight: 800;
    color: #C8D0DC;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    border-bottom: 1px solid rgba(200, 210, 225, 0.16);
  }
  .hardware-table td {
    padding: 5.5px 9px;
    border-bottom: 1px solid rgba(200, 210, 225, 0.08);
    color: #CBD5E1;
  }
  .hardware-table tr:last-child td {
    border-bottom: none;
  }
  .hardware-table td strong {
    color: #FFFFFF;
  }

  /* Bottom Order Bar */
  .order-action-bar {
    background: rgba(200, 210, 225, 0.06);
    border: 1px solid rgba(200, 210, 225, 0.16);
    border-radius: 7px;
    padding: 6px 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
  }
"""

html_pages = []

# =========================================================================
# PAGE 1: PORTADA & GUÍA MAESTRA DE NAVEGACIÓN
# =========================================================================
html_pages.append(f"""
<div class="page" style="gap: 12px;">
  <div class="page-header" style="border-bottom: none; margin-bottom: 0;">
    <div class="header-brand">
      <img src="{img_logo_3d}" class="header-logo" style="width: 34px; height: 34px;" />
      <div>
        <div class="header-brand-title">SYNTRA GROUP</div>
        <div class="header-brand-sub">DIVISIÓN MANUFACTURA ADITIVA & CONSUMIBLES 3D</div>
      </div>
    </div>
    <div class="header-badge">EDICIÓN 2026 • CATÁLOGO MAESTRO</div>
  </div>

  <div style="display: flex; flex-direction: column; align-items: center; text-align: center; margin: 4px 0;">
    <img src="{img_logo_3d}" style="width: 95px; height: 95px; border-radius: 20px; box-shadow: 0 12px 35px rgba(0,0,0,0.65); filter: drop-shadow(0 0 28px rgba(200, 210, 225, 0.28)); margin-bottom: 10px;" />
    <h1 style="font-family: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif; font-size: 34px; font-weight: 900; letter-spacing: 0.02em; color: #FFFFFF; text-shadow: 0 2px 10px rgba(0,0,0,0.5); margin-bottom: 4px;">
      SYNTRA SUPPLY
    </h1>
    <div style="font-family: 'Segoe UI', sans-serif; font-size: 11.5px; font-weight: 700; color: #C8D0DC; letter-spacing: 0.18em; text-transform: uppercase; margin-bottom: 5px;">
      DISTRIBUIDOR AUTORIZADO KINGROON • ALMACÉN LECHERÍA
    </div>
    <div style="font-size: 10.5px; color: #94A3B8; max-width: 530px; line-height: 1.45;">
      El inventario físico más completo de filamentos de grado técnico, placas magnéticas y hotends de alto rendimiento en el oriente venezolano.
    </div>
  </div>

  <div class="photo-gallery-3col" style="gap: 10px;">
    <div class="photo-card">
      <img src="{img_silk_dual_dragon}" style="height: 175px;" />
      <div class="photo-card-body" style="padding: 8px 10px;">
        <span class="photo-card-title">PLA Silk Bicolor Coaxial</span>
        <span class="photo-card-caption">Brillo metálico perlado y coextrusión bicromática continua.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_plaplus_prints}" style="height: 175px;" />
      <div class="photo-card-body" style="padding: 8px 10px;">
        <span class="photo-card-title">PLA+ High Speed Pro</span>
        <span class="photo-card-caption">Precisión geométrica y tolerancia micrométrica de ±0.02mm.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_tpu_shoe}" style="height: 175px;" />
      <div class="photo-card-body" style="padding: 8px 10px;">
        <span class="photo-card-title">TPU 95A Elastómero Flexible</span>
        <span class="photo-card-caption">450% de elongación a la rotura y memoria elástica estructural.</span>
      </div>
    </div>
  </div>

  <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px;">
    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 15px 10px; text-align: center;">
      <div style="font-family: 'Segoe UI', sans-serif; font-size: 21px; font-weight: 800; color: #FFFFFF; margin-bottom: 2px;">1.750 UN</div>
      <div style="font-size: 8px; font-weight: 600; color: #8F9AA9; text-transform: uppercase;">Stock Físico Real</div>
    </div>
    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 15px 10px; text-align: center;">
      <div style="font-family: 'Segoe UI', sans-serif; font-size: 21px; font-weight: 800; color: #FFFFFF; margin-bottom: 2px;">117 SKUs</div>
      <div style="font-size: 8px; font-weight: 600; color: #8F9AA9; text-transform: uppercase;">Variedad Inmediata</div>
    </div>
    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 15px 10px; text-align: center;">
      <div style="font-family: 'Segoe UI', sans-serif; font-size: 21px; font-weight: 800; color: #FFFFFF; margin-bottom: 2px;">±0.02 mm</div>
      <div style="font-size: 8px; font-weight: 600; color: #8F9AA9; text-transform: uppercase;">Calibración Láser</div>
    </div>
    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 15px 10px; text-align: center;">
      <div style="font-family: 'Segoe UI', sans-serif; font-size: 21px; font-weight: 800; color: #FFFFFF; margin-bottom: 2px;">15 - 30 MIN</div>
      <div style="font-size: 8px; font-weight: 600; color: #8F9AA9; text-transform: uppercase;">Despacho Lechería</div>
    </div>
  </div>

  <!-- NAVIGATION INDEX (Fills dead space cleanly) -->
  <div class="tech-guide-panel" style="padding: 12px 14px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><line x1="8" y1="6" x2="21" y2="6"></line><line x1="8" y1="12" x2="21" y2="12"></line><line x1="8" y1="18" x2="21" y2="18"></line><line x1="3" y1="6" x2="3.01" y2="6"></line><line x1="3" y1="12" x2="3.01" y2="12"></line><line x1="3" y1="18" x2="3.01" y2="18"></line></svg>
        ÍNDICE DE SECCIONES & ESTRUCTURA DEL CATÁLOGO
      </span>
      <span class="tech-guide-tag">GUÍA DE NAVEGACIÓN</span>
    </div>
    <div class="tech-guide-grid-4" style="gap: 7px;">
      <div class="guide-card" style="padding: 7px 8px;">
        <span class="guide-card-title">PÁG. 02 • INFRAESTRUCTURA</span>
        <span class="guide-card-desc">Ventaja local Lechería vs pedidos foráneos y matriz de valor.</span>
      </div>
      <div class="guide-card" style="padding: 7px 8px;">
        <span class="guide-card-title">PÁG. 03 • PLA & PLA+</span>
        <span class="guide-card-desc">Alta velocidad, prototipado rápido y 19 colores en inventario.</span>
      </div>
      <div class="guide-card" style="padding: 7px 8px;">
        <span class="guide-card-title">PÁG. 04 • PETG & MATTE</span>
        <span class="guide-card-desc">Termoplásticos mecánicos, acabado cerámico y mármol.</span>
      </div>
      <div class="guide-card" style="padding: 7px 8px;">
        <span class="guide-card-title">PÁG. 05 • SILK BICOLOR</span>
        <span class="guide-card-desc">Efecto seda reflectante y coextrusión a 180° tornasol.</span>
      </div>
      <div class="guide-card" style="padding: 7px 8px;">
        <span class="guide-card-title">PÁG. 06 • SILK TRICOLOR</span>
        <span class="guide-card-desc">Coextrusión a 120° y arcoíris continuo sin purga.</span>
      </div>
      <div class="guide-card" style="padding: 7px 8px;">
        <span class="guide-card-title">PÁG. 07 • TÉCNICOS & CF</span>
        <span class="guide-card-desc">TPU 95A, ASA solar UV y fibra de carbono estructural.</span>
      </div>
      <div class="guide-card" style="padding: 7px 8px;">
        <span class="guide-card-title">PÁG. 08 • BAMBU & H2D</span>
        <span class="guide-card-desc">Hotends ensamblados, boquillas y placas PEI / PEO.</span>
      </div>
      <div class="guide-card" style="padding: 7px 8px;">
        <span class="guide-card-title">PÁG. 09 • LOGÍSTICA & WA</span>
        <span class="guide-card-desc">Matriz de entregas, pagos en BCV/divisa y canal WhatsApp.</span>
      </div>
    </div>
  </div>

  <div style="background: linear-gradient(90deg, rgba(200, 210, 225, 0.12), rgba(14, 18, 26, 0.85)); border: 1px solid rgba(200, 210, 225, 0.22); border-radius: 8px; padding: 13px 18px; display: flex; justify-content: space-between; align-items: center;">
    <div>
      <div style="font-family: 'Segoe UI', sans-serif; font-size: 11.5px; font-weight: 800; color: #FFFFFF;">TU TALLER 3D, SIN INTERRUPCIONES NI FLETES COSTOSOS.</div>
      <div style="font-size: 8.5px; color: #94A3B8; margin-top: 2px;">Cobertura prioritaria: Lechería, Puerto La Cruz, Barcelona y envíos exprés a toda Venezuela.</div>
    </div>
    <div style="font-family: 'Consolas', monospace; font-size: 10px; font-weight: 700; color: #FFFFFF; background: rgba(200, 210, 225, 0.18); padding: 5px 13px; border-radius: 6px; border: 1px solid rgba(200, 210, 225, 0.3);">
      WA: +58 422-3446675
    </div>
  </div>

  <div class="page-footer">
    <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
    <div>ALMACÉN CENTRAL: LECHERÍA, ANZOÁTEGUI</div>
    <div>PÁG. 01 / 09</div>
  </div>
</div>
""")

# =========================================================================
# PAGE 2: MANIFIESTO Y PROPUESTA DE VALOR INDUSTRIAL
# =========================================================================
html_pages.append(f"""
<div class="page" style="gap: 9px;">
  <div class="page-header">
    <div class="header-brand">
      <img src="{img_logo_3d}" class="header-logo" />
      <div>
        <div class="header-brand-title">SYNTRA SUPPLY</div>
        <div class="header-brand-sub">ESTÁNDAR TÉCNICO & PROPUESTA DE VALOR</div>
      </div>
    </div>
    <div class="header-badge">01 / INFRAESTRUCTURA</div>
  </div>

  <div>
    <div class="section-tag">INGENIERÍA & OPERACIONES</div>
    <h2 class="page-title">La Ventaja Estratégica de Syntra Supply</h2>
    <div class="page-desc">Solución directa a las dos mayores fallas del ecosistema 3D en Venezuela: la rotura de stock por envíos lejanos y la degradación por la agresiva humedad costera.</div>
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 11px 13px;">
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
        <span style="font-family: 'Consolas', monospace; font-size: 9px; font-weight: 700; color: #FFFFFF; background: rgba(200, 210, 225, 0.15); padding: 2px 6px; border-radius: 4px;">01</span>
        <span style="font-family: 'Segoe UI', sans-serif; font-size: 10px; font-weight: 800; color: #FFFFFF;">DISPONIBILIDAD FÍSICA INMEDIATA</span>
      </div>
      <div style="font-size: 8px; color: #94A3B8; line-height: 1.4;">
        Stock en Lechería. Retira en 15 minutos o recibe en tu taller el mismo día en Barcelona, PLC y Lechería. Elimina los 3 a 5 días de incertidumbre y los $15+ de flete desde Caracas.
      </div>
    </div>

    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 11px 13px;">
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
        <span style="font-family: 'Consolas', monospace; font-size: 9px; font-weight: 700; color: #FFFFFF; background: rgba(200, 210, 225, 0.15); padding: 2px 6px; border-radius: 4px;">02</span>
        <span style="font-family: 'Segoe UI', sans-serif; font-size: 10px; font-weight: 800; color: #FFFFFF;">SELLADO ACTIVO ANTI-HUMEDAD</span>
      </div>
      <div style="font-size: 8px; color: #94A3B8; line-height: 1.4;">
        La humedad de la costa (>75% RH) arruina los filamentos. Cada bobina Kingroon viene envasada al vacío en film de alta barrera con 10g de desecante activo que garantiza cero burbujeo.
      </div>
    </div>

    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 11px 13px;">
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
        <span style="font-family: 'Consolas', monospace; font-size: 9px; font-weight: 700; color: #FFFFFF; background: rgba(200, 210, 225, 0.15); padding: 2px 6px; border-radius: 4px;">03</span>
        <span style="font-family: 'Segoe UI', sans-serif; font-size: 10px; font-weight: 800; color: #FFFFFF;">TOLERANCIA LÁSER ±0.02MM</span>
      </div>
      <div style="font-size: 8px; color: #94A3B8; line-height: 1.4;">
        Inspección óptica continua durante la extrusión y bobinado computarizado Tidy Winding libre de solapamientos o nudos. Diseñado para tiradas industriales de más de 48 horas continuas.
      </div>
    </div>

    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 11px 13px;">
      <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 4px;">
        <span style="font-family: 'Consolas', monospace; font-size: 9px; font-weight: 700; color: #FFFFFF; background: rgba(200, 210, 225, 0.15); padding: 2px 6px; border-radius: 4px;">04</span>
        <span style="font-family: 'Segoe UI', sans-serif; font-size: 10px; font-weight: 800; color: #FFFFFF;">FACTURACIÓN FORMAL & RESPALDO BCV</span>
      </div>
      <div style="font-size: 8px; color: #94A3B8; line-height: 1.4;">
        Operaciones 100% transparentes conforme a la ley venezolana. Precios de lista referenciados a tasa oficial BCV con facturación fiscal en Bolívares y atención directa para empresas y makers.
      </div>
    </div>
  </div>

  <!-- 3-COL REAL PHOTO SHOWCASE -->
  <div class="photo-gallery-3col" style="gap: 9px;">
    <div class="photo-card">
      <img src="{img_plaplus_winding}" style="height: 145px;" />
      <div class="photo-card-body" style="padding: 7px 10px;">
        <span class="photo-card-title">Bobinado Computarizado Tidy Winding</span>
        <span class="photo-card-caption">Alineación micrométrica capa por capa que elimina atascos y paradas críticas.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_pla_tolerance}" style="height: 145px;" />
      <div class="photo-card-body" style="padding: 7px 10px;">
        <span class="photo-card-title">Calibración Láser ±0.02mm</span>
        <span class="photo-card-caption">Control de flujo uniforme que evita subextrusión en boquillas de 0.2 a 0.8mm.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_petg_adhesion}" style="height: 145px;" />
      <div class="photo-card-body" style="padding: 7px 10px;">
        <span class="photo-card-title">Fusión Interfacial & Cohesión</span>
        <span class="photo-card-caption">Capas químicamente coalescentes que previenen la deslaminación mecánica.</span>
      </div>
    </div>
  </div>

  <!-- COMPARISON TABLE: LOCAL VS REMOTE -->
  <div class="tech-guide-panel" style="padding: 9px 12px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle><polyline points="16 11 18 13 22 9"></polyline></svg>
        MATRIZ DE VALOR: COMPRA LOCAL EN LECHERÍA VS. DISTRIBUIDOR FORÁNEO (CARACAS)
      </span>
      <span class="tech-guide-tag">BENEFICIO ECONÓMICO</span>
    </div>
    <table class="hardware-table" style="font-size: 7.8px; margin-top: 3px;">
      <thead>
        <tr>
          <th style="width: 25%;">FACTOR OPERATIVO</th>
          <th style="width: 37.5%; color: #FFFFFF;">SYNTRA SUPPLY (LECHERÍA)</th>
          <th style="width: 37.5%;">PEDIDOS A CARACAS / MERCADOLIBRE</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Tiempo de Abastecimiento</strong></td>
          <td style="color: #FFFFFF;"><strong>15 a 30 minutos</strong> (Retiro en almacén o Express)</td>
          <td>3 a 5 días hábiles de espera con agencia</td>
        </tr>
        <tr>
          <td><strong>Costo de Flete / Encomienda</strong></td>
          <td style="color: #FFFFFF;"><strong>$0 Flete Local</strong> (Retiro en mano sin recargos)</td>
          <td>$12 a $18 USD por bulto según la agencia</td>
        </tr>
        <tr>
          <td><strong>Integridad del Empaque</strong></td>
          <td style="color: #FFFFFF;"><strong>100% verificado en físico</strong> (Bolsa al vacío intacta)</td>
          <td>Riesgo de golpes y pérdida de vacío en transporte</td>
        </tr>
        <tr>
          <td><strong>Soporte Técnico de Slicer</strong></td>
          <td style="color: #FFFFFF;"><strong>Asistencia por WhatsApp</strong> con perfiles Bambu/Orca</td>
          <td>Atención genérica sin conocimiento en impresión</td>
        </tr>
      </tbody>
    </table>
  </div>

  <!-- LECHERIA STORAGE PROTOCOL (Fills dead space) -->
  <div class="tech-guide-panel" style="padding: 9px 12px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 12h-4l-3 9L9 3l-3 9H2"/></svg>
        ESTÁNDAR OPERATIVO EN ALMACÉN LECHERÍA
      </span>
      <span class="tech-guide-tag">CONTROL CLIMÁTICO</span>
    </div>
    <div class="tech-guide-grid-3">
      <div class="guide-card" style="padding: 8px 10px;">
        <span class="guide-card-title">Ambiente Climatizado a &lt;45% RH</span>
        <span class="guide-card-desc">Instalaciones con deshumidificación activa permanente. Protegemos cada lote de la humedad marina de la Bahía de Pozuelos.</span>
      </div>
      <div class="guide-card" style="padding: 8px 10px;">
        <span class="guide-card-title">Inspección de Vacío al Despacho</span>
        <span class="guide-card-desc">Cada caja se verifica al momento de la entrega. Si un empaque pierde el vacío en almacén, se descarta de la línea de venta.</span>
      </div>
      <div class="guide-card" style="padding: 8px 10px;">
        <span class="guide-card-title">Trazabilidad por Lote y SKU</span>
        <span class="guide-card-desc">117 SKUs registrados individualmente por color y fecha de arribo. Garantía de rotación FIFO y frescura del polímero.</span>
      </div>
    </div>
  </div>

  <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 10px 14px; display: flex; align-items: center; justify-content: space-between;">
    <div style="display: flex; align-items: center; gap: 11px;">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="flex-shrink: 0;"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>
      <div>
        <div style="font-family: 'Segoe UI', sans-serif; font-size: 9.5px; font-weight: 800; color: #FFFFFF;">GARANTÍA TÉCNICA SYNTRA GROUP</div>
        <div style="font-size: 8px; color: #94A3B8;">Reposición inmediata ante cualquier defecto de fábrica o pérdida de vacío comprobada al abrir el empaque.</div>
      </div>
    </div>
    <div style="font-family: 'Consolas', monospace; font-size: 8.5px; color: #C8D0DC; font-weight: 700;">CALIDAD CERTIFICADA</div>
  </div>

  <div class="page-footer">
    <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
    <div>ALMACÉN CENTRAL: LECHERÍA, ANZOÁTEGUI</div>
    <div>PÁG. 02 / 09</div>
  </div>
</div>
""")

# =========================================================================
# PAGE 3: PLA BASIC & PLA+ HIGH SPEED
# =========================================================================
pla_basic_items = products_by_material.get('PLA Basic', [])
plaplus_items = products_by_material.get('PLA+ Alta Resistencia', [])

html_pages.append(f"""
<div class="page" style="gap: 9px;">
  <div class="page-header">
    <div class="header-brand">
      <img src="{img_logo_3d}" class="header-logo" />
      <div>
        <div class="header-brand-title">SYNTRA SUPPLY</div>
        <div class="header-brand-sub">CONSUMIBLES DE PRODUCCIÓN RÁPIDA</div>
      </div>
    </div>
    <div class="header-badge">02 / FILAMENTOS BÁSICOS</div>
  </div>

  <div>
    <div class="section-tag">PRODUCCIÓN RÁPIDA & PROTOTIPADO</div>
    <h2 class="page-title">PLA Basic & PLA+ Alta Resistencia</h2>
    <div class="page-desc">El polímero biobasado estándar de alta velocidad para prototipado rápido, figuras estéticas y componentes que requieren máxima fidelidad dimensional (1.75mm • 1.0 KG neto).</div>
  </div>

  <div class="photo-gallery-3col" style="gap: 9px;">
    <div class="photo-card">
      <img src="{img_pla_spool}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Bobina Kingroon PLA 1KG</span>
        <span class="photo-card-caption">Empaque sellado con desecante activo.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_plaplus_prints}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Modelos Arquitectónicos & Mecánicos</span>
        <span class="photo-card-caption">Capas uniformes sin hilos ni deformaciones.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_plaplus_tough}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Tenacidad Reforzada PLA+</span>
        <span class="photo-card-caption">Hasta 5x más resistencia al impacto que PLA común.</span>
      </div>
    </div>
  </div>

  <div class="pricing-bar">
    <div class="pricing-item">
      <span class="pricing-label">PLA BASIC:</span>
      <span class="pricing-amount">Ref. $20.00 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(200 un • 12 tonos)</span>
    </div>
    <div class="pricing-item">
      <span class="pricing-label">PLA+:</span>
      <span class="pricing-amount">Ref. $21.50 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(80 un • 7 tonos)</span>
    </div>
    <div class="pricing-legal-note">
      Facturación formal en <strong>Bolívares a tasa oficial BCV</strong>.<br />Descuento de contado en divisas / USDT vía WhatsApp.
    </div>
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">PLA BASIC (12 TONOS DISPONIBLES)</span>
      <span class="swatches-header-badge">200 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(pla_basic_items, cols=4)}
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">PLA+ ALTA RESISTENCIA (7 TONOS DISPONIBLES)</span>
      <span class="swatches-header-badge">80 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(plaplus_items, cols=4)}
  </div>

  <!-- TECHNICAL SPEC GUIDE -->
  <div class="tech-guide-panel" style="padding: 9px 12px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="3"></circle><path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"></path></svg>
        PERFILES RECOMENDADOS & APLICACIÓN EN TALLER
      </span>
      <span class="tech-guide-tag">BAMBU STUDIO / ORCA / CURA</span>
    </div>
    <div class="tech-guide-grid-3">
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">PLA Basic (Estética & Prototipado)</span>
        <span class="guide-card-desc">Excelente acabado superficial y mínima contracción. Ideal para maquetas de arquitectura, cosplay y piezas decorativas.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">PLA+ High Speed (Piezas Mecánicas)</span>
        <span class="guide-card-desc">Modificado con elastómeros de tenacidad. Tolera hasta 300 mm/s sin delaminación ni atascos en extrusores direct drive.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Compatibilidad con Sistemas AMS</span>
        <span class="guide-card-desc">Bobinas con devanado perimetral balanceado 100% compatibles con Bambu Lab AMS y Anycubic ACE Pro sin trabas.</span>
      </div>
    </div>
  </div>

  <div class="tech-specs-bar">
    <div class="spec-item">
      <span class="spec-label">Temperatura Boquilla</span>
      <span class="spec-value">190 – 225 °C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Temperatura Cama</span>
      <span class="spec-value">50 – 60 °C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Velocidad Máxima</span>
      <span class="spec-value">Hasta 300 mm/s</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Ventilación de Capa</span>
      <span class="spec-value">100% Activa</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Tolerancia Diámetro</span>
      <span class="spec-value">±0.02 mm</span>
    </div>
  </div>

  <div class="order-action-bar">
    <span style="font-size: 8px; color: #CBD5E1;">¿Deseas apartar bobinas de PLA o PLA+ hoy mismo? Escríbenos con el código SKU.</span>
    <span style="font-family: 'Consolas', monospace; font-size: 8.5px; font-weight: 700; color: #FFFFFF;">WhatsApp: +58 422-3446675 • Despacho en Lechería</span>
  </div>

  <div class="page-footer">
    <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
    <div>ALMACÉN CENTRAL: LECHERÍA, ANZOÁTEGUI</div>
    <div>PÁG. 03 / 09</div>
  </div>
</div>
""")

# =========================================================================
# PAGE 4: PETG BASIC & ESPECIALES (MATTE & MARBLE)
# =========================================================================
petg_items = products_by_material.get('PETG Basic', [])
matte_items = products_by_material.get('PLA Matte', []) + products_by_material.get('PETG Matte', [])
marble_items = products_by_material.get('PLA Marble', [])
specials_items = matte_items + marble_items

html_pages.append(f"""
<div class="page" style="gap: 9px;">
  <div class="page-header">
    <div class="header-brand">
      <img src="{img_logo_3d}" class="header-logo" />
      <div>
        <div class="header-brand-title">SYNTRA SUPPLY</div>
        <div class="header-brand-sub">POLÍMEROS TÉCNICOS & ACABADOS PREMIUM</div>
      </div>
    </div>
    <div class="header-badge">03 / PETG & ESPECIALES</div>
  </div>

  <div>
    <div class="section-tag">INGENIERÍA MECÁNICA & ACABADOS SATINADOS</div>
    <h2 class="page-title">PETG Basic, PLA Matte & Marble Efecto Roca</h2>
    <div class="page-desc">Resistencia química y térmica para piezas de uso final, combinada con acabados satinados que eliminan el reflejo de las líneas de capa (1.75mm • 1.0 KG neto).</div>
  </div>

  <div class="photo-gallery-3col" style="gap: 9px;">
    <div class="photo-card">
      <img src="{img_petg_spool}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Bobina Kingroon PETG 1KG</span>
        <span class="photo-card-caption">Resistencia química a aceites, alcoholes y agua.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_petg_prints}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Piezas de Uso Final & Soportes</span>
        <span class="photo-card-caption">Termorresistencia hasta 75°C sin deformación.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_matte_prints}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">PLA Matte & Acabado Piedra Mármol</span>
        <span class="photo-card-caption">Textura cerámica que disimula al 100% las capas.</span>
      </div>
    </div>
  </div>

  <div class="pricing-bar">
    <div class="pricing-item">
      <span class="pricing-label">PETG BASIC:</span>
      <span class="pricing-amount">Ref. $19.50 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(120 un • 17 tonos)</span>
    </div>
    <div class="pricing-item">
      <span class="pricing-label">MATTE / MARBLE:</span>
      <span class="pricing-amount">Ref. $21.50 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(50 un • 5 tonos)</span>
    </div>
    <div class="pricing-legal-note">
      Facturación formal en <strong>Bolívares a tasa oficial BCV</strong>.<br />Descuento de contado en divisas / USDT vía WhatsApp.
    </div>
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">PETG BASIC (17 TONOS MECÁNICOS EN STOCK)</span>
      <span class="swatches-header-badge">120 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(petg_items, cols=4)}
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">PLA MATTE & MARBLE EFECTO CERÁMICO (5 TONOS)</span>
      <span class="swatches-header-badge">50 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(specials_items, cols=5)}
  </div>

  <!-- TECHNICAL APPLICATION GUIDE -->
  <div class="tech-guide-panel" style="padding: 9px 12px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
        CRITERIOS DE SELECCIÓN & PARÁMETROS TÉCNICOS
      </span>
      <span class="tech-guide-tag">GUÍA DE MATERIALES</span>
    </div>
    <div class="tech-guide-grid-2">
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">PETG (Grado Mecánico & Soportes de Taller)</span>
        <span class="guide-card-desc">Fusión entre capas casi indestructible y excelente resistencia a solventes. Configurar ventilador al 30-50% para maximizar la resistencia al desgarro interlaminar.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">PLA Matte & Mármol (Diseño de Producto & Escultura)</span>
        <span class="guide-card-desc">El PLA Matte dispersa el brillo para un aspecto tipo molde inyectado. El filamento Mármol incorpora micropartículas que reproducen la textura exacta de roca granítica.</span>
      </div>
    </div>
  </div>

  <div class="tech-specs-bar">
    <div class="spec-item">
      <span class="spec-label">PETG Boquilla / Cama</span>
      <span class="spec-value">220-250°C / 70-80°C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Matte Boquilla / Cama</span>
      <span class="spec-value">190-220°C / 50-60°C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Resistencia Térmica</span>
      <span class="spec-value">HDT 75 °C (PETG)</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Superficie Sugerida</span>
      <span class="spec-value">PEI Texturizada</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Velocidad Sugerida</span>
      <span class="spec-value">150 – 250 mm/s</span>
    </div>
  </div>

  <div class="order-action-bar">
    <span style="font-size: 8px; color: #CBD5E1;">¿Deseas apartar bobinas de PETG o acabados Matte/Marble? Escríbenos con el SKU.</span>
    <span style="font-family: 'Consolas', monospace; font-size: 8.5px; font-weight: 700; color: #FFFFFF;">WhatsApp: +58 422-3446675 • Despacho en Lechería</span>
  </div>

  <div class="page-footer">
    <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
    <div>ALMACÉN CENTRAL: LECHERÍA, ANZOÁTEGUI</div>
    <div>PÁG. 04 / 09</div>
  </div>
</div>
""")

# =========================================================================
# PAGE 5: PLA SILK SÓLIDO & SILK BICOLOR
# =========================================================================
silk_single_items = products_by_material.get('PLA Silk Sólido', [])
silk_dual_items = products_by_material.get('PLA Silk Bicolor', [])

html_pages.append(f"""
<div class="page" style="gap: 9px;">
  <div class="page-header">
    <div class="header-brand">
      <img src="{img_logo_3d}" class="header-logo" />
      <div>
        <div class="header-brand-title">SYNTRA SUPPLY</div>
        <div class="header-brand-sub">ACABADOS REFLECTANTES & BICOLOR COAXIAL</div>
      </div>
    </div>
    <div class="header-badge">04 / LÍNEA SILK PREMIUM</div>
  </div>

  <div>
    <div class="section-tag">EFECTOS METÁLICOS & COEXTRUSIÓN LONGITUDINAL</div>
    <h2 class="page-title">PLA Silk Sólido & Silk Bicolor (Doble Tono)</h2>
    <div class="page-desc">Polímeros de acabado seda con brillo perlado metálico y tecnología de coextrusión bicromática longitudinal a 180° que crea transiciones dinámicas al rotar la pieza (1.75mm • 1.0 KG neto).</div>
  </div>

  <div class="photo-gallery-3col" style="gap: 9px;">
    <div class="photo-card">
      <img src="{img_silk_single_spool}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Bobina Silk Oro Imperial</span>
        <span class="photo-card-caption">Brillo especular sin necesidad de posprocesado ni laca.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_silk_dual_dragon}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Coextrusión Bicolor 180°</span>
        <span class="photo-card-caption">Transición tonal según el ángulo de incidencia de luz.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_silk_single_prints}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Estatuillas & Trofeos</span>
        <span class="photo-card-caption">Superficie reflectante de alta fidelidad estética.</span>
      </div>
    </div>
  </div>

  <div class="pricing-bar">
    <div class="pricing-item">
      <span class="pricing-label">SILK SÓLIDO:</span>
      <span class="pricing-amount">Ref. $24.00 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(110 un • 11 tonos)</span>
    </div>
    <div class="pricing-item">
      <span class="pricing-label">SILK BICOLOR:</span>
      <span class="pricing-amount">Ref. $27.00 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(70 un • 7 combinaciones)</span>
    </div>
    <div class="pricing-legal-note">
      Facturación formal en <strong>Bolívares a tasa oficial BCV</strong>.<br />Descuento de contado en divisas / USDT vía WhatsApp.
    </div>
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">PLA SILK SÓLIDO METALIZADO (11 TONOS)</span>
      <span class="swatches-header-badge">110 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(silk_single_items, cols=4)}
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">PLA SILK BICOLOR COAXIAL (7 COMBINACIONES)</span>
      <span class="swatches-header-badge">70 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(silk_dual_items, cols=4)}
  </div>

  <!-- TECHNICAL PRINTING GUIDE -->
  <div class="tech-guide-panel" style="padding: 9px 12px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
        TIPS DE IMPRESIÓN PARA ACABADO METÁLICO ESPEJO
      </span>
      <span class="tech-guide-tag">OPTIMIZACIÓN DE BRILLO</span>
    </div>
    <div class="tech-guide-grid-3">
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Temperatura de Boquilla Óptima</span>
        <span class="guide-card-desc">Imprimir a 215°C – 225°C. A temperaturas ligeramente más altas, los agentes de seda fluyen libremente creando máxima reflexión especular.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Coextrusión sin Torre de Purga</span>
        <span class="guide-card-desc">Dos colores en una misma hebra. Permite imprimir dragones articulados y jarrones bicolores sin desperdicio de filamento ni sistemas multi-material.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Orientación Angular</span>
        <span class="guide-card-desc">Alinee la cara principal de la pieza a 45° respecto al pórtico para que la transición entre colores resalte nítidamente en aristas y curvas.</span>
      </div>
    </div>
  </div>

  <div class="tech-specs-bar">
    <div class="spec-item">
      <span class="spec-label">Temperatura Boquilla</span>
      <span class="spec-value">205 – 225 °C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Temperatura Cama</span>
      <span class="spec-value">50 – 60 °C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Acabado Superficial</span>
      <span class="spec-value">Brillo Seda Metálico</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Coextrusión</span>
      <span class="spec-value">Bicolor 180° Coaxial</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Aplicaciones Top</span>
      <span class="spec-value">Joyería, Trofeos, Arte</span>
    </div>
  </div>

  <div class="order-action-bar">
    <span style="font-size: 8px; color: #CBD5E1;">¿Deseas apartar bobinas Silk Sólido o Bicolor? Escríbenos con el código SKU.</span>
    <span style="font-family: 'Consolas', monospace; font-size: 8.5px; font-weight: 700; color: #FFFFFF;">WhatsApp: +58 422-3446675 • Despacho en Lechería</span>
  </div>

  <div class="page-footer">
    <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
    <div>ALMACÉN CENTRAL: LECHERÍA, ANZOÁTEGUI</div>
    <div>PÁG. 05 / 09</div>
  </div>
</div>
""")

# =========================================================================
# PAGE 6: PLA SILK TRICOLOR & SILK RAINBOW
# =========================================================================
silk_tri_items = products_by_material.get('PLA Silk Tricolor', [])
silk_rainbow_items = products_by_material.get('PLA Silk Rainbow', [])

html_pages.append(f"""
<div class="page" style="gap: 9px;">
  <div class="page-header">
    <div class="header-brand">
      <img src="{img_logo_3d}" class="header-logo" />
      <div>
        <div class="header-brand-title">SYNTRA SUPPLY</div>
        <div class="header-brand-sub">COEXTRUSIÓN COAXIAL & GRADIENTES CROMÁTICOS</div>
      </div>
    </div>
    <div class="header-badge">05 / MULTICOLOR & RAINBOW</div>
  </div>

  <div>
    <div class="section-tag">EFECTOS TRIDIMENSIONALES AVANZADOS</div>
    <h2 class="page-title">PLA Silk Tricolor (3-Tone) & Silk Rainbow</h2>
    <div class="page-desc">Tecnología de coextrusión tripartita en una sola hebra que revela 3 colores simultáneos según la rotación de la pieza, y gradientes continuos tipo arcoíris espectral (1.75mm • 1.0 KG neto).</div>
  </div>

  <div class="photo-gallery-3col" style="gap: 9px;">
    <div class="photo-card">
      <img src="{img_silk_tri}" style="height: 140px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Coextrusión Tricolor 120°</span>
        <span class="photo-card-caption">Tres tonalidades nítidas proyectadas sin cambiar de boquilla.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_silk_multi}" style="height: 140px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Colección Rainbow Gradient & Pastel</span>
        <span class="photo-card-caption">Transición tonal armónica y suave cada 15 a 20 metros de extrusión.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_silk_dual_vase}" style="height: 140px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Jarrones & Esculturas Dinámicas</span>
        <span class="photo-card-caption">Reflejos policromáticos de altísima riqueza visual.</span>
      </div>
    </div>
  </div>

  <div class="pricing-bar">
    <div class="pricing-item">
      <span class="pricing-label">SILK TRICOLOR:</span>
      <span class="pricing-amount">Ref. $27.00 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(80 un • 8 combos)</span>
    </div>
    <div class="pricing-item">
      <span class="pricing-label">SILK RAINBOW:</span>
      <span class="pricing-amount">Ref. $27.00 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(40 un • 4 variantes)</span>
    </div>
    <div class="pricing-legal-note">
      Facturación formal en <strong>Bolívares a tasa oficial BCV</strong>.<br />Descuento de contado en divisas / USDT vía WhatsApp.
    </div>
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">PLA SILK TRICOLOR (8 COMBINACIONES TRIPLES EN STOCK)</span>
      <span class="swatches-header-badge">80 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(silk_tri_items, cols=4)}
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">PLA SILK RAINBOW & GRADIENTES ESPECTRALES (4 VARIANTES)</span>
      <span class="swatches-header-badge">40 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(silk_rainbow_items, cols=4)}
  </div>

  <!-- COMPARATIVE OPTICAL EFFECTS GUIDE -->
  <div class="tech-guide-panel" style="padding: 8px 12px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a14.5 14.5 0 0 0 0 20 14.5 14.5 0 0 0 0-20"></path><path d="M2 12h20"></path></svg>
        ANÁLISIS DE EFECTOS ÓPTICOS: TRICOLOR 120° VS. GRADIENTE RAINBOW
      </span>
      <span class="tech-guide-tag">SELECCIÓN ESTÉTICA</span>
    </div>
    <div class="tech-guide-grid-2">
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Tricolor (Efecto Giroscópico Inmediato)</span>
        <span class="guide-card-desc">Tres colores coextruidos divididos a 120°. Cualquier pieza pequeña o grande muestra tres tonos simultáneos según el ángulo. Ideal para dragones articulados y coleccionables.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Silk Rainbow (Gradiente Espectral Continuo)</span>
        <span class="guide-card-desc">El color cambia a lo largo de la bobina cada 15 a 20 metros. En modelos de más de 12 cm de altura, la pieza luce capas completas en degradé suave pastel o arcoíris vivo.</span>
      </div>
    </div>
  </div>

  <!-- RECOMMENDED SLICER SETTINGS -->
  <div class="tech-guide-panel" style="padding: 8px 12px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"></path><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path></svg>
        PARÁMETROS SLICER PARA COEXTRUSIÓN TRICOLOR & RAINBOW
      </span>
      <span class="tech-guide-tag">CONFIGURACIÓN ÓPTIMA</span>
    </div>
    <div class="tech-guide-grid-3">
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Orientación en Cama (Tricolor)</span>
        <span class="guide-card-desc">Evite rotar la bobina durante la impresión. Configure la costura (seam) en 'Alineada' o 'Dorso' para mantener la continuidad cromática.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Altura de Capa Sugerida</span>
        <span class="guide-card-desc">0.16mm a 0.20mm para modelos de exhibición. Permite suficiente volumen por trazo para que las tres tonalidades resalten con igual saturación óptica.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Relleno (Infill) Recomendado</span>
        <span class="guide-card-desc">Giroide o Lightning al 10-15%. Los patrones concéntricos ayudan a que la luz atraviese las paredes perimetrales con mayor luminosidad.</span>
      </div>
    </div>
  </div>

  <div class="tech-specs-bar">
    <div class="spec-item">
      <span class="spec-label">Temperatura Boquilla</span>
      <span class="spec-value">205 – 225 °C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Temperatura Cama</span>
      <span class="spec-value">50 – 60 °C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Ciclo de Gradiente</span>
      <span class="spec-value">15 – 20 metros</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Bobinado</span>
      <span class="spec-value">Tidy Winding ±0.02mm</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Aplicaciones</span>
      <span class="spec-value">Joyería, Trofeos, Arte</span>
    </div>
  </div>

  <div class="order-action-bar">
    <span style="font-size: 8px; color: #CBD5E1;">¿Deseas apartar bobinas Tricolor o Rainbow? Escríbenos con el código SKU.</span>
    <span style="font-family: 'Consolas', monospace; font-size: 8.5px; font-weight: 700; color: #FFFFFF;">WhatsApp: +58 422-3446675 • Despacho en Lechería</span>
  </div>

  <div class="page-footer">
    <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
    <div>ALMACÉN CENTRAL: LECHERÍA, ANZOÁTEGUI</div>
    <div>PÁG. 06 / 09</div>
  </div>
</div>
""")

# =========================================================================
# PAGE 7: TPU 95A, ASA SOLAR & FIBRA DE CARBONO
# =========================================================================
tpu_items = products_by_material.get('TPU 95A Flexible', [])
asa_items = products_by_material.get('ASA Basic Solar UV', [])
cf_items = products_by_material.get('PETG-CF Fibra de Carbono', []) + products_by_material.get('PLA-CF Fibra de Carbono', [])
eng_items = asa_items + cf_items

html_pages.append(f"""
<div class="page" style="gap: 9px;">
  <div class="page-header">
    <div class="header-brand">
      <img src="{img_logo_3d}" class="header-logo" />
      <div>
        <div class="header-brand-title">SYNTRA SUPPLY</div>
        <div class="header-brand-sub">ELASTÓMEROS, INTEMPERIE & ULTRA-RIGIDEZ</div>
      </div>
    </div>
    <div class="header-badge">06 / TÉCNICOS & INGENIERÍA</div>
  </div>

  <div>
    <div class="section-tag">MATERIALES DE ALTO RENDIMIENTO</div>
    <h2 class="page-title">TPU 95A Flexible, ASA Solar & Fibra de Carbono</h2>
    <div class="page-desc">Polímeros especializados para partes mecánicas que requieren absorción de impactos, flexión repetitiva, resistencia solar UV prolongada o máxima rigidez estructural (1.75mm • 1.0 KG neto).</div>
  </div>

  <div class="photo-gallery-3col" style="gap: 9px;">
    <div class="photo-card">
      <img src="{img_tpu_shoe}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">TPU 95A: Flexión Extrema</span>
        <span class="photo-card-caption">450% de elongación a la rotura sin fatiga.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_tpu_models}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Juntas, Sellos & Amortiguación</span>
        <span class="photo-card-caption">Hermeticidad perfecta a fluidos y vibraciones.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_pacf_drone}" style="height: 135px;" />
      <div class="photo-card-body" style="padding: 6px 9px;">
        <span class="photo-card-title">Fibra de Carbono (CF)</span>
        <span class="photo-card-caption">Microfibras de refuerzo para chasis y drones.</span>
      </div>
    </div>
  </div>

  <div class="pricing-bar">
    <div class="pricing-item">
      <span class="pricing-label">TPU 95A:</span>
      <span class="pricing-amount">Ref. $28.50 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(120 un • 10 tonos)</span>
    </div>
    <div class="pricing-item">
      <span class="pricing-label">ASA UV:</span>
      <span class="pricing-amount">Ref. $28.50 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(30 un • 3 tonos)</span>
    </div>
    <div class="pricing-item">
      <span class="pricing-label">CF CARBON:</span>
      <span class="pricing-amount">Ref. $42.00 BCV</span>
      <span style="font-size: 8px; color: #8F9AA9; font-family: 'Consolas', monospace;">(20 un)</span>
    </div>
    <div class="pricing-legal-note">
      Facturación formal en <strong>Bolívares a tasa oficial BCV</strong>.<br />Descuento de contado en divisas / USDT vía WhatsApp.
    </div>
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">TPU 95A FLEXIBLE (10 COLORES DISPONIBLES)</span>
      <span class="swatches-header-badge">120 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(tpu_items, cols=5)}
  </div>

  <div class="swatches-container">
    <div class="swatches-header">
      <span class="swatches-header-title">ASA INTEMPERIE SOLAR UV & FIBRA DE CARBONO (CF)</span>
      <span class="swatches-header-badge">50 UNIDADES EN FÍSICO</span>
    </div>
    {render_swatch_grid(eng_items, cols=5)}
  </div>

  <!-- ADVANCED POLYMER ENGINEERING GUIDE -->
  <div class="tech-guide-panel" style="padding: 9px 12px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 2v20M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/></svg>
        PROTOCOLO INDUSTRIAL PARA POLÍMEROS AVANZADOS
      </span>
      <span class="tech-guide-tag">MANUFACTURA ADITIVA TÉCNICA</span>
    </div>
    <div class="tech-guide-grid-3">
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">TPU 95A (Elastómero Elástico)</span>
        <span class="guide-card-desc">Imprimir a 30-50 mm/s en extrusor directo. Desactivar retracciones agresivas. Inmune a grasas, combustibles e hidrocarburos automotrices.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">ASA Solar UV (Exterior & Náutica)</span>
        <span class="guide-card-desc">Soporta radiación solar directa y agua salina sin amarillear ni fragilizarse. Reemplazo del ABS sin deformación con cama a 90-100°C.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Fibra de Carbono (Boquilla Hardened)</span>
        <span class="guide-card-desc"><strong>Obligatorio boquilla de acero templado.</strong> Módulo de flexión >4500 MPa. Acabado mate granulado para brazos de drones y utillaje.</span>
      </div>
    </div>
  </div>

  <div class="tech-specs-bar">
    <div class="spec-item">
      <span class="spec-label">TPU Temp Boquilla</span>
      <span class="spec-value">210 – 235 °C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">ASA Temp Boquilla/Cama</span>
      <span class="spec-value">240–260°C / 90–110°C</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Boquilla Sugerida CF</span>
      <span class="spec-value">Acero Endurecido</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Resistencia ASA UV</span>
      <span class="spec-value">Exposición Solar Extrema</span>
    </div>
    <div class="spec-item">
      <span class="spec-label">Rigidez CF</span>
      <span class="spec-value">Módulo > 4500 MPa</span>
    </div>
  </div>

  <div class="order-action-bar">
    <span style="font-size: 8px; color: #CBD5E1;">¿Deseas apartar bobinas de TPU, ASA o Fibra de Carbono? Escríbenos con el SKU.</span>
    <span style="font-family: 'Consolas', monospace; font-size: 8.5px; font-weight: 700; color: #FFFFFF;">WhatsApp: +58 422-3446675 • Despacho en Lechería</span>
  </div>

  <div class="page-footer">
    <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
    <div>ALMACÉN CENTRAL: LECHERÍA, ANZOÁTEGUI</div>
    <div>PÁG. 07 / 09</div>
  </div>
</div>
""")

# =========================================================================
# PAGE 8: ECOSISTEMA HARDWARE BAMBU LAB & KINGROON H2D
# =========================================================================
html_pages.append(f"""
<div class="page" style="gap: 9px;">
  <div class="page-header">
    <div class="header-brand">
      <img src="{img_logo_3d}" class="header-logo" />
      <div>
        <div class="header-brand-title">SYNTRA SUPPLY</div>
        <div class="header-brand-sub">SUPERFICIES DE IMPRESIÓN, HOTENDS & ACCESORIOS</div>
      </div>
    </div>
    <div class="header-badge">07 / HARDWARE & REPUESTOS</div>
  </div>

  <div>
    <div class="section-tag">MANTENIMIENTO & DISPONIBILIDAD OPERATIVA</div>
    <h2 class="page-title">Placas Magnéticas, Hotends & Repuestos Críticos</h2>
    <div class="page-desc">Componentes originales y de reemplazo directo para ecosistemas Bambu Lab (X1, P1, A1, A1 Mini) y Kingroon H2D. Asegura que tu taller jamás se detenga por desgaste de piezas.</div>
  </div>

  <div class="photo-gallery-4col" style="gap: 8px;">
    <div class="photo-card">
      <img src="{img_bambu_hardened}" style="height: 125px;" />
      <div class="photo-card-body" style="padding: 6px 8px;">
        <span class="photo-card-title">Hotends A1 / Mini</span>
        <span class="photo-card-caption">Acero endurecido e inoxidable.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_bambu_pei}" style="height: 125px;" />
      <div class="photo-card-body" style="padding: 6px 8px;">
        <span class="photo-card-title">Placa PEI Oro Bambu</span>
        <span class="photo-card-caption">Texturizado doble cara 257mm.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_bambu_peo}" style="height: 125px;" />
      <div class="photo-card-body" style="padding: 6px 8px;">
        <span class="photo-card-title">Placa Diamante PEO</span>
        <span class="photo-card-caption">Patrón holográfico de contacto.</span>
      </div>
    </div>
    <div class="photo-card">
      <img src="{img_bambu_h2d}" style="height: 125px;" />
      <div class="photo-card-body" style="padding: 6px 8px;">
        <span class="photo-card-title">Camas Kingroon H2D</span>
        <span class="photo-card-caption">Gran formato 355x346mm doble PEI.</span>
      </div>
    </div>
  </div>

  <table class="hardware-table">
    <thead>
      <tr>
        <th style="width: 14%;">SKU</th>
        <th style="width: 44%;">Superficie de Construcción / Placa Magnética</th>
        <th style="width: 22%;">Compatibilidad</th>
        <th style="width: 10%;">Stock</th>
        <th style="width: 10%; text-align: right;">Ref. BCV</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>B02553</td><td><strong>Placa PEI Texturizada Oro Doble Cara</strong> (184x184mm)</td><td>Bambu A1 Mini</td><td><span class="swatch-stock">20 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$22.00</td></tr>
      <tr><td>B03151</td><td><strong>Placa Diamante PEO + PEI Texturizada</strong> (184x184mm)</td><td>Bambu A1 Mini</td><td><span class="swatch-stock">20 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$24.00</td></tr>
      <tr><td>B02716</td><td><strong>Placa PEI Texturizada Doble Cara Dorada</strong> (257x257mm)</td><td>Bambu X1 / P1 / A1</td><td><span class="swatch-stock">10 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$34.00</td></tr>
      <tr><td>B02653</td><td><strong>Placa Diamante PEO + Fibra de Carbono PET</strong> (257x257mm)</td><td>Bambu X1 / P1 / A1</td><td><span class="swatch-stock">10 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$38.00</td></tr>
      <tr><td>B02787</td><td><strong>Placa PEO Chameleon Tornasol + PEI</strong> (257x257mm)</td><td>Bambu X1 / P1 / A1</td><td><span class="swatch-stock">10 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$40.00</td></tr>
      <tr><td>XP250402</td><td><strong>Placa Gran Formato Doble PEI</strong> (355x346mm)</td><td>Kingroon H2D</td><td><span class="swatch-stock">10 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$48.00</td></tr>
    </tbody>
  </table>

  <table class="hardware-table">
    <thead>
      <tr>
        <th style="width: 14%;">SKU</th>
        <th style="width: 44%;">Hotend Ensamblado & Boquillas de Alto Flujo</th>
        <th style="width: 22%;">Material / Calibre</th>
        <th style="width: 10%;">Stock</th>
        <th style="width: 10%; text-align: right;">Ref. BCV</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>B02755-58</td><td><strong>Hotend Ensamblado Bambu Inoxidable</strong> (0.2 / 0.4 / 0.6 / 0.8mm)</td><td>Bambu A1 / A1 Mini</td><td><span class="swatch-stock">80 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$19.00</td></tr>
      <tr><td>B02759-62</td><td><strong>Hotend Acero Endurecido Alta Temp</strong> (0.2 / 0.4 / 0.6 / 0.8mm)</td><td>Bambu A1 / A1 Mini</td><td><span class="swatch-stock">80 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$25.00</td></tr>
      <tr><td>XP250413-16</td><td><strong>Hotend Kingroon H2D Hardened Steel</strong> (0.2 / 0.4 / 0.6 / 0.8mm)</td><td>Kingroon H2D</td><td><span class="swatch-stock">80 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$26.00</td></tr>
      <tr><td>XP250417-19</td><td><strong>Hotend Kingroon H2D High-Flow Racing</strong> (0.4 / 0.6 / 0.8mm)</td><td>Kingroon H2D</td><td><span class="swatch-stock">30 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$36.00</td></tr>
    </tbody>
  </table>

  <table class="hardware-table">
    <thead>
      <tr>
        <th style="width: 14%;">SKU</th>
        <th style="width: 44%;">Consumibles, Wipers & Sistema de Extrusión</th>
        <th style="width: 22%;">Presentación</th>
        <th style="width: 10%;">Stock</th>
        <th style="width: 10%; text-align: right;">Ref. BCV</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>XP240809-10</td><td><strong>Wipers Limpiadores de Silicona para Boquilla</strong></td><td>Set x3 unidades (A1 / Mini)</td><td><span class="swatch-stock">100 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$2.50-$4.50</td></tr>
      <tr><td>XP250421</td><td><strong>Funda Térmica de Silicona para Bloque Calefactor H2D</strong></td><td>Unidad sellada alta temp</td><td><span class="swatch-stock">100 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$3.50</td></tr>
      <tr><td>XP240606</td><td><strong>Engranaje Helicoidal de Extrusión en Acero Templado</strong></td><td>Unidad mecanizada CNC</td><td><span class="swatch-stock">10 un</span></td><td style="text-align: right; color: #FFFFFF; font-weight: 800;">$26.00</td></tr>
    </tbody>
  </table>

  <!-- HARDWARE MAINTENANCE & COMPATIBILITY GUIDE -->
  <div class="tech-guide-panel" style="padding: 9px 12px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14.7 6.3a1 1 0 0 0 0 1.4l1.6 1.6a1 1 0 0 0 1.4 0l3.77-3.77a6 6 0 0 1-7.94 7.94l-6.91 6.91a2.12 2.12 0 0 1-3-3l6.91-6.91a6 6 0 0 1 7.94-7.94l-3.76 3.76z"></path></svg>
        GUÍA DE SELECCIÓN DE BOQUILLAS & CUIDADO DE PLACAS PEI
      </span>
      <span class="tech-guide-tag">MANTENIMIENTO PRO</span>
    </div>
    <div class="tech-guide-grid-3">
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Acero Inoxidable vs. Endurecido</span>
        <span class="guide-card-desc">El acero inoxidable es ideal para PLA/PETG básico y piezas no abrasivas. Para fibra de carbono, mármol o glow-in-the-dark, el acero endurecido 55 HRC es obligatorio.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Desprendimiento Automático PEI</span>
        <span class="guide-card-desc">Las placas de acero elástico texturizado liberan las piezas por sí solas una vez que la cama enfría por debajo de 35°C. No requiere espátulas ni pegamentos.</span>
      </div>
      <div class="guide-card" style="padding: 7px 9px;">
        <span class="guide-card-title">Limpieza Preventiva</span>
        <span class="guide-card-desc">Limpiar periódicamente la superficie con alcohol isopropílico al 99% o agua tibia con jabón desengrasante neutro para retirar la grasa de dedos y mantener adhesión 100%.</span>
      </div>
    </div>
  </div>

  <div class="order-action-bar">
    <span style="font-size: 8px; color: #CBD5E1;">¿Necesitas repuestos o placas para tu impresora hoy? Consulta stock directo por WhatsApp.</span>
    <span style="font-family: 'Consolas', monospace; font-size: 8.5px; font-weight: 700; color: #FFFFFF;">WhatsApp: +58 422-3446675 • Despacho en Lechería</span>
  </div>

  <div class="page-footer">
    <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
    <div>ALMACÉN CENTRAL: LECHERÍA, ANZOÁTEGUI</div>
    <div>PÁG. 08 / 09</div>
  </div>
</div>
""")

# =========================================================================
# PAGE 9: LOGÍSTICA, ATENCIÓN, PAGOS & CONTACTO DIRECTO
# =========================================================================
html_pages.append(f"""
<div class="page" style="gap: 10px;">
  <div class="page-header">
    <div class="header-brand">
      <img src="{img_logo_3d}" class="header-logo" />
      <div>
        <div class="header-brand-title">SYNTRA SUPPLY</div>
        <div class="header-brand-sub">PROTOCOLO DE COMPRA, DESPACHO & CONTACTO</div>
      </div>
    </div>
    <div class="header-badge">08 / LOGÍSTICA DIRECTA</div>
  </div>

  <div>
    <div class="section-tag">ATENCIÓN INMEDIATA SIN INTERMEDIARIOS</div>
    <h2 class="page-title">Cómo Adquirir en Syntra Supply</h2>
    <div class="page-desc">Proceso ágil diseñado para abastecer a makers, odontólogos, arquitectos y talleres industriales con entrega récord en todo el oriente del país.</div>
  </div>

  <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 9px;">
    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 13px 14px;">
      <div style="font-family: 'Segoe UI', sans-serif; font-size: 11px; font-weight: 800; color: #FFFFFF; margin-bottom: 4px;">
        1. SELECCIONA TUS SKUS
      </div>
      <div style="font-size: 8.2px; color: #94A3B8; line-height: 1.4;">
        Revisa este catálogo y anota los códigos de filamento, color o repuestos que requiere tu taller para tu orden de producción.
      </div>
    </div>
    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 13px 14px;">
      <div style="font-family: 'Segoe UI', sans-serif; font-size: 11px; font-weight: 800; color: #FFFFFF; margin-bottom: 4px;">
        2. ENVÍA POR WHATSAPP
      </div>
      <div style="font-size: 8.2px; color: #94A3B8; line-height: 1.4;">
        Escríbenos directamente con tu pedido. Confirmamos stock en tiempo real y emitimos tu nota de entrega formal a tasa oficial BCV.
      </div>
    </div>
    <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 13px 14px;">
      <div style="font-family: 'Segoe UI', sans-serif; font-size: 11px; font-weight: 800; color: #FFFFFF; margin-bottom: 4px;">
        3. DESPACHO INMEDIATO
      </div>
      <div style="font-size: 8.2px; color: #94A3B8; line-height: 1.4;">
        Retira personalmente en nuestro almacén en Lechería en 15 min o recibe con delivery express en tu puerta en PLC, BCN o Lechería.
      </div>
    </div>
  </div>

  <div style="background: #0E121A; border: 1px solid rgba(200, 210, 225, 0.16); border-radius: 8px; padding: 11px 14px;">
    <div style="font-family: 'Segoe UI', sans-serif; font-size: 10px; font-weight: 800; color: #FFFFFF; text-transform: uppercase; letter-spacing: 0.08em; margin-bottom: 7px;">
      MATRIZ DE COBERTURA & TIEMPOS DE ENTREGA
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 7px; text-align: center;">
      <div style="background: #141923; padding: 9px 7px; border-radius: 6px; border: 1px solid rgba(200, 210, 225, 0.1);">
        <div style="font-size: 7.5px; color: #8F9AA9; text-transform: uppercase; font-weight: 700;">LECHERÍA</div>
        <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; font-weight: 800; color: #FFFFFF; margin: 2px 0;">15 - 30 MIN</div>
        <div style="font-size: 7.5px; color: #94A3B8;">Retiro o Express</div>
      </div>
      <div style="background: #141923; padding: 9px 7px; border-radius: 6px; border: 1px solid rgba(200, 210, 225, 0.1);">
        <div style="font-size: 7.5px; color: #8F9AA9; text-transform: uppercase; font-weight: 700;">PUERTO LA CRUZ</div>
        <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; font-weight: 800; color: #FFFFFF; margin: 2px 0;">30 - 45 MIN</div>
        <div style="font-size: 7.5px; color: #94A3B8;">Delivery Directo</div>
      </div>
      <div style="background: #141923; padding: 9px 7px; border-radius: 6px; border: 1px solid rgba(200, 210, 225, 0.1);">
        <div style="font-size: 7.5px; color: #8F9AA9; text-transform: uppercase; font-weight: 700;">BARCELONA</div>
        <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; font-weight: 800; color: #FFFFFF; margin: 2px 0;">45 - 90 MIN</div>
        <div style="font-size: 7.5px; color: #94A3B8;">Delivery Directo</div>
      </div>
      <div style="background: #141923; padding: 9px 7px; border-radius: 6px; border: 1px solid rgba(200, 210, 225, 0.1);">
        <div style="font-size: 7.5px; color: #8F9AA9; text-transform: uppercase; font-weight: 700;">TODO EL PAÍS</div>
        <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; font-weight: 800; color: #FFFFFF; margin: 2px 0;">24 - 48 HORAS</div>
        <div style="font-size: 7.5px; color: #94A3B8;">MRW / Tealca / Zoom</div>
      </div>
    </div>
  </div>

  <!-- PAYMENT METHODS -->
  <div class="tech-guide-panel" style="padding: 10px 14px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line></svg>
        MÉTODOS DE PAGO ACEPTADOS & POLÍTICA FISCAL
      </span>
      <span class="tech-guide-tag">FLEXIBILIDAD COMERCIAL</span>
    </div>
    <div class="tech-guide-grid-4">
      <div class="guide-card" style="padding: 8px 9px;">
        <span class="guide-card-title">Pago Móvil / VES</span>
        <span class="guide-card-desc">Banesco, Mercantil, BDV a tasa oficial BCV. Facturación legal con nota de entrega fiscal formal.</span>
      </div>
      <div class="guide-card" style="padding: 8px 9px;">
        <span class="guide-card-title">Binance Pay (USDT)</span>
        <span class="guide-card-desc">Transferencia P2P instantánea directa sin comisiones. Precios especiales con descuento de contado.</span>
      </div>
      <div class="guide-card" style="padding: 8px 9px;">
        <span class="guide-card-title">Efectivo en Divisas ($)</span>
        <span class="guide-card-desc">Pago en mano contra entrega en Lechería. Billetes limpios sin roturas ni tachaduras.</span>
      </div>
      <div class="guide-card" style="padding: 8px 9px;">
        <span class="guide-card-title">Zelle Corporativo</span>
        <span class="guide-card-desc">Aprobación inmediata para empresas, instituciones educativas y compras por volumen.</span>
      </div>
    </div>
  </div>

  <!-- WHOLESALE & VOLUME POLICY -->
  <div class="tech-guide-panel" style="padding: 10px 14px;">
    <div class="tech-guide-header">
      <span class="tech-guide-title">
        <svg width="13" height="13" viewBox="0 0 24 24" fill="none" stroke="#C8D0DC" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
        PLANES PARA TALLERES & COMPRAS AL MAYOR
      </span>
      <span class="tech-guide-tag">PROGRAMA PARTNER</span>
    </div>
    <div class="tech-guide-grid-3">
      <div class="guide-card" style="padding: 8px 9px;">
        <span class="guide-card-title">Pack Taller Maker (5 a 9 Unidades)</span>
        <span class="guide-card-desc">Descuento escalonado para mantener tu producción continua sin interrupciones de stock.</span>
      </div>
      <div class="guide-card" style="padding: 8px 9px;">
        <span class="guide-card-title">Pack Granja 3D (10+ Unidades)</span>
        <span class="guide-card-desc">Precios preferenciales de distribuidor mayorista directo con despacho prioritario y asesoría técnica.</span>
      </div>
      <div class="guide-card" style="padding: 8px 9px;">
        <span class="guide-card-title">Cotizaciones Formales a Empresas</span>
        <span class="guide-card-desc">Atención a clínicas odontológicas, firmas de arquitectura y contratistas industriales con cotizaciones en PDF.</span>
      </div>
    </div>
  </div>

  <!-- GRAND WHATSAPP & QR CENTERPIECE -->
  <div style="background: linear-gradient(135deg, rgba(200, 210, 225, 0.12) 0%, rgba(14, 18, 26, 0.95) 100%); border: 1.5px solid rgba(200, 210, 225, 0.28); border-radius: 8px; padding: 14px 18px; display: flex; align-items: center; justify-content: space-between; box-shadow: 0 6px 20px rgba(0,0,0,0.4);">
    <div style="display: flex; align-items: center; gap: 16px;">
      <img src="{img_qr}" style="width: 85px; height: 85px; border-radius: 8px; background: #FFFFFF; padding: 4px; box-shadow: 0 4px 12px rgba(0,0,0,0.5); flex-shrink: 0;" />
      <div>
        <div style="font-family: 'Segoe UI', sans-serif; font-size: 9px; font-weight: 700; color: #8F9AA9; letter-spacing: 0.14em; text-transform: uppercase;">LÍNEA DIRECTA DE ATENCIÓN & PEDIDOS</div>
        <div style="font-family: 'Segoe UI', sans-serif; font-size: 22px; font-weight: 900; color: #FFFFFF; letter-spacing: 0.04em; margin: 1px 0;">+58 422-3446675</div>
        <div style="font-size: 8.5px; color: #C8D0DC; margin-bottom: 2px;">Enlace directo: <strong>https://wa.me/584223446675</strong></div>
        <div style="font-size: 8px; color: #8F9AA9;">Horario: Lunes a Sábado de 8:00 AM a 7:00 PM • Almacén Central: Lechería, Estado Anzoátegui.</div>
      </div>
    </div>
    <div style="text-align: right; border-left: 1px solid rgba(200, 210, 225, 0.15); padding-left: 16px; max-width: 210px;">
      <div style="font-size: 8px; font-weight: 700; color: #FFFFFF; text-transform: uppercase; margin-bottom: 3px;">CONDICIONES FORMALES</div>
      <div style="font-size: 7.5px; color: #8F9AA9; line-height: 1.35;">
        Precios de lista referenciados a tasa oficial BCV. Descuentos especiales de contado disponibles al consultar por WhatsApp.
      </div>
    </div>
  </div>

  <div class="page-footer">
    <div>SYNTRA SUPPLY • CATÁLOGO INDUSTRIAL 2026</div>
    <div>ALMACÉN CENTRAL: LECHERÍA, ANZOÁTEGUI</div>
    <div>PÁG. 09 / 09</div>
  </div>
</div>
""")

full_html = f"""<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Syntra Supply - Catálogo Maestro Industrial 2026</title>
  <style>
{css_styles}
  </style>
</head>
<body>
{''.join(html_pages)}
</body>
</html>
"""

html_dest = "crm/static/catalogo_master_view.html"
with open(html_dest, "w", encoding="utf-8") as f:
    f.write(full_html)

print(f"HTML master catalog compiled to {html_dest} ({len(full_html)} chars)")

async def render_pdf_and_screenshots():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(
            viewport={'width': 794, 'height': 1123},
            device_scale_factor=2.0
        )
        page = await context.new_page()
        
        file_url = f"file:///{os.path.abspath(html_dest).replace(chr(92), '/')}"
        await page.goto(file_url, wait_until='networkidle')
        await page.wait_for_timeout(1000)
        
        # Render high-res PDF
        pdf_path = 'crm/static/catalogo_syntra_supply.pdf'
        await page.pdf(
            path=pdf_path,
            format='A4',
            print_background=True,
            prefer_css_page_size=True,
            margin={'top': '0mm', 'bottom': '0mm', 'left': '0mm', 'right': '0mm'}
        )
        print(f"High-Res PDF generated at {pdf_path} ({os.path.getsize(pdf_path)} bytes)")

        # Save copies to all required locations
        copies = [
            'crm/static/catalogo.pdf',
            'syntraweb/catalogo_syntra_supply.pdf',
            'syntraweb/catalogo.pdf'
        ]
        with open(pdf_path, 'rb') as f_in:
            data = f_in.read()
        for c_path in copies:
            with open(c_path, 'wb') as f_out:
                f_out.write(data)
            print(f"Copied PDF to {c_path}")

        # Render 9 Retina screenshots
        out_dir = "C:/Users/UNK/.gemini/antigravity/brain/1fbe410f-c733-4b9d-841e-cf76d3274e44"
        pages = await page.query_selector_all('.page')
        print(f"Total pages rendered: {len(pages)}")
        for i, p_elem in enumerate(pages):
            out_img = os.path.join(out_dir, f"retina_page_{i+1}.png")
            await p_elem.screenshot(path=out_img, scale='device')
            print(f"Captured Retina Page {i+1} -> {out_img} ({os.path.getsize(out_img)} bytes)")
            
        await browser.close()

asyncio.run(render_pdf_and_screenshots())
print("ALL TASKS FINISHED SUCCESSFULLY!")
