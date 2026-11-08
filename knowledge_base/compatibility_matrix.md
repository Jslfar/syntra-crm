# MATRIZ MAESTRA DE COMPATIBILIDAD TÉCNICA — SYNTRA SUPPLY

Esta matriz sirve como fuente de verdad única (*Ground Truth*) para el motor de inferencia de compatibilidad y recomendación del agente de Antigravity.

---

## 1. Hotends y Boquillas (Nozzles) por Familia de Impresora

| Fabricante | Modelo de Impresora | Tipo de Sistema de Hotend | Estilo de Boquilla | Materiales Disponibles | Diámetros Recomendados | Compatibilidad Abrasivos (CF/GF/Glow) | SKU / Repuesto Directo Syntra |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Bambu Lab** | A1 / A1 Mini | Quick-Swap Propietario (Clip con pestillo rápido) | Integrada en el bloque disipador (No roscada estándar) | Acero Inox / Acero Endurecido / Latón Heatsink | 0.2, 0.4, 0.6, 0.8 mm | SOLO versiones de Acero Endurecido (Hardened Steel) | `NOZ-BAM-A1-04-HS` / `NOZ-BAM-A1-02-SS` |
| **Bambu Lab** | P1P / P1S / X1-C | Ensamble Completo con fijación 2x M3 frontal | Integrada con garganta bi-metálica o roscada en clones H2D | Acero Inox / Acero Endurecido / Cobre Chapado | 0.2, 0.4, 0.6, 0.8 mm | SOLO versiones Hardened Steel (X1C viene de serie; P1P/P1S requiere upgrade) | `NOZ-BAM-P1-04-HS` / `HOT-BAM-H2D-HF` |
| **Creality** | K1 / K1 Max (Gen 1) | Hotend Cilíndrico de Alto Flujo (Heater cerámico 360°) | M6 x 28 mm Roscada Larga (Volcano-like modificada) | Latón / Bimetálica Cobre-Acero Endurecido | 0.4, 0.6, 0.8 mm | Requiere boquilla bi-metálica o de acero endurecido | `NOZ-CRE-K1-04-BI` |
| **Creality** | K1C / Ender-3 V3 / Ender-3 V3 Plus | Unicorn Quick-Swap All-in-One | Boquilla integrada con garganta de titanio y cobre | Cobre con punta de Acero Endurecido | 0.4, 0.6, 0.8 mm | SÍ, nativo de fábrica | `NOZ-CRE-UNI-04-HS` |
| **Creality** | Ender-3 V2 / Neo / S1 / Pro | Bloque calefactor clásico MK8 / Sprite Extruder | M6 x 13 mm (Estándar MK8) | Latón / Acero Endurecido / CHT Alto Flujo | 0.2, 0.3, 0.4, 0.5, 0.6, 0.8 mm | Versiones Hardened MK8 | `NOZ-MK8-04-BR` / `NOZ-MK8-04-HS` |
| **Elegoo** | Neptune 4 / 4 Pro | Hotend High-Flow con bloque alargado | M6 x 18 mm (Propietaria rosca larga Neptune 4) | Latón / Acero Endurecido | 0.4, 0.6 mm | Solo boquillas de acero para Neptune 4 | `NOZ-ELG-N4-04-BR` |
| **Anycubic** | Kobra 2 / Kobra 2 Pro / Neo | Hotend Volcano-Style | M6 x 21 mm (Volcano Estándar) | Latón / Acero Endurecido / CuCrZr | 0.4, 0.6, 0.8 mm | Boquillas Volcano Hardened Steel | `NOZ-VOL-04-HS` |

---

## 2. Placas de Construcción Magnéticas (Build Plates)

| Dimensiones (mm) | Modelos de Impresora Compatibles | Tipos de Recubrimiento Recomendados | Código QR / Alineación | Temp. Cama Sugerida (PLA / PETG / TPU / ABS) |
| :--- | :--- | :--- | :--- | :--- |
| **184 x 184** (Efectivo 180x180) | Bambu Lab A1 Mini, Kingroon KP3S Pro | PEI Texturizado Oro Doble Cara / PEO Holográfico + Diamante | Muescas traseras para A1 Mini | 60°C / 75°C / 45°C / N/A (Cama máx 80°C) |
| **235 x 235** (Efectivo 220x220 / 235x235) | Creality Ender-3 (Todas), Creality K1, Creality K1C, BIQU B1 | PEI Texturizado / PEI Liso Film / PEO Diamante Carbono | Esquinas biseladas frontales | 60°C / 75°C / 45°C / 100°C |
| **257 x 257** (Efectivo 256x256) | Bambu Lab A1, P1P, P1S, X1-Carbon | PEI Texturizado Oro Doble Cara / PEO Chameleon / PET Fibra / CryoGrip | Con marcas de alineación y lectura LIDAR/Micro-Lidar | 55-65°C / 70-80°C / 40-50°C / 95-105°C |
| **310 x 310 / 300 x 300** | Creality K1 Max, CR-10 Smart, Artillery Sidewinder X1/X2, Neptune 4 Plus | PEI Texturizado Doble Cara con chapa de acero elástico 0.5 mm | Ranuras traseras de posicionamiento | 60°C / 75°C / 45°C / 100°C |
| **355 x 346 / 350 x 350** | Voron 2.4 350mm, Impresoras de Gran Formato Industriales (H2D) | PEI Texturizado Doble Cara / PET Carbon Sheet | Perforaciones para tornillos avellanados según cama | 60°C / 80°C / 50°C / 110°C |

