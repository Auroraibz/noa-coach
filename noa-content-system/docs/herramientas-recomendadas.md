# Herramientas Recomendadas — Sistema NOA

> Evaluación honesta de cada herramienta del stack.
> Sin publicidad disfrazada de recomendación.
> Última revisión: mayo 2025.

---

## Criterios de Evaluación

Cada herramienta se evalúa en 6 dimensiones:

- **Propósito**: Para qué sirve exactamente en el sistema NOA
- **Costo**: Precio real del plan útil (no el plan de marketing)
- **API**: Disponibilidad y calidad de la API para automatización
- **Fiabilidad (1-10)**: Uptime histórico + consistencia de resultados
- **Curva de aprendizaje**: Tiempo real para que el sistema NOA la use bien
- **Veredicto**: Recomendación directa y opinionada

---

## Herramientas RECOMENDADAS (Stack Principal)

---

### 1. Claude API (Anthropic)

| Campo | Detalle |
|---|---|
| **Propósito** | Generación de guiones, hooks, captions, scoring de calidad, ideas |
| **Costo** | Pay-per-use. claude-sonnet-4-5: $3/1M tokens input, $15/1M tokens output. Para 30 guiones/mes: ~$15-25/mes |
| **API** | Sí. Excellente documentación. SDKs en Python, TypeScript, Node. |
| **Fiabilidad** | 9/10 |
| **Curva de aprendizaje** | Baja (3-5 horas). El reto está en escribir buenos system prompts, no en la API. |

**Veredicto**: El mejor modelo para el nicho AACC en 2025. La diferencia con GPT-4o no está en la inteligencia sino en el matiz emocional. Claude escribe guiones que suenan a humano preocupado por el tema; GPT-4o escribe guiones que suenan a consultor bien informado. Para una audiencia de padres que están solos con un problema complejo, ese matiz importa.

**Lo que necesitas saber antes de comprar**:
- El modelo correcto para producción es claude-sonnet-4-5, no claude-opus. Opus es 5x más caro y el incremento de calidad para guiones de Reels no justifica el gasto.
- Necesitas escribir un system prompt de NOA de 800-1200 palabras que defina exactamente la voz de marca, las restricciones del nicho y ejemplos de guiones buenos y malos. Sin eso, Claude produce contenido genérico.
- Anthropic cambia precios con más frecuencia que sus competidores. Revisar trimestralmente.

**Alternativa si Claude desaparece o se encarece**: GPT-4o Mini para guiones estándar, GPT-4o para los BOFU más críticos. El sistema puede migrar en 2-3 horas cambiando el endpoint de n8n.

---

### 2. ElevenLabs

| Campo | Detalle |
|---|---|
| **Propósito** | Síntesis de voz en español para todos los videos del sistema |
| **Costo** | Plan Creator: $22/mes (100k caracteres, ~25-30 videos/mes). Plan Starter: $5/mes (30k caracteres, 7-8 videos/mes). |
| **API** | Sí. REST API limpia. n8n tiene node nativo de ElevenLabs. |
| **Fiabilidad** | 9/10 |
| **Curva de aprendizaje** | Baja (2-4 horas para elegir voz y configurar parámetros). |

**Veredicto**: Sin alternativa real para español nativo de calidad. Esta es la decisión de infraestructura más importante del sistema después del guión. Una voz mala mata la retención del video independientemente de lo buen que sea el contenido. Azure TTS, Google TTS y Amazon Polly en español suenan a respuesta automática de banco. ElevenLabs suena a persona.

**Configuración óptima para NOA**:
- Voz: "Lara" (español ES-ES, femenina, tono cálido) o crear un voice clone con 10-15 minutos de audio limpio
- Modelo: eleven_multilingual_v2 (mejor calidad en español)
- Stability: 0.60-0.65 (más natural, menos robótico)
- Similarity boost: 0.75-0.80 (fiel a la voz elegida)
- Style exaggeration: 0.10-0.15 (ligero énfasis emocional sin exagerar)

**Trampa a evitar**: No cambies la voz elegida después de las primeras 4 semanas. La voz es parte de la identidad sonora del canal. Si la cambias, los seguidores lo notan aunque no sepan decir por qué. Elige bien desde el día 1.

