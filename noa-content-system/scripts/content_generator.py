#!/usr/bin/env python3
"""
content_generator.py — Generador de contenido para la app NOA.

Genera ideas, hooks, guiones y copy de publicación para Instagram/TikTok
usando la API de Claude (Anthropic). Guarda los resultados en Airtable
y en archivos JSON locales.

La app NOA ayuda a padres de adolescentes con Altas Capacidades (AACC)
a comprender y acompañar a sus hijos de forma efectiva.

Uso:
    python content_generator.py ideas --count 10
    python content_generator.py hooks --idea-id ABC123
    python content_generator.py script --idea-id ABC123 --format error-tipico
    python content_generator.py copy --script-id DEF456 --platform instagram
    python content_generator.py copy --script-id DEF456 --platform tiktok
"""

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import Any, Optional

# ─────────────────────────────────────────────
# Carga de variables de entorno
# ─────────────────────────────────────────────
try:
    from dotenv import load_dotenv
    _env_path = Path(__file__).resolve().parent.parent / ".env"
    if _env_path.exists():
        load_dotenv(_env_path)
except ImportError:
    pass  # Usaremos variables del sistema si python-dotenv no está instalado

# ─────────────────────────────────────────────
# Configuración de logging
# ─────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s — %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("noa.content_generator")

# ─────────────────────────────────────────────
# Rutas del proyecto
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs" / "raw"
CONFIG_PATH = BASE_DIR / "config.json"


# ─────────────────────────────────────────────────────────────────────────────
# CARGA DE CONFIGURACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def load_config() -> dict[str, Any]:
    """
    Carga la configuración del proyecto desde config.json.

    Returns:
        Diccionario con la configuración completa del proyecto.

    Raises:
        FileNotFoundError: Si config.json no existe (ejecuta setup_project.py primero).
    """
    if not CONFIG_PATH.exists():
        logger.error(f"No se encontró config.json en {CONFIG_PATH}")
        logger.error("Ejecuta primero: python scripts/setup_project.py")
        raise FileNotFoundError(f"Archivo de configuración no encontrado: {CONFIG_PATH}")

    with open(CONFIG_PATH, encoding="utf-8") as f:
        config = json.load(f)

    logger.debug(f"Configuración cargada desde {CONFIG_PATH}")
    return config


# ─────────────────────────────────────────────────────────────────────────────
# CLIENTE ANTHROPIC — con reintentos y rate limiting
# ─────────────────────────────────────────────────────────────────────────────

