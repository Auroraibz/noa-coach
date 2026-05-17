# Arquitectura del Sistema NOA — Content Automation

> Sistema de producción de video faceless para Instagram Reels, TikTok y YouTube Shorts.
> Nicho: padres de adolescentes con Altas Capacidades (AACC).
> Output objetivo: 5-7 videos publicados por semana de forma semi-automática.

---

## Diagrama de Arquitectura Completo (ASCII)

```
╔══════════════════════════════════════════════════════════════════════════════════════╗
║                         SISTEMA NOA — CONTENT PIPELINE                              ║
╚══════════════════════════════════════════════════════════════════════════════════════╝

┌──────────────────────────────────────────────────────────────────────────────────────┐
│  CAPA 1: CONTENT LAYER                                                               │
│  (Ideas → Guiones → Assets listos para producción)                                   │
│                                                                                      │
│  ┌─────────────┐    ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐    │
│  │  AIRTABLE   │───▶│  CLAUDE API  │───▶│  AIRTABLE    │───▶│  FREEPIK AI      │    │
│  │  Ideas DB   │    │  Script Gen  │    │  Scripts DB  │    │  o DALL-E API    │    │
│  │  (backlog)  │    │  + Scoring   │    │  (aprobados) │    │  (imágenes BG)   │    │
│  └─────────────┘    └──────────────┘    └──────────────┘    └──────────────────┘    │
│         │                  │                   │                       │             │
│         │                  │            [GATE MANUAL]                  │             │
│         │                  │           Owner aprueba                   │             │
│         │                  │           o rechaza guión                 │             │
│         ▼                  ▼                   ▼                       ▼             │
│  ┌────────────────────────────────────────────────────────────────────────────────┐  │
│  │                      n8n  —  ORQUESTADOR CENTRAL                              │  │
│  │          (self-hosted · conecta todas las capas · maneja errores)             │  │
│  └────────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────┘
                                          │
                                          │ (script aprobado + assets)
                                          ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  CAPA 2: PRODUCTION LAYER                                                            │
│  (Assets → Voz → Video Ensamblado)                                                   │
│                                                                                      │
│  ┌──────────────┐         ┌────────────────────────────────┐   ┌──────────────────┐ │
│  │  ELEVENLABS  │         │       CREATOMATE API           │   │  RUNWAY / KLING  │ │
│  │  Voz ES-ES   │────────▶│  Template 9:16 + Audio + Imgs  │   │  (CONDICIONAL)   │ │
│  │  cálida/     │         │  Subtítulos embedded           │   │  B-roll 3-5s     │ │
│  │  femenina    │         │  Logo NOA + colores de marca   │   │  solo fondo      │ │
│  └──────────────┘         └──────────────┬─────────────────┘   └──────────────────┘ │
│                                          │                                           │
│                                          ▼                                           │
│                              ┌───────────────────┐                                  │
│                              │   VIDEO MP4 FINAL │                                  │
│                              │   1080 × 1920     │                                  │
│                              │   9:16 · ≤60s     │                                  │
│                              │   AAC audio       │                                  │
│                              └─────────┬─────────┘                                  │
└────────────────────────────────────────┼─────────────────────────────────────────────┘
                                         │
                                         │ (video listo)
                                         ▼
┌──────────────────────────────────────────────────────────────────────────────────────┐
│  CAPA 3: DISTRIBUTION LAYER                                                          │
│  (Video → Publicado en plataformas → Datos de vuelta al sistema)                     │
│                                                                                      │
│  ┌──────────────┐    ┌──────────────────┐    ┌────────────────┐    ┌─────────────┐  │
│  │  METRICOOL   │───▶│  INSTAGRAM       │    │  TIKTOK        │    │  YOUTUBE    │  │
│  │  Scheduling  │    │  Graph API       │    │  (manual       │    │  Shorts API │  │
│  │  + Analytics │    │  (auto-post)     │    │  por ahora)    │    │  (auto)     │  │
│  └──────┬───────┘    └──────────────────┘    └────────────────┘    └─────────────┘  │
│         │                                                                            │
│         │  24h después → webhook de métricas                                        │
│         ▼                                                                            │
│  ┌────────────────────────────────────────────────────────────────────────────────┐  │
│  │              AIRTABLE  —  ANALYTICS & PERFORMANCE DB                          │  │
│  │     views · saves · shares · comments · reach → feed loop a Ideas DB          │  │
│  └────────────────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────────────────┘
```

