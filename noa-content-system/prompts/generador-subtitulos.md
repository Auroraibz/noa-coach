# GENERADOR DE SUBTÍTULOS — NOA CONTENT SYSTEM
# Sistema visual de subtítulos para Reels faceless
# Versión 2.0

---

## FILOSOFÍA DE SUBTÍTULOS NOA

Los subtítulos no son transcripción. Son la segunda capa narrativa del vídeo.

El 70% de los Reels se ven sin sonido en algún momento. Los subtítulos son la experiencia para esas personas. Y para las que sí tienen sonido, los subtítulos resaltados amplifican las palabras que importan.

**Regla de oro:** Si el vídeo se entiende completamente viendo solo los subtítulos sin audio, los subtítulos están bien. Si no, están mal.

---

## ESPECIFICACIONES VISUALES NOA

```
Fuente principal:     Montserrat Bold
Fuente secundaria:    Montserrat Regular (subtítulos continuos)
Tamaño subtítulo:     64-72px (móvil 1080px de ancho)
Tamaño destacado:     80-96px (palabras clave grandes)
Color base:           #FFFFFF (blanco puro)
Color highlight:      #E94560 (rojo coral NOA)
Color secundario:     #F5A623 (ámbar — para contraconceptos)
Sombra de texto:      #000000 a 65% opacidad, blur 4px, offset 0,2
Posición estándar:    Centro horizontal, 72-80% desde arriba
Zona segura:          Mínimo 150px del borde superior, 200px del inferior
Máximo caracteres:    40 por línea (2 líneas máximo simultáneas)
Máximo palabras:      6-8 por frame de subtítulo
```

---

## PLANTILLA SRT ESTÁNDAR

```srt
1
00:00:00,000 --> 00:00:02,400
El error que cometen casi todos

2
00:00:02,400 --> 00:00:04,800
los padres de AACC

3
00:00:04,800 --> 00:00:07,200
cuando discuten con su hijo.

4
00:00:07,200 --> 00:00:09,000
Explicáis el razonamiento.

5
00:00:09,000 --> 00:00:11,200
Dais argumentos.

6
00:00:11,200 --> 00:00:13,000
Justificáis la norma.

7
00:00:13,000 --> 00:00:14,500
Pensáis que eso ayuda.

8
00:00:15,100 --> 00:00:16,800
No ayuda.

9
00:00:17,400 --> 00:00:20,000
Un cerebro AACC en confrontación

10
00:00:20,000 --> 00:00:22,000
no procesa argumentos.

11
00:00:22,000 --> 00:00:24,500
Procesa grietas.

12
00:00:25,200 --> 00:00:27,800
No ganas explicando más.

13
00:00:27,800 --> 00:00:30,000
Ganas saliendo de la dinámica.
```

**Reglas de timing SRT:**
- Mínimo 0.8s por segmento (si es más corto, el ojo no lo lee)
- Máximo 3.5s por segmento (si es más largo, rompe el ritmo)
- Frases cortas con impacto: 0.8-1.2s
- Frases de desarrollo: 1.5-2.5s
- Pausa emocional representada como gap entre segmentos (sin subtítulo)

---

## PLANTILLA ASS/SSA CON ESTILO NOA

```ass
[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: NOA_Base,Montserrat,68,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,-1,0,0,0,100,100,0,0,1,0,4,8,60,60,1344,1
Style: NOA_Highlight,Montserrat,80,&H004560E9,&H000000FF,&H00000000,&H99000000,-1,0,0,0,100,100,0,0,1,0,4,8,60,60,1344,1
Style: NOA_Impact,Montserrat,96,&H00FFFFFF,&H000000FF,&H00000000,&H99000000,-1,0,0,0,100,100,0,0,1,0,4,8,60,60,960,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:02.40,NOA_Base,,0,0,0,,El error que cometen casi todos
Dialogue: 0,0:00:02.40,0:00:04.80,NOA_Base,,0,0,0,,los padres de AACC
Dialogue: 0,0:00:07.20,0:00:09.00,NOA_Base,,0,0,0,,Explicáis el razonamiento.
Dialogue: 0,0:00:13.00,0:00:14.50,NOA_Base,,0,0,0,,Pensáis que eso ayuda.
Dialogue: 0,0:00:15.10,0:00:16.80,NOA_Impact,,0,0,0,,NO AYUDA.
Dialogue: 0,0:00:22.00,0:00:24.50,NOA_Highlight,,0,0,0,,Procesa grietas.
Dialogue: 0,0:00:25.20,0:00:27.80,NOA_Base,,0,0,0,,No ganas explicando más.
Dialogue: 0,0:00:27.80,0:00:30.00,NOA_Highlight,,0,0,0,,Ganas saliendo de la dinámica.
```

