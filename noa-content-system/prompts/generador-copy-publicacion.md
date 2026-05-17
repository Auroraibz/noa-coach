# GENERADOR DE COPY DE PUBLICACIÓN — NOA CONTENT SYSTEM
# System Prompt Claude API + Plantillas Instagram y TikTok
# Versión 2.0

---

## SYSTEM PROMPT (listo para Claude API)

```
Eres el copywriter de NOA, una app para padres de adolescentes con AACC. Escribes captions para Instagram Reels y TikTok que generan guardados, comentarios y clics al link de descarga.

CONTEXTO:
- Audiencia: madres principalmente (80%), España, 35-50 años
- Idioma: español de España (vosotros, no ustedes)
- Tono: directo, emocional, adulto, sin motivación vacía
- Objetivo del caption: ampliar lo que el vídeo no puede decir + generar conversación

REGLAS ABSOLUTAS DEL CAPTION:
1. Las primeras 2 líneas son lo que aparece sin expandir. Deben ser irresistibles.
2. El caption NO repite el vídeo. Amplía, añade contexto, o hace una pregunta que genera comentarios.
3. Máximo 1 CTA claro. No 3.
4. Sin hashtags en el cuerpo del texto. Los hashtags van al final o en el primer comentario.
5. Sin emojis decorativos. Solo si refuerzan el mensaje (máximo 3-5 en todo el caption).
6. Las preguntas que generan comentarios son las que tienen respuesta de 2-3 palabras ("¿te ha pasado esto? / ¿cuántas veces a la semana?").
7. El primer comentario contiene hashtags adicionales + pregunta de engagement alternativa.

FORMATO DE SALIDA:
{
  "plataforma": "instagram|tiktok",
  "version": "larga|media|corta",
  "caption": "texto completo",
  "primer_comentario": "hashtags + texto adicional",
  "hashtags_principales": ["lista"],
  "cta_tipo": "guardar|comentar|link_bio|compartir"
}
```

---

## PLANTILLAS INSTAGRAM — 3 VERSIONES POR VÍDEO

### Versión LARGA (150-250 palabras)

```
[HOOK — primeras 2 líneas, no más de 120 caracteres]
[HOOK continúa o segunda frase de impacto]

[DESARROLLO — 2-3 párrafos breves]
[Párrafo 1: amplía el conflicto del vídeo con un ejemplo diferente]
[Párrafo 2: añade contexto que el vídeo no pudo dar en 30s]
[Párrafo 3: conecta con la experiencia emocional de la madre]

[PREGUNTA DE ENGAGEMENT]
[Una sola pregunta concreta con respuesta de 2-3 palabras]

[CTA]
[Un solo CTA. Directo. Sin rodeos.]

[HASHTAGS — al final, sin espacio antes]
```

**Ejemplo real — vídeo sobre argumentar con hijo AACC:**
```
Cuanto más razonáis con él, más grietas encuentra en vuestros argumentos.

Y no es que sea mala persona. Es que tiene un cerebro que procesa a otra velocidad.

El problema no es que seáis malos argumentadores. Es que en ese momento, la discusión ya no es sobre lo que empezó siendo. Es sobre quién tiene razón. Y eso no tiene solución lógica.

Lo que funciona no es un argumento mejor. Es salir de la dinámica antes de que escale.

¿Cuántas veces a la semana acabáis discutiendo por algo que empezó siendo trivial?

Guarda este vídeo para cuando llegue la próxima.

#AACC #AltasCapacidades #MadresAACC #AdolescentesAACC #AppNOA #CriarHijos #InteligenciaEmocional
```

---

### Versión MEDIA (80-120 palabras)

```
[HOOK — 2 líneas]

[DESARROLLO — 1-2 párrafos]

[PREGUNTA O CTA]

[HASHTAGS]
```

**Ejemplo:**
```
Cuanto más le explicáis el porqué de las normas, más argumentos os devuelve.

No es rebeldía. Es un cerebro que no puede no procesar.

La solución no es argumentar mejor. Es cambiar completamente el tipo de conversación.

¿Te ha pasado esto hoy?

Link en bio para descargar NOA gratis.
```

---

### Versión CORTA (30-60 palabras)

Para stories, para vídeos virales donde el caption no importa, o para pruebas A/B.

```
[HOOK de 1 línea]
[1 frase de desarrollo]
[CTA directo]
```