**Alternativa si ElevenLabs cierra o duplica precios**: PlayHT (peor calidad en español), Murf AI (aceptable pero menos natural), Resemble AI (más técnico, API menos amigable).

---

### 3. Creatomate

| Campo | Detalle |
|---|---|
| **Propósito** | Ensamblado automatizado de video via API (el "editor" del sistema) |
| **Costo** | Starter: $29/mes (100 renders). Growth: $99/mes (600 renders). Para 30 videos/mes, Starter es suficiente. |
| **API** | Sí. La mejor API de su categoría. Templates en JSON. Webhooks. SDK. |
| **Fiabilidad** | 8/10 |
| **Curva de aprendizaje** | Alta (3-5 días para crear y refinar los templates JSON iniciales). Una vez hechos, no hay mantenimiento. |

**Veredicto**: Creatomate resuelve el problema que ninguna otra herramienta resuelve bien: ensamblado de video programático de calidad con templates personalizables. La curva de aprendizaje del template JSON es real y requiere paciencia. Pero es un trabajo que se hace una vez y luego funciona indefinidamente. No hay alternativa directa con estas capacidades a este precio.

**Qué crea Creatomate para NOA**:
- Template "Reel Emocional": fondo de imagen/video suave, voz en over, subtítulos animados inferiores, logo NOA en esquina superior, música ambiente baja
- Template "Reel Educativo": fondo más estructurado, texto en pantalla para puntos clave, CTA final más prominente
- Template "Reel BOFU": apertura con branding NOA más visible, colores más saturados, CTA final con animación de botón

**Alternativas evaluadas**:
- **Shotstack**: Similar precio, peor documentación, templates menos flexibles. Válido si Creatomate falla.
- **Renderforest**: Cobra por render, escala mal, enfocado en usuarios manuales, no en APIs.
- **Lumen5**: No tiene API real para este caso de uso. Descartado.
- **Adobe Express API**: Existe pero es extremadamente limitada para video. Descartada.

---

### 4. n8n (self-hosted)

| Campo | Detalle |
|---|---|
| **Propósito** | Orquestador central del pipeline. Conecta y automatiza todas las herramientas. |
| **Costo** | Self-hosted en VPS: €5-10/mes (VPS Hetzner CX21 a €5.83/mes). n8n Cloud: $24/mes (plan Starter, 2.500 ejecuciones). |
| **API** | n8n ES el sistema de integración. No consume una API, las gestiona todas. |
| **Fiabilidad** | 8/10 (self-hosted depende del VPS; Cloud 9/10) |
| **Curva de aprendizaje** | Media (3-5 días para dominar los workflows del pipeline NOA). Instalar el VPS: 2-3 horas extra si no tienes experiencia Linux. |

**Veredicto**: La decisión de self-hosted vs. Cloud de n8n define el perfil del operador del sistema. Self-hosted es más barato y sin límites, pero requiere gestionar un servidor. n8n Cloud es más caro pero sin mantenimiento. Para un sistema que debe funcionar años con mínimo mantenimiento, recomiendo n8n Cloud en la fase inicial y migrar a self-hosted solo si el coste se vuelve relevante.

**Instalación recomendada para self-hosted**:
- VPS: Hetzner CX21 (2 vCPU, 4GB RAM, €5.83/mes)
- Despliegue: Docker + docker-compose oficial de n8n
- Dominio: Subdominio propio (ej: n8n.tunoa.com) con SSL via Caddy o Nginx + Certbot
- Backup: Volumen de Docker con copia diaria a Backblaze B2 (~$0.50/mes)

**Alternativa principal**: Make.com (antes Integromat). Más visual, más fácil de configurar, sin servidor. Precio: $9-29/mes con límite de operaciones. Para el volumen de NOA (5-7 videos/semana con todos los pasos), el plan de $29/mes con 10.000 operaciones es suficiente. Recomendable si no quieres gestionar infraestructura.

---

### 5. Airtable

| Campo | Detalle |
|---|---|
| **Propósito** | Base de datos de contenido, CMS de aprobación, analytics tracker |
| **Costo** | Free: 1 base, 1.000 registros, sin automations avanzadas. Team: $20/mes por usuario. Para NOA: Free al inicio, Team cuando necesites webhooks y más de 5.000 registros. |
| **API** | Sí. REST API bien documentada. Personal Access Tokens. Webhooks nativos (plan Team). |
| **Fiabilidad** | 9/10 |
| **Curva de aprendizaje** | Baja (4-6 horas para crear la estructura de bases). |

