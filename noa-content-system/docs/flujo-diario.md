# Flujo Diario del Sistema NOA

> Tiempo del owner: máximo 30 minutos por día.
> El resto corre solo.
> Output diario: 1 video publicado + pipeline avanzado para el siguiente.

---

## Resumen Ejecutivo del Día Tipo

```
06:00 - 08:59  → El sistema duerme. No hay triggers.
09:00          → TRIGGER AUTOMÁTICO: n8n se despierta y arranca el pipeline.
09:00 - 09:05  → Automático: Claude genera el guión del día.
09:05          → Automático: Notificación push al owner con el guión.
09:05 - 09:20  → MANUAL (owner): Lee y aprueba el guión. 15 min máximo.
09:20          → Aprobación recibida → pipeline retoma solo.
09:20 - 09:35  → Automático: ElevenLabs genera voz + Freepik genera imágenes (paralelo).
09:35 - 09:45  → Automático: Creatomate ensambla el video.
09:45 - 09:50  → MANUAL (owner): Revisa preview del video. 5 min máximo.
09:50          → Aprobación de video → Metricool programa publicación.
18:00 - 20:00  → Automático: Video se publica en Instagram + YouTube Shorts.
20:00 - 20:05  → MANUAL (owner, opcional): Responde 2-3 comentarios importantes.
24 horas después → Automático: Métricas recogidas + análisis de rendimiento.
```

**Total tiempo del owner: 20-25 minutos activos.**

---

## Hora por Hora — Flujo Detallado

### 09:00 — TRIGGER AUTOMÁTICO (n8n Cron)

**Responsable**: Sistema automático (n8n)
**Duración**: 30 segundos

n8n ejecuta el workflow principal:
1. Consulta Airtable [Ideas_Queue] filtrando `status = "ready_to_produce"` y `priority_score >= 7`
2. Selecciona la idea con mayor puntuación
3. Verifica que no existe ya un video publicado sobre ese tema en los últimos 45 días (anti-repetición)
4. Si la cola está vacía: envía alerta crítica al owner y detiene el pipeline. Esto no debería pasar si el flujo semanal se sigue correctamente.

**Lo que necesita estar listo antes de las 09:00**:
- Mínimo 3 ideas con `status = "ready_to_produce"` en Airtable
- El VPS de n8n online (verificar con UptimeRobot)
- Token de ElevenLabs vigente
- Token de Instagram vigente (no haber expirado)

---

### 09:00 - 09:05 — GENERACIÓN DE GUIÓN (Claude API)

**Responsable**: Sistema automático (n8n → Claude API)
**Duración**: 60-90 segundos

n8n envía el prompt a Claude con:
- System prompt de NOA (voz de marca, restricciones, ejemplos de guiones exitosos)
- Tema de la idea seleccionada
- Formato: Reel 60s o Short 45s según el slot del día
- Pain point asociado a la idea
- Nivel del funnel: TOFU / MOFU / BOFU

Claude devuelve JSON estructurado:
```json
{
  "hook": "¿Tu hijo lleva 3 años sin encontrar amigos que lo entiendan?",
  "body_segments": [
    { "text": "Los adolescentes con AC procesan el mundo diferente.", "timing_s": 8 },
    { "text": "No es que sean raros. Es que van 3 pasos por delante.", "timing_s": 6 },
    { "text": "El problema no es tu hijo. Es el entorno que no está diseñado para él.", "timing_s": 10 }
  ],
  "cta": "Guarda este video si esto le está pasando a tu familia",
  "caption_ig": "El mayor error que cometen los padres de niños con AC es...",
  "hashtags": ["#altascapacidades", "#aacc", "#padreshijos", "#adolescentes", "#superdotados"],
  "title_a": "Por qué tu hijo con AC no encaja — y no es su culpa",
  "title_b": "3 señales de que tu adolescente tiene altas capacidades"
}
```

El guión pasa por un segundo call de Claude que lo puntúa en 5 criterios:
- Fuerza del hook (1-10): ¿genera pregunta o urgencia en < 3 segundos?
- Resonancia emocional (1-10): ¿toca un dolor real del padre?
- Especificidad AACC (1-10): ¿podría aplicar a cualquier niño o es específico del nicho?
- Claridad del CTA (1-10): ¿queda claro qué quiero que haga el espectador?
- Longitud correcta (1-10): ¿encaja en el tiempo del formato elegido?

