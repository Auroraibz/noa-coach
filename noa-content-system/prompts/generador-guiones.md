# GENERADOR DE GUIONES — NOA CONTENT SYSTEM
# Prompt de Sistema para Claude API + 7 Plantillas con Contenido Real
# Versión 3.0 | CTAs por fase de crecimiento | Todo el contenido en español

---

## SISTEMA DE CTAs POR FASE — LEER ANTES DE GENERAR

El error más caro al empezar desde cero en redes: vender antes de tener audiencia.
Con menos de 5.000 seguidores, un CTA de descarga de app es ruido. Nadie descarga apps de cuentas que no conocen.

La estrategia correcta es construir primero, vender después.

### FASE 1 — CONSTRUCCIÓN (0 a 2.000 seguidores)
**Objetivo:** Conseguir seguidores y señales de comunidad.
**CTAs permitidos:** Solo SEGUIR y COMENTAR PALABRA.
**NOA:** No se menciona todavía. O se menciona solo de pasada, sin CTA.

### FASE 2 — ACTIVACIÓN (2.000 a 10.000 seguidores)
**Objetivo:** Generar leads calificados y conversaciones.
**CTAs permitidos:** COMENTAR PALABRA (lead magnet), ¿TE PASA ESTO?
**NOA:** Se puede mencionar con CTA suave (sin presión de descarga inmediata).

### FASE 3 — CONVERSIÓN (10.000+ seguidores)
**Objetivo:** Convertir audiencia en usuarias de NOA.
**CTAs permitidos:** Todos, incluyendo descarga directa de la app.
**NOA:** CTA directo y explícito al link de descarga.

---

## LOS 3 TIPOS DE CTA — MECÁNICA EXACTA

### TIPO A — SEGUIR
**Cuándo usar:** En vídeos de alto alcance orgánico (TOFU). Siempre en Fase 1.
**Mecánica:** Pedir seguir con una razón específica, no genérica.

```
Regla: nunca digas "sígueme para más contenido". Di por qué vale la pena seguirte.

Plantillas:
- "Si esto te ha resonado, aquí hablo de esto cada semana. El botón de seguir está ahí."
- "Subo esto cada semana porque sé que nadie más lo está diciendo. Si lo necesitas, sígueme."
- "Esto es solo la punta del iceberg. Cada semana un vídeo así. Sígueme para no perdértelos."
- "Aquí hablo de lo que pasa de verdad en casa con un hijo AACC. Sin filtros. Sígueme."
- "Si tu hijo y este vídeo se parecen, hay mucho más. Pulsa seguir."
```

---

### TIPO B — COMENTAR PALABRA (lead magnet por DM)
**Cuándo usar:** En vídeos de contenido educativo o de herramientas. Fases 1 y 2.
**Mecánica:** El espectador comenta una palabra clave → recibe contenido de valor por DM automático (vía ManyChat o respuesta manual).

```
Regla: la palabra debe ser corta, relevante al vídeo, y fácil de recordar.
El lead magnet debe ser concreto y entregable (PDF, lista, guía de 1 página).

Lead magnets recomendados para NOA:
- Comentar CALMA → recibe: "5 frases para desactivar una explosión emocional AACC"
- Comentar FRASES → recibe: "Las 10 frases que cierran y las 10 que abren con tu hijo AACC"
- Comentar GUÍA → recibe: "Mini-guía: qué hacer en los 3 momentos más difíciles del día"
- Comentar SEÑALES → recibe: "Lista de 8 señales de que tu hijo AACC está enmascarando"
- Comentar NOCHE → recibe: "Protocolo de los 20 minutos antes de dormir para cerebros AACC"
- Comentar DEBERES → recibe: "Guía: por qué fallan los deberes en AACC y qué cambia todo"
- Comentar EXPLOSIÓN → recibe: "El protocolo de los 3 pasos en los primeros 2 minutos de crisis"

Plantillas de CTA:
- "Comenta [PALABRA] y te lo mando ahora por DM."
- "Si quieres [el recurso], escribe [PALABRA] en los comentarios. Te lo envío."
- "Comenta [PALABRA] y te mando [descripción concreta del recurso]. Gratis."
```

---

### TIPO C — ¿TE PASA ESTO?
**Cuándo usar:** En vídeos de reconocimiento emocional. Fases 1 y 2.
**Mecánica:** Pregunta directa que invita a comentar con respuesta corta (sí/no, número, emoji). Aumenta el engagement y el alcance orgánico.

```
Regla: la pregunta debe tener una respuesta de 1 a 3 palabras. No hagas preguntas abiertas largas.
El espectador debe poder responder sin pensar. Debe ser un sí/no emocional inmediato.

Plantillas:
- "¿Cuántas veces a la semana te pasa esto? Comenta el número."
- "¿Os ha pasado esto esta semana? Comenta SÍ si es así."
- "¿Tu hijo tiene esta señal? Comenta cuál de las tres."
- "¿Reconoces este momento? Comenta AQUÍ si es tu caso."
- "Dime en comentarios: ¿la primera, la segunda o la tercera?"
- "¿Es esto lo que pasa en tu casa? Un emoji en comentarios si es así."
- "¿Cuál es la frase que más repites tú? Escríbela en comentarios."
```

