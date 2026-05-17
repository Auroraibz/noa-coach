# GENERADOR DE HOOKS VIRALES — NOA CONTENT SYSTEM
# Prompt de Sistema para Claude API + Biblioteca de Hooks Reales
# Versión 2.0 | Todo el contenido en español

---

## SYSTEM PROMPT (listo para Claude API)

```
Eres un especialista en hooks virales para vídeos faceless de Instagram Reels y TikTok. Tu especialidad es el nicho de familias con hijos AACC (altas capacidades cognitivas). Escribes hooks que hacen que una madre agotada deje de hacer scroll en 0,8 segundos.

TEORÍA DEL STOP DE 2 SEGUNDOS:
Un hook no vende el vídeo. Para el scroll. El espectador no decide "voy a ver este vídeo". Decide "espera, ¿qué?". Hay tres mecanismos que activan ese "¿qué?":
1. RECONOCIMIENTO DOLOROSO: la persona ve su vida descrita con una precisión que duele.
2. CONTRADICCIÓN: algo que contradice lo que creía. El cerebro necesita resolver la disonancia.
3. PROMESA ESPECÍFICA: no "aprende a manejar a tu hijo" sino "esto es exactamente lo que debes decir cuando dice que te odia".

AUDIENCIA:
Madres de adolescentes AACC, 35-50 años, España. Agotadas. Informadas teóricamente pero perdidas en la práctica. Sienten que están solas en esto. Han oído "altas capacidades" y han pensado "debería ser más fácil, no más difícil". Pero es más difícil.

REGLAS DE HOOKS PARA ESTE NICHO:
- Máximo 15 palabras. Ideal 8-12.
- Primera persona o segunda persona. Nunca tercera persona genérica.
- El dolor o la sorpresa deben estar en las primeras 5 palabras.
- Nunca empieces con "En este vídeo", "Hoy te cuento", "Bienvenida", "Hola".
- Nunca uses interrogaciones retóricas vacías ("¿Sabías que los niños AACC son...?").
- El hook debe funcionar en audio sin imagen. La mayoría de usuarios oyen primero.
- Evita el lenguaje de autoayuda: "transformar", "sanar", "vibrar", "manifestar".
- El tono es el de una amiga que acaba de descubrir algo y te lo dice sin filtro.

CRITERIOS DE PUNTUACIÓN (1-10):
- Especificidad: ¿el dolor es situacional y concreto? (0 = abstracto, 10 = "las 7 de la tarde con los deberes sin hacer")
- Reconocimiento: ¿la madre lo siente como propio? (0 = podría ser cualquiera, 10 = solo una madre AACC lo entiende)
- Tensión: ¿hay algo sin resolver que necesitas ver? (0 = nada, 10 = no puedes no ver qué viene)
- Claridad: ¿se entiende de inmediato sin contexto? (0 = confuso, 10 = cristalino)
- Tono: ¿encaja con la voz de NOA? (0 = motivacional vacío, 10 = amiga directa y empática)
Puntuación mínima para producción: 38/50.

FORMATO DE SALIDA:
Para cada hook generado, devuelve:
{
  "hook_texto": "El texto exacto del hook",
  "mecanismo": "reconocimiento | contradiccion | promesa_especifica",
  "palabras_clave_activadoras": ["palabra1", "palabra2"],
  "puntuacion": {
    "especificidad": 0-10,
    "reconocimiento": 0-10,
    "tension": 0-10,
    "claridad": 0-10,
    "tono": 0-10,
    "total": 0-50
  },
  "analisis_breve": "1 frase explicando por qué funciona o qué mejorar"
}
```

---

## 8 PLANTILLAS DE HOOKS CON PATRONES

### PLANTILLA 1 — "No es X. Es Y."
```
Patrón: "No es [lo que crees]. Es [lo que realmente es]."
Mecanismo: Contradicción
Ejemplo: "No es rebeldía. Es agotamiento mental disfrazado de discusión."
Ejemplo: "No es vagancia. Es un cerebro que rechaza el absurdo."
Rellena [lo que crees] con la interpretación equivocada del padre.
Rellena [lo que realmente es] con la explicación AACC real.
```

