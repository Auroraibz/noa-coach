# NOA Content System
## Máquina de contenido viral para padres de adolescentes AACC

> Sistema semiautónomo de producción de contenido diario para Instagram Reels, TikTok y YouTube Shorts.

---

## ¿Qué es esto?

Un pipeline completo que va desde **idea → guion → voz → subtítulos → vídeo → publicación → reciclaje**, con intervención humana mínima (30 min/día).

**Output esperado:** 5-7 Reels semanales publicados, cada vídeo reciclado en 8 formatos adicionales.

---

## Inicio rápido

```bash
# 1. Instalar dependencias
cd scripts/
pip install -r requirements.txt

# 2. Configurar credenciales
cp .env.example .env
# → Editar .env con tus API keys

# 3. Inicializar proyecto
python setup_project.py

# 4. Generar primera tanda de ideas
python content_generator.py ideas --count 10

# 5. Revisar ideas en Airtable, aprobar las mejores
# 6. Generar guiones desde ideas aprobadas
python content_generator.py script --idea-id [ID] --format error-tipico
```

---

## Estructura del sistema

```
noa-content-system/
├── README.md                    ← Este archivo
├── docs/
│   ├── arquitectura-del-sistema.md    ← Arquitectura completa + stack
│   ├── flujo-diario.md               ← Qué pasa cada día, hora a hora
│   ├── flujo-semanal.md              ← Calendario operativo semanal
│   ├── herramientas-recomendadas.md  ← Stack honesto con costes
│   └── errores-a-evitar.md           ← Los 40+ errores más comunes
├── prompts/
│   ├── generador-ideas.md            ← Prompt Claude para ideas
│   ├── generador-hooks.md            ← 30 hooks + generador
│   ├── generador-guiones.md          ← 7 plantillas de guion
│   ├── generador-prompts-visuales.md ← Prompts para Runway/Kling/Veo
│   ├── generador-voz.md              ← Config ElevenLabs
│   ├── generador-subtitulos.md       ← SRT/ASS + sistema visual
│   ├── generador-copy-publicacion.md ← Copies Instagram/TikTok
│   └── reciclaje-contenido.md        ← x8 multiplicador de contenido
├── scripts/
│   ├── setup_project.py              ← Setup inicial del proyecto
│   ├── content_generator.py          ← Generador Claude API
│   ├── file_organizer.py             ← Organización y renombrado
│   └── requirements.txt              ← Dependencias Python
├── workflows-n8n/
│   ├── ideas-semanales.json          ← Workflow generación de ideas
│   ├── guiones-desde-ideas.json      ← Workflow generación de guiones
│   ├── voz-subtitulos.json           ← Workflow voz + SRT
│   ├── reciclaje-contenido.json      ← Workflow reciclaje x8
│   └── README-workflows.md           ← Guía de importación n8n
├── templates/
│   ├── calendario-editorial.csv      ← 4 semanas de contenido planificado
│   ├── base-ideas.csv                ← Base de datos de ideas
│   ├── guion-reel.md                 ← Plantilla de guion completa
│   ├── storyboard.md                 ← Plantilla storyboard visual
│   └── checklist-publicacion.md      ← Checklist pre-publicación
├── assets/
│   ├── backgrounds/                  ← Fondos para vídeos
│   ├── music/                        ← Música para Reels
│   ├── fonts/                        ← Tipografías NOA
│   ├── icons/                        ← Iconografía
│   └── overlays/                     ← Overlays y efectos
├── outputs/
│   ├── raw/                          ← Archivos sin editar
│   ├── edited/                       ← Editados pendientes aprobación
│   ├── approved/                     ← Aprobados pendientes publicación
│   └── published/                    ← Publicados
├── calendar/                         ← Calendarios editorials exportados
├── subtitles/                        ← Archivos SRT/ASS
├── voices/                           ← Audio generado con ElevenLabs
├── videos/
│   ├── raw/                          ← Footage B-roll
│   └── final/                        ← Vídeos finales
└── recycled-content/                 ← Contenido reciclado
```

---

## Stack tecnológico (resumen honesto)