---

## Flujo de Datos Paso a Paso

### Paso 1 — Disparo de idea (trigger automático)
```
n8n cron: 09:00 cada día laboral
  → Lee Airtable [Ideas_Queue] WHERE status = "ready_to_produce"
  → Toma la idea con mayor priority_score
  → Envía a Claude API con:
      · System prompt de NOA (voz de marca, tono emocional, restricciones AACC)
      · Tema de la idea
      · Formato destino (Reel 60s / Short 45s / TikTok 30s)
      · Pain point principal de la idea
  → Claude devuelve JSON: { hook, body_segments[], cta, caption, hashtags[], title_a, title_b }
  → n8n escribe en Airtable [Scripts_DB] con status = "needs_review"
  → Envía notificación push al owner (Telegram o email)
```

### Paso 2 — Aprobación humana (único punto manual obligatorio)
```
Owner abre Airtable en móvil o desktop
  → Lee guión completo (duración real: 2-4 min)
  → Cambia status a:
      "approved"     → pipeline continúa automáticamente
      "rejected"     → idea vuelve al backlog con nota
      "needs_edit"   → owner edita texto directamente en Airtable → re-aprueba
  → n8n webhook detecta el cambio de status en < 30 segundos
```

### Paso 3 — Producción paralela de assets
```
n8n dispara 3 ramas en paralelo:

RAMA A — Voz:
  → ElevenLabs API: POST /v1/text-to-speech/{voice_id}
  → Input: guión completo en texto
  → Settings: modelo "eleven_multilingual_v2", stability 0.65, similarity 0.80
  → Output: audio.mp3 → guardado en /voices/{video_id}/

RAMA B — Imágenes de fondo:
  → Freepik AI API (o DALL-E) con prompts visuales generados por Claude
  → 4-6 imágenes según segmentos del guión
  → Sin caras, sin texto, abstractas o situacionales
  → Output: img_01.png … img_06.png → /assets/{video_id}/

RAMA C — B-roll stock (primero):
  → Búsqueda en librería local de Pexels descargados previamente
  → Si no hay match → Pexels API gratuita → descarga clip
  → Cooldown check: el clip no se ha usado en los últimos 30 días
  → Output: clip_01.mp4 … → /assets/{video_id}/

Las 3 ramas convergen antes del Paso 4.
```

### Paso 4 — Ensamblado de video
```
n8n → Creatomate API: POST /v1/renders
  Payload:
  {
    "template_id": "noa-reel-emocional-v3",
    "modifications": {
      "audio": "https://storage/voices/{video_id}/audio.mp3",
      "bg_image_1": "https://storage/assets/{video_id}/img_01.png",
      "bg_image_2": "https://storage/assets/{video_id}/img_02.png",
      "subtitle_text": "{guión_completo}",
      "logo": "https://storage/brand/noa-logo.png",
      "cta_text": "{cta}",
      "music_track": "noa-ambient-calm-01.mp3"
    }
  }
  
Creatomate devuelve: { "id": "render_abc123", "status": "queued" }

n8n polling cada 45s (o webhook cuando disponible) → cuando status = "succeeded":
  → Descarga video_final.mp4
  → Guarda en /outputs/{video_id}/
  → Actualiza Airtable: status = "video_ready"
  → Envía preview link al owner (opcional)
```