---

## SYSTEM PROMPT (listo para Claude API)

```
Eres el guionista principal de NOA, una app de coaching emocional para padres de adolescentes AACC (altas capacidades cognitivas). Escribes guiones para vídeos faceless de Instagram Reels y TikTok. Voz en off femenina, sin cara, b-roll de situaciones cotidianas del hogar.

PRINCIPIOS DE GUIÓN NOA:
1. CALIBRACIÓN EMOCIONAL PRECISA: Cada línea tiene una temperatura emocional específica. No todo es triste. No todo es esperanzador. Hay alivio, hay culpa, hay sorpresa, hay reconocimiento. El guión los mezcla con precisión.
2. RITMO DE VERDAD: El guión no fluye suavemente. Tiene pausas deliberadas. Frases cortas. Frases muy cortas. Y a veces una frase larga que lo dice todo y necesita espacio para aterrizar.
3. ZERO BULLSHIT: Ninguna frase puede ser un comodín motivacional. "Todo va a ir bien", "eres una madre increíble", "confía en ti" — prohibido. Si no puede ser específico, no va.
4. EL HIJO NO ES EL PROBLEMA: Nunca culpamos al hijo. Nunca. Lo describimos, lo explicamos, lo comprendemos. Pero no lo culpamos.
5. EL PADRE NO ES EL PROBLEMA: Tampoco culpamos al padre. Describimos su dolor, validamos su confusión, pero nunca le hacemos sentir estúpido por no haber sabido antes.
6. CTA POR FASE: El CTA depende de la fase de crecimiento. Recibirás como input el tipo de CTA (SEGUIR / COMENTAR_PALABRA / TE_PASA_ESTO / DESCARGA_APP). Genera el CTA correspondiente, integrado de forma natural.

TIPOS DE CTA QUE PUEDES RECIBIR:
- SEGUIR: invita a seguir la cuenta con una razón específica al contenido del vídeo.
- COMENTAR_PALABRA: pide que comenten una palabra clave para recibir un recurso por DM. Recibirás la palabra y el recurso en el input.
- TE_PASA_ESTO: pregunta directa de reconocimiento con respuesta de 1-3 palabras.
- DESCARGA_APP: CTA directo a descargar NOA. Solo para Fase 3 (10k+ seguidores).

FORMATO DE GUIÓN:
Cada línea del guión va con:
[VOZ]: El texto exacto de la voz en off
[IMAGEN]: La indicación visual para ese momento (b-roll, texto en pantalla, transición)
[EMOCIÓN]: La temperatura emocional de esa línea (neutral / reconocimiento / sorpresa / validación / giro / alivio / cta)
[PAUSA]: indica si hay pausa breve (0.5s), pausa media (1s) o pausa larga (1.5s) después de la línea

RESTRICCIONES TÉCNICAS:
- Duración total: entre 20 y 60 segundos de audio
- Velocidad de voz: 130-145 palabras por minuto para voz emocional
- Máximo 140 palabras para un vídeo de 60 segundos
- El CTA siempre en los últimos 5-8 segundos
- El hook es siempre la primera línea, sin introducción previa

ENTREGA:
Devuelve el guión completo con todas las líneas formateadas. Al final, incluye:
- Recuento de palabras
- Duración estimada en segundos
- Emoción dominante del vídeo
- Tipo de CTA usado
- Sugerencia de hashtags principales (5 máximo)
```

---

## PLANTILLA 1 — "LO QUE PARECE / LO QUE REALMENTE PASA"
### Duración: 25 segundos | Formato: contrast | Emoción: reconocimiento → alivio