| Herramienta | Uso | Veredicto |
|-------------|-----|-----------|
| **Claude API** | Ideas, guiones, hooks, copies | ✅ MANTENER — mejor para contenido emocional |
| **ElevenLabs** | Voz IA española | ✅ MANTENER — único estable para ES-ES emocional |
| **Creatomate** | Ensamblaje de vídeo automatizado | ✅ MANTENER — API real, escalable |
| **n8n** | Orquestación de workflows | ✅ MANTENER — self-hosted, fiable |
| **Airtable** | Base de datos de contenido | ✅ MANTENER — ideal para este volumen |
| **Metricool** | Programación + métricas | ✅ MANTENER — mejor que Buffer para RRSS |
| **Runway/Kling** | B-roll generado por IA | ⚠️ CONDICIONAL — solo para B-roll emocional |
| **CapCut** | Edición | ❌ DROP para automatización — no tiene API |
| **Canva** | Diseño | ❌ DROP para automatización — manual |
| **HeyGen** | Avatar IA | ❌ DROP — mata la estética faceless |
| **Make.com** | Alternativa a n8n | ⚠️ ALTERNATIVA si n8n es complejo |

---

## Convención de nombres de archivos

```
NOA_YYYYMMDD_TEMA_HOOK_ESTADO

Ejemplos:
NOA_20260520_EXPLOSION-EMOCIONAL_NO-ES-RABIA_SCRIPT
NOA_20260521_LIMITES-PANTALLAS_CUANTOS-MINUTOS_VOICE
NOA_20260522_AGOTAMIENTO-PARENTAL_NADIE-LO-ENTIENDE_PUBLISHED
```

**Estados:**
- `IDEA` → `SCRIPT` → `VOICE` → `SUBS` → `VIDEO` → `APPROVED` → `PUBLISHED` → `RECYCLED`

---

## Paleta de colores NOA

```
Principal:   #1A1A2E  (azul noche profundo)
Acento:      #E94560  (rojo coral — emoción, urgencia)
Cálido:      #F5A623  (ámbar — calidez, esperanza)
Neutro:      #F8F8F8  (blanco cálido — limpieza)
Texto:       #FFFFFF  (sobre fondos oscuros)
Highlight:   #E94560  (palabras clave en subtítulos)
```

---

## Tu función como creador (30 min/día)

| Momento | Tarea | Tiempo |
|---------|-------|--------|
| 8:30h | Revisar ideas generadas automáticamente | 5 min |
| 8:35h | Aprobar/rechazar 2-3 ideas | 3 min |
| 8:38h | Revisar guiones de ideas aprobadas ayer | 10 min |
| 8:48h | Aprobar guión o dar feedback rápido | 2 min |
| 8:50h | Revisar vídeo final del día | 8 min |
| 8:58h | Aprobar publicación o solicitar cambios | 2 min |
| **Total** | | **30 min** |

---

## Métricas de éxito

| Métrica | Objetivo semana 1-4 | Objetivo mes 3+ |
|---------|---------------------|-----------------|
| Reels publicados/semana | 5 | 7 |
| Visualizaciones promedio | >2.000 | >10.000 |
| Tasa de guardados | >3% | >5% |
| Tasa de compartidos | >1% | >2% |
| Clics a bio/link | >50/semana | >300/semana |
| Descargas NOA atribuidas | >5/semana | >30/semana |

---

## Cómo empezar hoy

1. **Lee** `docs/arquitectura-del-sistema.md` completo
2. **Configura** las APIs siguiendo `docs/herramientas-recomendadas.md`
3. **Ejecuta** `python scripts/setup_project.py`
4. **Importa** los workflows en tu instancia de n8n
5. **Crea** la base en Airtable siguiendo el esquema en `workflows-n8n/README-workflows.md`
6. **Genera** las primeras 10 ideas y aprueba 3
7. **Produce** el primer vídeo siguiendo `docs/flujo-diario.md`

---

*Sistema diseñado para producir contenido que haga pensar a una madre: "Esto es EXACTAMENTE lo que pasa en mi casa."*