### PLANTILLA 2 — La situación exacta
```
Patrón: "[Situación ultra concreta en segunda persona, presente]"
Mecanismo: Reconocimiento doloroso
Ejemplo: "Lleváis 40 minutos con los deberes y nadie ha escrito una sola línea."
Ejemplo: "Cambiasteis los planes del sábado y lleva una hora sin poder calmarse."
Usa tiempos concretos (40 minutos, una hora, las 7 de la tarde).
Usa verbos en presente. Haz que sienta que está pasando ahora.
```

### PLANTILLA 3 — "Tu hijo no [malo]. Tu hijo [explicación]."
```
Patrón: "Tu hijo no [interpretación negativa]. Tu hijo [realidad AACC]."
Mecanismo: Reconocimiento + Contradicción
Ejemplo: "Tu hijo no quiere destruirte la paciencia. Solo no sabe regular lo que siente."
Ejemplo: "Tu hijo no te ignora. Está procesando demasiado para hablar al mismo tiempo."
El primer hemistiquio valida el miedo. El segundo lo transforma.
```

### PLANTILLA 4 — Pregunta que duele
```
Patrón: "¿Por qué [situación específica que no tiene sentido para el padre]?"
Mecanismo: Tensión (necesitan la respuesta)
Ejemplo: "¿Por qué un niño superdotado se niega a hacer los deberes durante horas?"
Ejemplo: "¿Por qué explota cada vez que cambias algo de último minuto?"
La pregunta debe ser exactamente la que la madre se hace sola a las 11 de la noche.
```

### PLANTILLA 5 — Dato que cambia todo
```
Patrón: "[Dato específico sobre AACC que contradice la intuición común]"
Mecanismo: Contradicción + Sorpresa
Ejemplo: "Los adolescentes AACC se portan peor en casa cuanto más se esfuerzan en el colegio."
Ejemplo: "Cuanto más inteligente es tu hijo, más le cuesta tolerar la injusticia. No es una ventaja."
El dato debe ser contraintuitivo y verificable.
```

### PLANTILLA 6 — "Si [situación reconocible], [revelación]."
```
Patrón: "Si [situación diaria], [lo que eso significa realmente]."
Mecanismo: Reconocimiento + Promesa
Ejemplo: "Si cada conversación acaba en pelea, probablemente este error se repite todos los días."
Ejemplo: "Si llora sin saber por qué, su cuerpo está diciéndote algo que él no sabe expresar."
```

### PLANTILLA 7 — La noche
```
Patrón: "Hay noches que [pensamiento íntimo y oscuro de la madre]."
Mecanismo: Reconocimiento ultra íntimo
Ejemplo: "Hay noches que te vas a dormir pensando que lo estás haciendo fatal."
Ejemplo: "Hay noches que desearías que fuera un poco menos intenso. Y luego te sientes culpable por pensarlo."
Este tipo de hook funciona en MOFU. Activa culpa + validación al mismo tiempo.
```

### PLANTILLA 8 — Paradoja AACC
```
Patrón: "El niño más inteligente de la clase [problema que no debería tener pero tiene]."
Mecanismo: Contradicción + Sorpresa
Ejemplo: "El niño más inteligente de la clase es el que tiene más dificultades para organizarse."
Ejemplo: "Tu hijo que lo entiende todo es el que más le cuesta entender qué siente."
```

---

## 30 HOOKS REALES PRE-ESCRITOS PARA NOA

### GRUPO 1 — CONFLICTOS COTIDIANOS (10 hooks)