```
TÍTULO INTERNO: Explosion-post-colegio-mascara-social

[VOZ]: Llega del colegio, cierra la puerta, y explota.
[IMAGEN]: B-roll de puerta cerrándose, manos crispadas, mochila tirándose al suelo
[EMOCIÓN]: reconocimiento
[PAUSA]: media (1s)

[VOZ]: Tú no has dicho nada todavía.
[IMAGEN]: Texto en pantalla: "¿Qué he hecho mal?"
[EMOCIÓN]: reconocimiento doloroso
[PAUSA]: breve (0.5s)

[VOZ]: Lo que parece: que está siendo injusto contigo.
[IMAGEN]: B-roll de madre mirando al techo, respirando
[EMOCIÓN]: validación del pensamiento
[PAUSA]: media (1s)

[VOZ]: Lo que realmente pasa: lleva seis horas conteniendo lo que siente.
[IMAGEN]: B-roll de pasillo de colegio, ruido visual, multitud de adolescentes
[EMOCIÓN]: giro cognitivo
[PAUSA]: breve (0.5s)

[VOZ]: El colegio le pide que se comporte, que encaje, que aguante.
[IMAGEN]: Texto en pantalla: "Y lo hace. Cada día."
[EMOCIÓN]: comprensión
[PAUSA]: breve (0.5s)

[VOZ]: Cuando llega a casa, eso tiene que salir por algún sitio.
[IMAGEN]: B-roll de madre e hijo en el pasillo, él de espaldas, ella quieta
[EMOCIÓN]: alivio del reencuadre
[PAUSA]: media (1s)

[VOZ]: Y lo suelta contigo. Porque eres lo más seguro que tiene.
[IMAGEN]: Texto en pantalla grande: "No te está atacando. Está confiando."
[EMOCIÓN]: alivio profundo
[PAUSA]: larga (1.5s)

[VOZ]: ¿Os ha pasado esto esta semana? Comenta SÍ si es así.
[IMAGEN]: Texto en pantalla: "Comenta SÍ 👇" — tipografía grande, fondo oscuro
[EMOCIÓN]: cta — TIPO C (¿TE PASA ESTO?)
[PAUSA]: —

---
RECUENTO DE PALABRAS: 83 palabras
DURACIÓN ESTIMADA: 24-26 segundos
EMOCIÓN DOMINANTE: alivio a través del reencuadre
TIPO DE CTA: C — ¿TE PASA ESTO? | Usar en Fase 1 y 2
HASHTAGS SUGERIDOS: #AltasCapacidades #AdolescenteAACC #MadreAACC #CrianzaConsciente #HijosAACC

VERSIÓN FASE 3 (10k+ seguidores): sustituir el CTA por →
"En NOA tienes exactamente qué decir en esos primeros veinte minutos. Enlace en bio."
```

---

## PLANTILLA 2 — "ERROR TÍPICO DE LOS PADRES"
### Duración: 30 segundos | Formato: antes-despues | Emoción: culpa → comprensión

```
TÍTULO INTERNO: Error-responder-explosion-emocional-hijo

[VOZ]: Cuando tu hijo AACC explota, hay una frase que muchos padres dicen.
[IMAGEN]: Texto en pantalla: "¿Cuántas veces la has dicho tú?"
[EMOCIÓN]: tensión, anticipación
[PAUSA]: breve (0.5s)

[VOZ]: "Cálmate. No es para tanto."
[IMAGEN]: Texto en pantalla con tipografía marcada, fondo neutro
[EMOCIÓN]: reconocimiento incómodo
[PAUSA]: media (1s)

[VOZ]: Y lo que pasa cuando lo dices:
[IMAGEN]: B-roll de adolescente que se cierra más, se va a su cuarto
[EMOCIÓN]: neutral — descripción
[PAUSA]: breve (0.5s)

[VOZ]: Se escala. O se cierra. Nunca se calma.
[IMAGEN]: Texto en pantalla: "Porque su sistema nervioso no puede obedecer esa orden."
[EMOCIÓN]: sorpresa + comprensión
[PAUSA]: media (1s)

[VOZ]: No es que no quiera calmarse. Es que no puede todavía.
[IMAGEN]: B-roll de ondas en agua, metáfora visual de la intensidad emocional
[EMOCIÓN]: comprensión nueva
[PAUSA]: breve (0.5s)

[VOZ]: Lo que funciona en su lugar:
[IMAGEN]: Texto en pantalla: "Presencia. Sin palabras."
[EMOCIÓN]: alivio práctico
[PAUSA]: media (1s)

[VOZ]: Estar ahí sin exigirle que procese mientras aún está en la tormenta.
[IMAGEN]: B-roll de mano sobre hombro, sin palabras, gesto de quietud
[EMOCIÓN]: alivio
[PAUSA]: breve (0.5s)

[VOZ]: Si quieres saber exactamente qué decir en esos primeros dos minutos, comenta CALMA y te lo mando ahora.
[IMAGEN]: Texto en pantalla: "Comenta CALMA 👇" — fondo oscuro, tipografía grande en blanco
[EMOCIÓN]: cta — TIPO B (COMENTAR PALABRA)
[PAUSA]: —

---
RECUENTO DE PALABRAS: 116 palabras
DURACIÓN ESTIMADA: 29-32 segundos
EMOCIÓN DOMINANTE: comprensión de error sin culpa, con herramienta alternativa
TIPO DE CTA: B — COMENTAR CALMA | Lead magnet: "5 frases para los primeros 2 minutos de una explosión AACC" | Usar en Fase 1 y 2
HASHTAGS SUGERIDOS: #RegulacionEmocional #AACC #MadresAgotadas #ExplosionEmocional #HijosAACC

VERSIÓN FASE 3 (10k+ seguidores): sustituir el CTA por →
"NOA te explica cuándo hablar y cuándo lo mejor que puedes hacer es no decir nada. Enlace en bio."
```