Si la puntuación media < 7: Claude regenera el guión una vez más con instrucciones específicas sobre qué mejorar. Si sigue < 7: el sistema marca la idea como "needs_human_rewrite" y pasa a la siguiente idea de la cola.

---

### 09:05 — NOTIFICACIÓN AL OWNER

**Responsable**: Sistema automático (n8n → Telegram o Email)
**Duración**: Instantáneo

El owner recibe:
- El guión completo formateado en Telegram o email
- La puntuación de calidad (5 criterios)
- El link directo a la fila en Airtable para aprobar/rechazar con un clic
- Tiempo estimado del video (basado en el conteo de palabras)

Mensaje ejemplo en Telegram:
```
🟡 NOA — Guión listo para revisión

Tema: "Por qué tu hijo con AC no encaja"
Formato: Reel 60s | TOFU | Puntuación: 8.2/10

HOOK: ¿Tu hijo lleva 3 años sin encontrar amigos que lo entiendan?

[ver guión completo en Airtable →]

✅ Aprobar  ❌ Rechazar  ✏️ Editar
```

---

### 09:05 - 09:20 — REVISIÓN DEL OWNER (MANUAL)

**Responsable**: Owner
**Duración real objetivo**: 10-15 minutos
**Duración máxima tolerable**: 20 minutos

**Qué hace el owner**:
1. Lee el guión de principio a fin (2-3 min)
2. Verifica que el hook es poderoso y específico para el nicho AACC
3. Comprueba que el tono es empático, no condescendiente con los padres
4. Revisa que el CTA tiene sentido para el nivel del funnel (TOFU no pide comprar nada)
5. Decide: aprobar / rechazar / editar

**Criterios de aprobación rápida** (si se cumplen estos 3, aprueba directamente):
- El hook te genera una emoción real al leerlo
- El contenido es específico de AACC, no aplica a "cualquier niño"
- El CTA es suave y natural (guardar, comentar, reflexionar) — no agresivo

**Criterios de rechazo directo**:
- El guión parece sacado de un blog genérico de crianza
- Usa frases como "es importante que", "debes saber que", "como padre"
- El hook es una pregunta retórica vacía ("¿Sabes qué es la inteligencia emocional?")
- El contenido podría ofender a padres que todavía no han aceptado el diagnóstico de su hijo

**Si necesita edición**:
- El owner edita directamente en Airtable (el campo "script_text" es editable)
- Cambia el status a "approved" cuando termina
- NO reescribe el guión desde cero; eso es trabajo de Claude. Solo corrige 1-2 frases problemáticas.

**El owner NO hace en este momento**:
- Generar ideas nuevas
- Buscar imágenes
- Pensar en hashtags
- Revisar métricas de días anteriores

---

### 09:20 — APROBACIÓN DETECTADA → PRODUCCIÓN AUTOMÁTICA

**Responsable**: Sistema automático (n8n detecta cambio en Airtable vía webhook)
**Duración**: 3-5 segundos de latencia

n8n detecta el cambio de status a "approved" y dispara inmediatamente 3 ramas en paralelo.

---

### 09:20 - 09:35 — PRODUCCIÓN DE ASSETS (Paralelo)

**Responsable**: Sistema automático (ElevenLabs + Freepik/DALL-E + stock checker)
**Duración total**: 10-15 minutos

**Rama A — Voz (ElevenLabs)**:
- n8n extrae el texto completo del guión de Airtable
- Llama a ElevenLabs API con el voice_id de la voz NOA
- Parámetros: modelo eleven_multilingual_v2, stability 0.62, similarity_boost 0.78, style 0.15
- El audio incluye pausas naturales basadas en los puntos del guión
- Output: audio_raw.mp3 (sin música de fondo aún)
- Tiempo: 30-60 segundos

**Rama B — Imágenes de fondo (Freepik AI / DALL-E)**:
- Claude previamente generó "visual_prompts" para cada segmento del guión
- n8n envía cada prompt a Freepik AI o DALL-E
- Reglas de generación: sin caras reconocibles, sin texto en la imagen, colores cálidos/neutros, estilo foto-realista suave
- Output: 4-6 imágenes PNG de 1080×1920 (formato vertical)
- Tiempo: 60-120 segundos (paralelo para todas las imágenes)

