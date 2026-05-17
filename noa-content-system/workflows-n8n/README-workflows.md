# GUÍA DE WORKFLOWS N8N — NOA CONTENT SYSTEM
# Importación, configuración y operación de los 4 workflows

---

## RESUMEN DE WORKFLOWS

| Workflow | Trigger | Frecuencia | Propósito |
|---------|---------|------------|-----------|
| `ideas-semanales.json` | Lunes 8:00 AM | Semanal | Genera 10 ideas nuevas y las guarda en Airtable |
| `guiones-desde-ideas.json` | Airtable trigger | Al aprobar una idea | Genera 3 variaciones de guion para la idea aprobada |
| `voz-subtitulos.json` | Airtable trigger | Al aprobar un guion | Genera audio ElevenLabs + archivo SRT |
| `reciclaje-contenido.json` | Airtable trigger | Al marcar recycle_flag | Genera 8 formatos reciclados del vídeo publicado |

---

## REQUISITOS PREVIOS

### 1. Instancia n8n
- n8n versión 1.30+ (self-hosted recomendado)
- Acceso a internet para llamadas a APIs externas
- Mínimo 1GB RAM disponible para la instancia

**Opciones de instalación:**
```bash
# Docker (recomendado)
docker run -d --name n8n -p 5678:5678 \
  -e N8N_BASIC_AUTH_ACTIVE=true \
  -e N8N_BASIC_AUTH_USER=admin \
  -e N8N_BASIC_AUTH_PASSWORD=tupassword \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# npm
npm install -g n8n && n8n start
```

### 2. Variables de entorno en n8n
Añadir en Settings → Variables de entorno de n8n (NO hardcodear en los workflows):

```
ANTHROPIC_API_KEY=sk-ant-...
ELEVENLABS_API_KEY=...
ELEVENLABS_VOICE_ID=...
AIRTABLE_API_KEY=pat...
AIRTABLE_BASE_ID=app...
GOOGLE_DRIVE_FOLDER_ID=1A2B...
SLACK_WEBHOOK_URL=https://hooks.slack.com/...
```

### 3. Credenciales en n8n
Crear en n8n → Settings → Credentials:

- **Anthropic API**: tipo "HTTP Header Auth", header name: `x-api-key`, valor: `{{ $env.ANTHROPIC_API_KEY }}`
- **Airtable**: tipo "Airtable Token API", token: `{{ $env.AIRTABLE_API_KEY }}`
- **ElevenLabs**: tipo "HTTP Header Auth", header name: `xi-api-key`, valor: `{{ $env.ELEVENLABS_API_KEY }}`

---

## ESTRUCTURA AIRTABLE REQUERIDA

### Base: `NOA_Content_System`

#### Tabla: `Ideas`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | Auto Number | ID interno Airtable |
| titulo_interno | Single line text | Nombre del vídeo |
| hook_v1 | Long text | Hook versión 1 |
| hook_v2 | Long text | Hook versión 2 |
| hook_v3 | Long text | Hook versión 3 |
| angulo_emocional | Single line text | Ej: agotamiento parental |
| problema_principal | Long text | Descripción del conflicto |
| emocion_dominante | Single line text | Ej: frustración |
| etapa_funnel | Single select | TOFU / MOFU / BOFU |
| cta_recomendado | Long text | Texto del CTA |
| formato_visual | Single select | lista / historia / contraste / 3-señales |
| duracion_estimada | Number | Segundos |
| palabras_clave | Long text | Keywords separadas por coma |
| estado | Single select | IDEA / SCRIPT / VOICE / SUBS / VIDEO / APPROVED / PUBLISHED / RECYCLED |
| prioridad | Single select | ALTA / MEDIA / BAJA |
| semana_publicacion | Single line text | Ej: S21 |
| notas | Long text | Notas adicionales |
| veces_reciclado | Number | Default 0 |
| recycle_flag | Checkbox | Activar para disparar workflow de reciclaje |
| fecha_creacion | Date | Auto |

#### Tabla: `Guiones`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_guion | Auto Number | |
| idea_relacionada | Link to Ideas | |
| formato | Single select | error-tipico / mini-historia / 3-señales / etc |
| hook | Long text | Hook final del guion |
| guion_completo | Long text | Texto completo con marcas de dirección |
| notas_visuales | Long text | |
| notas_voz | Long text | |
| cta | Long text | |
| duracion_estimada | Number | |
| estado | Single select | DRAFT / APPROVED / REJECTED |
| version | Number | Default 1 |

#### Tabla: `Produccion`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id_produccion | Auto Number | |
| guion_relacionado | Link to Guiones | |
| url_audio_gdrive | URL | Link al MP3 en Drive |
| url_srt_gdrive | URL | Link al SRT en Drive |
| url_video_final | URL | Link al MP4 final |
| estado | Single select | VOICE / SUBS / VIDEO / APPROVED / PUBLISHED |
| fecha_publicacion | Date | |
| plataforma | Multiple select | Instagram / TikTok / YouTube |
| metricas_24h | Long text | JSON con métricas |
| recycle_flag | Checkbox | |

#### Tabla: `Reciclados`
| Campo | Tipo | Descripción |
|-------|------|-------------|
| produccion_origen | Link to Produccion | |
| formato_reciclaje | Single select | hook / guion / carrusel / email / story / post / ad / faq |
| contenido | Long text | El contenido generado |
| estado | Single select | DRAFT / APPROVED / PUBLISHED |

---

## IMPORTAR WORKFLOWS

### Método 1: Interfaz n8n (recomendado)
1. Abrir n8n en el navegador (`http://localhost:5678`)
2. Click en el botón "+" para crear nuevo workflow
3. Click en "..." (tres puntos) → "Import from file"
4. Seleccionar el archivo JSON correspondiente
5. Guardar y activar