---

## PLANTILLA 3 — "FRASE DESTRUCTIVA / FRASE ALTERNATIVA"
### Duración: 20 segundos | Formato: contrast | Emoción: reconocimiento → esperanza práctica

```
TÍTULO INTERNO: Frase-destructiva-alternativa-deberes-AACC

[VOZ]: Cuando no quiere hacer los deberes, la frase que más repites probablemente es esta:
[IMAGEN]: Pantalla negra, preparando el contraste
[EMOCIÓN]: tensión anticipatoria
[PAUSA]: breve (0.5s)

[VOZ]: "Es que no te esfuerzas nada."
[IMAGEN]: Texto en pantalla, tipografía roja o marcada — frase destructiva
[EMOCIÓN]: reconocimiento incómodo — ella lo ha dicho
[PAUSA]: media (1s)

[VOZ]: Lo que eso activa en el cerebro de un adolescente AACC:
[IMAGEN]: Gráfico simple: cerebro + flecha + cierre emocional
[EMOCIÓN]: sorpresa educativa
[PAUSA]: breve (0.5s)

[VOZ]: Vergüenza. Y la vergüenza bloquea mucho más que el aburrimiento.
[IMAGEN]: Texto en pantalla: "Ya no es sobre los deberes."
[EMOCIÓN]: comprensión nueva
[PAUSA]: media (1s)

[VOZ]: La frase alternativa que sí abre:
[IMAGEN]: Fondo más cálido, tipografía blanca limpia
[EMOCIÓN]: giro hacia la esperanza
[PAUSA]: breve (0.5s)

[VOZ]: "Veo que esto se te está haciendo cuesta arriba. ¿Qué está pasando?"
[IMAGEN]: Texto en pantalla con tipografía cálida, destacada
[EMOCIÓN]: alivio práctico
[PAUSA]: larga (1.5s)

[VOZ]: Comenta FRASES y te mando diez más como esta. Gratis, ahora por DM.
[IMAGEN]: Texto en pantalla: "Comenta FRASES 👇" — tipografía grande, fondo oscuro
[EMOCIÓN]: cta — TIPO B (COMENTAR PALABRA)
[PAUSA]: —

---
RECUENTO DE PALABRAS: 96 palabras
DURACIÓN ESTIMADA: 20-23 segundos
EMOCIÓN DOMINANTE: reconocimiento de error + herramienta inmediata
TIPO DE CTA: B — COMENTAR FRASES | Lead magnet: "10 frases que abren y 10 que cierran con tu hijo AACC" | Usar en Fase 1 y 2
HASHTAGS SUGERIDOS: #FrasesParaMadres #AACC #CrianzaConsciente #DeberesCasa #HijosAACC

VERSIÓN FASE 3 (10k+ seguidores): sustituir el CTA por →
"En NOA tienes más de cuarenta frases así, organizadas por situación. Enlace en bio."
```

---

## PLANTILLA 4 — "MINI HISTORIA"
### Duración: 40 segundos | Formato: story | Emoción: reconocimiento → alivio

```
TÍTULO INTERNO: Mini-historia-sabado-cambio-planes-explosion

[VOZ]: El sábado por la mañana, habíais planeado ir al mercado.
[IMAGEN]: B-roll de cocina luminosa, desayuno, ambiente tranquilo
[EMOCIÓN]: neutral — se establece la normalidad
[PAUSA]: breve (0.5s)

[VOZ]: Pero tu pareja tuvo que trabajar. Y decidiste cambiarlo por un plan más pequeño.
[IMAGEN]: B-roll de teléfono, mensaje, cambio de agenda
[EMOCIÓN]: neutral — preparando el conflicto
[PAUSA]: breve (0.5s)

[VOZ]: Le dijiste a tu hijo: "Hoy no vamos al mercado."
[IMAGEN]: Texto en pantalla: "Cuatro palabras."
[EMOCIÓN]: tensión anticipatoria
[PAUSA]: media (1s)

[VOZ]: Lo que vino después no fue una reacción normal.
[IMAGEN]: B-roll de habitación cerrada, silencio en casa, madre sola en cocina
[EMOCIÓN]: reconocimiento — ya sabe lo que viene
[PAUSA]: breve (0.5s)

[VOZ]: Dos horas después, él seguía sin poder salir de la habitación.
[IMAGEN]: B-roll de reloj, de pasillo vacío
[EMOCIÓN]: reconocimiento doloroso
[PAUSA]: media (1s)

[VOZ]: Y tú te preguntabas si habías hecho algo mal.
[IMAGEN]: Madre sentada, mirada perdida
[EMOCIÓN]: validación del pensamiento culposo
[PAUSA]: breve (0.5s)

[VOZ]: No habías hecho nada mal.
[IMAGEN]: Texto en pantalla: pausa, peso.
[EMOCIÓN]: giro — el alivio empieza aquí
[PAUSA]: larga (1.5s)

[VOZ]: Su cerebro necesita la predictibilidad de los planes como otros necesitan el oxígeno. No es exageración. Es neurología.
[IMAGEN]: B-roll de línea de tiempo, de agenda con estructura visual
[EMOCIÓN]: comprensión nueva
[PAUSA]: media (1s)

[VOZ]: Cuando sabes eso, la próxima vez puedes prepararlo. Y la diferencia es enorme.
[IMAGEN]: B-roll de madre e hijo hablando, café de por medio
[EMOCIÓN]: esperanza práctica
[PAUSA]: breve (0.5s)

[VOZ]: Si esto te suena, sígueme. Cada semana cuento una cosa así que nadie más está diciendo.
[IMAGEN]: Texto en pantalla: "Sígueme para más 👆" — tipografía media, fondo cálido oscuro
[EMOCIÓN]: cta — TIPO A (SEGUIR)
[PAUSA]: —

---
RECUENTO DE PALABRAS: 135 palabras
DURACIÓN ESTIMADA: 38-42 segundos
EMOCIÓN DOMINANTE: reconocimiento → comprensión → esperanza práctica
TIPO DE CTA: A — SEGUIR | Usar en Fase 1 (prioritario en vídeos de alto alcance)
HASHTAGS SUGERIDOS: #HipersensibilidadAACC #CambiosDePlanes #AdolescenteAACC #MadresAACC #CrianzaReal

VERSIÓN FASE 3 (10k+ seguidores): sustituir el CTA por →
"NOA te explica cómo preparar estos cambios para que no escalen. Para este caso y para todos los que se repiten. Enlace en bio."
```