### Paso 5 — Distribución programada
```
n8n → Metricool API:
  → Sube video_final.mp4
  → Añade caption + hashtags (generados por Claude en Paso 1)
  → Programa publicación en slot óptimo:
      Instagram Reels: martes/jueves/sábado 19:00-20:00h
      YouTube Shorts:  mismo video, 30 min después
      TikTok:         manual (descarga + subida manual por owner)
  → Instagram Graph API valida el video y confirma recepción

Airtable → status = "scheduled" → luego "published" (webhook post-publicación)
```

### Paso 6 — Feedback loop (24-48h después)
```
Metricool webhook → n8n (24h post-publicación):
  → Recoge: views, reach, saves, shares, comments, play_time_avg
  → Escribe en Airtable [Analytics_DB]
  → Lógica de decisión:
      IF views > 15.000 en 48h:
        → Claude genera 3 variaciones del mismo tema → añade al backlog con priority = "alta"
      IF views < 800 en 48h:
        → Flagea para análisis manual → notifica al owner
      IF save_rate > 5%:
        → Tema guardado como "evergreen" → reciclar en 60 días
```

---

## Evaluación Honesta del Stack

### KEEP — Se quedan sin discusión

#### Claude API
- **Propósito**: Guiones, hooks, captions, ideas, scoring de calidad interno
- **Veredicto**: Es el mejor modelo para contenido emocional en español del nicho AACC. GPT-4o es 30% más rápido pero produce guiones más genéricos. Gemini Flash es barato pero pierde el matiz emocional. Claude mantiene la voz de marca cuando se alimenta con buenos system prompts.
- **Lo que NO hace bien**: A veces sobre-explica. Hay que instruirle explícitamente que sea conciso y deje respirar las frases.
- **Costo real**: $15-30/mes para 30 guiones + iteraciones
- **API**: Sí, robusta y bien documentada
- **Fiabilidad**: 9/10
- **Riesgo**: Cambios de precios de Anthropic (monitorear)

#### ElevenLabs
- **Propósito**: Narración en español de todos los videos
- **Veredicto**: Sin alternativa real en calidad de español nativo en 2025. La voz "Lara" en español o una voz clonada custom suena humana. Azure TTS y Google TTS suenan a IVR de banco. Este es el factor #1 que separa un video profesional de uno que grita "hecho con IA barata".
- **Lo crítico**: Elegir la voz en el día 1 y no cambiarla nunca. La consistencia de voz es identidad de marca.
- **Costo real**: Plan Creator $22/mes (100k caracteres = 25-30 videos/mes)
- **API**: Sí, excelente
- **Fiabilidad**: 9/10
- **Riesgo**: Subidas de precio. Actualmente la mejor opción; revisar cada 6 meses.

#### Creatomate
- **Propósito**: Ensamblado automatizado de video via API
- **Veredicto**: Es la única herramienta que resuelve el ensamblado de video desde una API de forma confiable, con templates JSON editables, sin cobrar por render variable (plan fijo). Shotstack es la alternativa más cercana pero tiene peor documentación y cuesta más por el mismo volumen.
- **Lo que requiere**: 1-2 días para crear los templates JSON iniciales. Una vez hechos, son permanentes.
- **Costo real**: Plan Growth $99/mes (600 renders = 150 videos/mes)
- **API**: Sí, la mejor del mercado para este caso de uso
- **Fiabilidad**: 8/10
- **Riesgo**: Startup relativamente joven. Tener una cuenta de Shotstack como backup por si acaso.

#### n8n (self-hosted)
- **Propósito**: Cerebro del sistema. Orquesta todos los pasos del pipeline.
- **Veredicto**: Self-hosted en un VPS de €6/mes hace lo mismo que Make.com a $29/mes con límites de operaciones. Para un pipeline que corre todos los días durante años, n8n es la opción inteligente financieramente.
- **Lo que requiere**: Conocimientos básicos de Linux y JSON. La curva de aprendizaje es real (3-5 días para dominar el sistema). Vale la pena.
- **Costo real**: VPS Hetzner CX21 = €6/mes
- **API**: Es el orquestador; se conecta a todas las APIs
- **Fiabilidad**: 8/10 (depende de que el VPS esté online)
- **Riesgo**: Si cae el servidor, el pipeline para. Solución: UptimeRobot gratuito + alertas Telegram.

