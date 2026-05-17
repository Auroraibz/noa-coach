# RECICLAJE DE CONTENIDO — NOA CONTENT SYSTEM
# Sistema x8: un vídeo publicado → 8 piezas nuevas
# Versión 2.0

---

## FILOSOFÍA DEL RECICLAJE

No estás reutilizando contenido. Estás amplificando lo que ya demostró que funciona.

Un vídeo con >5.000 reproducciones o >3% de guardados es una señal clara: ese dolor, ese ángulo, ese hook, resonó. El reciclaje no repite el contenido. Cambia el formato para llegar a diferentes momentos, plataformas y tipos de consumidor.

**Criterio de entrada al pipeline de reciclaje:**
- >5.000 reproducciones en 48h, O
- >3% tasa de guardados, O
- >20 comentarios orgánicos, O
- >50 compartidos

---

## SYSTEM PROMPT (listo para Claude API)

```
Eres el estratega de reciclaje de contenido de NOA. Tu función es tomar un vídeo ya publicado que funcionó y transformarlo en 8 formatos nuevos sin repetir el mismo contenido.

REGLAS:
1. No copies el guion original. Usa el mismo NÚCLEO (el dolor, el insight, el micro-giro) pero en formato diferente.
2. Cada formato tiene una audiencia diferente en un momento diferente. Escríbelo pensando en ese contexto.
3. Mantén el tono NOA: directo, emocional, adulto, sin motivación vacía.
4. El CTA a NOA debe estar presente en todos los formatos, integrado de forma natural.
5. Los hooks de los 3 nuevos vídeos deben ser completamente diferentes al hook original.

INPUT QUE RECIBIRÁS:
{
  "titulo_original": "",
  "hook_original": "",
  "guion_completo": "",
  "metricas": {
    "reproducciones": 0,
    "guardados_pct": 0,
    "comentarios": 0,
    "shares": 0
  },
  "angulo_emocional": "",
  "etapa_funnel_original": "TOFU|MOFU|BOFU"
}

OUTPUT QUE DEBES GENERAR:
JSON con los 8 formatos definidos abajo.
```

---

## LOS 8 FORMATOS DE RECICLAJE

### FORMATO 1 — 3 Hooks nuevos para variaciones de Reel

Misma idea, ángulo completamente diferente. Cubrir los 3 mecanismos de stop: reconocimiento, contradicción, promesa específica.

**Ejemplo — vídeo original sobre argumentar con hijo AACC:**
```json
{
  "hooks_nuevos": [
    {
      "texto": "Le das la razón para que pare la discusión. Y empeoráis la relación sin darte cuenta.",
      "mecanismo": "contradiccion",
      "angulo": "consecuencia_a_largo_plazo"
    },
    {
      "texto": "Lleva 45 minutos discutiendo por qué tiene que ducharse. Y nadie ha ganado nada.",
      "mecanismo": "reconocimiento",
      "angulo": "situacion_cotidiana_especifica"
    },
    {
      "texto": "La respuesta exacta que desactiva una discusión AACC en menos de 30 segundos.",
      "mecanismo": "promesa_especifica",
      "angulo": "herramienta_concreta"
    }
  ]
}
```

---

### FORMATO 2 — 3 Variaciones de guion (formatos diferentes)

Cada variación usa un formato distinto de los 7 disponibles en `generador-guiones.md`:
- Variación A: diferente formato del vídeo original
- Variación B: diferente ángulo emocional (del problema al error, o del error a la solución)
- Variación C: diferente etapa de funnel (si el original era TOFU, una variación va a MOFU)

---

### FORMATO 3 — 1 Carrusel (5-7 diapositivas)

Para Instagram Feed. El carrusel tiene mejor retención en feed que en Reels. Audiencia diferente: la que para en el feed, no la que consume stories/reels.

**Estructura:**
```
Diapositiva 1: Hook visual — la frase más poderosa del vídeo original, en grande
Diapositiva 2: El problema — la situación cotidiana descrita
Diapositiva 3: Por qué pasa — la explicación AACC en una frase
Diapositiva 4: El error típico — lo que los padres hacen y no funciona
Diapositiva 5: Lo que sí funciona — la herramienta/micro-giro del vídeo
Diapositiva 6: (opcional) Ejemplo real — la frase exacta que puedes decir
Diapositiva 7: CTA — descarga NOA, con visual de la app
```

**Especificaciones técnicas:**
- Formato: 1080×1080 (cuadrado) o 1080×1350 (vertical 4:5)
- Fondo: #1A1A2E o blanco cálido #F8F8F8
- Tipografía: Montserrat Bold para títulos, Regular para cuerpo
- Color acento: #E94560 para palabras clave
- Máximo 50 palabras por diapositiva

---

### FORMATO 4 — 1 Email

Para la lista de email de NOA (usuarios registrados o lista de espera).

**Estructura:**
```
Asunto: [Hook del vídeo adaptado como asunto de email]
Pre-encabezado: [Segunda frase de impacto]

Cuerpo:
- Saludo sin nombre (sin personalización forzada)
- El conflicto del vídeo reescrito para email (más íntimo, más largo)
- La explicación completa (en email tienes más espacio que en Reel)
- La herramienta con más detalle
- CTA: botón de descarga de NOA
- P.D.: una frase adicional que amplía
```

**Longitud objetivo:** 250-350 palabras. Ni demasiado corto (parece spam) ni demasiado largo (nadie lo lee).

**Ejemplo asunto:** "Le di todos mis argumentos. Y empeoré la situación."
**Pre-encabezado:** "Lo que funciona no es razonar mejor."

---

### FORMATO 5 — 1 Secuencia de Stories (3-5 frames)

