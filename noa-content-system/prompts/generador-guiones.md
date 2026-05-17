# GENERADOR DE GUIONES — NOA CONTENT SYSTEM
# Prompt de Sistema para Claude API + 7 Plantillas con Contenido Real
# Versión 2.0 | Todo el contenido en español

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
6. NOA APARECE COMO CONSECUENCIA: El CTA a NOA no se siente como un anuncio. Se siente como la siguiente pregunta natural: "¿y qué hago con esto que acabo de entender?"

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

[VOZ]: En NOA tienes exactamente qué decir en esos primeros veinte minutos.
[IMAGEN]: Logo NOA, pantalla de app, fondo cálido
[EMOCIÓN]: cta
[PAUSA]: —

---
RECUENTO DE PALABRAS: 88 palabras
DURACIÓN ESTIMADA: 24-26 segundos
EMOCIÓN DOMINANTE: alivio a través del reencuadre
HASHTAGS SUGERIDOS: #AltasCapacidades #AdolescenteAACC #MadreAACC #CrianzaConsciente #NOAapp
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

[VOZ]: NOA te explica cuándo hablar y cuándo lo mejor que puedes hacer es no decir nada.
[IMAGEN]: Pantalla app NOA, conversación corta, módulo de crisis emocional
[EMOCIÓN]: cta natural
[PAUSA]: —

---
RECUENTO DE PALABRAS: 112 palabras
DURACIÓN ESTIMADA: 29-32 segundos
EMOCIÓN DOMINANTE: comprensión de error sin culpa, con herramienta alternativa
HASHTAGS SUGERIDOS: #RegulacionEmocional #AACC #MadresAgotadas #HighlyGiftedChild #NOAcoach
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

[VOZ]: En NOA tienes más frases así. Para el momento exacto en que no sabes qué decir.
[IMAGEN]: App NOA, sección de respuestas para momentos de conflicto
[EMOCIÓN]: cta
[PAUSA]: —

---
RECUENTO DE PALABRAS: 98 palabras
DURACIÓN ESTIMADA: 20-23 segundos
EMOCIÓN DOMINANTE: reconocimiento de error + herramienta inmediata
HASHTAGS SUGERIDOS: #FrasesParaMadres #AACC #CrianzaPositiva #DeberesCasa #NOAapp
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

[VOZ]: NOA te explica cómo. Para este caso y para todos los que se repiten.
[IMAGEN]: App NOA, módulo de hipersensibilidad y cambios
[EMOCIÓN]: cta
[PAUSA]: —

---
RECUENTO DE PALABRAS: 138 palabras
DURACIÓN ESTIMADA: 38-42 segundos
EMOCIÓN DOMINANTE: reconocimiento → comprensión → esperanza práctica
HASHTAGS SUGERIDOS: #HipersensibilidadAACC #CambiosDePlanes #AdolescenteAACC #NOAapp #MadresQueEntienden
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

[VOZ]: Si esto te suena, NOA tiene un módulo completo sobre el retorno del colegio. Empieza hoy.
[IMAGEN]: App NOA, pantalla de módulo específico
[EMOCIÓN]: cta
[PAUSA]: —

---
RECUENTO DE PALABRAS: 132 palabras
DURACIÓN ESTIMADA: 33-37 segundos
EMOCIÓN DOMINANTE: sorpresa → reconocimiento → comprensión nueva
HASHTAGS SUGERIDOS: #EnmascaramientoAACC #SenalesAACC #VueltaColegio #MadresAACC #NOAapp
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

[VOZ]: En NOA tienes respuestas así para las veinte situaciones que más se repiten.
[IMAGEN]: App NOA, lista de situaciones frecuentes
[EMOCIÓN]: cta
[PAUSA]: —

---
RECUENTO DE PALABRAS: 127 palabras
DURACIÓN ESTIMADA: 29-32 segundos
EMOCIÓN DOMINANTE: reconocimiento de error → herramienta práctica → confianza
HASHTAGS SUGERIDOS: #RespuestasParaMadres #AACC #ConexionFamiliar #NOAapp #QuéDecir
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

[VOZ]: Eso es lo que hace NOA. Enlace en bio.
[IMAGEN]: Logo NOA, CTA limpio, enlace visible
[EMOCIÓN]: cta
[PAUSA]: —

---
RECUENTO DE PALABRAS: 98 palabras
DURACIÓN ESTIMADA: 24-27 segundos
EMOCIÓN DOMINANTE: validación profunda → esperanza práctica
HASHTAGS SUGERIDOS: #NOAapp #MadreAACC #NoEstásSola #CrianzaReal #AltasCapacidades
```

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
    emocion_dominante: str = "reconocimiento"
):
    user_message = f"""
    Genera un guión usando la plantilla "{plantilla}".
    
    Tema específico: {tema}
    Duración máxima: {duracion_max} segundos
    Emoción dominante objetivo: {emocion_dominante}
    
    Entrega el guión completo con todas las líneas formateadas según las instrucciones.
    Al final incluye: recuento de palabras, duración estimada, emoción dominante y 5 hashtags.
    """
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        temperature=0.9,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    return response.content[0].text

# Uso:
guion = generar_guion(
    plantilla="Lo que parece / lo que realmente pasa",
    tema="discusión por los deberes a las 7 de la tarde",
    duracion_max=30,
    emocion_dominante="reconocimiento → alivio"
)
```