**Notas ASS:**
- `NOA_Base`: subtítulo estándar, blanco, 68px
- `NOA_Highlight`: palabras clave, rojo coral #E94560, 80px
- `NOA_Impact`: frases de máximo impacto (micro-giro, revelación), blanco, 96px, mayúsculas
- `BackColour: &H99000000` = fondo semitransparente negro al 60% detrás del texto

---

## SISTEMA DE RESALTADO EMOCIONAL

### Categorías de palabras que se resaltan en #E94560

**Palabras de contradicción:**
no, nunca, jamás, al contrario, pero, sin embargo, en realidad, lo que realmente

**Palabras de diagnóstico emocional:**
agotamiento, colapso, explosión, pánico, bloqueo, frustración, rabia, culpa, vergüenza

**Palabras de revelación:**
esto es lo que pasa, la razón real, lo que nadie te dice, el error, la clave

**Frases de validación directa:**
no estás fallando, no eres mala madre, tiene solución, hay una forma

### Palabras que se resaltan en #F5A623 (ámbar)

Palabras de esperanza y solución:
puede mejorar, hay una forma, NOA, herramienta, respuesta, solución, funciona

---

## GENERADOR DE TIMESTAMPS DESDE ELEVENLABS

ElevenLabs puede devolver timestamps a nivel de palabra con la API de timestamps. Usar este snippet para generar SRT automáticamente:

```python
import requests
import json
from dotenv import load_dotenv
import os

load_dotenv()

def generar_srt_desde_elevenlabs(texto: str, voice_id: str, output_path: str) -> str:
    """
    Genera audio + timestamps y crea archivo SRT automáticamente.
    Requiere ElevenLabs plan Creator o superior.
    """
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/with-timestamps"
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": os.getenv("ELEVENLABS_API_KEY")
    }
    payload = {
        "text": texto,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.42,
            "similarity_boost": 0.88,
            "style": 0.28,
            "use_speaker_boost": True
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Guardar audio
    import base64
    audio_path = output_path.replace(".srt", ".mp3")
    with open(audio_path, "wb") as f:
        f.write(base64.b64decode(data["audio_base64"]))

    # Generar SRT desde caracteres con timestamps
    srt = _construir_srt(data["alignment"])
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(srt)

    return output_path


def _construir_srt(alignment: dict) -> str:
    """Agrupa caracteres en segmentos de frase y genera SRT."""
    chars = alignment["characters"]
    starts = alignment["character_start_times_seconds"]
    ends = alignment["character_end_times_seconds"]

    segmentos = []
    actual = ""
    inicio = 0.0

    for i, (char, start, end) in enumerate(zip(chars, starts, ends)):
        actual += char
        # Cortar en puntuación o cada 6-8 palabras
        if char in ".!?,…" or len(actual.split()) >= 7:
            segmentos.append((inicio, end, actual.strip()))
            actual = ""
            if i + 1 < len(starts):
                inicio = starts[i + 1]

    if actual.strip():
        segmentos.append((inicio, ends[-1], actual.strip()))

    # Construir SRT
    lineas = []
    for idx, (t_inicio, t_fin, texto) in enumerate(segmentos, 1):
        lineas.append(str(idx))
        lineas.append(f"{_fmt_srt(t_inicio)} --> {_fmt_srt(t_fin)}")
        lineas.append(texto)
        lineas.append("")

    return "\n".join(lineas)


def _fmt_srt(t: float) -> str:
    h = int(t // 3600)
    m = int((t % 3600) // 60)
    s = int(t % 60)
    ms = int((t % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
```

---

## REGLAS DE SUBTITULADO NOA

1. **Máximo 8 palabras por frame** — Si hay más, el espectador no lee y escucha a la vez.
2. **Las frases cortas con impacto van SOLAS** — "No ayuda." ocupa su propio frame, sin nada más.
3. **Nunca cortar por la mitad un concepto** — "no procesa / argumentos" MAL. "no procesa argumentos" BIEN.
4. **Pausa emocional = frame vacío** — Entre el desarrollo y el micro-giro, 0.4-0.6s sin subtítulo.
5. **El CTA final siempre en NOA_Impact** — Grande, claro, imposible de ignorar.
6. **Nunca subtítulo en los primeros 0.5s** — El hook visual llega antes que el texto.
7. **Sincronización máxima ±0.1s** — Si el subtítulo aparece visiblemente antes o después de la voz, destruye la experiencia.

---

## CHECKLIST DE SUBTÍTULOS

- [ ] Máximo 8 palabras por frame
- [ ] Palabras clave resaltadas en #E94560
- [ ] Frases de impacto en NOA_Impact (grande, mayúsculas si aplica)
- [ ] Sincronización verificada ±0.1s
- [ ] Sin subtítulos en zona de botones (15% inferior en TikTok)
- [ ] El vídeo se entiende completamente sin audio
- [ ] Ningún segmento dura menos de 0.8s
- [ ] Ningún segmento dura más de 3.5s
- [ ] Pausa emocional representada como gap
- [ ] CTA final visible y legible en pantalla de 5 pulgadas
