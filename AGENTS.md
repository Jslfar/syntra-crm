# AGENTS.md — MEMORIA PERMANENTE Y REGLAS OPERATIVAS DE SYNTRA GROUP

Este archivo contiene la memoria central, reglas de negocio y restricciones contextuales para cualquier agente que opere en este repositorio.

---

## 🇻🇪 1. REALIDAD CAMBIARIA Y REGLA DE PRECIOS EN VENEZUELA (CRÍTICO)

### A. El Desfase Cambiario (Brecha BCV vs. USDT / Binance P2P)
En Venezuela coexisten dos realidades monetarias obligatorias:
1. **Tasa Oficial BCV (Banco Central de Venezuela):** Obligatoria legalmente para precios de lista, facturación en Bolívares (VES), puntos de venta y Pago Móvil.
2. **Tasa de Mercado Real (Binance P2P / USDT / Paralelo):** Determina el costo real de reposición internacional de mercancía (China / FOB). Es volátil y superior a la tasa BCV (ejemplo actual: BCV a ~896,12 Bs. vs. Binance P2P a ~1.025,00 Bs., con brecha de 12% a 15%+).

### B. La Trampa del Arbitraje Cambiario del Consumidor
- Si el comercio vende a **$20 BCV**, el cliente que posee USDT vende en Binance P2P a tasa alta y obtiene los bolívares necesarios pagando el equivalente a solo **~$17,48 USD reales**.
- Si el comercio ofrece "$19 en divisa", el cliente seguirá pagando en bolívares porque $17,48 < $19,00.
- Si el comercio recibe bolívares por Pago Móvil, sufre:
  - Fricción bancaria y límites de transferencia.
  - Riesgo de devaluación mientras convierte de vuelta a divisa.
  - Exposición tributaria (SENIAT, IGTF, Alcaldía de Lechería).

### C. Estrategia Obligatoria de Precios Duales (Defensa y Captación Rápida de Divisas)
Syntra Group opera bajo un **Modelo de Precios Duales**:
1. **Precio de Lista Oficial (PVP Lista BCV):** Precio público formal y legal (ej: PLA Basic a $20,00 = 17.922,40 Bs.). Quien pague en Bolívares paga a este precio exacto a tasa BCV. Al convertir esos bolívares en Binance P2P, Syntra recupera el valor de reposición sin pérdida.
2. **Precio Contado en Divisa Limpia (USDT Binance Pay / Efectivo $ en Lechería / Zelle):** Precio especial con descuento real y directo (ej: PLA Basic a $18,00 USDT, PETG Basic a $17,50 USDT).
   - Destruye el incentivo de arbitraje del cliente: pagar directo en USDT o Cash es más barato y rápido que vender en P2P.
   - **Interés Primario:** Captar divisa líquida dura que **no pasa por bancos locales, no tributa y permite reponer inventario en China inmediatamente a tasa 1:1**.

---

## 🏢 2. IDENTIDAD Y VENTAJA COMPETITIVA DE SYNTRA GROUP
- **Ubicación:** Lechería, Estado Anzoátegui, Venezuela (cobertura prioritaria Lechería, Puerto La Cruz, Barcelona y envíos nacionales vía MRW, Tealca y Zoom).
- **Contacto Oficial WhatsApp Syntra:** `+58 422-3446675` (enlace directo: `https://wa.me/584223446675`). Todo mensaje emitido por el panel, nota de entrega, comprobante o material para afiliados debe llevar obligatoriamente esta línea oficial.
- **Competencia Local:** Sin competidores directos en la zona norte de Anzoátegui con el volumen y stock físico de Syntra. Los competidores nacionales de referencia (Filaven, MercadoLibre Caracas) venden a $20-$22 BCV con envío gratis.
- **Ventaja Syntra:** Disponibilidad física inmediata en Lechería (retiro en el acto sin esperar 3-5 días de flete), asesoría técnica especializada y precios imbatibles de contado en Binance Pay / Efectivo ($17,50 - $18,00).

---

## 📦 3. PARÁMETROS DEL INVENTARIO ACTIVO
- **Total de Unidades:** 1.750 unidades físicas (FOB Kingroon: $7.972,00 | Costo Landed Almacén Lechería: $11.386,20).
- **Desglose de SKUs:** 117 ítems individuales itemizados por tipo de material y color exacto en `crm/syntra_crm.db`.
- **Precios Clave Contado Divisas:**
  - PETG Basic: $17,50 Cash / $19,50 BCV
  - PLA Basic: $18,00 Cash / $20,00 BCV
  - PLA+: $19,00 Cash / $21,50 BCV
  - PLA Silk Oro Imperial: $21,00 Cash / $24,00 BCV
  - PLA Silk Dual/Tri/Rainbow: $23,50 Cash / $27,00 BCV
  - TPU 95A / ASA: $25,00 Cash / $28,50 BCV
  - Fibra de Carbono (PETG-CF / PLA-CF): $36,00 Cash / $42,00 BCV

---

## 🛠️ 4. REGLAS PARA DESARROLLO Y CAMBIOS FUTUROS
- **Siempre preservar el modelo de Precios Duales** en cotizadores, APIs, base de datos y vistas (`pvp_usd` para Lista Oficial BCV y `pvp_cash_usd` para Contado Divisas).
- **Tasa BCV y P2P Dinámicas:** La tasa BCV y la tasa Binance P2P deben ser configurables desde el cotizador/calculadora (`#calc-bcv` y `#calc-p2p`) para reflejar los movimientos continuos del mercado venezolano.
- **Priorizar flujos en Divisas:** Todo mensaje o cotización generado para WhatsApp debe destacar en primer lugar y con mayor beneficio la opción de pago en **Binance Pay (USDT)** y **Efectivo en mano**, presentando el pago en Bolívares como alternativa secundaria al precio de lista oficial.
- **Comisiones Diferenciadas para Afiliados (Incentivo Pro-Divisa):**
  - **$1.50 USD por bobina (o 8.0%)** si el cliente paga en **Divisa Limpia** (Binance USDT, Efectivo $ en Lechería, Zelle).
  - **$1.25 USD por bobina (o 6.5%)** si el cliente paga en **Bolívares** (Pago Móvil / Transferencia VES a tasa BCV).
  - El cotizador y el modal de venta deben recalcular automáticamente la comisión del promotor al conmutar el método de pago del cliente.