class AnthropicClient:
    """
    Wrapper del SDK de Anthropic con reintentos exponenciales y control de tasa.
    """

    # Modelo recomendado para contenido de marketing: balance coste/calidad
    MODELO = "claude-sonnet-4-5"
    MAX_TOKENS = 4096
    MAX_REINTENTOS = 3
    PAUSA_BASE_SEGUNDOS = 2.0

    def __init__(self) -> None:
        """Inicializa el cliente Anthropic con la clave API del entorno."""
        try:
            import anthropic
            self._anthropic = anthropic
        except ImportError:
            logger.error("SDK de Anthropic no instalado. Ejecuta: pip install anthropic")
            raise

        api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise EnvironmentError(
                "ANTHROPIC_API_KEY no configurada. "
                "Añádela a tu archivo .env o variables de entorno."
            )

        self.cliente = self._anthropic.Anthropic(api_key=api_key)
        logger.info(f"Cliente Anthropic inicializado (modelo: {self.MODELO})")

    def completar(
        self,
        system_prompt: str,
        user_message: str,
        temperatura: float = 0.85,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Envía una solicitud a la API de Claude con reintentos en caso de error.

        Args:
            system_prompt: Instrucciones de comportamiento para el modelo.
            user_message: El mensaje del usuario / tarea concreta.
            temperatura: Control de creatividad (0.0–1.0).
            max_tokens: Máximo de tokens en la respuesta.

        Returns:
            El texto de la respuesta generada por Claude.

        Raises:
            RuntimeError: Si se agotan los reintentos.
        """
        tokens = max_tokens or self.MAX_TOKENS
        ultimo_error: Optional[Exception] = None

        for intento in range(1, self.MAX_REINTENTOS + 1):
            try:
                logger.debug(f"Llamada a Claude — intento {intento}/{self.MAX_REINTENTOS}")
                respuesta = self.cliente.messages.create(
                    model=self.MODELO,
                    max_tokens=tokens,
                    system=system_prompt,
                    messages=[{"role": "user", "content": user_message}],
                )
                texto = respuesta.content[0].text.strip()
                logger.debug(f"Respuesta recibida ({len(texto)} caracteres)")
                return texto

            except self._anthropic.RateLimitError as e:
                pausa = self.PAUSA_BASE_SEGUNDOS * (2 ** intento)
                logger.warning(f"Rate limit alcanzado — esperando {pausa:.0f}s (intento {intento})")
                time.sleep(pausa)
                ultimo_error = e

            except self._anthropic.APIStatusError as e:
                logger.error(f"Error de API de Anthropic (status {e.status_code}): {e.message}")
                if e.status_code in (500, 529):
                    # Error del servidor, reintentamos
                    pausa = self.PAUSA_BASE_SEGUNDOS * intento
                    logger.warning(f"Servidor de Anthropic con problemas — esperando {pausa:.0f}s")
                    time.sleep(pausa)
                    ultimo_error = e
                else:
                    # Error del cliente (autenticación, etc.) — no reintentamos
                    raise

            except Exception as e:
                logger.error(f"Error inesperado en llamada a Claude: {e}")
                raise

        raise RuntimeError(
            f"Se agotaron {self.MAX_REINTENTOS} reintentos al llamar a Claude. "
            f"Último error: {ultimo_error}"
        )


# ─────────────────────────────────────────────────────────────────────────────
# CLIENTE AIRTABLE
# ─────────────────────────────────────────────────────────────────────────────

class AirtableClient:
    """
    Wrapper de pyairtable para operaciones CRUD en la base de contenido NOA.
    """

    def __init__(self, config: dict[str, Any]) -> None:
        """
        Inicializa el cliente de Airtable.

        Args:
            config: Configuración del proyecto (contiene nombres de tablas).
        """
        try:
            from pyairtable import Api
            self._Api = Api
        except ImportError:
            logger.warning("pyairtable no instalado — las operaciones de Airtable fallarán.")
            self._Api = None  # type: ignore

        self.api_key = os.environ.get("AIRTABLE_API_KEY")
        self.base_id = os.environ.get("AIRTABLE_BASE_ID")
        self.tablas = config.get("airtable", {}).get("tablas", {})
        self._api: Any = None

        if self.api_key and self.base_id and self._Api:
            try:
                self._api = self._Api(self.api_key)
                logger.info("Cliente Airtable inicializado correctamente")
            except Exception as e:
                logger.warning(f"No se pudo inicializar Airtable: {e}")

    @property
    def disponible(self) -> bool:
        """True si Airtable está configurado y disponible."""
        return self._api is not None and bool(self.api_key) and bool(self.base_id)

    def crear_registro(self, tabla_clave: str, campos: dict[str, Any]) -> Optional[str]:
        """
        Crea un nuevo registro en la tabla especificada.

        Args:
            tabla_clave: Clave interna de la tabla (ej: 'ideas', 'scripts').
            campos: Diccionario con los campos del registro.

        Returns:
            ID del registro creado, o None si falló.
        """
        if not self.disponible:
            logger.debug("Airtable no disponible — saltando creación de registro")
            return None

        nombre_tabla = self.tablas.get(tabla_clave, tabla_clave)
        try:
            tabla = self._api.table(self.base_id, nombre_tabla)
            registro = tabla.create(campos)
            record_id = registro["id"]
            logger.info(f"Registro creado en Airtable ({nombre_tabla}): {record_id}")
            return record_id
        except Exception as e:
            logger.error(f"Error al crear registro en Airtable ({nombre_tabla}): {e}")
            return None

    def obtener_registro(self, tabla_clave: str, record_id: str) -> Optional[dict[str, Any]]:
        """
        Obtiene un registro por su ID.

        Args:
            tabla_clave: Clave interna de la tabla.
            record_id: ID del registro a obtener.

        Returns:
            Diccionario con los campos del registro, o None si no se encontró.
        """
        if not self.disponible:
            return None

        nombre_tabla = self.tablas.get(tabla_clave, tabla_clave)
        try:
            tabla = self._api.table(self.base_id, nombre_tabla)
            registro = tabla.get(record_id)
            return registro.get("fields", {})
        except Exception as e:
            logger.error(f"Error al obtener registro {record_id} de Airtable: {e}")
            return None

    def actualizar_registro(self, tabla_clave: str, record_id: str, campos: dict[str, Any]) -> bool:
        """
        Actualiza campos de un registro existente.

        Args:
            tabla_clave: Clave interna de la tabla.
            record_id: ID del registro a actualizar.
            campos: Campos a actualizar.

        Returns:
            True si la actualización fue exitosa.
        """
        if not self.disponible:
            return False

        nombre_tabla = self.tablas.get(tabla_clave, tabla_clave)
        try:
            tabla = self._api.table(self.base_id, nombre_tabla)
            tabla.update(record_id, campos)
            logger.info(f"Registro actualizado en Airtable ({nombre_tabla}): {record_id}")
            return True
        except Exception as e:
            logger.error(f"Error al actualizar registro {record_id} en Airtable: {e}")
            return False


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIONES DE PERSISTENCIA LOCAL
# ─────────────────────────────────────────────────────────────────────────────

def save_locally(data: dict[str, Any], categoria: str) -> str:
    """
    Guarda datos en un archivo JSON local dentro de outputs/raw/.

    El nombre del archivo sigue la convención NOA:
    NOA_YYYYMMDD_HHMMSS_{categoria}.json

    Args:
        data: Diccionario con los datos a guardar.
        categoria: Categoría del contenido (ej: 'idea', 'hook', 'script', 'copy').

    Returns:
        Ruta absoluta al archivo guardado.
    """
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nombre_archivo = f"NOA_{timestamp}_{categoria.upper()}.json"
    ruta_archivo = OUTPUTS_DIR / nombre_archivo

    # Añadimos metadatos de generación
    data_con_meta = {
        "_meta": {
            "generado_en": datetime.now().isoformat(),
            "categoria": categoria,
            "version": "1.0",
            "sistema": "NOA Content Automation",
        },
        **data,
    }

    with open(ruta_archivo, "w", encoding="utf-8") as f:
        json.dump(data_con_meta, f, ensure_ascii=False, indent=2)

    logger.info(f"Datos guardados localmente: {ruta_archivo}")
    return str(ruta_archivo)


def save_to_airtable(
    airtable: AirtableClient,
    tabla: str,
    data: dict[str, Any],
) -> str:
    """
    Guarda un registro en Airtable. Si falla, devuelve un ID local temporal.

    Args:
        airtable: Cliente de Airtable inicializado.
        tabla: Clave de la tabla destino.
        data: Campos a guardar.

    Returns:
        ID del registro en Airtable, o ID local temporal si Airtable no está disponible.
    """
    record_id = airtable.crear_registro(tabla, data)
    if record_id:
        return record_id

    # Fallback: generamos un ID local para trazabilidad
    import hashlib
    contenido_hash = hashlib.md5(json.dumps(data, sort_keys=True).encode()).hexdigest()[:8].upper()
    id_local = f"LOCAL_{contenido_hash}"
    logger.warning(f"Airtable no disponible — usando ID local: {id_local}")
    return id_local


# ─────────────────────────────────────────────────────────────────────────────
# PROMPTS DEL SISTEMA — Específicos para NOA/AACC
# ─────────────────────────────────────────────────────────────────────────────

SYSTEM_PROMPT_IDEAS = """\
Eres el estratega de contenido de NOA, una app para padres de adolescentes con Altas Capacidades (AACC).

CONTEXTO DE LA APP NOA:
NOA es una app móvil que ayuda a padres de adolescentes con AACC (sobredotación intelectual) a:
- Entender los comportamientos intensos y las crisis emocionales de sus hijos
- Comunicarse mejor sin conflictos constantes
- Distinguir qué es AACC y qué es adolescencia normal
- Dejar de sentirse solos, culpables o agotados
- Tomar decisiones educativas (cambio de centro, enriquecimiento, etc.)

AUDIENCIA OBJETIVO:
- Padres y madres de adolescentes de 12-18 años diagnosticados o en proceso de diagnóstico con AACC
- Nivel sociocultural medio-alto
- Agotados, confundidos, amando profundamente a sus hijos pero sin saber cómo ayudarles
- Se identifican más con "mi hijo es muy intenso" que con "mi hijo es superdotado"
- Usan Instagram y TikTok, ven Reels, siguen cuentas de psicología y parentalidad

PILARES DE CONTENIDO NOA:
1. TOFU (40%): Contenido de descubrimiento — conflictos diarios, momentos de agotamiento, escenas reconocibles
2. MOFU (40%): Educación y herramientas — qué es AACC de verdad, mitos, técnicas de comunicación
3. BOFU (20%): Conversión directa — CTA a NOA, testimonios, beneficios concretos de la app

VOZ Y TONO:
- Cálida pero directa. Como una amiga que también vivió esto y encontró el camino
- Sin tecnicismos innecesarios, pero precisa psicológicamente
- Valida el dolor antes de ofrecer soluciones
- Nunca juzga a los padres — ellos ya se sienten suficientemente culpables
- Usa el nombre "NOA" solo al final como CTA, no en el contenido del video

FORMATOS DE VÍDEO DISPONIBLES:
- error-tipico: "El error que todos los padres cometen con sus hijos AACC"
- mito-vs-realidad: "Mito: los niños con AACC son felices en el cole. Realidad: el 73% sufre acoso"
- antes-despues: Transformación emocional de padre/madre
- consejo-rapido: 3 pasos accionables en 30 segundos
- historia-real: Narración de un momento real de familia AACC
- pregunta-reflexion: Pregunta que golpea en el pecho y hace parar el scroll

Cuando generes ideas, devuelve SIEMPRE un JSON válido con esta estructura exacta:
{
  "ideas": [
    {
      "titulo": "Título interno de la idea (no es el hook)",
      "pilar": "TOFU|MOFU|BOFU",
      "formato": "error-tipico|mito-vs-realidad|antes-despues|consejo-rapido|historia-real|pregunta-reflexion",
      "conflicto_central": "El dolor o situación específica que aborda",
      "angulo_emocional": "La emoción que queremos activar en el espectador",
      "dato_o_verdad_inesperada": "Dato, estadística o verdad contraintuitiva que sorprende",
      "cta_sugerido": "Llamada a la acción específica para este contenido",
      "palabras_clave_seo": ["keyword1", "keyword2", "keyword3"],
      "urgencia": "alta|media|baja",
      "notas_produccion": "Indicaciones para grabación, música, ritmo visual"
    }
  ]
}
"""

SYSTEM_PROMPT_HOOKS = """\
Eres el especialista en hooks virales de NOA, la app para padres de adolescentes con AACC.

Tu misión: crear los primeros 2 segundos que paran el scroll en Instagram y TikTok.

REGLAS DE ORO DE LOS HOOKS NOA:
1. ESPECIFICIDAD: No "tu hijo con AACC", sino "cuando tu hijo te dice 'os odio' y te cierra la puerta"
2. EMOCIÓN INMEDIATA: La primera palabra debe activar algo — culpa, reconocimiento, sorpresa, miedo
3. PROMESA IMPLÍCITA: El hook debe prometer que lo que viene después cambiará algo
4. LONGITUD: Máximo 12 palabras. Menos es más.
5. CONVERSACIONAL: Como si lo dijera una madre a otra madre, no un psicólogo en una conferencia
6. PROHIBIDO: Emojis en el hook, tecnicismos, "altas capacidades" en el hook (demasiado frío)

TIPOS DE HOOKS QUE FUNCIONAN EN AACC:
- Confesión de culpa: "Durante años pensé que el problema era yo..."
- Escena reconocible: "Cuando tu hijo lleva 3 días sin salir de la habitación..."
- Dato que rompe la idea: "El 68% de adolescentes con AACC nunca llega a ser diagnosticado"
- Pregunta que duele: "¿Cuándo fue la última vez que tu hijo te sonrió de verdad?"
- Contradicción: "Tener un hijo brillante puede ser lo más agotador del mundo"
- Error común: "Lo que creías que motivaba a tu hijo en realidad le bloquea"

Devuelve SIEMPRE un JSON válido con esta estructura:
{
  "hooks": [
    {
      "texto": "El hook completo listo para usar",
      "tipo": "confesion|escena|dato|pregunta|contradiccion|error",
      "emocion_activada": "culpa|reconocimiento|sorpresa|miedo|esperanza|curiosidad",
      "segundos_estimados_lectura": 2,
      "variante_tiktok": "Versión ligeramente adaptada para TikTok si aplica",
      "nota": "Por qué funciona este hook específico"
    }
  ]
}
"""

SYSTEM_PROMPT_SCRIPT = """\
Eres el guionista principal de NOA, la app para padres de adolescentes con AACC.

Escribes guiones para vídeos de 20-45 segundos que se publican como Reels en Instagram y TikToks.
Los vídeos son narración en voz en off (la voz de NOA) sobre imágenes o texto animado.

ESTRUCTURA DEL GUION NOA:
1. HOOK (0-3 seg): La frase de apertura que para el scroll — ya la tienes, úsala
2. PROBLEMA/CONFLICTO (3-12 seg): Ampliar la herida emocional, hacerla reconocible
3. GIRO/REVELACIÓN (12-25 seg): La perspectiva nueva, el dato inesperado, la verdad incómoda
4. SOLUCIÓN/ALIVIO (25-38 seg): El camino, no la solución completa — eso lo da NOA
5. CTA (38-45 seg): Llamada a la acción natural, integrada, no agresiva

REGLAS DE ESCRITURA DEL GUION:
- Escribe como se habla, no como se escribe. Lee en voz alta y si suena raro, reescribe.
- Frases cortas. Punto. Seguido. Como esto.
- Una idea por frase. Nunca dos.
- Evita: "además", "también", "por otro lado", "en conclusión"
- Usa: "Y eso es agotador.", "Pero hay algo que nadie te dijo.", "Esto cambia todo."
- La voz es de madre a madre — cálida, directa, sin condescendencia
- El CTA siempre nombra NOA y da una acción concreta (descargar, hacer el test, etc.)

FORMATOS ESPECÍFICOS:

error-tipico:
  - Hook: El error en primera persona o tercera
  - Conflicto: Por qué todos lo cometen (no es su culpa)
  - Giro: Lo que en realidad necesita el hijo AACC
  - Solución: Qué cambiar (pista, no manual completo)
  - CTA: "En NOA encuentras exactamente cómo hacerlo"

mito-vs-realidad:
  - Hook: El mito como verdad afirmada
  - Conflicto: Por qué este mito hace daño real
  - Giro: La realidad con dato o ejemplo concreto
  - Solución: Qué significa esto para las familias
  - CTA: "NOA tiene el test para saber dónde está tu hijo"

Devuelve SIEMPRE un JSON válido con esta estructura:
{
  "guion": {
    "titulo_interno": "Nombre del vídeo para uso interno",
    "formato": "El formato del vídeo",
    "duracion_estimada_segundos": 35,
    "segmentos": [
      {
        "nombre": "hook|problema|giro|solucion|cta",
        "tiempo_inicio": 0,
        "tiempo_fin": 3,
        "texto_locucion": "Texto exacto que leerá la voz en off",
        "texto_pantalla": "Texto que aparece en pantalla (puede diferir o ser null)",
        "nota_produccion": "Indicaciones de ritmo, énfasis, emoción"
      }
    ],
    "guion_completo": "Todo el texto de locución seguido, listo para ElevenLabs",
    "palabras_clave_subtitulos": ["palabras", "a", "enfatizar", "en", "subtitulos"],
    "musica_sugerida": "Descripción del estilo musical (tempo, emoción, género)",
    "hashtags_especificos": ["#hashtag1", "#hashtag2"]
  }
}
"""

SYSTEM_PROMPT_COPY = """\
Eres el copywriter de publicación de NOA, la app para padres de adolescentes con AACC.

Escribes el copy para la publicación en redes sociales: el caption de Instagram y la descripción de TikTok.

INSTAGRAM CAPTION (máx 2200 caracteres, pero ideal 150-300):
- Primera línea = HOOK del vídeo (para que aparezca antes del "ver más")
- Segundo párrafo: Amplía el contenido del vídeo, no lo repite
- Pregunta al final: Activa comentarios ("¿Te pasa esto?", "¿Cuántas veces has pensado esto?")
- CTA claro: Link en bio / Descarga NOA / Haz el test gratis
- Salto de línea entre párrafos con punto o emoji de separación
- Hashtags al final en bloque separado (30 hashtags)

TIKTOK DESCRIPCIÓN (máx 300 caracteres):
- Hook de 1 frase (los primeros 50 caracteres son los más importantes)
- Máx 3-4 hashtags integrados en el texto, no en bloque separado
- Sin link directo (no funciona en TikTok) — mencionar "link en bio" si hay CTA

TONO POR PLATAFORMA:
- Instagram: Más reflexivo, emocional, permite texto más largo
- TikTok: Más inmediato, coloquial, directo al grano

Devuelve SIEMPRE un JSON válido con esta estructura:
{
  "copy": {
    "plataforma": "instagram|tiktok",
    "caption_completo": "El texto completo listo para copiar y pegar",
    "primera_linea": "Solo la primera línea visible antes del 'ver más'",
    "cuerpo": "El resto del caption sin hashtags",
    "pregunta_engagement": "La pregunta que activa comentarios",
    "cta": "La llamada a la acción exacta",
    "hashtags": ["#hashtag1", "#hashtag2"],
    "emojis_sugeridos": ["emoji1", "emoji2"],
    "mejor_hora_publicacion": "HH:MM zona horaria España (CET/CEST)",
    "notas": "Observaciones adicionales sobre la publicación"
  }
}
"""


# ─────────────────────────────────────────────────────────────────────────────
# FUNCIONES DE GENERACIÓN
# ─────────────────────────────────────────────────────────────────────────────

def _parsear_json_respuesta(respuesta: str, clave_raiz: str) -> Any:
    """
    Extrae y parsea JSON de la respuesta de Claude.

    Claude a veces envuelve el JSON en bloques de código (```json...```).
    Esta función lo limpia y lo parsea.

    Args:
        respuesta: Texto completo de la respuesta de Claude.
        clave_raiz: Clave raíz del JSON esperado (ej: 'ideas', 'hooks', 'guion').

    Returns:
        El valor de la clave raíz parseada.

    Raises:
        ValueError: Si no se puede parsear el JSON.
    """
    texto = respuesta.strip()

    # Eliminar bloques de código markdown si existen
    if "```json" in texto:
        inicio = texto.index("```json") + 7
        fin = texto.rindex("```")
        texto = texto[inicio:fin].strip()
    elif "```" in texto:
        inicio = texto.index("```") + 3
        fin = texto.rindex("```")
        texto = texto[inicio:fin].strip()

    try:
        datos = json.loads(texto)
    except json.JSONDecodeError as e:
        logger.error(f"Error parseando JSON de Claude: {e}")
        logger.debug(f"Respuesta recibida:\n{respuesta[:500]}...")
        raise ValueError(f"La respuesta de Claude no es JSON válido: {e}") from e

    if clave_raiz not in datos:
        raise ValueError(
            f"La respuesta de Claude no contiene la clave '{clave_raiz}'. "
            f"Claves disponibles: {list(datos.keys())}"
        )

    return datos[clave_raiz]


def generate_ideas(
    count: int,
    claude: AnthropicClient,
    airtable: AirtableClient,
    config: dict[str, Any],
) -> list[dict[str, Any]]:
    """
    Genera ideas de contenido para vídeos de NOA usando Claude.

    Se enfoca en conflictos familiares diarios, momentos de agotamiento parental
    y situaciones reconocibles para padres de adolescentes con AACC.

    Args:
        count: Número de ideas a generar.
        claude: Cliente de Anthropic.
        airtable: Cliente de Airtable.
        config: Configuración del proyecto.

    Returns:
        Lista de diccionarios con las ideas generadas.
    """
    print(f"\n🎯 Generando {count} ideas de contenido NOA...")
    logger.info(f"Iniciando generación de {count} ideas de contenido")

    hashtags_core = config.get("hashtags", {}).get("hashtags_core", [])
    formatos = config.get("contenido", {}).get("formatos_video", [])

    mensaje_usuario = f"""
Genera exactamente {count} ideas de contenido para vídeos cortos de NOA.

CONTEXTO ACTUAL (semana del {datetime.now().strftime('%d/%m/%Y')}):
- Temporada: {'vuelta al cole' if datetime.now().month in [9, 10] else 'curso escolar activo' if datetime.now().month in [1, 2, 3, 4, 5] else 'verano/vacaciones'}
- Hashtags core a tener en cuenta: {', '.join(hashtags_core)}
- Formatos disponibles: {', '.join(formatos)}

DISTRIBUCIÓN REQUERIDA de las {count} ideas:
- {round(count * 0.40)} ideas TOFU (conflictos diarios reconocibles)
- {round(count * 0.40)} ideas MOFU (educación, mitos, herramientas)
- {round(count * 0.20)} ideas BOFU (conversión directa a NOA)

TEMAS PRIORITARIOS ESTA SEMANA:
1. Conflictos a la hora de estudiar / hacer deberes con adolescentes AACC
2. El aislamiento social del adolescente superdotado (no encaja, no tiene amigos)
3. Las explosiones emocionales que "no tienen sentido" pero tienen todo el sentido
4. El agotamiento del padre/madre que no sabe si está haciendo bien las cosas
5. Las decisiones educativas (¿cambiamos de cole?, ¿le ponemos en un programa de enriquecimiento?)

Asegúrate de que cada idea sea diferente y aborde un ángulo único.
Devuelve exactamente {count} ideas en el JSON solicitado.
"""

    respuesta = claude.completar(
        system_prompt=SYSTEM_PROMPT_IDEAS,
        user_message=mensaje_usuario,
        temperatura=0.90,  # Alta creatividad para ideas
    )

    ideas_raw = _parsear_json_respuesta(respuesta, "ideas")

    # Enriquecemos cada idea con metadatos y la guardamos
    ideas_procesadas = []
    for idx, idea in enumerate(ideas_raw[:count], start=1):
        idea_completa = {
            "id_generacion": f"IDEA_{datetime.now().strftime('%Y%m%d')}_{idx:03d}",
            "estado": "generada",
            "fecha_generacion": datetime.now().isoformat(),
            **idea,
        }

        # Guardar en Airtable
        record_id = save_to_airtable(airtable, "ideas", {
            "ID Generación": idea_completa["id_generacion"],
            "Título": idea_completa.get("titulo", "Sin título"),
            "Pilar": idea_completa.get("pilar", "TOFU"),
            "Formato": idea_completa.get("formato", ""),
            "Conflicto Central": idea_completa.get("conflicto_central", ""),
            "Ángulo Emocional": idea_completa.get("angulo_emocional", ""),
            "Dato/Verdad": idea_completa.get("dato_o_verdad_inesperada", ""),
            "CTA Sugerido": idea_completa.get("cta_sugerido", ""),
            "Estado": "Generada",
        })
        idea_completa["airtable_id"] = record_id

        ideas_procesadas.append(idea_completa)
        print(f"  ✓ Idea {idx}/{count}: {idea_completa.get('titulo', 'Sin título')} [{idea_completa.get('pilar')}]")

    # Guardar todo el lote localmente
    ruta_local = save_locally(
        {"ideas": ideas_procesadas, "total": len(ideas_procesadas)},
        categoria="ideas",
    )
    print(f"\n✓ {len(ideas_procesadas)} ideas guardadas")
    print(f"  Archivo local: {ruta_local}")

    return ideas_procesadas


def generate_hooks(
    idea: dict[str, Any],
    claude: AnthropicClient,
    airtable: AirtableClient,
) -> list[str]:
    """
    Genera 5 variantes de hook para una idea de contenido específica.

    Los hooks son los primeros 2 segundos del vídeo que deben parar el scroll.
    Son emocionales, directos y específicos al mundo de las familias AACC.

    Args:
        idea: Diccionario con los datos de la idea (de generate_ideas).
        claude: Cliente de Anthropic.
        airtable: Cliente de Airtable.

    Returns:
        Lista de textos de hook (mínimo 5).
    """
    print(f"\n🪝 Generando hooks para: {idea.get('titulo', 'idea sin título')}...")
    logger.info(f"Generando hooks para idea: {idea.get('id_generacion', 'desconocida')}")

    mensaje_usuario = f"""
Genera 5 hooks para este vídeo de NOA:

IDEA:
- Título interno: {idea.get('titulo', '')}
- Pilar: {idea.get('pilar', '')}
- Formato: {idea.get('formato', '')}
- Conflicto central: {idea.get('conflicto_central', '')}
- Ángulo emocional: {idea.get('angulo_emocional', '')}
- Dato/verdad inesperada: {idea.get('dato_o_verdad_inesperada', '')}

REQUISITOS:
- 5 hooks completamente diferentes en estructura y enfoque
- Al menos uno de cada tipo: confesion, escena, dato, pregunta, contradiccion
- Todos deben estar relacionados directamente con el conflicto central
- Longitud: 6-12 palabras cada uno
- En español de España (no usar "vos", usar "tú")

Ordénalos de más a menos impactante según tu criterio.
"""

    respuesta = claude.completar(
        system_prompt=SYSTEM_PROMPT_HOOKS,
        user_message=mensaje_usuario,
        temperatura=0.92,  # Máxima creatividad para hooks
    )

    hooks_raw = _parsear_json_respuesta(respuesta, "hooks")

    # Extraer solo el texto de cada hook
    hooks_texto = [h["texto"] for h in hooks_raw if "texto" in h]

    # Actualizar registro de Airtable de la idea con los hooks
    airtable_id = idea.get("airtable_id")
    if airtable_id and not airtable_id.startswith("LOCAL_"):
        hooks_json = json.dumps(hooks_raw, ensure_ascii=False)
        airtable.actualizar_registro("ideas", airtable_id, {
            "Hooks Generados": hooks_json[:5000],  # Airtable tiene límite de caracteres
            "Estado": "Hooks generados",
        })

    # Guardar localmente
    save_locally(
        {
            "idea_id": idea.get("id_generacion", ""),
            "idea_titulo": idea.get("titulo", ""),
            "hooks": hooks_raw,
        },
        categoria="hooks",
    )

    for idx, hook in enumerate(hooks_texto, start=1):
        print(f"  {idx}. {hook}")

    print(f"\n✓ {len(hooks_texto)} hooks generados")
    return hooks_texto


def generate_script(
    idea: dict[str, Any],
    format_type: str,
    claude: AnthropicClient,
    airtable: AirtableClient,
    hook_seleccionado: Optional[str] = None,
) -> dict[str, Any]:
    """
    Genera el guion completo de un vídeo NOA de 20-45 segundos.

    El guion incluye texto de locución por segmento, indicaciones de producción,
    texto para pantalla y el guion completo listo para enviar a ElevenLabs.

    Args:
        idea: Diccionario con los datos de la idea.
        format_type: Tipo de formato (error-tipico, mito-vs-realidad, etc.).
        claude: Cliente de Anthropic.
        airtable: Cliente de Airtable.
        hook_seleccionado: Hook específico a usar (opcional, Claude elegirá si no se da).

    Returns:
        Diccionario con el guion completo y sus metadatos.
    """
    print(f"\n📝 Generando guion [{format_type}] para: {idea.get('titulo', 'idea sin título')}...")
    logger.info(f"Generando guion formato '{format_type}' para: {idea.get('id_generacion', '')}")

    formatos_validos = [
        "error-tipico", "mito-vs-realidad", "antes-despues",
        "consejo-rapido", "historia-real", "pregunta-reflexion",
    ]
    if format_type not in formatos_validos:
        raise ValueError(
            f"Formato '{format_type}' no válido. "
            f"Opciones: {', '.join(formatos_validos)}"
        )

    hook_instruccion = (
        f"Usa este hook exacto como apertura: '{hook_seleccionado}'"
        if hook_seleccionado
        else "Crea el hook más potente que puedas para esta idea"
    )

    mensaje_usuario = f"""
Escribe el guion completo para este vídeo de NOA:

IDEA:
- Título: {idea.get('titulo', '')}
- Pilar: {idea.get('pilar', '')}
- Formato requerido: {format_type}
- Conflicto central: {idea.get('conflicto_central', '')}
- Ángulo emocional: {idea.get('angulo_emocional', '')}
- Dato/verdad: {idea.get('dato_o_verdad_inesperada', '')}
- CTA sugerido: {idea.get('cta_sugerido', '')}

HOOK: {hook_instruccion}

DURACIÓN OBJETIVO: 30-40 segundos (aprox. 90-110 palabras en el guion completo)

REQUISITOS ESPECÍFICOS PARA FORMATO '{format_type.upper()}':
- Sigue la estructura exacta de este formato según las instrucciones del sistema
- El CTA debe mencionar NOA y dar una acción concreta (descargar, test gratuito, etc.)
- Palabras clave a enfatizar en subtítulos: las 5-7 palabras más impactantes del guion

NOTAS DE PRODUCCIÓN:
- Notas de producción: {idea.get('notas_produccion', 'Sin notas específicas')}
- Voz: femenina, cálida, ritmo natural — como una amiga hablando, no un anuncio
"""

    respuesta = claude.completar(
        system_prompt=SYSTEM_PROMPT_SCRIPT,
        user_message=mensaje_usuario,
        temperatura=0.80,  # Creatividad controlada para guiones
    )

    guion_raw = _parsear_json_respuesta(respuesta, "guion")

    # Enriquecemos con metadatos
    guion_completo = {
        "id_guion": f"SCRIPT_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "idea_id": idea.get("id_generacion", ""),
        "idea_airtable_id": idea.get("airtable_id", ""),
        "formato": format_type,
        "estado": "generado",
        "fecha_generacion": datetime.now().isoformat(),
        "hook_utilizado": hook_seleccionado or "generado automáticamente",
        **guion_raw,
    }

    # Guardar en Airtable (tabla de scripts)
    record_id = save_to_airtable(airtable, "scripts", {
        "ID Guion": guion_completo["id_guion"],
        "Idea ID": idea.get("id_generacion", ""),
        "Título": guion_raw.get("titulo_interno", ""),
        "Formato": format_type,
        "Duración Estimada (seg)": guion_raw.get("duracion_estimada_segundos", 0),
        "Guion Completo": guion_raw.get("guion_completo", ""),
        "Música Sugerida": guion_raw.get("musica_sugerida", ""),
        "Estado": "Generado",
    })
    guion_completo["airtable_id"] = record_id

    # Guardar localmente
    ruta_local = save_locally(guion_completo, categoria="script")

    print(f"✓ Guion generado ({guion_raw.get('duracion_estimada_segundos', '?')} seg estimados)")
    print(f"  Guion completo ({len(guion_raw.get('guion_completo', ''))} caracteres):")
    print(f"  \"{guion_raw.get('guion_completo', '')[:120]}...\"")
    print(f"  Archivo local: {ruta_local}")

    return guion_completo


def generate_publication_copy(
    script: dict[str, Any],
    platform: str,
    claude: AnthropicClient,
    airtable: AirtableClient,
    config: dict[str, Any],
) -> dict[str, Any]:
    """
    Genera el copy de publicación para Instagram o TikTok a partir de un guion.

    Incluye caption completo, hashtags, CTA y hora óptima de publicación.

    Args:
        script: Diccionario con el guion generado (de generate_script).
        platform: Plataforma destino ('instagram' o 'tiktok').
        claude: Cliente de Anthropic.
        airtable: Cliente de Airtable.
        config: Configuración del proyecto (para hashtags).

    Returns:
        Diccionario con el copy completo de publicación.
    """
    platforms_validas = ["instagram", "tiktok"]
    if platform.lower() not in platforms_validas:
        raise ValueError(
            f"Plataforma '{platform}' no válida. "
            f"Opciones: {', '.join(platforms_validas)}"
        )

    platform = platform.lower()
    print(f"\n📱 Generando copy de publicación para {platform.upper()}...")
    logger.info(f"Generando copy para {platform} del guion: {script.get('id_guion', '')}")

    todos_hashtags = config.get("hashtags", {}).get("lista", [])
    hashtags_core = config.get("hashtags", {}).get("hashtags_core", [])
    guion_texto = script.get("guion_completo", "")
    guion_segmentos = script.get("segmentos", [])

    # Extraemos el texto de los segmentos para dar más contexto
    resumen_segmentos = "\n".join([
        f"- {seg.get('nombre', '').upper()}: {seg.get('texto_locucion', '')}"
        for seg in guion_segmentos
    ]) if guion_segmentos else "No disponible"

    mensaje_usuario = f"""
Genera el copy de publicación para {platform.upper()} de este vídeo de NOA:

GUION COMPLETO:
{guion_texto}

SEGMENTOS DEL VÍDEO:
{resumen_segmentos}

METADATOS:
- Formato del vídeo: {script.get('formato', '')}
- Duración estimada: {script.get('duracion_estimada_segundos', '?')} segundos
- Hook utilizado: {script.get('hook_utilizado', '')}
- Plataforma destino: {platform.upper()}

HASHTAGS DISPONIBLES (selecciona los más relevantes):
{' '.join(todos_hashtags)}

HASHTAGS CORE (incluir siempre):
{' '.join(hashtags_core)}

REQUISITOS ESPECÍFICOS PARA {platform.upper()}:
{'- Caption entre 150-300 caracteres idealmente (máx 2200)' if platform == 'instagram' else '- Descripción máx 300 caracteres'}
{'- 30 hashtags en bloque separado al final' if platform == 'instagram' else '- Máx 3-4 hashtags integrados en el texto'}
{'- Pregunta al final que active comentarios' if platform == 'instagram' else '- Sin links directos, mencionar "link en bio"'}
- CTA debe mencionar NOA y ser accionable
- Primera línea = hook del vídeo (para el preview antes del "ver más")
"""

    respuesta = claude.completar(
        system_prompt=SYSTEM_PROMPT_COPY,
        user_message=mensaje_usuario,
        temperatura=0.78,
    )

    copy_raw = _parsear_json_respuesta(respuesta, "copy")

    # Enriquecemos con metadatos
    copy_completo = {
        "id_copy": f"COPY_{platform.upper()}_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
        "script_id": script.get("id_guion", ""),
        "script_airtable_id": script.get("airtable_id", ""),
        "plataforma": platform,
        "estado": "generado",
        "fecha_generacion": datetime.now().isoformat(),
        **copy_raw,
    }

    # Guardar en Airtable (tabla de publicación)
    record_id = save_to_airtable(airtable, "publicacion", {
        "ID Copy": copy_completo["id_copy"],
        "Script ID": script.get("id_guion", ""),
        "Plataforma": platform.capitalize(),
        "Caption Completo": copy_raw.get("caption_completo", ""),
        "Primera Línea": copy_raw.get("primera_linea", ""),
        "CTA": copy_raw.get("cta", ""),
        "Mejor Hora": copy_raw.get("mejor_hora_publicacion", ""),
        "Estado": "Pendiente aprobación",
    })
    copy_completo["airtable_id"] = record_id

    # Guardar localmente
    ruta_local = save_locally(copy_completo, categoria=f"copy_{platform}")

    print(f"✓ Copy para {platform.upper()} generado")
    print(f"  Primera línea: \"{copy_raw.get('primera_linea', '')[:80]}...\"")
    print(f"  Mejor hora: {copy_raw.get('mejor_hora_publicacion', '?')}")
    print(f"  Hashtags: {len(copy_raw.get('hashtags', []))} etiquetas")
    print(f"  Archivo local: {ruta_local}")

    return copy_completo


# ─────────────────────────────────────────────────────────────────────────────
# CLI — Interfaz de línea de comandos con argparse
# ─────────────────────────────────────────────────────────────────────────────

def _inicializar_clientes() -> tuple[AnthropicClient, AirtableClient, dict[str, Any]]:
    """
    Inicializa todos los clientes y carga la configuración.

    Returns:
        Tupla con (cliente Anthropic, cliente Airtable, configuración).
    """
    config = load_config()
    claude = AnthropicClient()
    airtable = AirtableClient(config)

    if not airtable.disponible:
        print("⚠  Airtable no configurado — los datos solo se guardarán localmente.")

    return claude, airtable, config


def cmd_ideas(args: argparse.Namespace) -> None:
    """Subcomando: genera ideas de contenido."""
    print(f"\n{'='*60}")
    print(f"  NOA Content Generator — GENERACIÓN DE IDEAS")
    print(f"{'='*60}")

    if args.count < 1 or args.count > 50:
        print("Error: --count debe estar entre 1 y 50")
        sys.exit(1)

    claude, airtable, config = _inicializar_clientes()
    ideas = generate_ideas(args.count, claude, airtable, config)

    print(f"\n{'─'*60}")
    print(f"✓ Proceso completado. {len(ideas)} ideas generadas.")
    print(f"  Usa el ID de Airtable o el archivo JSON para continuar.")
    print(f"{'─'*60}\n")


def cmd_hooks(args: argparse.Namespace) -> None:
    """Subcomando: genera hooks para una idea existente."""
    print(f"\n{'='*60}")
    print(f"  NOA Content Generator — GENERACIÓN DE HOOKS")
    print(f"{'='*60}")

    claude, airtable, config = _inicializar_clientes()

    # Intentar obtener la idea de Airtable primero
    idea = airtable.obtener_registro("ideas", args.idea_id)

    if not idea:
        # Buscar en archivos locales
        print(f"  Buscando idea '{args.idea_id}' en archivos locales...")
        archivos_ideas = list(OUTPUTS_DIR.glob("*_IDEAS.json"))

        for archivo in sorted(archivos_ideas, reverse=True):
            with open(archivo, encoding="utf-8") as f:
                datos = json.load(f)
            for idea_local in datos.get("ideas", []):
                if idea_local.get("id_generacion") == args.idea_id or \
                   idea_local.get("airtable_id") == args.idea_id:
                    idea = idea_local
                    break
            if idea:
                break

    if not idea:
        print(f"Error: No se encontró la idea con ID '{args.idea_id}'")
        print("  Verifica el ID en Airtable o en los archivos JSON de outputs/raw/")
        sys.exit(1)

    hooks = generate_hooks(idea, claude, airtable)

    print(f"\n{'─'*60}")
    print(f"✓ {len(hooks)} hooks generados para: {idea.get('titulo', args.idea_id)}")
    print(f"{'─'*60}\n")


def cmd_script(args: argparse.Namespace) -> None:
    """Subcomando: genera el guion completo para una idea."""
    print(f"\n{'='*60}")
    print(f"  NOA Content Generator — GENERACIÓN DE GUION")
    print(f"{'='*60}")

    claude, airtable, config = _inicializar_clientes()

    # Buscar la idea
    idea = airtable.obtener_registro("ideas", args.idea_id)

    if not idea:
        archivos_ideas = list(OUTPUTS_DIR.glob("*_IDEAS.json"))
        for archivo in sorted(archivos_ideas, reverse=True):
            with open(archivo, encoding="utf-8") as f:
                datos = json.load(f)
            for idea_local in datos.get("ideas", []):
                if idea_local.get("id_generacion") == args.idea_id or \
                   idea_local.get("airtable_id") == args.idea_id:
                    idea = idea_local
                    break
            if idea:
                break

    if not idea:
        print(f"Error: No se encontró la idea con ID '{args.idea_id}'")
        sys.exit(1)

    guion = generate_script(
        idea=idea,
        format_type=args.format,
        claude=claude,
        airtable=airtable,
        hook_seleccionado=args.hook,
    )

    print(f"\n{'─'*60}")
    print(f"✓ Guion generado: {guion.get('id_guion')}")
    print(f"  Formato: {args.format} | Duración: {guion.get('duracion_estimada_segundos', '?')} seg")
    print(f"{'─'*60}\n")


def cmd_copy(args: argparse.Namespace) -> None:
    """Subcomando: genera copy de publicación para un guion."""
    print(f"\n{'='*60}")
    print(f"  NOA Content Generator — GENERACIÓN DE COPY")
    print(f"{'='*60}")

    claude, airtable, config = _inicializar_clientes()

    # Buscar el guion
    script = airtable.obtener_registro("scripts", args.script_id)

    if not script:
        archivos_scripts = list(OUTPUTS_DIR.glob("*_SCRIPT.json"))
        for archivo in sorted(archivos_scripts, reverse=True):
            with open(archivo, encoding="utf-8") as f:
                script_local = json.load(f)
            if script_local.get("id_guion") == args.script_id or \
               script_local.get("airtable_id") == args.script_id:
                script = script_local
                break

    if not script:
        print(f"Error: No se encontró el guion con ID '{args.script_id}'")
        sys.exit(1)

    plataforma = args.platform.lower()
    copy_resultado = generate_publication_copy(script, plataforma, claude, airtable, config)

    # Si se piden las dos plataformas, generamos ambas
    if args.both_platforms:
        otra_plataforma = "tiktok" if plataforma == "instagram" else "instagram"
        print(f"\n  Generando también para {otra_plataforma.upper()}...")
        generate_publication_copy(script, otra_plataforma, claude, airtable, config)

    print(f"\n{'─'*60}")
    print(f"✓ Copy generado para {plataforma.upper()}: {copy_resultado.get('id_copy')}")
    print(f"{'─'*60}\n")


def build_parser() -> argparse.ArgumentParser:
    """Construye el parser de argumentos de la CLI."""
    parser = argparse.ArgumentParser(
        prog="content_generator.py",
        description="Generador de contenido NOA — Ideas, hooks, guiones y copy para AACC",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos de uso:
  python content_generator.py ideas --count 10
  python content_generator.py hooks --idea-id IDEA_20250516_001
  python content_generator.py script --idea-id IDEA_20250516_001 --format error-tipico
  python content_generator.py script --idea-id recABC123 --format mito-vs-realidad --hook "¿Cuándo fue la última vez que tu hijo te sonrió de verdad?"
  python content_generator.py copy --script-id SCRIPT_20250516_143022 --platform instagram
  python content_generator.py copy --script-id SCRIPT_20250516_143022 --platform tiktok --both-platforms
        """,
    )

    subparsers = parser.add_subparsers(dest="comando", help="Operación a realizar")
    subparsers.required = True

    # ── Subcomando: ideas ────────────────────────────────────────────────────
    parser_ideas = subparsers.add_parser(
        "ideas",
        help="Genera ideas de contenido",
    )
    parser_ideas.add_argument(
        "--count",
        type=int,
        default=5,
        metavar="N",
        help="Número de ideas a generar (1-50, default: 5)",
    )
    parser_ideas.set_defaults(func=cmd_ideas)

    # ── Subcomando: hooks ────────────────────────────────────────────────────
    parser_hooks = subparsers.add_parser(
        "hooks",
        help="Genera hooks para una idea existente",
    )
    parser_hooks.add_argument(
        "--idea-id",
        required=True,
        metavar="ID",
        help="ID de la idea (Airtable recXXX o IDEA_YYYYMMDD_NNN)",
    )
    parser_hooks.set_defaults(func=cmd_hooks)

    # ── Subcomando: script ───────────────────────────────────────────────────
    parser_script = subparsers.add_parser(
        "script",
        help="Genera el guion completo para una idea",
    )
    parser_script.add_argument(
        "--idea-id",
        required=True,
        metavar="ID",
        help="ID de la idea a guionizar",
    )
    parser_script.add_argument(
        "--format",
        required=True,
        choices=[
            "error-tipico", "mito-vs-realidad", "antes-despues",
            "consejo-rapido", "historia-real", "pregunta-reflexion",
        ],
        help="Formato del vídeo",
    )
    parser_script.add_argument(
        "--hook",
        default=None,
        metavar="TEXTO",
        help="Hook específico a usar (entre comillas). Si no se indica, Claude elige.",
    )
    parser_script.set_defaults(func=cmd_script)

    # ── Subcomando: copy ─────────────────────────────────────────────────────
    parser_copy = subparsers.add_parser(
        "copy",
        help="Genera copy de publicación para un guion",
    )
    parser_copy.add_argument(
        "--script-id",
        required=True,
        metavar="ID",
        help="ID del guion (Airtable recXXX o SCRIPT_YYYYMMDD_HHMMSS)",
    )
    parser_copy.add_argument(
        "--platform",
        default="instagram",
        choices=["instagram", "tiktok"],
        help="Plataforma destino (default: instagram)",
    )
    parser_copy.add_argument(
        "--both-platforms",
        action="store_true",
        help="Genera copy para Instagram Y TikTok",
    )
    parser_copy.set_defaults(func=cmd_copy)

    return parser


def main() -> None:
    """Punto de entrada principal del generador de contenido NOA."""
    parser = build_parser()
    args = parser.parse_args()

    try:
        args.func(args)
    except KeyboardInterrupt:
        print("\n\n⏹  Proceso interrumpido por el usuario.")
        sys.exit(0)
    except EnvironmentError as e:
        print(f"\nError de configuración: {e}")
        print("Revisa tu archivo .env y ejecuta setup_project.py si es necesario.")
        sys.exit(1)
    except Exception as e:
        logger.exception(f"Error inesperado: {e}")
        print(f"\nError inesperado: {e}")
        print("Revisa los logs para más información.")
        sys.exit(1)


if __name__ == "__main__":
    main()
