# 📐 BIBLIA MAESTRA DE CREACIÓN DE STL Y 3MF PARA IMPRESIÓN 3D MULTICOLOR
*Syntra Lab — Compendio de Ingeniería de Mallas, Topología Computacional y Arquitectura Bambu Studio*

---

## 1. TOPOLOGÍA DE MALLAS 2-MANIFOLD (LA LEY ABSOLUTA DE LA IMPRESIÓN 3D)

Para que cualquier software laminador (Bambu Studio, OrcaSlicer, PrusaSlicer) pueda cortar un modelo en capas (slicing), el archivo DEBE ser una **variedad bidimensional cerrada (2-Manifold Watertight Solid)**. Si una malla viola esta condición, el motor de corte no puede determinar qué es "adentro" y qué es "afuera" del sólido.

### Las 4 Condiciones Matemáticas Inviolables:
1. **La Regla del Borde Compartido (Edge Manifold):**
   * Cada arista de la malla debe pertenecer a **EXACTAMENTE DOS triángulos**.
   * Si una arista pertenece a 1 triángulo: hay un **agujero o fisura** (Hole/Open edge).
   * Si una arista pertenece a 3 o más triángulos: hay una **intersección interna o unión en T** (Non-manifold edge).
2. **Consistencia de Orientación y Regla de la Mano Derecha (Winding Order):**
   * Todos los triángulos deben tener sus vértices ordenados en sentido **anti-horario (CCW)** cuando se miran desde el exterior del objeto.
   * Si una arista $(V_A, V_B)$ es recorrida de $V_A \to V_B$ por el triángulo 1, el triángulo adyacente DEBE recorrerla en sentido opuesto: $V_B \to V_A$.
   * Violar esto genera **caras invertidas (inverted normals)** que el laminador interpreta como material negativo (huecos fantasmas).
3. **Cero Caras Interiores / Auto-Intersecciones:**
   * Nunca deben solaparse dos sólidos independientes sin haber calculado previamente su unión booleana. Si se colocan dos cajas o cilindros superpuestos, las caras interiores que quedan atrapadas rompen la topología y disparan el error de *Non-Manifold Edges*.
4. **Cero Singularidades de Vértice (Pinch Points):**
   * Dos partes sólidas no pueden tocarse únicamente en un solo vértice o arista compartida (como dos cubos que se tocan en diagonal). Esto crea una singularidad donde la superficie se cruza a sí misma.

---

## 2. POR QUÉ FALLAN LOS RELIEVES 2D EN MALLAS DISCRETAS (EL PROBLEMA DE LAS LÍNEAS DISCONTINUAS)

### El Fenómeno del "Dotted / Dashed Line" (Aliasing Espacial):
Cuando se genera una línea sobre una grilla espacial discreta (Heightmap o Vóxeles):
* Si el paso de la grilla ($RES$) es de $0.35\text{ mm}$ y el grosor de línea es de $0.90\text{ mm}$ (radio $hw = 0.45\text{ mm}$):
* La distancia diagonal entre nodos contiguos es $0.35 \times \sqrt{2} = 0.495\text{ mm}$.
* Como $0.495\text{ mm} > 0.45\text{ mm}$, **la línea cae en el espacio vacío entre dos nodos diagonales**, no activa ningún nodo de la grilla y **desaparece en ese punto**.
* Consecuencia: una curva continua se transforma en una serie de guiones o puntos punteados aislados.

### La Solución Matemática de Syntra Lab:
1. **Teorema de Muestreo de Nyquist:** El paso de la grilla debe ser como mínimo $3\times$ menor que el ancho del trazo ($RES \le W / 3$). Para una línea de $0.9\text{ mm}$, $RES$ debe ser $\le 0.25\text{ mm}$.
2. **Estampado Continuo con Paso Submétrico:** Al trazar líneas, arcos o curvas, el algoritmo no debe muestrear a saltos de 1 mm. Debe avanzar en pasos de **$0.05\text{ mm}$** estampando un pincel circular continuo. Esto garantiza que no exista ni una sola discontinuidad geométrica.
3. **Conectividad 4-Vecinos (Anti-Pinch):** Todo nodo diagonal activo debe estar conectado con al menos un vecino ortogonal para eliminar singularidades en damero (checkerboard).

---

## 3. ARQUITECTURA DE ARCHIVOS `.3MF` EN BAMBU STUDIO (MULTICOLOR REAL)

Bambu Studio **NO utiliza** la etiqueta genérica `<m:colorgroup>` de 3MF estándar para colorear modelos en su interfaz gráfica. Bambu Studio organiza los colores mediante **PARTES DE ENSAMBLAJE (Multipart Objects)**.