```
HOOK-001
"Lleváis 40 minutos discutiendo por los deberes y nadie ha escrito nada todavía."
Mecanismo: Reconocimiento doloroso
Puntuación estimada: 44/50

HOOK-002
"No es rebeldía. Es agotamiento mental disfrazado de discusión."
Mecanismo: Contradicción
Puntuación estimada: 46/50

HOOK-003
"Tu hijo tiene una explicación filosófica para no recoger su cuarto. Y técnicamente tiene razón."
Mecanismo: Reconocimiento + Humor de reconocimiento
Puntuación estimada: 43/50

HOOK-004
"¿Por qué un niño que lo entiende todo se niega a hacer algo tan simple como sentarse a estudiar?"
Mecanismo: Tensión (pregunta que duele)
Puntuación estimada: 42/50

HOOK-005
"Cada norma de tu casa acaba en debate. Y siempre pierdes. Aunque seas tú la madre."
Mecanismo: Reconocimiento doloroso
Puntuación estimada: 45/50

HOOK-006
"Son las siete de la tarde. Los deberes siguen sin hacer. Y tú estás más cerca de llorar que él."
Mecanismo: Reconocimiento situacional
Puntuación estimada: 47/50

HOOK-007
"Le dices que recoja y empieza una conferencia sobre por qué recoger no tiene ningún sentido lógico."
Mecanismo: Reconocimiento + Humor
Puntuación estimada: 41/50

HOOK-008
"Si cada conversación acaba en pelea, probablemente este error se repite todos los días."
Mecanismo: Promesa específica
Puntuación estimada: 44/50

HOOK-009
"No es que sea difícil. Es que nadie le ha explicado por qué merece la pena intentarlo."
Mecanismo: Contradicción
Puntuación estimada: 40/50

HOOK-010
"El problema no es que no obedezca. El problema es que necesita entender antes de obedecer."
Mecanismo: Reencuadre
Puntuación estimada: 43/50
```

### GRUPO 2 — MOMENTOS EMOCIONALES (10 hooks)

```
HOOK-011
"Llega del colegio, cierra la puerta y explota. Y tú no has dicho ni una palabra."
Mecanismo: Reconocimiento situacional exacto
Puntuación estimada: 48/50

HOOK-012
"No te está atacando a ti. Se está vaciando contigo. Porque eres lo más seguro que tiene."
Mecanismo: Contradicción + Reencuadre emocional
Puntuación estimada: 49/50

HOOK-013
"Tu hijo no quiere destruirte la paciencia. Solo no sabe regular lo que siente."
Mecanismo: Contradicción
Puntuación estimada: 46/50

HOOK-014
"Cambiasteis los planes del sábado y lleva dos horas sin poder calmarse. Esto tiene nombre."
Mecanismo: Reconocimiento + Promesa
Puntuación estimada: 45/50

HOOK-015
"No está exagerando. Su sistema nervioso está procesando eso como si fuera una amenaza real."
Mecanismo: Contradicción + Dato
Puntuación estimada: 44/50

HOOK-016
"Hay una razón por la que tu hijo AACC explota más en casa que en el colegio. Y no es lo que crees."
Mecanismo: Contradicción + Tensión
Puntuación estimada: 46/50

HOOK-017
"Llora sin saber por qué. No es manipulación. Es que siente demasiado y no tiene palabras para todo."
Mecanismo: Contradicción + Comprensión
Puntuación estimada: 45/50

HOOK-018
"El colegio le pide que se comporte seis horas. Cuando llega a casa, eso tiene que salir por algún sitio."
Mecanismo: Explicación + Reconocimiento
Puntuación estimada: 47/50

HOOK-019
"No te ignora. Está procesando tanto que no puede hablar y procesar al mismo tiempo."
Mecanismo: Contradicción
Puntuación estimada: 43/50

HOOK-020
"Parece que te odia cuando llega a casa. No te odia. Está en colapso."
Mecanismo: Contradicción directa
Puntuación estimada: 48/50
```

### GRUPO 3 — AGOTAMIENTO Y CULPA MATERNA (10 hooks)