**Veredicto**: Airtable es el CMS de aprobación. El owner vive en esta interfaz cuando revisa guiones. La interfaz es lo suficientemente visual e intuitiva para que la revisión desde el móvil tome 3 minutos, no 15. Notion no tiene esa fluidez para revisar y aprobar registros. Google Sheets puede hacer lo mismo técnicamente pero la UX es inferior.

**Estructura de bases recomendada para NOA**:
- `Ideas_Queue`: idea, pain_point, funnel_stage, format, priority_score, source, status
- `Scripts_DB`: script_text, score_total, score_hook, score_emotion, score_aacc, score_cta, status, approved_by, approved_at
- `Videos_DB`: video_id, script_id, audio_url, video_url, preview_url, creatomate_render_id, status
- `Published_DB`: video_id, platform, publish_time, post_url, post_id
- `Analytics_DB`: video_id, views_24h, views_48h, views_7d, saves, shares, comments, play_time_avg, save_rate, reach_followers, reach_non_followers

**Trampa a evitar**: No uses las "automations" nativas de Airtable para el pipeline. Son lentas y tienen límites arbitrarios. Toda la lógica de automatización va en n8n. Airtable es solo la base de datos y la interfaz humana.

**Alternativa si Airtable sube precios drásticamente**: Notion (API disponible pero peor para workflows de aprobación), NocoDB (open-source, self-hosted, API compatible con Airtable — opción nuclear para reducir costos).

---

### 6. Metricool

| Campo | Detalle |
|---|---|
| **Propósito** | Scheduling de publicaciones y analytics unificados |
| **Costo** | Plan Advanced: $22/mes (1 marca, múltiples redes, analytics completos). |
| **API** | Sí. API disponible pero documentación limitada. Para scheduling programático, funciona bien. |
| **Fiabilidad** | 8/10 |
| **Curva de aprendizaje** | Baja (2-3 horas). |

**Veredicto**: Metricool es el mejor scheduler para creadores hispanohablantes en 2025. Soporte real para IG Reels (no todos los schedulers publican Reels correctamente). Analytics suficientes para las decisiones del sistema NOA. La API no es la mejor del mercado pero cumple para programar publicaciones desde n8n.

**Alternativas evaluadas**:
- **Buffer**: Más simple, peor soporte para Reels, límites absurdos en plan básico. Descartado.
- **Later**: Buen producto pero más caro para el mismo resultado. Solo si ya lo usas.
- **Hootsuite**: Excesivamente caro y complejo para el caso de uso de NOA. Descartado.
- **Publicar directo vía Instagram Graph API** (sin Metricool): Técnicamente viable desde n8n, elimina la dependencia de Metricool, pero requiere gestionar el scheduling y los tokens tú mismo. Recomendable en fase avanzada si quieres reducir costos.

---

### 7. Instagram Graph API (Meta)

| Campo | Detalle |
|---|---|
| **Propósito** | Publicación directa de Reels en Instagram |
| **Costo** | Gratis (requiere Meta Developer App configurada y cuenta de negocio) |
| **API** | Sí. Oficial de Meta. Bien documentada pero compleja de configurar inicialmente. |
| **Fiabilidad** | 7/10 (Meta es el actor menos predecible de este stack) |
| **Curva de aprendizaje** | Alta para configurar (6-10 horas la primera vez). Una vez configurada, se mantiene sola. |

**Veredicto**: Obligatoria. Sin esta API, la publicación es manual. El mayor riesgo es Meta: cambia las políticas de su API, los scopes de permisos y los límites sin aviso consistente. Tener Metricool como capa intermedia reduce el impacto de estos cambios.

**Configuración crítica**:
- Cuenta Instagram Business (no Personal ni Creator)
- Facebook Page vinculada a la cuenta IG
- Meta Developer App con permisos: `pages_read_engagement`, `pages_manage_posts`, `instagram_basic`, `instagram_content_publish`
- Long-lived token (60 días): renovar cada 45 días vía workflow automático en n8n

---

## Herramientas CONDICIONALES