### Método 2: API n8n
```bash
curl -X POST http://localhost:5678/api/v1/workflows \
  -H "Content-Type: application/json" \
  -H "X-N8N-API-KEY: tu_api_key" \
  -d @workflows-n8n/ideas-semanales.json
```

### Orden de importación recomendado
1. `ideas-semanales.json` — Base del pipeline
2. `guiones-desde-ideas.json` — Depende de Ideas en Airtable
3. `voz-subtitulos.json` — Depende de Guiones en Airtable
4. `reciclaje-contenido.json` — Depende de Produccion en Airtable

---

## TESTING DE CADA WORKFLOW

### ideas-semanales.json
```bash
# Test manual: activar trigger manualmente en n8n
# 1. Abrir el workflow en n8n
# 2. Click "Test workflow" (el botón de play)
# 3. Verificar que se crean 10 registros en Airtable tabla Ideas
# 4. Verificar que llega notificación Slack

# Resultado esperado:
# ✓ 10 registros nuevos en Airtable con estado IDEA
# ✓ Notificación Slack con resumen
# ✓ Tiempo de ejecución < 30 segundos
```

### guiones-desde-ideas.json
```bash
# Trigger: cambiar estado de cualquier Idea a "APPROVED" en Airtable
# Resultado esperado:
# ✓ 3 registros nuevos en tabla Guiones con estado DRAFT
# ✓ Estado de la Idea cambia a "SCRIPT"
# ✓ Notificación con los 3 guiones para revisión
```

### voz-subtitulos.json
```bash
# Trigger: cambiar estado de cualquier Guion a "APPROVED" en Airtable
# Resultado esperado:
# ✓ Archivo MP3 generado y subido a Google Drive
# ✓ Archivo SRT generado y subido a Google Drive
# ✓ URLs guardadas en Airtable tabla Produccion
# ✓ Estado del Guion cambia a "VOICE"
# Tiempo esperado: 45-90 segundos (ElevenLabs + Drive upload)
```

### reciclaje-contenido.json
```bash
# Trigger: marcar recycle_flag = true en cualquier registro de Produccion
# Resultado esperado:
# ✓ 8+ registros en tabla Reciclados con estado DRAFT
# ✓ 3 nuevas Ideas en tabla Ideas
# ✓ Campo veces_reciclado incrementado en el registro original
# ✓ Notificación con resumen del reciclaje
```

---

## ERRORES COMUNES Y SOLUCIONES

### Error: "Airtable: Field cannot be found"
**Causa:** El nombre del campo en el workflow no coincide con el de Airtable.
**Solución:** Verificar nombres exactos de campos en Airtable (case-sensitive). Actualizar el nodo Airtable en n8n.

### Error: "Claude API: 429 Too Many Requests"
**Causa:** Rate limit de la API de Anthropic.
**Solución:** Añadir nodo Wait de 2 segundos entre llamadas consecutivas a Claude. En el workflow de ideas, usar batch de 5 en vez de 10.

### Error: "ElevenLabs: 422 Unprocessable Entity"
**Causa:** El texto supera los 2500 caracteres por petición o contiene caracteres no soportados.
**Solución:** El script `content_generator.py` divide automáticamente. Si el error es desde n8n, añadir un nodo Code antes de la llamada a ElevenLabs para dividir el texto.

### Error: "Google Drive: insufficient permissions"
**Causa:** El Service Account no tiene acceso a la carpeta especificada.
**Solución:** Compartir la carpeta de Drive con el email del Service Account (visible en el JSON de credenciales).

### El workflow de Airtable trigger no dispara
**Causa:** Los triggers de Airtable en n8n requieren polling (no webhooks nativos). El intervalo por defecto es 1 minuto.
**Solución:** En el nodo Airtable Trigger, ajustar el polling interval a 1 minuto. Para tests instantáneos, usar "Test workflow" manual.

---

## COSTES ESTIMADOS POR EJECUCIÓN

| Workflow | Claude API | ElevenLabs | Drive | Total/ejecución |
|---------|-----------|------------|-------|-----------------|
| ideas-semanales | ~$0.05 | — | — | ~$0.05 |
| guiones-desde-ideas | ~$0.08 | — | — | ~$0.08 |
| voz-subtitulos | — | ~$0.15 | <$0.01 | ~$0.16 |
| reciclaje-contenido | ~$0.12 | — | — | ~$0.12 |

**Coste semanal estimado (5 vídeos):**
- Ideas: $0.05 × 1 = $0.05/semana
- Guiones: $0.08 × 5 = $0.40/semana
- Voz: $0.16 × 5 = $0.80/semana
- Reciclaje: $0.12 × 3 = $0.36/semana (solo los que superan umbrales)
- **Total: ~$1.61/semana = ~$7/mes**

---

## ESCALABILIDAD

El sistema actual está optimizado para 5-7 vídeos semanales. Para escalar a 14+ vídeos:

1. **Claude API:** Migrar a `claude-opus-4-7` para guiones más complejos, mantener `claude-haiku-4-5` para ideas.
2. **ElevenLabs:** Si >20 vídeos/mes, considerar plan Business para mayor quota.
3. **n8n:** Si el servidor se satura, separar workflows en instancias diferentes o usar n8n Cloud.
4. **Airtable:** Hasta 50.000 registros con el plan Pro. Más que suficiente para 2+ años de contenido.

---

## MONITORIZACIÓN

Revisar cada lunes:
- [ ] Logs de n8n: Settings → Executions → Filtrar por "Error"
- [ ] Uso de APIs: Anthropic Console, ElevenLabs Dashboard
- [ ] Espacio en Google Drive
- [ ] Créditos Airtable (si es plan gratuito)
- [ ] Webhook de Slack recibiendo notificaciones correctamente