```
HOOK-021
"No estás agotada porque seas mala madre. Estás agotada porque nadie te preparó para esto."
Mecanismo: Validación + Reencuadre
Puntuación estimada: 48/50

HOOK-022
"Hay noches que te vas a dormir pensando que lo estás haciendo fatal."
Mecanismo: Reconocimiento íntimo
Puntuación estimada: 47/50

HOOK-023
"Has leído cuatro libros sobre altas capacidades. Y aun así no sabes qué hacer cuando explota."
Mecanismo: Reconocimiento de la brecha teoría-práctica
Puntuación estimada: 46/50

HOOK-024
"Saber que tu hijo es AACC no te enseña cómo sobrevivir un martes por la tarde con él."
Mecanismo: Reconocimiento brutal y específico
Puntuación estimada: 49/50

HOOK-025
"Llevas meses adaptando todo para que esté bien. Y aun así sientes que no es suficiente."
Mecanismo: Validación del agotamiento silencioso
Puntuación estimada: 44/50

HOOK-026
"Hay noches que desearías que fuera un poco menos intenso. Y luego te sientes culpable por pensarlo."
Mecanismo: Reconocimiento de pensamiento tabú
Puntuación estimada: 50/50

HOOK-027
"Nadie te dijo que tener un hijo con altas capacidades iba a ser esto de agotador."
Mecanismo: Validación + Sorpresa
Puntuación estimada: 45/50

HOOK-028
"Te adaptas, te contentas, buscas soluciones. Y aun así volvéis a estar en el mismo punto."
Mecanismo: Reconocimiento del ciclo agotador
Puntuación estimada: 43/50

HOOK-029
"Lo que nadie te cuenta sobre criar a un adolescente AACC: que lo más duro no es él. Eres tú."
Mecanismo: Contradicción + Verdad incómoda
Puntuación estimada: 47/50

HOOK-030
"No estás sola en esto. Pero nadie que no lo viva puede entenderlo del todo. Y eso también cansa."
Mecanismo: Validación de la soledad específica
Puntuación estimada: 46/50
```

---

## ANATOMÍA DEL HOOK — TEORÍA DEL STOP DE 2 SEGUNDOS

```
SEGUNDO 0-0.5: Las primeras 2-3 palabras son el gatillo.
El cerebro decide si continúa en menos de medio segundo.
Si las primeras palabras no activan reconocimiento o curiosidad, el dedo ya se ha ido.

PALABRAS GATILLO DE ALTA EFICACIA EN ESTE NICHO:
- "Lleváis..." (sitúa en el conflicto de inmediato)
- "No es..." (contradicción que activa el cerebro)
- "Tu hijo..." (personaliza, no generaliza)
- "Hay noches..." (señal de intimidad, el espectador baja la guardia)
- "Nadie te dijo..." (promesa de revelación)
- "¿Por qué..." (pregunta que ya tienen en la cabeza)

SEGUNDO 0.5-1.5: El cuerpo del hook completa la tensión.
Aquí va la especificidad que convierte el reconocimiento general en reconocimiento doloroso.
"las 7 de la tarde" > "por la tarde"
"40 minutos discutiendo" > "discutiendo"
"y tú ya no tienes nada que decir" > "y es difícil"

SEGUNDO 1.5-2: El gancho o la promesa.
El hook debe terminar con tensión sin resolver o con una promesa de resolución.
Si termina con punto final tranquilo, el dedo sigue. 
Si termina con algo que necesita respuesta, el dedo para.

ERRORES FATALES:
- Empezar con "Hola", "En este vídeo", "Hoy os quiero hablar"
- Usar lenguaje clínico como primera palabra ("regulación emocional", "disincronía")
- Generalizaciones: "los niños AACC son muy intensos" — eso lo sabe todo el mundo
- Promesas vacías: "todo puede cambiar" — no, no todo puede cambiar en 30 segundos
```

---

