import os
import sys
import time
import json
from playwright.sync_api import sync_playwright

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
USER_DATA_DIR = os.path.join(BASE_DIR, "session_data")
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

class WhatsAppClient:
    def __init__(self, headless=True):
        self.headless = headless
        self.playwright = None
        self.context = None
        self.page = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        
        launch_args = {
            "user_data_dir": USER_DATA_DIR,
            "headless": self.headless,
            "args": [
                "--no-sandbox",
                "--disable-blink-features=AutomationControlled"
            ]
        }
        if os.path.exists(EDGE_PATH):
            launch_args["executable_path"] = EDGE_PATH
            
        self.context = self.playwright.chromium.launch_persistent_context(**launch_args)
        self.page = self.context.pages[0] if self.context.pages else self.context.new_page()
        self.page.goto("https://web.whatsapp.com", wait_until="domcontentloaded")
        
        self._wait_for_ready()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.context:
            self.context.close()
        if self.playwright:
            self.playwright.stop()

    def _wait_for_ready(self, timeout=30):
        start = time.time()
        while time.time() - start < timeout:
            if self.page.query_selector("#side") or self.page.query_selector("[data-testid='chat-list']"):
                # Si hay algún popup de bienvenida o etiquetas, hacer clic para descartarlo
                time.sleep(1)
                try:
                    self.page.mouse.click(628, 795)
                except:
                    pass
                return True
            time.sleep(1)
        return False

    def is_connected(self):
        return bool(self.page.query_selector("#side") or self.page.query_selector("[data-testid='chat-list']"))

    def get_chats_overview(self, limit=10):
        if not self.is_connected():
            return {"status": "error", "message": "No hay sesión activa"}
        
        time.sleep(2)
        chats_data = self.page.evaluate("""(limit) => {
            const rows = document.querySelectorAll('#pane-side [role="row"], #pane-side div[role="listitem"]');
            const result = [];
            
            rows.forEach((row) => {
                if (result.length >= limit) return;
                const titleEl = row.querySelector('[title]');
                const name = titleEl ? titleEl.getAttribute('title') : '';
                if (!name) return;
                
                const spans = Array.from(row.querySelectorAll('span'));
                let preview = '';
                let unreadCount = 0;
                
                const unreadBadge = row.querySelector('[aria-label*="no leído"], [aria-label*="unread"]');
                if (unreadBadge) {
                    const badgeText = unreadBadge.getAttribute('aria-label') || unreadBadge.textContent;
                    const match = badgeText.match(/\\d+/);
                    unreadCount = match ? parseInt(match[0], 10) : 1;
                }
                
                const textNodes = spans.map(s => s.textContent.trim()).filter(t => t.length > 0);
                if (textNodes.length > 1) {
                    preview = textNodes[textNodes.length - 1];
                }
                
                result.push({
                    name: name,
                    preview: preview,
                    unread: unreadCount
                });
            });
            return result;
        }""", limit)
        return {"status": "ok", "chats": chats_data}

    def open_chat(self, chat_name):
        time.sleep(2)
        # 1. Intentar clic directo si está en la lista visible
        chat_el = self.page.query_selector(f"#pane-side span[title='{chat_name}']")
        if not chat_el:
            chat_el = self.page.query_selector(f"xpath=//div[@id='pane-side']//span[contains(@title, '{chat_name}')]")
            
        if chat_el:
            chat_el.click()
            time.sleep(2)
            return True
            
        # 2. Buscar mediante el buscador
        search_box = (
            self.page.query_selector("div[contenteditable='true'][data-tab='3']") or 
            self.page.query_selector("#side div[role='textbox']") or
            self.page.query_selector("#side div[contenteditable='true']")
        )
        if search_box:
            search_box.click()
            self.page.keyboard.press("Control+A")
            self.page.keyboard.press("Backspace")
            search_box.fill(chat_name)
            time.sleep(2)
            self.page.keyboard.press("Enter")
            time.sleep(2)
            return True
        return False

    def get_last_messages(self, count=8):
        time.sleep(1)
        messages = self.page.evaluate("""(count) => {
            const rows = document.querySelectorAll('#main div[role="row"]');
            const result = [];
            const items = Array.from(rows).slice(-count);
            
            items.forEach(row => {
                const textEl = row.querySelector('.selectable-text, .copyable-text');
                const metaEl = row.querySelector('[data-pre-plain-text]');
                const meta = metaEl ? metaEl.getAttribute('data-pre-plain-text') : '';
                const text = textEl ? textEl.textContent.trim() : row.textContent.trim();
                
                if (text) {
                    result.push({
                        sender: meta.trim() || 'Desconocido',
                        text: text
                    });
                }
            });
            return result;
        }""", count)
        return messages

    def send_message(self, message):
        time.sleep(1)
        msg_input = (
            self.page.query_selector("#main footer div[contenteditable='true']") or 
            self.page.query_selector("#main footer [role='textbox']") or
            self.page.query_selector("footer [data-lexical-editor='true']")
        )
        
        if not msg_input:
            return {"status": "error", "message": "No se encontró el campo de texto en el chat"}
            
        msg_input.click()
        time.sleep(0.5)
        
        # Enviar texto
        self.page.evaluate("""(text) => {
            const dt = new DataTransfer();
            dt.setData('text/plain', text);
            const evt = new ClipboardEvent('paste', { clipboardData: dt, bubbles: true });
            document.activeElement.dispatchEvent(evt);
        }""", message)
        
        time.sleep(1)
        self.page.keyboard.press("Enter")
        time.sleep(2)
        return {"status": "ok", "message": "Mensaje enviado exitosamente"}
