import os
import sys
import time
from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(line_buffering=True)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_DIR = os.path.join(BASE_DIR, "session_data")

def launch_for_login():
    print(f"[*] Directorio de sesión: {USER_DATA_DIR}", flush=True)
    os.makedirs(USER_DATA_DIR, exist_ok=True)
    
    with sync_playwright() as p:
        print("[*] Abriendo ventana del navegador para WhatsApp...", flush=True)
        context = p.chromium.launch_persistent_context(
            user_data_dir=USER_DATA_DIR,
            headless=False,
            args=[
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled",
                "--start-maximized"
            ],
            viewport=None
        )
        
        page = context.pages[0] if context.pages else context.new_page()
        print("[*] Cargando https://web.whatsapp.com ...", flush=True)
        page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
        
        print("\n" + "="*60, flush=True)
        print("  POR FAVOR ESCANEA EL CÓDIGO QR CON TU TELÉFONO:", flush=True)
        print("  WhatsApp Business > Dispositivos vinculados > Vincular", flush=True)
        print("="*60 + "\n", flush=True)
        
        # Esperar hasta que aparezca el panel de chats o timeout de 5 minutos
        logged_in = False
        start_time = time.time()
        qr_saved = False
        
        while time.time() - start_time < 300:
            try:
                side_panel = page.query_selector("#side")
                chat_list = page.query_selector("[data-testid='chat-list']")
                
                # Guardar captura del QR por si la ventana se abrió minimizada
                if not qr_saved and time.time() - start_time > 8:
                    qr_canvas = page.query_selector("canvas[aria-label='Scan me!']") or page.query_selector("div[data-ref]")
                    if qr_canvas:
                        qr_path = os.path.join(BASE_DIR, "qr_code.png")
                        page.screenshot(path=qr_path)
                        print(f"[*] Captura del código QR guardada en: {qr_path}", flush=True)
                        qr_saved = True

                if side_panel or chat_list:
                    qr_canvas = page.query_selector("canvas[aria-label='Scan me!']") or page.query_selector("div[data-ref]")
                    if not qr_canvas:
                        logged_in = True
                        break
            except Exception:
                pass
            
            time.sleep(2)
        
        if logged_in:
            print("\n[+] ¡ÉXITO! WhatsApp Web conectado y sesión guardada correctamente.", flush=True)
            time.sleep(4)
        else:
            print("\n[-] Tiempo de espera agotado o ventana cerrada sin escanear.", flush=True)
        
        context.close()
        return logged_in

if __name__ == "__main__":
    success = launch_for_login()
    sys.exit(0 if success else 1)