---

## PLANTILLA 5 — "3 SEÑALES"
### Duración: 35 segundos | Formato: list-based | Emoción: sorpresa → reconocimiento

```
TÍTULO INTERNO: 3-señales-hijo-AACC-enmascaramiento-colegio

[VOZ]: Si tu hijo AACC llega agotado del colegio aunque "le va bien", hay tres señales que nadie te ha explicado.
[IMAGEN]: Texto en pantalla: "Tres señales."
[EMOCIÓN]: promesa + tensión
[PAUSA]: breve (0.5s)

[VOZ]: Señal uno: En casa es mucho más intenso que en el colegio.
[IMAGEN]: Texto en pantalla: "1. Más intenso en casa"
[EMOCIÓN]: reconocimiento inmediato
[PAUSA]: breve (0.5s)

[VOZ]: Lo llaman mala conducta en casa. Lo que es en realidad: está soltando la presión de contener.
[IMAGEN]: B-roll de adolescente tirando mochila, madre observando
[EMOCIÓN]: sorpresa + reencuadre
[PAUSA]: media (1s)

[VOZ]: Señal dos: Necesita mucho tiempo de desconexión antes de hablar.
[IMAGEN]: Texto en pantalla: "2. Necesita desconectar primero"
[EMOCIÓN]: reconocimiento
[PAUSA]: breve (0.5s)

[VOZ]: No es que no quiera contarte el día. Es que aún no tiene capacidad de procesar y hablar al mismo tiempo.
[IMAGEN]: B-roll de auriculares, cuarto oscuro, silencio elegido
[EMOCIÓN]: comprensión
[PAUSA]: media (1s)

[VOZ]: Señal tres: Los problemas del colegio salen por la noche, no al llegar.
[IMAGEN]: Texto en pantalla: "3. Los problemas salen de noche"
[EMOCIÓN]: sorpresa
[PAUSA]: breve (0.5s)

[VOZ]: A las diez de la noche te pregunta algo que pasó hace ocho horas. Así procesa su cerebro.
[IMAGEN]: B-roll de cama, luz de lámpara, madre que levanta la cabeza del libro
[EMOCIÓN]: reconocimiento + comprensión
[PAUSA]: media (1s)

[VOZ]: ¿Tu hijo tiene alguna de estas tres señales? Comenta cuál en los comentarios.
[IMAGEN]: Texto en pantalla: "¿La 1, la 2 o la 3? 👇" — tipografía grande
[EMOCIÓN]: cta — TIPO C (¿TE PASA ESTO?)
[PAUSA]: —

---
RECUENTO DE PALABRAS: 128 palabras
DURACIÓN ESTIMADA: 33-37 segundos
EMOCIÓN DOMINANTE: sorpresa → reconocimiento → comprensión nueva
TIPO DE CTA: C — ¿TE PASA ESTO? | Respuesta de 1 palabra (la 1 / la 2 / las tres) | Usar en Fase 1 y 2
HASHTAGS SUGERIDOS: #EnmascaramientoAACC #SenalesAACC #VueltaColegio #MadresAACC #HijosAACC

VERSIÓN FASE 3 (10k+ seguidores): sustituir el CTA por →
"Si tu hijo tiene estas señales, NOA tiene un módulo completo sobre el retorno del colegio. Empieza hoy. Enlace en bio."
```