**Ejemplo:**
```
No ganas la discusión con tu hijo AACC explicando más.

Ganas saliendo de la dinámica antes de que escale.

NOA te dice cómo. Gratis. Link en bio.
```

---

## PLANTILLAS TIKTOK

TikTok es diferente. El caption compite menos (la mayoría no lo lee). Pero los primeros 50 caracteres aparecen bajo el vídeo y sí generan interacción.

### Caption TikTok estándar

```
[FRASE IMPACTO — máximo 50 caracteres]
[1-2 frases adicionales de contexto]
[Pregunta directa o CTA]
#AACC #altascapacidades #hijosAACC #NOAapp
```

**Ejemplo:**
```
Esto pasa en el 80% de familias AACC 👇

Cuanto más razonáis, más argumentos os devuelve. No es rebeldía. Es cómo funciona su cerebro.

¿Te suena?

#AACC #altascapacidades #hijosAACC #crianza #adolescentes
```

---

## ESTRATEGIA DE HASHTAGS

### Set permanente (usar siempre — 5 hashtags de marca)
```
#AppNOA
#NOAparents
#AACC
#AltasCapacidades
#HijosAACC
```

### Set de nicho (rotar — usar 8-10 por publicación)
```
#MadresAACC
#PadresAACC
#AdolescentesAACC
#AlumnosAACC
#SuperdotadosEspaña
#InteligenciaEmocionalFamiliar
#CriarHijos
#CrianzaConsciente
#RegulacionEmocional
#ConflictosFamiliares
#AsincroniaEmocional
#NecesidadesEspeciales
#EducacionEmocional
#PsicologiaFamiliar
#VidaConHijos
```

### Set de conversación (añadir 3-5 por publicación)
```
#Maternidad
#Paternidad
#FamiliaEspañola
#MamasInstagram
#CriarAdolescentes
#VidaFamiliar
#HijosDificiles
#AgotamientoParental
```

### Hashtags a EVITAR
- Cualquier hashtag con más de 50M publicaciones (demasiado genérico, pierde en el ruido)
- #Motivación #Inspiración #Coaching (te asocia con el contenido de gurú que queremos evitar)
- #Psicología #Terapia (te asocia con contenido médico/clínico)

---

## VARIACIONES DE CTA

### Para vídeos TOFU (conciencia)
```
"Guarda este vídeo para la próxima vez."
"¿Cuántas veces te ha pasado esto esta semana? Comenta el número."
"Guarda si te ha resonado."
```

### Para vídeos MOFU (consideración)
```
"NOA tiene el protocolo completo para este momento. Link en bio."
"Si quieres la respuesta exacta que funciona, está en NOA. Gratis."
"En NOA tienes esto desarrollado con 40 situaciones más. Link en bio."
```

### Para vídeos BOFU (conversión)
```
"Descarga NOA ahora. Gratis. Está en el link de bio."
"Lleva NOA en el bolsillo. Es gratis. Link en bio."
"La próxima vez que llegue ese momento, abre NOA. Gratis. Link en bio."
```

---

## PRIMER COMENTARIO (publicar inmediatamente después)

El primer comentario tiene dos funciones:
1. Hashtags adicionales que no cabrían en el caption
2. Pregunta alternativa para activar el engagement

**Plantilla:**
```
¿Reconocéis este patrón en casa? 👇

#hijosinteligentes #sobredotados #gifted #giftedkids #altascapacidades #MadresEspañolas #PadresEspañoles #EducacionHijos #FamiliaConValores #ConvivenciaFamiliar #CrisisAdolescente #ComunicacionFamiliar #habilidadessociales #emocionesinfantiles #niñossensibles
```

---

## CHECKLIST DE COPY ANTES DE PUBLICAR

- [ ] Las primeras 2 líneas funcionan solas como anzuelo
- [ ] El caption NO repite el vídeo — amplía o pregunta algo diferente
- [ ] Un solo CTA claro
- [ ] Sin hashtags en el cuerpo del texto
- [ ] Pregunta de engagement tiene respuesta corta (2-3 palabras)
- [ ] Set de hashtags rotados (no los mismos que el último vídeo)
- [ ] Primer comentario preparado para pegar inmediatamente
- [ ] Tono: español de España (vosotros)
- [ ] Sin motivación vacía ni lenguaje de gurú
