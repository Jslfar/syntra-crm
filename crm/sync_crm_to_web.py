def push_to_github_background():
    import threading, subprocess
    def _push():
        try:
            script_dir = os.path.dirname(os.path.abspath(__file__))
            root_dir = os.path.dirname(script_dir) if os.path.basename(script_dir) == 'crm' else script_dir
            web_dir = os.path.join(root_dir, 'syntraweb')
            subprocess.run(['git', '-C', web_dir, 'add', 'lib/manifest.js', 'index.html'], capture_output=True, text=True)
            res = subprocess.run(['git', '-C', web_dir, 'commit', '-m', 'auto(sync): actualizar stock disponible tras operacion en CRM'], capture_output=True, text=True)
            if res.returncode == 0:
                subprocess.run(['git', '-C', web_dir, 'push', 'origin', 'main'], capture_output=True, text=True)
                print("[Syntra Sync] Cambios de inventario subidos a GitHub con exito.")
        except Exception as err:
            print(f"[Syntra Sync] Auto-push omitido: {err}")

    t = threading.Thread(target=_push, daemon=True)
    t.start()

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

CURIOSITIES_3D_POOL = [
    {
        "id": 1,
        "badge": "Tip 1 • Adherencia PEI",
        "title": "Higiene y Limpieza de Camas PEI",
        "text": "Lavar la placa PEI con agua tibia y jabón líquido desengrasante para platos restaura el 100% de la adherencia sin usar fijadores químicos ni alcohol isopropílico."
    },
    {
        "id": 2,
        "badge": "Tip 2 • Flujo Volumétrico",
        "title": "Flujo Volumétrico Máximo en PLA",
        "text": "Los filamentos Kingroon alcanzan 21 mm³/s de flujo volumétrico continuo en Bambu Lab, permitiendo velocidades de 500 mm/s sin capas débiles."
    },
    {
        "id": 3,
        "badge": "Tip 3 • Fibra de Carbono",
        "title": "Protección Anti-Abrasión de Boquillas",
        "text": "Filamentos como PETG-CF y PA-CF desgastan una boquilla de latón en menos de 500g. Usa siempre boquillas de Acero Endurecido de 0.4mm o 0.6mm."
    },
    {
        "id": 4,
        "badge": "Tip 4 • Secado de TPU",
        "title": "Cero Poros e Hilos en TPU 95A",
        "text": "El TPU absorbe humedad en 6 horas. Imprimir directo desde un secador Sunlu S2 a 50°C elimina las burbujas de vapor y deja acabados de goma limpios."
    },
    {
        "id": 5,
        "badge": "Tip 5 • Efecto Seda",
        "title": "Máximo Brillo Metalizado en PLA Silk",
        "text": "Imprime las paredes externas de filamentos Silk Dual y Tri-Color a 215°C–220°C y velocidad moderada de 80 mm/s para resaltar el brillo espejo."
    },
    {
        "id": 6,
        "badge": "Tip 6 • Mantenimiento Bambu A1",
        "title": "Limpiadores de Silicona de Nozzle",
        "text": "Reemplazar los limpiadores de silicona en la Bambu Lab A1 Mini evita que restos de filamento quemado manchen la primera capa de tus impresiones."
    },
    {
        "id": 7,
        "badge": "Tip 7 • Resistencia UV",
        "title": "ASA vs ABS para Piezas Exteriores",
        "text": "El ASA posee resistencia natural a rayos solar UV y no amarillea ni se cristaliza expuesto al sol directo, siendo ideal para autopartes y carcasas."
    },
    {
        "id": 8,
        "badge": "Tip 8 • Factor",
        "title": "Pressure Advance para Esquinas Afiladas",
        "text": "Ajustar el Factor K (0.020–0.025 para extrusión directa Bambu) elimina los abultamientos en las esquinas de tus piezas a alta velocidad."
    },
    {
        "id": 9,
        "badge": "Tip 9 • Scarf Seams",
        "title": "Costuras Invisibles en Bambu Studio",
        "text": "Configurar Scarf Seams con altura inicial de 0.02 mm y longitud de 20 mm logra costuras verticales prácticamente imperceptibles en figuras redondas."
    },
    {
        "id": 10,
        "badge": "Tip 10 • Hop",
        "title": "Evita Arañazos en Capas Superiores",
        "text": "Usar Z-Hop en espiral (0.2–0.4 mm) junto con Wipe While Retracting evita que la boquilla arrastre plástico caliente sobre superficies lisas."
    },
    {
        "id": 11,
        "badge": "Tip 11 • Placas PEO Diamante",
        "title": "Transferencia Holográfica en la Cama",
        "text": "Las placas PEO Diamante transfieren el patrón geométrico grabado con láser directamente a la cara inferior de tu modelo sin químicos."
    },
    {
        "id": 12,
        "badge": "Tip 12 • Adherencia de ABS",
        "title": "Cámara Cerrada y Temperatura de Cama",
        "text": "El ABS requiere cama a 90°C–100°C y ambiente cerrado sin corrientes de aire para prevenir el desprendimiento de esquinas (warping)."
    },
    {
        "id": 13,
        "badge": "Tip 13 • Impresión con Madera",
        "title": "Lijado y Barnizado de PLA Wood",
        "text": "El filamento PLA Wood contiene 20% de fibras sintéticas de madera. Puedes lijarlo con lija de agua fina y aplicar barniz de madera real."
    },
    {
        "id": 14,
        "badge": "Tip 14 • Enfriamiento de Capa",
        "title": "Ventilador Auxiliar en Bambu X1/P1",
        "text": "Apagar o reducir el ventilador auxiliar al 10–20% en piezas grandes de PETG evita la deformación por choque térmico unilateral."
    },
    {
        "id": 15,
        "badge": "Tip 15 • Cambio de Boquilla",
        "title": "Torque en Caliente de Hotends",
        "text": "Al cambiar boquillas desmontables en hotends de acero, aprieta la boquilla a 250°C para evitar fugas de plástico caliente por la rosca."
    },
    {
        "id": 16,
        "badge": "Tip 16 • Tolerancias Mecánicas",
        "title": "Holgura para Piezas Ensamblables",
        "text": "Un margen de diseño de 0.2 mm entre piezas móviles garantiza que engranajes y bisagras impresas en PLA giren libremente sin lijar."
    },
    {
        "id": 17,
        "badge": "Tip 17 • PETG Transparente",
        "title": "Efecto Vidrio Translucido",
        "text": "Imprime PETG Transparente a 240°C, altura de capa de 0.1 mm, 100% de relleno en una sola dirección y ventilador al 0% para máxima claridad."
    },
    {
        "id": 18,
        "badge": "Tip 18 • CF Nylon CF",
        "title": "Sustituto de Aluminio en Ingeniería",
        "text": "El Nylon PA-CF ofrece una resistencia a la tracción superior a 110 MPa, siendo ideal para soportes de motores y herramental industrial."
    },
    {
        "id": 19,
        "badge": "Tip 19 • Horario Continuo",
        "title": "Atención 6:00 AM a 11:00 PM",
        "text": "Syntra Supply atiende urgencias de materiales y repuestos en Lechería de Lunes a Domingo de 6am a 11pm."
    },
    {
        "id": 20,
        "badge": "Tip 20 • Almacén Lechería",
        "title": "Retiro Directo o Delivery Express",
        "text": "Ubicados en Sector Morro II, ofrecemos retiro en almacén o despacho en minutos para la Zona Norte de Anzoátegui."
    },
    {
        "id": 21,
        "badge": "Tip 21 • Envíos Nacionales",
        "title": "MRW, Zoom y Tealca Diarios",
        "text": "Despachamos encomiendas nacionales a toda Venezuela el mismo día para compras procesadas antes de las 5:00 PM."
    },
    {
        "id": 22,
        "badge": "Tip 22 • Múltiples Formas de Pago",
        "title": "Binance P2P, Zelle y BCV",
        "text": "Aceptamos Binance USDT, Zelle, Pago Móvil a Tasa Oficial BCV y Efectivo USD en nuestro almacén central."
    },
    {
        "id": 23,
        "badge": "Tip 23 • Flota de Pruebas",
        "title": "Validación en Bambu A1 Mini & A2L",
        "text": "Todos nuestros filamentos son probados en nuestra flota interna para certificar tolerancia de ±0.02 mm y fluidez perfecta."
    },
    {
        "id": 24,
        "badge": "Tip 24 • Remover Pegamento",
        "title": "Agua Caliente para Camas de Vidrio",
        "text": "El pegamento en barra sobre camas de vidrio se disuelve en segundos con un paño humedecido en agua tibia sin usar navajas."
    },
    {
        "id": 25,
        "badge": "Tip 25 • Engranajes de Extrusor",
        "title": "Acero Endurecido Helicoidal",
        "text": "Los engranajes helicoidales traccionan el filamento con menor vibración armónica, reduciendo patrones de bandeo vertical (VFA)."
    },
    {
        "id": 26,
        "badge": "Tip 26 • Torre de Temperatura",
        "title": "Encontrar el Punto Dulce del Filamento",
        "text": "Imprimir una torre de temperatura cada vez que abres una marca nueva identifica la mejor resistencia entre capas y acabado."
    },
    {
        "id": 27,
        "badge": "Tip 27 • Ancho de Línea",
        "title": "Regla del 120% del Diámetro de Boquilla",
        "text": "Ajustar el ancho de línea a 0.48 mm para una boquilla de 0.4 mm mejora la adherencia entre paredes y reduce el tiempo total."
    },
    {
        "id": 28,
        "badge": "Tip 28 • Flujo Volumétrico TPU",
        "title": "Límite de Velocidad en Flexibles",
        "text": "El TPU 95A debe limitarse a un flujo volumétrico de 3–5 mm³/s para evitar que el filamento elástico se enrolle en la rueda del extrusor."
    },
    {
        "id": 29,
        "badge": "Tip 29 • Deformación Cama Caliente",
        "title": "Esperar Enfriamiento Antes de Retirar",
        "text": "Dejar enfriar la placa PEI por debajo de 35°C permite que la pieza se desprenda sola sin doblar ni rayar la lámina magnética."
    },
    {
        "id": 30,
        "badge": "Tip 30 • Color",
        "title": "Orientación de Modelo en la Cama",
        "text": "Rotar la pieza 45° sobre la cama cambia el ángulo de revelación de los dos colores en filamentos Silk Dual-Color."
    },
    {
        "id": 31,
        "badge": "Tip 31 • Ahorro de Energía",
        "title": "Fundas de Silicona en Hotends",
        "text": "La funda aislante de silicona conserva el calor del bloque térmico, reduciendo el consumo eléctrico de la impresora en un 20%."
    },
    {
        "id": 32,
        "badge": "Tip 32 • Luz UV en Resina",
        "title": "Post-Curado Uniforme",
        "text": "Lavar la pieza impresa en resina con alcohol isopropílico al 99% y secar completamente antes del curado UV evita manchas blancas."
    },
    {
        "id": 33,
        "badge": "Tip 33 • Desatasco de Boquilla",
        "title": "Método Cold Pull con Nylon / PETG",
        "text": "Insertar filamento a 230°C, dejar enfriar a 90°C y tirar firmemente remueve micro-residuos de dentro de la garganta del hotend."
    },
    {
        "id": 34,
        "badge": "Tip 34 • Almacenamiento Sellado",
        "title": "Bolsas de Vacío con Gel de Sílice",
        "text": "Guardar tus carretes abiertos en bolsas herméticas con desecante preserva las propiedades del polímero durante meses."
    },
    {
        "id": 35,
        "badge": "Tip 35 • Etiquetas de Carretes",
        "title": "Anotar Peso Vacío de la Spool",
        "text": "Pesar el carrete plástico vacío te permite saber exactamente cuántos gramos de filamento te quedan antes de mandar una impresión larga."
    },
    {
        "id": 36,
        "badge": "Tip 36 • Primera Capa Perfecta",
        "title": "Compensación Babystep Z",
        "text": "Ajustar el offset Z en pasos de 0.01 mm durante las líneas de purga asegura que el plástico quede levemente aplastado sin rozar."
    },
    {
        "id": 37,
        "badge": "Tip 37 • Velocidad de Purga AMS",
        "title": "Ajuste de Multiplicador de Purga",
        "text": "Reducir el volumen de purga en cambios de color similares ahorra hasta un 40% de filamento desperdiciado en torres de purga."
    },
    {
        "id": 38,
        "badge": "Tip 38 • CF",
        "title": "Resistencia a Químicos e Impacto",
        "text": "El PETG-CF combina la rigidez de la fibra de carbono con la tolerancia química a aceites y combustibles del PETG."
    },
    {
        "id": 39,
        "badge": "Tip 39 • Infill Giroide",
        "title": "Resistencia Multidireccional Isotrópica",
        "text": "El relleno Giroide ofrece igual resistencia mecánica en ejes X, Y y Z evitando los colapsos internos del relleno rejilla."
    },
    {
        "id": 40,
        "badge": "Tip 40 • Flow H2D",
        "title": "Fundición Ultra Rápida 32 mm³/s",
        "text": "El hotend H2D de alto flujo cuenta con una zona de fusión extendida para mantener la temperatura en boquillas de 0.8 mm."
    },
    {
        "id": 41,
        "badge": "Tip 41 • Tolerancia Filamento",
        "title": "Control Láser de Diámetro ±0.02 mm",
        "text": "Kingroon utiliza sensores láser duales en fábrica para garantizar diámetro constante de 1.75 mm y evitar atascos."
    },
    {
        "id": 42,
        "badge": "Tip 42 • Costura de Inicio",
        "title": "Ubicación en Esquinas Ocultas",
        "text": "Alinear la costura de inicio en las esquinas traseras del modelo evita puntos visibles en caras frontales estéticas."
    },
    {
        "id": 43,
        "badge": "Tip 43 • Temperatura de Transición Vitrea",
        "title": "Límite HDT de Materiales",
        "text": "El PLA se ablanda a los 55°C, mientras que el PETG resiste 75°C y el ABS/ASA hasta 95°C sin deformarse bajo carga."
    },
    {
        "id": 44,
        "badge": "Tip 44 • Aislamiento de Cables",
        "title": "Fundas Ignífugas de Hotend",
        "text": "Proteger los cables del termistor y cartucho calefactor evita cortocircuitos accidental durante la limpieza de la boquilla."
    },
    {
        "id": 45,
        "badge": "Tip 45 • Stamping",
        "title": "Impresión en Frío de PLA",
        "text": "Las placas Cold-Stamping permiten imprimir PLA con la cama a temperatura ambiente (25°C), ahorrando energía."
    },
    {
        "id": 46,
        "badge": "Tip 46 • PLA Mármol Decorativo",
        "title": "Disimulo Total de Capas",
        "text": "Las micro-motas oscuras del PLA Mármol rompen la luz refractada, logrando esculturas y jarrones donde no se notan las capas."
    },
    {
        "id": 47,
        "badge": "Tip 47 • Ajuste de Correa",
        "title": "Frecuencia de Tensión en Ejes X/Y",
        "text": "Ajustar las correas de distribución a una frecuencia de resonancia de 110 Hz elimina el ghosting y los ecos en las paredes."
    },
    {
        "id": 48,
        "badge": "Tip 48 • Soporte en Árbol",
        "title": "Tree Supports con Cero Marcado",
        "text": "Usar soportes tipo árbol con distancia Z de 0.2 mm permite retirarlos con la mano dejando una interfaz limpia."
    },
    {
        "id": 49,
        "badge": "Tip 49 • Relleno Variable",
        "title": "Adaptive Infill por Altura",
        "text": "Aumentar la densidad de relleno solo cerca de las superficies superiores ahorra tiempo y material en piezas volumétricas grandes."
    },
    {
        "id": 50,
        "badge": "Tip 50 • Asesoría Syntra Supply",
        "title": "Soporte Técnico Directo por WhatsApp",
        "text": "Si tienes dudas sobre qué material usar para tu proyecto, escríbenos a WhatsApp y un ingeniero en impresión 3D te guiará gratis."
    }
]

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
            "crm_category": crm_cat,
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
        "curiosities3D": CURIOSITIES_3D_POOL,
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
        index_content = re.sub(r'\?v=20261109_[a-zA-Z0-9_]+', '?v=20261109_v20_live', index_content)

        with open(index_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(index_content)

    push_to_github_background()
    return len(products_list), sum(p['stock_qty'] for p in products_list)

if __name__ == '__main__':
    cnt, stk = sync_crm_database_to_manifest()
    print(f"[EXITO] Sincronización finalizada: {cnt} productos con {stk} unidades físicas.")