**Rama C — Stock footage check**:
- n8n busca en la librería local de clips pre-descargados de Pexels
- Criterios de búsqueda: tags de la idea (ej: "adolescente", "estudio", "familia", "libro")
- Verifica cooldown: clip no usado en últimos 30 días
- Si no hay match local: consulta Pexels API y descarga el clip
- Output: 1-3 clips .mp4 de 5-10 segundos

---

### 09:35 - 09:45 — ENSAMBLADO DE VIDEO (Creatomate)

**Responsable**: Sistema automático (n8n → Creatomate API)
**Duración**: 3-6 minutos (render + descarga)

n8n construye el payload para Creatomate:
```json
{
  "template_id": "noa-reel-v3",
  "output_format": "mp4",
  "modifications": {
    "audio_layer": "URL_del_audio_mp3",
    "bg_images": ["URL_img1", "URL_img2", "URL_img3"],
    "subtitle_text": "texto_del_guión_completo",
    "subtitle_style": "noa-default",
    "logo_overlay": "URL_logo_noa",
    "background_music": "noa-ambient-calm-02.mp3",
    "music_volume": 0.08,
    "color_accent": "#E8845A",
    "cta_text": "Guarda este video ↓"
  }
}
```

Creatomate renderiza. n8n espera el webhook de finalización (no polling activo).
Cuando llega el webhook con `status: "succeeded"`:
- n8n descarga el MP4 final desde la URL de Creatomate
- Guarda en /outputs/{video_id}/video_final.mp4
- Actualiza Airtable: status = "video_ready", añade preview_url

---

### 09:45 - 09:50 — REVISIÓN DEL VIDEO (MANUAL OPCIONAL)

**Responsable**: Owner (opcional pero recomendado)
**Duración**: 3-5 minutos

El owner recibe notificación con link de preview del video final.

**Qué verifica en 5 minutos**:
- Los primeros 3 segundos enganchan (hook visual + audio inmediato)
- Los subtítulos están correctamente sincronizados
- La voz suena natural, sin cortes o respiraciones raras
- El CTA final es visible y claro
- El video NO parece AI-generated de forma obvia

**Opciones**:
- **Todo bien**: Aprueba en Airtable → pipeline continúa
- **Problema menor** (subtítulo desajustado, música muy alta): Anota en Airtable para mejorar el template. Aprueba el video igualmente si el problema no es grave.
- **Problema mayor** (voz cortada, video negro, error visible): Rechaza → n8n registra el error → reintenta el render con ajustes

**La revisión del video puede saltarse** después de 4-6 semanas si la calidad es consistentemente buena. En ese punto, el sistema puede publicar automáticamente sin revisión de video.

---

### 09:50 — PROGRAMACIÓN DE PUBLICACIÓN (Metricool)

**Responsable**: Sistema automático (n8n → Metricool API)
**Duración**: 30 segundos

n8n envía a Metricool:
- El archivo MP4
- El caption en español (generado por Claude en el Paso 1)
- Los hashtags del guión
- El slot de publicación del día (consultado de una tabla de horarios en Airtable)

Horarios óptimos por día de la semana (basados en datos de audiencia AACC en España):
- Lunes: 19:30
- Martes: 20:00 (mejor slot de la semana)
- Miércoles: 18:45
- Jueves: 20:15
- Viernes: 18:00 (audiencia sale antes)
- Sábado: 11:00 (padres activos por la mañana)
- Domingo: 20:30

YouTube Shorts: mismo video, mismo día, 45 minutos después del horario de Instagram.

---

### 18:00 - 20:30 — PUBLICACIÓN AUTOMÁTICA

**Responsable**: Metricool → Instagram Graph API → YouTube Data API
**Intervención del owner**: Ninguna

El video se publica automáticamente en el slot programado.
Instagram devuelve el post_id y la URL del Reel.
n8n recoge la confirmación y actualiza Airtable: status = "published".

---

### 20:00 - 20:05 — GESTIÓN DE COMUNIDAD (MANUAL, OPCIONAL pero importante)

**Responsable**: Owner
**Duración**: 5 minutos
**Frecuencia**: Solo días donde el video ya lleva 30-60 min publicado

**Qué hace el owner**:
- Responde los 2-3 primeros comentarios significativos
- Un comentario de respuesta en los primeros 60 minutos multiplica el alcance orgánico en Instagram
- No necesita responder a todos; solo los que hacen preguntas reales o comparten experiencias