### Estructura Correcta del Archivo `.3MF` para AMS:
```
Capibara_Zen_MULTICOLOR_AMS.3mf (Archivo ZIP)
├── 3D/3dmodel.model            -> Definición de las geometrías (Object 1: Base, Object 2: Líneas)
├── Metadata/model_settings.config -> Mapeo exacto de qué objeto pertenece a qué extrusor
└── Metadata/slice_info.config     -> Definición de filamentos (Color 1 = Blanco, Color 2 = Negro)
```

### Reglas de Configuración:
1. **La Base Blanca (Part 1):** Un sólido 2-manifold independiente con espesor de $Z = 0.0$ a $Z = 1.40\text{ mm}$.
2. **Las Líneas Negras (Part 2):** Un sólido 2-manifold independiente con espesor de $Z = 1.40$ a $Z = 2.60\text{ mm}$.
3. **En `model_settings.config`:**
   ```xml
   <object id="3">
     <part id="1" subtype="normal_part">
       <metadata key="name" value="Base_Blanca"/>
       <metadata key="extruder" value="1"/>
     </part>
     <part id="2" subtype="normal_part">
       <metadata key="name" value="Lineas_Negras"/>
       <metadata key="extruder" value="2"/>
     </part>
   </object>
   ```
4. Al abrirlo, Bambu Studio asigna **automáticamente** el filamento blanco a la base y el negro a las líneas, mostrando la ilustración perfecta en pantalla y permitiendo laminar en 1 solo segundo.

---

## 4. PROTOCOLO AUTOMÁTICO DE VALIDACIÓN PRE-ENTREGA (THE FAILSAFE CHECKLIST)

Ningún modelo STL o 3MF se entrega al usuario sin haber ejecutado y superado esta prueba computacional:

```python
def auditar_malla_estricta(triangles):
  # 1. Mapa de aristas y orientación
  # 2. Verificar que cada arista tenga EXACTAMENTE 2 triángulos (0 no-manifold)
  # 3. Verificar que los vectores de arista sean opuestos (0 caras invertidas)
  # 4. Verificar que no haya triángulos de área cero o degenerados
  assert aristas_no_manifold == 0, "ERROR: Aristas no-manifold detectadas"
  assert caras_invertidas == 0, "ERROR: Caras invertidas detectadas"
```

---

## 5. GENERADOR DE PAREDES ARACHNE VS CLÁSICO EN BAMBU STUDIO

Para el laminado de líneas finas de dibujo ($0.85\text{ mm}$ a $1.00\text{ mm}$) con boquilla de $0.4\text{ mm}$:
* **El Motor Clásico:** Utiliza extrusión de ancho fijo ($0.42\text{ mm}$). Si una línea mide $0.85\text{ mm}$, intenta meter dos pasadas ($0.84\text{ mm}$) dejando un espacio central microscópico no extruido o descartando segmentos si caen por debajo del umbral de detección de paredes delgadas.
* **El Motor Arachne (Recomendado):** Varía dinámicamente el ancho de la línea de extrusión en tiempo real. Puede ensanchar la pasada a $0.50\text{ mm}$ o reducirla a $0.35\text{ mm}$, asegurando que cualquier trazo curvado o convergente se imprima 100% sólido y sin huecos internos.
* **Configuración obligatoria en Bambu Studio:** `Quality -> Wall Generator -> Arachne`.

---

## 6. ACABADO SUPERFICIAL PREMIUM: ALISADO TÉRMICO (IRONING)

Para que el piso del lienzo se sienta como una tarjeta plástica satinada o papel de acuarela liso (sin estrías de extrusión):
* **Ironing Pattern:** `Rectilinear` o `Monotonic Line`.
* **Ironing Flow:** `12% - 15%`.
* **Ironing Speed:** `25 mm/s`.
* **Target:** `Top surface only` (Aplica únicamente a la capa $Z = 1.40\text{ mm}$ de la base blanca antes de que el AMS comience a depositar los bordes negros). El resultado es un piso 100% liso donde los marcadores acrílicos corren con fluidez sin trabarse en líneas de capa.

---

## 7. GESTIÓN DE PURGA Y TRANSICIÓN MULTICOLOR EN AMS LITE

Dado que el modelo solo realiza **1 cambio de material en toda la impresión** (Capa 7: termina el blanco en $Z = 1.40\text{ mm}$ y cambia a negro para las capas 8 a 13):
* **Purge Volume (Flushing volumes):** Reducir de 250 mm³ a **80 mm³**.
  * Al pasar de Blanco a Negro, no existe riesgo de contaminación visible porque el pigmento negro domina completamente al blanco.
  * Ahorro de tiempo: 3 minutos.
  * Ahorro de filamento de purga: 80% menos desperdicio de torre de purga.
* **Tiempo total de impresión:** ~38 minutos por lienzo en la Bambu Lab A1 Mini.
