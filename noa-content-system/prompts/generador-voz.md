# GENERADOR DE VOZ IA — NOA CONTENT SYSTEM
# Configuración ElevenLabs para voz femenina española emocional
# Versión 2.0

---

## FILOSOFÍA DE VOZ NOA

La voz de NOA no es una locutora. No es una psicóloga. No es una presentadora.

Es la amiga que sabe más que tú sobre esto, te habla sin filtro y sin juzgarte, y cuando dice algo importante hace una pausa de verdad.

**Tres palabras que definen la voz:** Cálida. Directa. Con peso.

---

## CONFIGURACIÓN ELEVENLABS

### Voz recomendada
```
Idioma: Spanish (Spain) es-ES
Género: Femenino
Perfil: Warm, confident, mid-30s
```

> **Honestidad:** En 2026, ElevenLabs no tiene una voz femenina española perfecta de fábrica para este tono. La mejor opción es clonar una voz real con 3-5 minutos de audio. Si no tienes acceso a una locutora, usar la voz más cercana disponible con los parámetros ajustados abajo.

---

### Parámetros de API

```json
{
  "voice_settings": {
    "stability": 0.42,
    "similarity_boost": 0.88,
    "style": 0.28,
    "use_speaker_boost": true
  },
  "model_id": "eleven_multilingual_v2",
  "output_format": "mp3_44100_128"
}
```

**Por qué estos valores:**
- `stability 0.42` — Ligeramente bajo para variación natural. Por encima de 0.55 suena robótico.
- `similarity_boost 0.88` — Alto para preservar el timbre entre vídeos.
- `style 0.28` — Moderado. Por encima de 0.45 se vuelve teatral.
- `eleven_multilingual_v2` — Mejor modelo para español de España. No usar v1 (solo inglés).

---

## LLAMADA API PYTHON

```python
import os
import requests
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")


def generar_voz_noa(texto: str, nombre_archivo: str, carpeta_salida: str = "voices/") -> str:
    """Genera audio para NOA. Retorna la ruta del archivo generado."""
    if len(texto) > 500:
        segmentos = _dividir_texto(texto)
        audios = [generar_voz_noa(seg, f"{nombre_archivo}_seg{i}", carpeta_salida)
                  for i, seg in enumerate(segmentos)]
        return _concatenar_audios(audios, nombre_archivo, carpeta_salida)

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICE_ID}"
    headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ELEVENLABS_API_KEY
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

    Path(carpeta_salida).mkdir(parents=True, exist_ok=True)
    ruta = f"{carpeta_salida}{nombre_archivo}.mp3"
    with open(ruta, "wb") as f:
        f.write(response.content)
    return ruta


def _dividir_texto(texto: str, max_chars: int = 480) -> list[str]:
    frases = texto.split(". ")
    segmentos, actual = [], ""
    for frase in frases:
        if len(actual) + len(frase) + 2 <= max_chars:
            actual += frase + ". "
        else:
            if actual:
                segmentos.append(actual.strip())
            actual = frase + ". "
    if actual:
        segmentos.append(actual.strip())
    return segmentos


def _concatenar_audios(rutas: list[str], nombre_final: str, carpeta: str) -> str:
    import subprocess
    lista_path = f"{carpeta}_lista_temp.txt"
    with open(lista_path, "w") as f:
        f.write("\n".join([f"file '{r}'" for r in rutas]))
    salida = f"{carpeta}{nombre_final}.mp3"
    subprocess.run(
        ["ffmpeg", "-f", "concat", "-safe", "0", "-i", lista_path, "-c", "copy", salida, "-y"],
        check=True, capture_output=True
    )
    for r in rutas:
        Path(r).unlink(missing_ok=True)
    Path(lista_path).unlink(missing_ok=True)
    return salida
```

---

## PROCESADO DE AUDIO POST-GENERACIÓN

```bash
# Normalización estándar streaming (-14 LUFS)
ffmpeg -i input.mp3 -af loudnorm=I=-14:LRA=11:TP=-1.5 output_final.mp3

# Si hay ruido de fondo
ffmpeg -i input.mp3 -af "afftdn=nf=-25,loudnorm=I=-14:LRA=11:TP=-1.5" output_final.mp3
```

---

## DIRECCIÓN DE VOZ POR SECCIÓN

### Hook (0-3s)
- Energía media-alta. Velocidad ligeramente sobre la media.
- Sin pausa al inicio. El hook interrumpe, no presenta.
- Primera sílaba de la frase más marcada.

### Desarrollo (3-25s)
- Ritmo conversacional. Pausas de 0.3-0.4s entre ideas distintas.
- Bajar 10% velocidad en ejemplos concretos.
- Subir 5% en enumeraciones.

### Micro-giro (25-35s)
- Pausa antes de la frase clave: 0.5-0.6s.
- Voz más suave, velocidad 90%.
- La frase más importante se dice más despacio, no más fuerte.

### CTA (últimos 5s)
- Energía hacia arriba sin gritar. Presencia, no volumen.
- "Gratis" siempre con énfasis natural.
- Última palabra con entonación descendente (seguridad, no pregunta).

---

## SSML PARA CONTROL EMOCIONAL

```xml
<!-- Pausa emocional -->
<speak>
  No estás fallando como madre.
  <break time="600ms"/>
  Solo nadie te dio las herramientas para esto.
</speak>

<!-- Énfasis en palabra clave -->
<speak>
  Es <emphasis level="strong">agotamiento</emphasis> disfrazado de discusión.
</speak>

<!-- Ritmo más lento en micro-giro -->
<speak>
  <prosody rate="90%">
    Hay una forma de hacerlo sin parecer que te rindes.
  </prosody>
</speak>
```

---

## ERRORES COMUNES Y SOLUCIONES

| Error | Causa | Solución |
|-------|-------|----------|
| "AACC" pronunciado como siglas en inglés | ElevenLabs no conoce la sigla | Escribir "a, a, ce, ce" o "altas capacidades" |
| Voz sube en preguntas retóricas | Entonación española vs latina | Añadir punto al final para forzar bajada |
| Pausa larga entre párrafos | Salto de línea interpretado como pausa | Unir párrafos, usar "..." para pausas breves |
| "NOA" con énfasis raro | Sílaba corta y desconocida | Escribir "Noa" (minúscula) en el texto |
| Ritmo uniforme en listas | Sin variación prosódica | Punto y aparte entre cada elemento |

---

## SISTEMA DE NOMBRES

```
Formato:   NOA_YYYYMMDD_TEMA_VOICE_vX.mp3
Carpeta:   /voices/YYYY-WXX/

Ejemplo:   NOA_20260520_ERROR-TIPICO_VOICE_v1.mp3
```

---

## CHECKLIST ANTES DE APROBAR AUDIO

- [ ] Suena natural escuchándolo sin leer el guion
- [ ] Las pausas emocionales están en su sitio
- [ ] El CTA tiene energía hacia arriba
- [ ] "NOA" y "AACC" se pronuncian correctamente
- [ ] Sin artefactos ni clicks audibles
- [ ] Normalizado a -14 LUFS
- [ ] Duración: entre 18 y 50 segundos
- [ ] Archivo en `/voices/` con naming correcto