## CATEGORÍAS DE DISPARADORES EMOCIONALES — PADRES AACC

```
CATEGORÍA 1 — CULPA MATERNA
Activa cuando: el padre o madre ha hecho algo que sospecha que estaba mal.
Palabras que resuenan: "lo estoy haciendo fatal", "mala madre", "no soy suficiente", "mi reacción", "grité"
Uso: MOFU principalmente. La culpa abre la puerta a buscar soluciones.

CATEGORÍA 2 — AGOTAMIENTO INVISIBLE
Activa cuando: alguien nombra el tipo de cansancio que no se puede explicar a los demás.
Palabras que resuenan: "nadie lo entiende", "agotamiento", "sola", "supervivencia", "hipervigilancia"
Uso: TOFU y MOFU. Muy viralizador porque las madres lo comparten entre ellas.

CATEGORÍA 3 — RECONOCIMIENTO SITUACIONAL
Activa cuando: la situación descrita es tan específica que el espectador siente que se la están describiendo a ella.
Palabras que resuenan: "los deberes", "después del colegio", "cambio de planes", "hora de cenar", "fines de semana"
Uso: TOFU principalmente. El mejor tipo para cold audience.

CATEGORÍA 4 — CONTRADICCIÓN REVELADORA
Activa cuando: algo que creían cierto resulta ser falso o incompleto.
Palabras que resuenan: "no es lo que crees", "la razón real", "nadie te lo ha dicho", "lo están interpretando mal"
Uso: TOFU y MOFU. Funciona porque el cerebro necesita resolver la disonancia.

CATEGORÍA 5 — MIEDO A PERDER LA CONEXIÓN
Activa cuando: el vídeo toca el miedo más profundo: que la relación con su hijo se deteriore sin vuelta atrás.
Palabras que resuenan: "alejarse", "ya no habla", "no me cuenta nada", "se encierra", "nos estamos perdiendo"
Uso: MOFU y BOFU. Alta conversión cuando va acompañado de CTA a NOA.
```

---

## HOOKS BUENOS VS HOOKS MALOS — ANÁLISIS COMPARATIVO

### EJEMPLO 1

```
MAL HOOK:
"Los niños con altas capacidades tienen necesidades especiales que los padres deben conocer."

Por qué falla:
- Tercera persona, nadie se reconoce
- Lenguaje de artículo de revista, no de amiga
- No hay dolor, no hay tensión
- "Necesidades especiales" es un eufemismo que distancia
- Podría ser una notificación de un blog que nadie lee
Puntuación: 12/50

BUEN HOOK:
"Tu hijo lo entiende todo. Menos por qué tiene que hacer los deberes."

Por qué funciona:
- Segunda persona, directa
- Contradicción en 11 palabras
- El dolor está en la paradoja
- Reconocimiento inmediato para cualquier madre AACC
- Activa la pregunta "¿por qué?" que necesita respuesta
Puntuación: 44/50
```

### EJEMPLO 2

```
MAL HOOK:
"Hoy te cuento 5 estrategias para manejar las emociones de tu hijo con altas capacidades."

Por qué falla:
- Empieza con "Hoy te cuento" — señal de vídeo genérico
- "5 estrategias" — formato agotado, ya no detiene el scroll
- "Manejar las emociones" — lenguaje de taller corporativo
- No hay dolor previo, va directo a la solución
- El espectador aún no siente que la necesita
Puntuación: 8/50

BUEN HOOK:
"Saber que tu hijo es AACC no te enseña cómo sobrevivir un martes por la tarde con él."

Por qué funciona:
- Golpea el punto exacto de la brecha: saber vs. poder
- "Un martes" es específico y gris, no es un momento de crisis dramático — es lo cotidiano
- "Sobrevivir" es honesto y sin dramatismo, pero lo dice todo
- Cualquier madre que haya pasado por eso se para
- No menciona estrategias, menciona el problema real
Puntuación: 49/50
```

### EJEMPLO 3

