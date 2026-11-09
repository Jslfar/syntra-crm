# ⚙️ PERFIL MAESTRO DE PRODUCCIÓN BAMBU STUDIO — SYNTRA ART-TILES
*Optimización Integral para Bambu Lab A1 Mini + AMS Lite (Boquilla 0.4 mm)*
*Categoría: Cuadros y Lienzos 2.5D para Colorear / Decoración Coleccionable*
*Fecha de Registro: 2026-11-08 | Syntra Lab Standard v1.0*

---

## 1. RESUMEN EJECUTIVO DE RENDIMIENTO POR UNIDAD

| Métrica | Perfil Estándar Genérico | Perfil Maestro SYNTRA | Impacto / Beneficio |
| :--- | :---: | :---: | :--- |
| **Tiempo de Impresión** | ~52 min | **~34 - 38 min** | **-28% de tiempo por pieza** |
| **Consumo PLA Blanco** | 22.0 g | **21.5 g** | Base rígida y 100% opaca |
| **Consumo PLA Negro** | 8.5 g | **5.8 g** | Paredes sólidas sin gap-fill innecesario |
| **Desperdicio en Purga AMS** | 14.5 g (torre grande + 280 mm³) | **2.8 g** (torre 20 mm + 70 mm³) | **-80% de plástico a la basura** |
| **Costo Landed Total (Lechería)** | $0.65 USD | **$0.39 USD** | **Margen de ganancia bruto > 90%** (PVP: $4 - $6) |
| **Acabado Superficial** | Líneas ásperas, sombras desiguales | **Porcelana Satinada** | Trazos negros nítidos, fondo liso para marcadores |

---

## 2. CONFIGURACIÓN EXHAUSTIVA PESTAÑA POR PESTAÑA

### A. PESTAÑA `FUERZA` (STRENGTH)

#### 1. Paredes (*Walls*)
* **Bucles de pared (*Wall loops*):** `2`
  * *Razón:* Con boquilla de $0.4\text{ mm}$, 2 bucles = $0.84 - 0.90\text{ mm}$. Dado que los trazos del Capibara fueron diseñados entre $0.85\text{ mm}$ y $1.00\text{ mm}$, las líneas negras se imprimen como un perímetro continuo 100% sólido. No genera vibraciones ni micropuntos de relleno.
* **Alternar pared extra:** `Desactivado` (Unchecked).
* **Incorporación de la pared en el relleno:** `Desactivado` (Unchecked).
* **Detectar la pared delgada:** `Desactivado` (Al usar el generador *Arachne*, Arachne lo calcula dinámicamente).

#### 2. Capas Superiores / Inferiores (*Top / Bottom Shells*)
* **Patrón de la superficie superior:** `Línea continua` o `Línea monótona global`.
  * *Razón:* Evita el efecto cebra. Todos los filamentos de la base blanca se depositan en el mismo ángulo angular de 45°, logrando reflexión uniforme de la luz.
* **Densidad de la superficie superior:** `100%`.
* **Capas superiores de la cubierta (*Top shell layers*):** `4` o `5` (Espesor: $0.80 - 1.00\text{ mm}$).
* **Capas inferiores de cubierta (*Bottom shell layers*):** `3` ($0.60\text{ mm}$).
  * *Razón:* La base blanca mide $1.40\text{ mm}$ en total ($7$ capas de $0.20\text{ mm}$). Con 3 capas inferiores y 4 superiores, la base blanca queda 100% sólida. Esto garantiza:
    1. **Opacidad absoluta:** El blanco queda blanco puro (leche/porcelana), impidiendo que se transparente la textura de la cama o la mesa.
    2. **Anti-Warping:** Cero curvaturas al enfriarse.
* **Patrón de la superficie inferior:** `Monotónico` o `Rectilíneo`.
* **Patrón interno de relleno sólido:** `Rectilíneo`.

#### 3. Relleno Poco Denso (*Sparse Infill*)
* **Densidad de relleno:** `10%` o `12%`.
* **Patrón de relleno disperso:** `Giroide` (*Gyroid*).
* *Razón:* Si en modelos más gruesos se requiere relleno, el Giroide resiste esfuerzos isotrópicos y no colisiona con la boquilla al imprimir.

#### 4. Avanzado de Fuerza / Paredes
* **Orden de las paredes:** `Exterior / Interior` (*Outer / Inner*).
  * *Razón:* Coloca primero la pared perimetral visible con precisión micrométrica antes de la pared interna de respaldo.
* **Sólo una pared en las superficies superiores:** **`No` / `Desactivado`** (*Crítico*).
  * *Razón:* Si está activado, en la cima de los bordes negros ($0.85\text{ mm}$) Bambu Studio intenta meter una sola pared y rellenar $0.1\text{ mm}$ con zigzag. Al desactivarlo, los 2 bucles de pared suben hasta la cima limpia y perfectamente redondeada.