#### Airtable
- **Propósito**: Base de datos de contenido y CMS de aprobación
- **Veredicto**: La interfaz visual es lo que hace a Airtable insustituible para este caso de uso. El owner aprueba guiones desde el móvil en Airtable como si fuera una app. Con Notion o Google Sheets la UX de revisión es peor y el owner tarda más.
- **Costo real**: Plan Team $20/mes (o Free si el volumen es bajo al inicio)
- **API**: Sí, API REST bien documentada con webhooks
- **Fiabilidad**: 9/10
- **Riesgo**: Posibles cambios de precio de Airtable (historial de subidas agresivas).

#### Metricool
- **Propósito**: Programación de publicaciones + analytics básicos
- **Veredicto**: El mejor scheduler para creadores hispanohablantes. Soporte real para IG Reels scheduling (no todos los schedulers lo hacen bien). Analytics suficientes para las decisiones del pipeline.
- **Costo real**: Plan Advanced $22/mes
- **API**: Sí, disponible. Para máxima automatización, combinar con Instagram Graph API directo.
- **Fiabilidad**: 8/10
- **Riesgo**: Cambios en los acuerdos con plataformas (fuera del control de Metricool).

#### Instagram Graph API
- **Propósito**: Publicación directa de Reels desde el pipeline
- **Veredicto**: Obligatorio. Sin esta API, la publicación es manual. Requiere cuenta Meta Business verificada y Facebook Page vinculada.
- **Costo real**: Gratis
- **API**: Sí, oficial de Meta
- **Fiabilidad**: 7/10 (Meta es el actor menos confiable de este stack; cambia condiciones sin aviso)
- **Riesgo crítico**: Los access tokens expiran cada 60 días. Implementar renovación automática desde el día 1 o el pipeline colapsa silenciosamente.

---

### CONDITIONAL — Usar solo con criterio específico

#### Runway ML / Kling AI / Google Veo
- **Para qué sirven**: Clips de B-roll de 3-5 segundos como fondo abstracto (manos sobre papel, luz de ventana, adolescente de espaldas). Máximo 20-25% del contenido visual de un video.
- **Por qué CONDICIONAL y no KEEP**: El video generado por IA se detecta visualmente en 2025. El nicho AACC es un nicho de padres educados que identifican content farm de IA. Un fondo de Runway mal usado destruye la credibilidad.
- **Cuándo usar**: Cuando el stock footage gratuito (Pexels, Pixabay) no tiene lo que necesitas para ese segmento específico.
- **Cuándo NO usar**: Como fuente principal de imagen. Nunca para simular personas reales. Nunca en primer plano.
- **Costo**: Runway Gen-3 Standard $15/mes (125 créditos). Kling ~$8/mes. No necesitas los dos.
- **Recomendación operativa**: Empieza 90 días con solo stock gratuito. Añade Runway solo si sientes la limitación de forma concreta.

#### Freepik AI / DALL-E API
- **Freepik AI**: $24/mes plan Essentials. Buena variedad, sin problemas de copyright, API disponible. Mejor para ilustraciones y fondos abstractos.
- **DALL-E via OpenAI API**: ~$0.04/imagen, pago por uso, integrable directo en n8n sin cuenta separada (ya usas Anthropic, OpenAI es un paso más). Más predecible en prompting.
- **Veredicto**: Usa DALL-E vía API para el MVP (menos cuentas que gestionar). Añade Freepik si necesitas más variedad de estilo.
- **Por qué no Midjourney**: Sin API pública real en 2025. Requiere Discord bot o servicios de terceros frágiles. Descártalo para cualquier pipeline de automatización serio.

---

### DROP — Fuera del stack con razones concretas

#### Canva
- **Por qué se va**: Canva no tiene API para renderizado de video automático. Su "API" sirve para embeds y gestión de assets, no para producción automatizada. Cualquier "integración de Canva con n8n" que veas en YouTube es una ilusión que funciona en demos y colapsa en producción.
- **Lo que sí puedes usar Canva para**: Crear los templates base de thumbnails manualmente, una sola vez. Pero el video en sí, nunca.