---

### 8. Freepik AI

| Campo | Detalle |
|---|---|
| **Propósito** | Generación de imágenes para fondos y visuals de los videos |
| **Costo** | Plan Essentials: $24/mes (100 generaciones/día, uso comercial) |
| **API** | Sí. API disponible en plan de pago. |
| **Fiabilidad** | 7/10 |
| **Curva de aprendizaje** | Baja. |

**Veredicto**: Buena opción para imágenes abstractas, naturaleza, fondos emocionales. Problemas con caras humanas (como todas las herramientas de imagen en 2025). Si generas imágenes sin personas, funciona bien. Alternativa directa: DALL-E vía OpenAI API (pago por uso, ~$0.04/imagen, integrable directamente en n8n sin cuenta extra si ya usas Claude vía OpenAI).

---

### 9. DALL-E 3 (OpenAI API)

| Campo | Detalle |
|---|---|
| **Propósito** | Generación de imágenes como alternativa a Freepik AI |
| **Costo** | $0.040/imagen (1024×1024), $0.080/imagen (1792×1024). Para 5 imágenes × 30 videos = ~$6-12/mes |
| **API** | Sí. Excelente, misma API que GPT. |
| **Fiabilidad** | 9/10 |
| **Curva de aprendizaje** | Mínima si ya usas OpenAI. |

**Veredicto**: Si ya tienes API key de OpenAI para cualquier otro uso, DALL-E es la opción más sencilla de integrar en n8n para imágenes. El prompting es más predecible que Freepik. La calidad es suficiente para fondos y visuales abstractos.

---

### 10. Runway ML

| Campo | Detalle |
|---|---|
| **Propósito** | Generación de clips de B-roll de IA (solo clips de fondo cortos) |
| **Costo** | Standard: $15/mes (125 créditos, ~62 clips de 5 segundos) |
| **API** | Sí. API disponible. |
| **Fiabilidad** | 8/10 |
| **Curva de aprendizaje** | Baja para generación de clips simples. |

**Veredicto**: Úsalo solo después de 60-90 días de operación cuando el stock footage gratuito ya no te da lo que necesitas. No es prioritario desde el día 1. Pexels.com tiene suficiente contenido libre de derechos para los primeros 3-4 meses.

---

## Herramientas A EVITAR

---

### Canva (para automatización)

**Por qué no**: Canva es una herramienta manual brillante. No es una herramienta de automatización. Su "API" está diseñada para que otras plataformas de diseño se integren con Canva, no para que pipelines de producción de video la usen programáticamente. Cualquier "integración Canva + Zapier" que hayas visto en YouTube para producir videos automáticamente es una demo que no aguanta producción real.

**Uso válido**: Crear los templates visuales de referencia para Creatomate. Diseñas en Canva, replicar el diseño en Creatomate.

---

### CapCut (para automatización)

**Por qué no**: Sin API. Punto. Cualquier "integración" es scraping no oficial que rompe con la próxima actualización de la app. Además, es software de ByteDance. Dependencia de ByteDance en un nicho donde los padres son sensibles a la privacidad de datos de sus hijos es un riesgo reputacional que no vale la pena asumir.

---

### HeyGen

**Por qué no**: HeyGen genera avatares con cara. Un canal faceless con un avatar de HeyGen no es un canal faceless, es un canal de avatar de IA, que es peor que ninguno de los dos. Los padres de AACC son una audiencia educada con baja tolerancia a la manipulación visual. Un avatar de HeyGen detectado destruye la credibilidad instantáneamente.

---

### Synthesia

**Por qué no**: Misma razón que HeyGen. Avatares con cara. No es el formato de NOA.

---

### Pictory AI

**Por qué no**: Pictory genera videos a partir de texto con footage de stock, pero la selección de clips es automática y genérica. No hay control sobre qué imágenes aparecen en cada segmento del guión. El resultado final parece una presentación de PowerPoint hecha en 2018. No hay forma de aplicar la identidad visual de NOA con fidelidad.

---

### Descript

**Por qué no**: Descript es una herramienta de edición de video asistida por IA, no una herramienta de automatización. No tiene API para producción programática. Excelente para editores humanos. Inútil para un pipeline de n8n.

---

### Midjourney