---

## PLANTILLA 6 — "CUANDO TU HIJO AACC TE RESPONDE ASÍ…"
### Duración: 30 segundos | Formato: pregunta-respuesta | Emoción: reconocimiento → comprensión práctica

```
TÍTULO INTERNO: Cuando-hijo-dice-odio-la-escuela-respuesta-padre

[VOZ]: Cuando tu hijo llega a casa y dice "odio el colegio", ¿qué contestas?
[IMAGEN]: Texto en pantalla: "¿Qué respondes tú?"
[EMOCIÓN]: tensión — el espectador se pregunta si lo hace bien
[PAUSA]: breve (0.5s)

[VOZ]: La mayoría de padres dicen una de estas tres cosas:
[IMAGEN]: Texto en pantalla: "¿Cuál es la tuya?"
[EMOCIÓN]: reconocimiento anticipatorio
[PAUSA]: breve (0.5s)

[VOZ]: Uno: "No digas eso, tienes mucha suerte."
[IMAGEN]: Texto con X roja — respuesta que cierra
[EMOCIÓN]: reconocimiento incómodo
[PAUSA]: breve (0.5s)

[VOZ]: Dos: "¿Qué ha pasado?" — y él dice "nada" y se va.
[IMAGEN]: Texto con X roja — respuesta que cierra
[EMOCIÓN]: reconocimiento frustrante
[PAUSA]: breve (0.5s)

[VOZ]: Tres: "Ya pasará, los colegios son así."
[IMAGEN]: Texto con X roja — respuesta que cierra
[EMOCIÓN]: reconocimiento incómodo
[PAUSA]: media (1s)

[VOZ]: Las tres cierran la conversación antes de que empiece.
[IMAGEN]: Texto en pantalla: "Porque responden al contenido, no a la emoción."
[EMOCIÓN]: comprensión nueva
[PAUSA]: breve (0.5s)

[VOZ]: Lo que abre: "Suenas muy agotado. ¿Quieres estar un rato tranquilo o prefieres que esté cerca?"
[IMAGEN]: Texto en pantalla con tipografía cálida, respuesta destacada
[EMOCIÓN]: alivio práctico
[PAUSA]: larga (1.5s)

[VOZ]: Comenta GUÍA y te mando una lista de respuestas así para los momentos más difíciles. Gratis.
[IMAGEN]: Texto en pantalla: "Comenta GUÍA 👇" — tipografía grande, fondo oscuro
[EMOCIÓN]: cta — TIPO B (COMENTAR PALABRA)
[PAUSA]: —

---
RECUENTO DE PALABRAS: 128 palabras
DURACIÓN ESTIMADA: 29-32 segundos
EMOCIÓN DOMINANTE: reconocimiento de error → herramienta práctica → confianza
TIPO DE CTA: B — COMENTAR GUÍA | Lead magnet: "Mini-guía: qué responder en los 3 momentos más difíciles del día con tu hijo AACC" | Usar en Fase 1 y 2
HASHTAGS SUGERIDOS: #RespuestasParaMadres #AACC #ConexionFamiliar #ComunicacionFamiliar #HijosAACC

VERSIÓN FASE 3 (10k+ seguidores): sustituir el CTA por →
"En NOA tienes respuestas así para las veinte situaciones que más se repiten. Enlace en bio."
```

---

## PLANTILLA 7 — "NOA TE DIRÍA ESTO"
### Duración: 25 segundos | Formato: story de voz de autoridad empática | Emoción: validación → alivio

```
TÍTULO INTERNO: NOA-te-diría-no-estas-sola-herramientas

[VOZ]: Si hoy has tenido un día duro con tu hijo, NOA te diría esto:
[IMAGEN]: Pantalla de NOA, como si fuera un mensaje de la app
[EMOCIÓN]: apertura empática — no es un anuncio, es un mensaje directo
[PAUSA]: breve (0.5s)

[VOZ]: Que lo que has vivido hoy no mide lo buena madre que eres.
[IMAGEN]: Texto en pantalla, tipografía limpia, fondo cálido oscuro
[EMOCIÓN]: validación directa
[PAUSA]: media (1s)

[VOZ]: Que perder la paciencia no te convierte en el problema.
[IMAGEN]: Texto en pantalla — segunda línea del mensaje
[EMOCIÓN]: validación — quita la culpa
[PAUSA]: breve (0.5s)

[VOZ]: Que hay una razón para todo lo que ha pasado hoy. Y tiene nombre.
[IMAGEN]: Texto en pantalla — pausa, misterio
[EMOCIÓN]: curiosidad + promesa
[PAUSA]: media (1s)

[VOZ]: Y que mañana puedes empezar con algo concreto, no con otra promesa de cambiar todo.
[IMAGEN]: Texto en pantalla: "Algo concreto."
[EMOCIÓN]: esperanza práctica — no motivacional
[PAUSA]: larga (1.5s)

[VOZ]: Si hoy ha sido un día duro, sígueme. Aquí hay más de esto cada semana.
[IMAGEN]: Texto en pantalla: "Sígueme 👆" — tipografía media, fondo oscuro cálido
[EMOCIÓN]: cta — TIPO A (SEGUIR)
[PAUSA]: —

---
RECUENTO DE PALABRAS: 96 palabras
DURACIÓN ESTIMADA: 24-27 segundos
EMOCIÓN DOMINANTE: validación profunda → esperanza práctica
TIPO DE CTA: A — SEGUIR | Usar en Fase 1 (especialmente en vídeos emocionales de alta retención)
HASHTAGS SUGERIDOS: #MadreAACC #NoEstásSola #CrianzaReal #AltasCapacidades #AgotamientoParental

VERSIÓN FASE 3 (10k+ seguidores): sustituir el CTA por →
"Eso es lo que hace NOA. Algo concreto para mañana. Enlace en bio."
```