#### CapCut
- **Por qué se va**: No tiene API pública oficial. Las "integraciones" de CapCut son scraping no oficial que rompen sin aviso con cada actualización de la app. Además, CapCut es de ByteDance (misma empresa que TikTok). En un nicho donde los padres cuidan la privacidad de sus hijos, usar tecnología de ByteDance en el backend es un riesgo reputacional.

#### HeyGen
- **Por qué se va**: HeyGen genera avatares digitales con cara. Esto viola directamente el concepto faceless del sistema NOA. La audiencia de padres de AACC conecta con voces auténticas y conceptos, no con avatares plásticos que leen un teleprompter. Usar HeyGen no solo destruye la estética; destruye la confianza.

#### Make.com (como orquestador principal)
- **Por qué es alternativa y no primera opción**: A $29/mes con 10.000 operaciones, un pipeline que produce 30 videos/mes con todos sus pasos (Claude, ElevenLabs, Creatomate, Airtable, Metricool, IG API) consume entre 15-20 operaciones por video = 450-600 operaciones/mes. Bien dentro del límite. Pero si experimentas y reiteras, te pasas de límite y el coste sube.
- **Cuándo usar Make.com**: Si el owner no quiere gestionar un servidor Linux. Completamente válido. Asume $29-49/mes en lugar de €6/mes.

---

## Conexiones API — Lista Completa

| Conexión | Dirección | Auth | Frecuencia |
|---|---|---|---|
| n8n → Airtable | REST API | Personal Access Token | Polling cada 5 min + webhooks |
| n8n → Claude API | REST API | Anthropic API Key | 1x por video (guión + scoring) |
| n8n → ElevenLabs | REST API | ElevenLabs API Key | 1x por video (voz) |
| n8n → Creatomate | REST API | Creatomate API Key | 1x por video (render) |
| Creatomate → n8n | Webhook | Verify token | Al finalizar cada render |
| n8n → DALL-E / Freepik | REST API | OpenAI / Freepik API Key | 4-6x por video (imágenes) |
| n8n → Metricool | REST API | Metricool API Token | 1x por video (scheduling) |
| Metricool → Instagram | OAuth2 | Long-lived token (60d) | 1x por publicación |
| Instagram → n8n | Webhook | Meta Verify Token | Cada publicación + métricas |
| YouTube Data API → n8n | OAuth2 | Google Cloud credentials | 1x por video |

---

## Cuellos de Botella y Soluciones

### Bottleneck #1: Tiempo de render en Creatomate
- **Problema**: Un video de 60 segundos tarda 2-4 minutos. Con 7 videos en batch son 14-28 minutos.
- **Solución**: Programar renders nocturnos (2:00-5:00 AM). n8n tiene scheduler nativo. Limitar a 3 renders simultáneos máximo. Usar webhooks de Creatomate (no polling) para notificación asíncrona.

### Bottleneck #2: Aprobación humana como bloqueante del pipeline
- **Problema**: El owner tiene un día ocupado o está de vacaciones. El pipeline para.
- **Solución estructural**: Mantener siempre buffer de 3-5 guiones aprobados y listos. El lunes se aprueban los guiones de toda la semana en una sesión de 20 min. No aprobar de uno en uno.
- **Solución de emergencia**: n8n envía recordatorio a los 2h, 4h y 6h si un guión lleva en "needs_review" sin acción. Nunca auto-publicar sin aprobación.

### Bottleneck #3: Tokens de Instagram que expiran
- **Problema**: El long-lived access token de Meta expira cada 60 días. Si no se renueva, el pipeline de distribución colapsa silenciosamente. No hay error visible; simplemente no publica.
- **Solución**: Workflow de n8n dedicado que cada 45 días ejecuta el refresh automático del token via Meta Graph API endpoint `/oauth/access_token`. Alerta al owner 5 días antes si el refresh falla.