Stories de Instagram. Audiencia de alta confianza (ya te siguen). Formato más íntimo, más directo, más conversacional.

**Estructura:**
```
Story 1: Pregunta directa — "¿Os ha pasado esto esta semana?" + encuesta Sí/No
Story 2: El conflicto — 1 frase del vídeo + imagen/video de fondo cálido
Story 3: El micro-giro — la revelación principal en texto grande sobre fondo oscuro
Story 4: La herramienta — qué hacer exactamente, en 1-2 frases
Story 5: CTA — "NOA tiene 40 situaciones más. Link en bio." + sticker de link
```

**Especificaciones:**
- Formato 9:16 (1080×1920)
- Texto máximo por story: 2-3 líneas
- Fondo: gradiente #1A1A2E → #2A2A4E o imagen B-roll con overlay oscuro
- Duración: configurar en 7 segundos (el máximo que la gente lee)

---

### FORMATO 6 — 1 Post de texto

Para Instagram (solo texto) o LinkedIn (si el contenido tiene ángulo profesional).

**Estructura para Instagram texto:**
```
Primera línea: HOOK que para el scroll en feed
[línea en blanco]
Párrafo 1: El conflicto desarrollado (3-4 frases)
[línea en blanco]
Párrafo 2: Por qué pasa (1-2 frases, explicación AACC)
[línea en blanco]
Párrafo 3: Lo que funciona (la herramienta)
[línea en blanco]
Pregunta de cierre
[línea en blanco]
CTA a NOA
```

**Longitud:** 150-200 palabras. Los posts de texto en Instagram funcionan mejor cuando son visualmente aireados (muchos saltos de línea).

---

### FORMATO 7 — 1 Script de anuncio Meta Ads (15 segundos)

Para campañas de pago. Estructura completamente diferente al Reel orgánico.

**Estructura:**
```
0-3s: HOOK de dolor ultra específico (igual que en Reel orgánico, puede ser el mismo)
3-8s: AGITACIÓN — empeora brevemente el problema antes de resolverlo
8-12s: SOLUCIÓN — NOA como herramienta concreta
12-15s: CTA — "Descarga gratis" + nombre de la app visible
```

**Diferencias vs. Reel orgánico:**
- El micro-giro puede ser más corto
- NOA se menciona antes (segundo 8, no el 28)
- El CTA incluye nombre de la app y "gratis" explícitamente
- El tono puede ser ligeramente más directo hacia la conversión

**Ejemplo:**
```
0-3s: "Lleváis 30 minutos discutiendo por algo que empezó con 'recoge la ropa'."
3-8s: "Y cuanto más razonáis, más argumentos os devuelve. Esa dinámica no tiene solución lógica."
8-12s: "NOA te dice exactamente qué responder para salir de esa espiral. En segundos."
12-15s: "Descarga NOA gratis." [visual de pantalla de la app]
```

---

### FORMATO 8 — 1 FAQ (para destacados de Instagram o bio de TikTok)

Un Q&A basado en el tema del vídeo, optimizado para aparecer en búsquedas y en destacados.

**Estructura:**
```
PREGUNTA: [La pregunta que haría una madre AACC buscando este tema]
RESPUESTA: [Respuesta de 100-150 palabras que responde completamente]
REFERENCIA A NOA: [Una frase natural al final conectando con la app]
```

**Ejemplo:**
```
PREGUNTA: ¿Por qué mi hijo AACC tiene siempre un contraargumento para todo?

RESPUESTA:
Los adolescentes con altas capacidades tienen una forma de procesar la información que les hace identificar patrones, incoherencias y excepciones de forma automática. Cuando alguien les da un argumento, su cerebro busca instintivamente si ese argumento es sólido o tiene fisuras. No lo hacen para fastidiarte. Lo hacen porque no pueden no hacerlo.

Cuando estás en una discusión con él y presentas tus razones, no lo está evaluando como "mamá tiene razón o no tiene razón". Lo está procesando como un problema lógico. Y su cerebro es muy bueno resolviendo problemas lógicos.

Lo que cambia la dinámica no es tener un argumento mejor. Es salir completamente del modo argumentativo y entrar en otro tipo de conversación. NOA te ayuda a saber exactamente cómo hacer ese cambio en el momento.
```

---

## PIPELINE DE RECICLAJE EN N8N

El workflow `reciclaje-contenido.json` maneja esto automáticamente cuando:
1. El campo `recycle_flag = TRUE` en Airtable (se activa manualmente o por métricas)
2. El workflow llama a Claude con el guion + métricas del vídeo original
3. Claude genera los 8 formatos en JSON
4. n8n crea registros nuevos en Airtable para cada formato
5. Notificación al owner con resumen de lo generado

**Estados generados automáticamente:**
- Los 3 hooks nuevos → estado IDEA en tabla Ideas
- Las 3 variaciones de guion → estado SCRIPT en tabla Guiones
- Carrusel, email, stories, post, ad, FAQ → estado DRAFT en tabla Reciclados

**Todos requieren aprobación antes de publicar.**

---

## TRACKING DEL RECICLAJE

En Airtable, el campo `veces_reciclado` del vídeo original se incrementa con cada ciclo.

Regla de calidad: **máximo 3 ciclos de reciclaje** por pieza original. Después del tercer ciclo, el contenido ya ha agotado sus variaciones útiles y empieza a parecer repetitivo.

```
Ciclo 1: Mismo canal, formatos diferentes
Ciclo 2: Mismo canal, ángulo completamente diferente
Ciclo 3: Cross-platform (ej: lo que fue un Reel se convierte en newsletter y carrusel)
Ciclo 4+: Archivo. No reciclar más.
```