**Lo que NO hace en este momento**:
- Revisar métricas (es demasiado pronto)
- Buscar ideas nuevas
- Programar más contenido

---

### 24-48 horas después — FEEDBACK LOOP AUTOMÁTICO

**Responsable**: Sistema automático (Metricool webhook → n8n → Airtable)
**Intervención del owner**: Solo si hay una alerta

n8n recoge las métricas de 24h y 48h:
- Views totales
- Reach (cuentas alcanzadas)
- Saves (el KPI más importante para AACC)
- Shares
- Comments
- Play time promedio (% del video visto)

**Lógica de decisión automática**:

```
IF views_48h > 15.000:
  → Claude genera 3 variaciones del mismo tema
  → Las añade al backlog con priority = "urgente"
  → Notifica al owner: "Video viral — variaciones generadas"

IF saves_rate > 5% (saves/views):
  → Video marcado como "evergreen"
  → Programado para reciclar en 60 días con nuevo visual
  → Tema añadido a "temas calientes" del canal

IF views_48h < 800 AND publish_time > 24h:
  → Video flagged como "underperformer"
  → Notificación al owner con análisis automático de Claude:
    ¿El hook era débil? ¿El formato era incorrecto? ¿El horario era el peor?
  → Se añade a la cola de análisis del viernes

IF play_time_avg < 30%:
  → El guión era demasiado largo o el hook no retuvo
  → Claude recibe feedback para los próximos guiones del mismo formato
```

---

## Lo que el Owner NUNCA hace en el flujo diario

Estas cosas están automatizadas. Si el owner las hace manualmente, está rompiendo el sistema:

- Buscar imágenes de fondo manualmente
- Editar el video en ninguna aplicación
- Subir el video manualmente a Instagram
- Copiar y pegar hashtags
- Programar publicaciones una a una en Metricool
- Generar ideas desde cero sin el sistema de scoring
- Buscar trending audios (el sistema NOA es faceless + voz propia; no usa audios de tendencia)

---

## Protocolos de Error

### Error: La cola de ideas está vacía en el trigger de las 09:00
1. n8n detiene el pipeline
2. Envía alerta crítica al owner: "No hay ideas en la cola. Añadir al menos 3 ideas antes de las 10:00 para no perder el slot de hoy"
3. Owner añade ideas manualmente en 10 min o activa el "generador de emergencia" (n8n workflow que le pide a Claude 10 ideas nuevas basadas en los posts más guardados de la semana anterior)

### Error: ElevenLabs devuelve 429 (rate limit)
1. n8n espera 90 segundos y reintenta
2. Máximo 3 reintentos
3. Si falla en los 3: el audio se marca como "failed", el video no se produce ese día
4. n8n reprograma el intento para las 14:00 con la misma idea
5. Notificación al owner

### Error: Creatomate render falla
1. n8n espera 5 minutos y reintenta con los mismos assets
2. Si falla 2 veces: notificación al owner con el error específico
3. Owner revisa el template (puede haber una URL de asset rota) y reintenta manualmente desde n8n UI

### Error: Publicación en Instagram falla (token expirado)
1. n8n detecta el error 401 de la Graph API
2. Intenta renovar el token automáticamente
3. Si la renovación falla: alerta urgente al owner
4. El video queda en status "ready_to_publish" y no se pierde
5. Owner renueva el token manualmente (proceso de 5 minutos en Meta Developer portal) y lo actualiza en n8n credentials

### Error: Airtable no responde (rate limit o downtime)
1. n8n reintenta en 60 segundos
2. Máximo 5 reintentos con backoff exponencial
3. Si sigue fallando: el pipeline se detiene y almacena el estado en la memoria de n8n para retomar cuando Airtable vuelva

---

## Output Diario Objetivo

| Elemento | Cantidad | Quién lo hace |
|---|---|---|
| Video publicado en IG Reels | 1 | Automático |
| Video publicado en YT Shorts | 1 | Automático |
| Guión aprobado para el siguiente día | 1 | Owner (10 min) |
| Ideas procesadas en backlog | 2-3 | Automático (feedback loop) |
| Métricas recogidas y analizadas | 1 video anterior | Automático |

**Si un día el owner no puede revisar el guión**, el pipeline simplemente no produce ese día. No es un desastre. El buffer de guiones pre-aprobados del lunes cubre estos días. La meta es 5-7 videos por semana, no 7 exactos cada semana.