---

## 3. Matriz de Superficie vs. Material y Agente Desmoldante

| Tipo de Superficie | PLA / PLA High-Speed | PETG | TPU (Flexible) | ABS / ASA | Cuidados / Limpieza |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **PEI Texturizado (Gold / Black)** | Directo a 55-65°C. Excelente desmolde al enfriar a <35°C. | Directo a 70-80°C. **NUNCA forzar en caliente**. Despega solo al enfriar. | **OBLIGATORIO** usar pegamento en barra o 3DLAC como desmoldante (evita desgarre de capa PEI). | Directo a 95-105°C con cámara cerrada. | Agua tibia + jabón desengrasante neutro (Dawn/Axion sin crema). Secar con microfibra limpia. Evitar acetona pura continua. |
| **PEI Liso (Smooth Sheet)** | Directo a 55-60°C. Acabado brillante espejo de primera capa. | **PROHIBIDO imprimir directo**. Se fusiona químicamente. Usar pegamento en barra como interfaz desmoldante. | **PROHIBIDO imprimir directo**. Riesgo crítico de arrancar el film de PEI. Usar desmoldante. | Directo a 100-110°C. Ocasionalmente requiere laca para prevenir warping en esquinas filosas. | Alcohol Isopropílico (IPA) al 99% entre impresiones. No usar acetona (degrada el film liso). |
| **PEO / PET Holográfico / Patrón Carbono** | Directo a 50-60°C. Transfiere el patrón fractal o tridimensional exacto a la pieza. | Directo a 65-75°C. Probar adherencia moderada. | Usar capa fina de adhesivo líquido como desmoldante preventivo. | No recomendado en láminas PEO estándar (la temperatura >85°C deslamina el adhesivo decorativo). | Limpiar EXCLUSIVAMENTE con alcohol isopropílico 99% y paño suave sin pelusa. No frotar con esponjas abrasivas. |
| **CryoGrip / Placa Fría (Cool Plate)** | Directo a 30-45°C. Reduce el calor interior en Bambu X1/P1S evitando atascos por Heat Creep. | No recomendado para placas frías sin pegamento líquido Bambu. | Directo a 30-40°C con adhesivo líquido. | Requiere placa de alta temperatura (>90°C). | Limpieza con IPA 99% y agua tibia. |

---

## 4. Repuestos Mecánicos Críticos de Rápida Rotación

| Componente | Máquinas Compatibles | Síntoma de Falla / Desgaste | Vida Útil Estimada | SKU Syntra |
| :--- | :--- | :--- | :--- | :--- |
| **Cortador de Filamento (Cutter Blade)** | Bambu Lab P1 / X1 / A1 | Error de descarga de filamento (*AMS filament retract failed*), corte mordido no recto. | 3,000 a 5,000 cortes mecánicos | `REP-CUT-BAM-P1` / `REP-CUT-BAM-A1` |
| **Limpiador de Boquilla (Wiper) de Silicona** | Bambu Lab A1 / A1 Mini | Acumulación de restos plásticos en boquilla, bolas de filamento sueltas en la cama. | 250 a 400 horas de impresión | `REP-WIP-BAM-A1` / `REP-WIP-BAM-MINI` |
| **Calcetín de Silicona (Silicone Sock)** | Ecosistema Bambu / Creality K1 | Errores de fluctuación de temperatura (*Thermal Runaway / Heater Error*), boquilla sucia. | 500 horas o tras retiro de atasco severo | `REP-SCK-BAM-H2D` / `REP-SCK-CRE-K1` |
| **Engranajes de Extrusor en Acero Endurecido** | Bambu Lab P1P / P1S (Upgrade de inox a endurecido) | Dientes mellados por imprimir filamentos con fibra de carbono (CF), salto de pasos y sub-extrusión. | >2,500 horas con filamento abrasivo | `GEAR-EXT-BAM-HS` |
| **Tubo PTFE de Baja Fricción (Capricorn)** | Conexión AMS, Cabezal de Extrusor, Bowden | Resistencia en alimentación de filamento, errores de sensor de filamento atascado. | 800 a 1,200 horas | `ACC-PTFE-CAPRICORN` |
| **Conectores Neumáticos PC4-M6 / PC4-M10** | Uniones de tubos PTFE en cabezal y buffer | Tubo PTFE se suelta durante retracciones rápidas de 30-60 mm/s. | 6 a 12 meses de operación activa | `REP-CONN-PC4-M6` / `REP-CONN-PC4-M10` |