* **Evite cruzar las paredes (*Avoid crossing walls / Combing*):** **`ACTIVAR (Checked)`** con Desvío máximo = `0` o `50 mm`.
  * *Razón SECRET PRO:* Obliga al extrusor a desplazarse por encima de las líneas existentes en vez de cruzar volando en línea recta por encima del lienzo blanco. Evita al 100% los hilos negros fantasmas (*stringing*) sobre el fondo blanco.

---

### B. PESTAÑA `VELOCIDAD` (SPEED)

Para vender un producto a clientes de decoración, **la nitidez visual manda sobre la velocidad extrema de la impresora**. En un lienzo plano de 2.6 mm, bajar las velocidades exteriores solo añade ~2 minutos al tiempo total, pero elimina el 100% del *ringing*, vibración y esquinas abultadas.

#### 1. Capa Inicial (Adhesión y Base)
* **Capa inicial:** Cambiar de 50 mm/s a **`30 mm/s`**.
* **Relleno de la capa inicial:** Cambiar de 105 mm/s a **`50 mm/s`**.
* *Razón:* Asegura que el PEI texturizado agarre la primera capa como soldadura, garantizando que el borde nunca se despegue ni curve.

#### 2. Otras Capas (Definición y Acabado)
* **Pared exterior:** Cambiar de 200 mm/s a **`80 mm/s`** *(Muy Importante)*.
  * *Razón:* A 200 mm/s la inercia del cabezal deforma los pequeños círculos de la fruta, ojos y mejillas. A 80 mm/s los círculos salen perfectamente redondos y nítidos.
* **Pared interior:** Cambiar de 300 mm/s a **`150 mm/s`**.
* **Superficie superior:** Cambiar de 100 mm/s a **`50 - 60 mm/s`** *(Muy Importante)*.
  * *Razón:* La boquilla caliente aplana el plástico a baja velocidad, fundiendo la superficie como plancha de calor.
* **Relleno de huecos (*Gap fill*):** Cambiar de 250 mm/s a **`100 mm/s`**.
  * *Razón:* Evita ruidos y microvibraciones en curvas estrechas.
* **Recorrido de desplazamiento (*Travel speed*):** Mantener en `700 mm/s`.

#### 3. Aceleraciones
* **Pared exterior:** Cambiar de 5000 mm/s² a **`2500 - 3000 mm/s²`**.
  * *Razón:* Suaviza los frenados bruscos en los detalles faciales del Capibara.
* **Superficie superior:** Mantener en `2000 mm/s²`.
* **Capa inicial:** Mantener en `500 mm/s²`.

---

### C. PESTAÑA `CALIDAD` (QUALITY)

* **Altura de capa:** `0.20 mm Standard`.
* **Altura de primera capa:** `0.20 mm`.
* **Generador de Paredes:** **`Arachne`** *(Indispensable)*.
  * *Razón:* Varía el ancho del flujo automáticamente para sellar esquinas convergentes sin dejar microporos.
* **Costura (*Seam Position*):** `Atrás` (*Rear*) o `Alineada` con **`Scarf Joint Seam`** (Costura en bufanda) activada si está disponible.
* **Alisado (*Ironing*):** `Opcional`. Con `Línea continua` a 50 mm/s ya queda espectacular; si se activa alisado, usar flujo `10% - 12%` a `30 mm/s`.

---

### D. PESTAÑA `OTROS` Y FILAMENTOS (PURGA Y AMS LITE)

#### 1. Volúmenes de Purga (*Flushing Volumes*)
* **Blanco (1) $\to$ Negro (2):** **`70 mm³`**.
* **Negro (2) $\to$ Blanco (1):** `80 mm³` (Inactivo en este trabajo).
* **Multiplicador:** `1.0`.

#### 2. Torre de Cebado (*Prime Tower*)
* **Habilitada:** `Sí`.
* **Ancho de la torre:** Reducir de 35 mm a **`20 mm`**.
* **Volumen de cebado:** **`15 mm³`**.

---

## 3. CHECKLIST PARA EXPORTACIÓN Y VENTA DIRECTA
1. [ ] Cargar `Capibara_Zen_MULTICOLOR_AMS.3mf`.
2. [ ] Verificar en la pestaña de objetos: Base en Filamento 1 (Blanco), Líneas en Filamento 2 (Negro).
3. [ ] Ajustar paredes a 80 mm/s y superficie superior a 50 mm/s.
4. [ ] Activar *Evite cruzar las paredes*.
5. [ ] Configurar volumen de purga a 70 mm³.
6. [ ] Laminar y verificar en la vista previa de capas:
   - Capas 1 a 7: 100% Blanco.
   - Capas 8 a 13: 100% Negro.
   - 1 solo cambio de filamento reportado en la barra vertical de colores.
   - Peso total: ~26 - 28 gramos.
