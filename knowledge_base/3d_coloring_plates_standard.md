# 🎨 ESTÁNDAR MAESTRO: LIENZOS 3D COLORING PLATES — SYNTRA LAB
*Documento de Memoria y Reglas de Diseño de Producto*

---

## 1. HARDWARE Y CAPACIDADES DEL TALLER
* **Máquina Principal:** Bambu Lab A1 Mini (Cama de impresión: $180 \times 180 \times 180\text{ mm}$).
* **Sistema de Color:** AMS Lite (Impresión multicolor nativa automática).
* **Filamentos:** Kingroon PLA / PETG técnicos (distribuidos por Syntra Supply).
* **Boquilla estándar:** $0.4\text{ mm}$ (motor de corte Arachne en Bambu Studio).

---

## 2. REGLAS ESTÉTICAS Y DE TRAZO (DISEÑO ULTRA ESTÉTICO)
* **Grosor de Línea Interior (Líneas Negras):** **`0.85 mm` a `1.00 mm`**.
  * Equivale exactamente a **2 perímetros limpios** con boquilla de $0.4\text{ mm}$.
  * Evita la sensación de "dibujo tosco o infantil de trazo grueso".
  * Deja el **máximo espacio interior útil** para que el cliente pinte con comodidad.
* **Grosor del Marco / Borde Exterior:** **`1.50 mm` a `1.80 mm`** (le da soporte estructural sin robar espacio visual).
* **Fondo del Lienzo (Base donde se pinta):** **100% PLANO y LISO**.
  * Altura de la base: **`1.40 mm` a `1.60 mm`** (7 u 8 capas a 0.20 mm).
* **Altura de las Paredes en Relieve:** **`1.00 mm` a `1.20 mm` por encima de la base** (Altura total del modelo: `2.60 mm`).
  * Profundidad perfecta: retiene rotuladores acrílicos sin sobresalir en exceso ni gastar filamento innecesario.
* **Estilo Visual:** **Kawaii / Chibi / Estética Japonesa Limpia (Pokémon / Sanrio).**
  * Siluetas redondeadas, proporciones tiernas, celdas amplias y armónicas, trazos fluidos sin vértices cortantes.

---

## 3. CHECKLIST DE VALIDACIÓN ANTES DE EXPORTAR STL
1. ¿Las líneas interiores tienen entre 0.85 mm y 1.0 mm?
2. ¿El fondo de todas las cavidades está a la misma altura plana?
3. ¿Las cavidades tienen suficiente espacio abierto para pintar cómodamente?
4. ¿El modelo cabe en la cama de 180x180 mm de la A1 Mini?
5. ¿Requiere soportes? (Debe ser SIEMPRE 0% soportes).


---

## 5. REGLA DE OPTIMIZACIÓN DE MALLA Y RENDIMIENTO DEL LAMINADOR (BAMBU STUDIO FIX)
* **Causa del cuelgue al laminar:** Si la base o las líneas se generan como grillas raster densas, el modelo supera los **1.000.000 de triángulos**, haciendo que el motor booleano de Bambu Studio se congele al calcular intersecciones coplanares.
* **Solución permanente de Syntra Lab:**
  1. La **Base Blanca** se genera como un prisma vectorial de bordes redondeados (**~150 triángulos** en total).
  2. Las **Líneas Negras** se extruyen como cintas vectoriales suaves (**~24.000 triángulos** en total).
  3. El archivo `.3MF` pesa menos de **200 KB** y Bambu Studio lo lamina en **menos de 1 segundo sin tirones**.