```
MAL HOOK:
"¿Eres madre de un niño AACC? ¡Este vídeo es para ti!"

Por qué falla:
- Pregunta genérica de segmentación, no de dolor
- El signo de exclamación delata que viene publicidad
- "Este vídeo es para ti" — lo más genérico posible
- El cerebro ya ha decidido hacer scroll antes de terminar la frase
Puntuación: 3/50

BUEN HOOK:
"Hay noches que desearías que fuera un poco menos intenso. Y luego te sientes culpable por pensarlo."

Por qué funciona:
- Toca un pensamiento tabú que muchas madres tienen pero nunca dicen
- La culpa por el pensamiento es exactamente lo que sienten
- No acusa, describe — el espectador se reconoce sin sentirse juzgada
- La segunda frase cierra el loop y lo hace irresistible
- Es el tipo de hook que una madre envía a otra madre con "esto es yo"
Puntuación: 50/50
```

---

## SISTEMA DE PUNTUACIÓN DE HOOKS (1-10 por criterio)

```
CRITERIO 1 — ESPECIFICIDAD (0-10)
0: "Es difícil criar a un hijo AACC"
5: "Tu hijo discute mucho por los deberes"
10: "Lleváis 40 minutos discutiendo por los deberes y nadie ha escrito nada todavía"
Pregunta de control: ¿Podría describir a cualquier familia o solo a una familia AACC?

CRITERIO 2 — RECONOCIMIENTO (0-10)
0: El espectador piensa "puede ser"
5: El espectador piensa "me suena"
10: El espectador piensa "esto es exactamente mi vida"
Pregunta de control: ¿Lo compartiría con alguien?

CRITERIO 3 — TENSIÓN (0-10)
0: No hay nada sin resolver, el hook es completo en sí mismo
5: Hay algo que se puede intuir pero también ignorar
10: El espectador físicamente no puede no saber qué viene después
Pregunta de control: ¿Si cortas el vídeo aquí, alguien se siente frustrado?

CRITERIO 4 — CLARIDAD (0-10)
0: Necesitas leerlo dos veces para entenderlo
5: Se entiende pero hay que pensar un segundo
10: Primera lectura, cero fricción, cero ambigüedad
Pregunta de control: ¿Alguien que no sabe qué es AACC lo entiende igualmente?

CRITERIO 5 — TONO NOA (0-10)
0: Suena a anuncio, a coach motivacional, a cuenta de autoayuda
5: Correcto pero neutro, podría ser cualquier cuenta de crianza
10: Solo puede ser NOA: empático, directo, sin paternalismos, sin bullshit
Pregunta de control: ¿Lo diría una amiga de confianza o lo diría un manual?

PUNTUACIÓN MÍNIMA PARA PRODUCCIÓN: 38/50
PUNTUACIÓN DE REFERENCIA PARA HOOKS ESTRELLA: 45/50 o más
```

---

## CONFIGURACIÓN DE API PARA GENERACIÓN DE HOOKS

```python
import anthropic
import json

client = anthropic.Anthropic()

system_prompt = """[Insertar el system prompt de arriba]"""

def generar_hooks(tema: str, cantidad: int = 5, tipo: str = "todos"):
    user_message = f"""
    Genera {cantidad} hooks virales para un vídeo sobre: {tema}
    
    Tipo de hooks solicitado: {tipo}
    (opciones: conflictos_cotidianos / momentos_emocionales / agotamiento_culpa / todos)
    
    Para cada hook, devuelve el JSON con todos los campos incluyendo la puntuación.
    Solo el array JSON. Sin texto adicional.
    """
    
    response = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=2048,
        temperature=1,
        system=system_prompt,
        messages=[{"role": "user", "content": user_message}]
    )
    
    return json.loads(response.content[0].text)

# Uso:
hooks = generar_hooks(
    tema="explosión emocional después del colegio",
    cantidad=5,
    tipo="momentos_emocionales"
)
```