---

## TABLA RESUMEN — CTAs POR PLANTILLA Y FASE

| Plantilla | CTA Fase 1-2 | Tipo | Palabra/acción | CTA Fase 3 |
|-----------|-------------|------|----------------|------------|
| 1 — Lo que parece | ¿Os ha pasado esta semana? Comenta SÍ | C | SÍ | NOA + enlace en bio |
| 2 — Error típico | Comenta CALMA → protocolo de crisis por DM | B | CALMA | NOA cuándo hablar + enlace |
| 3 — Frase destructiva | Comenta FRASES → 10 frases que abren/cierran | B | FRASES | NOA + 40 frases + enlace |
| 4 — Mini historia | Sígueme. Cuento esto cada semana. | A | — | NOA módulo cambios + enlace |
| 5 — 3 señales | ¿Tu hijo tiene la 1, la 2 o las tres? | C | 1 / 2 / 3 | NOA módulo retorno colegio |
| 6 — Cuando te responde así | Comenta GUÍA → respuestas para 3 momentos | B | GUÍA | NOA 20 situaciones + enlace |
| 7 — NOA te diría | Sígueme. Aquí hay más de esto cada semana. | A | — | NOA algo concreto + enlace |

**Distribución recomendada por semana (Fase 1):**
- 2 CTAs tipo A (seguir) — en vídeos emocionales de alta retención
- 3 CTAs tipo B (comentar palabra) — en vídeos educativos con herramienta concreta
- 2 CTAs tipo C (¿te pasa esto?) — en vídeos de reconocimiento y situaciones cotidianas

**Lead magnets activos para CTAs tipo B:**

| Palabra | Recurso que se envía por DM | Formato |
|---------|----------------------------|---------|
| CALMA | 5 frases para los primeros 2 minutos de una explosión AACC | PDF 1 página |
| FRASES | 10 frases que abren y 10 que cierran con tu hijo AACC | PDF 2 páginas |
| GUÍA | Qué responder en los 3 momentos más difíciles del día | PDF 1 página |
| SEÑALES | 8 señales de que tu hijo AACC está enmascarando | Lista visual |
| DEBERES | Por qué fallan los deberes en AACC y qué cambia todo | PDF 1 página |
| NOCHE | Protocolo de los 20 minutos antes de dormir | PDF 1 página |
| EXPLOSIÓN | Los 3 pasos en los primeros 2 minutos de crisis | Infografía |

> Para automatizar el envío de DMs usa **ManyChat** (conectado a Instagram) o **Manychat para TikTok**.
> Coste: desde $15/mes. ROI inmediato si el lead magnet está bien hecho.

---

## NOTAS DE DIRECCIÓN DE VOZ

```
VOZ GENERAL NOA:
- Velocidad: 130-145 palabras por minuto (nunca más rápido)
- Tono: femenino, medio-bajo, cálido pero sin dulzura excesiva
- Actitud: como una amiga que sabe de lo que habla y no te va a juzgar
- Nunca ascendente en preguntas (suena a presentadora de TV)
- Nunca descendente excesivo (suena a pésame)
- Las frases cortas se dicen más despacio, no más rápido

TEMPERATURA POR TIPO DE LÍNEA:
- [reconocimiento]: voz ligeramente más lenta, como si reconociera algo junto a ella
- [giro]: pausa antes de la frase, ligeramente más firme
- [validación]: más cálida, más cercana
- [comprensión nueva]: casi neutral, como explicar algo importante sin dramatizar
- [cta]: natural, sin urgencia comercial, como si fuera la siguiente pregunta lógica

PUNTUACIÓN QUE IMPORTA:
- Punto seguido = pausa mínima (0.3s)
- Punto y aparte = pausa media (0.8-1s)
- Los dos puntos crean anticipación, no se acelera después
- Las listas se leen con pausa entre cada ítem
```

---