**Por qué no**: Sin API pública real en mayo 2025. El "acceso API" requiere Discord como intermediario, con dependencia en bots de terceros que pueden dejar de funcionar. Freepik AI y DALL-E dan resultados comparables con APIs reales y fiables. No hay justificación para usar Midjourney en automatización.

---

### Zapier (como alternativa a n8n para este volumen)

**Por qué no en producción**: Zapier cobra por "Zap run" (ejecución). Un pipeline completo de producción de video tiene 15-25 pasos por video. A 30 videos/mes son 450-750 Zap runs adicionales a cualquier otra automatización. El plan Professional de Zapier cuesta $49/mes para 2.000 Zap runs — justo. Pero el plan Team ($69/mes) da solo 50.000 runs y tiene límites que no se comunican bien. Además, Zapier cobra aunque el Zap falle. n8n no tiene este problema.

**Uso válido**: Automatizaciones simples de 1-3 pasos donde no quieres configurar n8n. No para el pipeline central de NOA.

---

### Hootsuite

**Por qué no**: Demasiado caro para el valor que da. El plan Professional cuesta $99/mes. Metricool da funcionalidades equivalentes para el caso de uso de NOA a $22/mes. Hootsuite tiene sentido para agencias con 20+ cuentas. Para NOA, es desperdicio.

---

## Stack Final Recomendado — Presupuesto Detallado

### Stack de Producción (mes 3 en adelante)

```
HERRAMIENTA          PLAN            COSTO/MES   PROPÓSITO
─────────────────────────────────────────────────────────────────
Claude API           Pay-per-use     ~$20        Guiones + scoring
ElevenLabs           Creator         $22         Voz en español
Creatomate           Starter         $29         Ensamblado de video
n8n                  Cloud Starter   $24         Orquestación
  (o VPS self-hosted)                €6          (alternativa)
Airtable             Team            $20         Base de datos / CMS
Metricool            Advanced        $22         Scheduling
Freepik AI           Essentials      $24         Imágenes
─────────────────────────────────────────────────────────────────
TOTAL (con n8n Cloud)                ~$161/mes
TOTAL (con n8n self-hosted)          ~$143/mes
```

### Stack de Validación (meses 1-2)

```
HERRAMIENTA          PLAN            COSTO/MES   NOTA
─────────────────────────────────────────────────────────────────
Claude API           Pay-per-use     ~$8         10-12 guiones/mes
ElevenLabs           Starter         $5          30k chars (8-10 videos)
Creatomate           Free            $0          5 renders gratis (solo pruebas)
  → o Starter        Starter         $29         Si ya produces
n8n                  Free (Railway)  $0          Limitado pero funciona
Airtable             Free            $0          1 base, 1.000 registros
Metricool            Advanced        $22         Sin esto no publicas
DALL-E               Pay-per-use     ~$3         Imágenes básicas
─────────────────────────────────────────────────────────────────
TOTAL MÍNIMO                         ~$38-67/mes
```

**Por qué no bajar más de $38/mes**: Metricool es no-negociable. Sin scheduler, publicas manualmente y pierdes el tiempo que el sistema debería ahorrarte. ElevenLabs es no-negociable porque la voz define si el canal suena profesional o amateur.

---

## Tabla de Fiabilidad del Stack

| Herramienta | Fiabilidad | Mayor riesgo | Mitigation |
|---|---|---|---|
| Claude API | 9/10 | Cambios de precio | Alternativa: GPT-4o |
| ElevenLabs | 9/10 | Cambio de modelo de voz | Exportar voz clonada si la tienes |
| Creatomate | 8/10 | Startup joven | Cuenta backup en Shotstack |
| n8n Cloud | 9/10 | Cambio de precios | Migrar a self-hosted |
| n8n self-hosted | 8/10 | VPS down | UptimeRobot + restart automático |
| Airtable | 9/10 | Subidas de precio | NocoDB como alternativa OSS |
| Metricool | 8/10 | Cambios en APIs de plataformas | Instagram Graph API directa |
| Instagram Graph API | 7/10 | Meta cambia reglas sin aviso | Metricool como buffer |
| Freepik AI | 7/10 | Calidad inconsistente | DALL-E como backup |
| DALL-E | 9/10 | Precio por imagen | Cambiar a Freepik si el volumen sube |