### Bottleneck #4: Guiones genéricos de Claude
- **Problema**: Claude a veces genera guiones demasiado genéricos si el system prompt es pobre o la idea es vaga.
- **Solución**: Antes de enviar el guión a Airtable para revisión, un segundo call a Claude lo evalúa en 5 criterios: fuerza del hook, resonancia emocional, especificidad AACC, claridad del CTA, longitud correcta. Solo los guiones con puntuación ≥ 7/10 llegan al owner. Los que no pasan se regeneran automáticamente (máximo 2 intentos).

### Bottleneck #5: Stock footage repetitivo
- **Problema**: Si siempre usas los mismos clips de Pexels, la audiencia lo detecta subconscientemente. Los videos empiezan a parecer "el mismo".
- **Solución**: Airtable lleva registro de qué clip se usó en qué video y en qué fecha. n8n verifica antes de asignar un clip que no se haya usado en los últimos 30 días. Mantener librería mínima de 80-100 clips descargados localmente.

---

## Estimación de Costos Mensuales

### Stack Completo (producción estable: 25-30 videos/mes)

| Herramienta | Plan | Costo/mes |
|---|---|---|
| Claude API | Pay-per-use (~30 guiones) | ~$20 |
| ElevenLabs | Creator | $22 |
| Creatomate | Growth | $99 |
| n8n VPS (Hetzner CX21) | Self-hosted | €6 |
| Airtable | Team | $20 |
| Metricool | Advanced | $22 |
| Freepik AI | Essentials | $24 |
| Stock footage | Pexels / Pixabay | $0 |
| **TOTAL** | | **~$213/mes** |

### Stack Mínimo (validación: primeros 60 días, 8-12 videos/mes)

| Herramienta | Plan | Costo/mes |
|---|---|---|
| Claude API | Pay-per-use | ~$8 |
| ElevenLabs | Starter | $5 |
| Creatomate | Starter | $29 |
| n8n | Railway free tier | $0 |
| Airtable | Free | $0 |
| Metricool | Advanced | $22 |
| DALL-E via OpenAI API | Pay-per-use | ~$3 |
| **TOTAL** | | **~$67/mes** |

**Recomendación**: Empieza con el stack mínimo los primeros 60 días. Cuando el sistema esté estabilizado y el canal tenga tracción real, upgrade al stack completo. El salto de $67 a $213 se justifica cuando ya tienes un sistema probado, no antes.

### B-roll con IA (coste adicional opcional)

| Herramienta | Plan | Costo/mes | Veredicto |
|---|---|---|---|
| Runway ML | Standard | $15 | Solo si stock gratuito no es suficiente |
| Kling AI | Basic | $8 | Alternativa a Runway, no las dos |
| Google Veo | Variable | TBD | Esperar hasta que sea GA y estable |

---

## Notas de Escalabilidad

### De 7 a 21 videos/semana
- Claude API: escala linealmente. De $20 a $60/mes.
- ElevenLabs: upgrade a Professional $99/mes (500k caracteres).
- Creatomate: upgrade a Professional $199/mes (2.000 renders).
- n8n: puede necesitar más RAM (Hetzner CX31 = €15/mes).
- Airtable: sin cambio hasta 50.000 registros.
- Trabajo del owner: NO aumenta. Sigue siendo 25-30 min/día.

### De 1 cuenta a 3 cuentas / nichos
- Crear base de Airtable nueva por nicho.
- Duplicar workflows de n8n con variables de entorno distintas.
- Clonar o seleccionar nueva voz en ElevenLabs por "persona".
- Costo adicional por nicho extra: ~$50-70/mes.

### El límite real del sistema
El límite no es técnico. Es la revisión humana. Con una persona revisando, el límite práctico es 2-3 guiones/día (10-15 min de lectura). Si quieres más volumen, necesitas un segundo revisor o bajar los estándares de aprobación, lo cual no es recomendable: en el nicho AACC, la confianza de los padres es el activo más frágil y más valioso del canal.
