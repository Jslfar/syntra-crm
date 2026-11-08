import os
import sys
import argparse
import json
from whatsapp_agent import WhatsAppClient
import login

def cmd_login(args):
    print("[*] Iniciando asistente de vinculación por código QR...")
    success = login.launch_for_login()
    if success:
        print("[+] Dispositivo vinculado exitosamente con WhatsApp Business.")
    else:
        print("[-] No se pudo completar la vinculación.")

def cmd_status(args):
    try:
        with WhatsAppClient(headless=True) as client:
            if client.is_connected():
                print(json.dumps({"status": "connected", "message": "Sesión activa y lista"}, indent=2))
            else:
                print(json.dumps({"status": "disconnected", "message": "Sesión no iniciada. Requiere login."}, indent=2))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))

def cmd_list(args):
    try:
        with WhatsAppClient(headless=True) as client:
            res = client.get_chats_overview(limit=args.limit)
            print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))

def cmd_read(args):
    try:
        with WhatsAppClient(headless=True) as client:
            opened = client.open_chat(args.name)
            if not opened:
                print(json.dumps({"status": "error", "message": f"No se pudo encontrar el chat '{args.name}'"}, indent=2))
                return
            messages = client.get_last_messages(count=args.count)
            print(json.dumps({"status": "ok", "chat": args.name, "messages": messages}, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))

def cmd_send(args):
    try:
        with WhatsAppClient(headless=True) as client:
            opened = client.open_chat(args.name)
            if not opened:
                print(json.dumps({"status": "error", "message": f"No se pudo encontrar el chat '{args.name}'"}, indent=2))
                return
            res = client.send_message(args.message)
            print(json.dumps(res, indent=2, ensure_ascii=False))
    except Exception as e:
        print(json.dumps({"status": "error", "message": str(e)}, indent=2))

def main():
    parser = argparse.ArgumentParser(description="Puente de WhatsApp para Syntra Group")
    subparsers = parser.add_subparsers(dest="command", help="Comando a ejecutar")
    
    # login
    subparsers.add_parser("login", help="Abre ventana para escanear código QR")
    
    # status
    subparsers.add_parser("status", help="Comprueba el estado de conexión")
    
    # list
    p_list = subparsers.add_parser("list", help="Lista los chats recientes y pendientes")
    p_list.add_argument("--limit", type=int, default=10, help="Cantidad de chats a listar")
    
    # read
    p_read = subparsers.add_parser("read", help="Lee los últimos mensajes de un contacto")
    p_read.add_argument("--name", required=True, help="Nombre o número del contacto")
    p_read.add_argument("--count", type=int, default=8, help="Número de mensajes a leer")
    
    # send
    p_send = subparsers.add_parser("send", help="Envía un mensaje a un contacto")
    p_send.add_argument("--name", required=True, help="Nombre o número del contacto")
    p_send.add_argument("--message", required=True, help="Contenido del mensaje a enviar")
    
    args = parser.parse_args()
    
    if args.command == "login":
        cmd_login(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "list":
        cmd_list(args)
    elif args.command == "read":
        cmd_read(args)
    elif args.command == "send":
        cmd_send(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