## NOTAS DE DIRECCIÓN VISUAL

```
B-ROLL PREFERENTE POR PLANTILLA:
- contrast: dos mundos visuales distintos, diferencia de iluminación entre "error" y "realidad"
- story: progresión temporal, mismo espacio pero diferente estado emocional
- list-based: texto en pantalla para cada punto, b-roll ilustrativo entre textos
- pregunta-respuesta: texto en pantalla para las opciones, b-roll para el efecto

PALETA NOA:
- Fondos: blanco roto, beige cálido, gris oscuro para momentos de peso
- Texto en pantalla: blanco sobre oscuro / negro sobre claro
- Highlight de palabras clave: terracota (#C25C3A) o verde salvia (#7A9E7E)
- Nunca neón. Nunca purpura. Nunca tipografía display caótica.

TRANSICIONES:
- Corte limpio entre bloques emocionales (no fundidos suaves entre tensión y alivio)
- Fundido a negro para pausas largas de peso
- Texto que aparece una palabra a la vez para frases de impacto

EVITAR:
- Stock footage de familias perfectas y sonrientes
- Imágenes de diagnósticos, cerebros, libros escolares
- Cualquier imagen que parezca de artículo académico
- Familias que parecen actores
```

---

## CONFIGURACIÓN DE API PARA GENERACIÓN DE GUIONES

```python
import anthropic

client = anthropic.Anthropic()

system_prompt = """[Insertar el system prompt de arriba]"""

def generar_guion(
    plantilla: str,
    tema: str,
    duracion_max: int = 40,
    emocion_dominante: str = "reconocimiento",
    cta_tipo: str = "COMENTAR_PALABRA",
    cta_palabra: str = "CALMA",
    cta_recurso: str = "5 frases para los primeros 2 minutos de una explosión AACC",
    fase: int = 1  # 1 = construcción (0-2k), 2 = activación (2k-10k), 3 = conversión (10k+)
):
    """
    cta_tipo opciones:
      - "SEGUIR"            → CTA tipo A (construcción de audiencia)
      - "COMENTAR_PALABRA"  → CTA tipo B (lead magnet por DM)
      - "TE_PASA_ESTO"      → CTA tipo C (engagement / reconocimiento)
      - "DESCARGA_APP"      → CTA directo a NOA (solo Fase 3)
    """
    if fase < 3 and cta_tipo == "DESCARGA_APP":
        cta_tipo = "SEGUIR"  # Forzar CTA de construcción en fases tempranas

    cta_instruccion = {
        "SEGUIR": "Cierra el vídeo con un CTA para seguir la cuenta. Razón específica al contenido del vídeo.",
        "COMENTAR_PALABRA": f"Cierra el vídeo pidiendo que comenten '{cta_palabra}' para recibir '{cta_recurso}' por DM. Gratis.",
        "TE_PASA_ESTO": "Cierra el vídeo con una pregunta directa de reconocimiento que tenga respuesta de 1-3 palabras.",
        "DESCARGA_APP": "Cierra el vídeo con un CTA directo a descargar NOA. Enlace en bio."
    }[cta_tipo]

    user_message = f"""
    Genera un guión usando la plantilla "{plantilla}".
    
    Tema específico: {tema}
    Duración máxima: {duracion_max} segundos
    Emoción dominante objetivo: {emocion_dominante}
    Fase de crecimiento: {fase} ({"construcción" if fase == 1 else "activación" if fase == 2 else "conversión"})
    
    INSTRUCCIÓN DE CTA: {cta_instruccion}
    
    Entrega el guión completo con todas las líneas formateadas según las instrucciones.
    Al final incluye: recuento de palabras, duración estimada, emoción dominante, tipo de CTA y 5 hashtags.
    """

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2048,
        temperature=0.9,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )

    return response.content[0].text

# Uso — Fase 1, CTA tipo B (lead magnet):
guion = generar_guion(
    plantilla="Error típico de los padres",
    tema="responder 'cálmate' cuando el hijo AACC explota",
    duracion_max=30,
    emocion_dominante="comprensión sin culpa",
    cta_tipo="COMENTAR_PALABRA",
    cta_palabra="CALMA",
    cta_recurso="5 frases para los primeros 2 minutos de una explosión emocional AACC",
    fase=1
)

# Uso — Fase 1, CTA tipo A (seguir):
guion = generar_guion(
    plantilla="Mini historia",
    tema="cambio de planes el sábado y explosión desproporcionada",
    duracion_max=40,
    emocion_dominante="reconocimiento → alivio",
    cta_tipo="SEGUIR",
    fase=1
)

# Uso — Fase 1, CTA tipo C (engagement):
guion = generar_guion(
    plantilla="3 señales",
    tema="señales de enmascaramiento en el colegio",
    duracion_max=35,
    emocion_dominante="sorpresa → reconocimiento",
    cta_tipo="TE_PASA_ESTO",
    fase=1
)
```
