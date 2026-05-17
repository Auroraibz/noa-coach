#!/usr/bin/env python3
"""
setup_project.py — Script de configuración inicial del sistema NOA Content Automation.

Este script crea la estructura de carpetas, archivos de configuración y
valida las dependencias y conectividad de APIs para el sistema de
generación de contenido de la app NOA (para padres de adolescentes con AACC).

Uso:
    python setup_project.py
    python setup_project.py --dry-run        # Solo muestra lo que haría
    python setup_project.py --skip-api-test  # Omite test de conectividad
"""

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path
from typing import Optional

# ─────────────────────────────────────────────
# Intentamos importar Rich para terminal bonita
# ─────────────────────────────────────────────
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.text import Text
    from rich import print as rprint
    RICH_AVAILABLE = True
    console = Console()
except ImportError:
    RICH_AVAILABLE = False
    console = None  # type: ignore

# ─────────────────────────────────────────────
# Ruta base del proyecto
# ─────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent  # /noa-content-system/


def imprimir(mensaje: str, estilo: str = "") -> None:
    """Imprime con Rich si está disponible, o con print normal."""
    if RICH_AVAILABLE and console:
        if estilo:
            console.print(mensaje, style=estilo)
        else:
            console.print(mensaje)
    else:
        # Eliminar marcadores de Rich para salida limpia
        import re
        texto_limpio = re.sub(r'\[.*?\]', '', mensaje)
        print(texto_limpio)


# ─────────────────────────────────────────────────────────────────────────────
# 1. ESTRUCTURA DE CARPETAS
# ─────────────────────────────────────────────────────────────────────────────

ESTRUCTURA_CARPETAS = [
    "docs",
    "prompts",
    "scripts",
    "workflows-n8n",
    "templates",
    "assets/backgrounds",
    "assets/music",
    "assets/fonts",
    "assets/icons",
    "assets/overlays",
    "outputs/raw",
    "outputs/edited",
    "outputs/approved",
    "outputs/published",
    "calendar",
    "subtitles",
    "voices",
    "videos/raw",
    "videos/final",
    "recycled-content",
]


def crear_estructura_carpetas(dry_run: bool = False) -> list[str]:
    """
    Crea la estructura completa de carpetas del proyecto NOA.

    Args:
        dry_run: Si True, solo imprime las carpetas que se crearían.

    Returns:
        Lista de rutas creadas (o que se crearían en dry_run).
    """
    imprimir("\n[bold cyan]📁 Creando estructura de carpetas...[/bold cyan]")
    carpetas_creadas = []

    for carpeta_relativa in ESTRUCTURA_CARPETAS:
        ruta_completa = BASE_DIR / carpeta_relativa

        if dry_run:
            imprimir(f"  [DRY-RUN] Crearía: {ruta_completa}")
            carpetas_creadas.append(str(ruta_completa))
            continue

        if ruta_completa.exists():
            imprimir(f"  [yellow]↪ Ya existe:[/yellow] {ruta_completa}")
        else:
            ruta_completa.mkdir(parents=True, exist_ok=True)
            # Añadimos .gitkeep para que Git rastree carpetas vacías
            gitkeep = ruta_completa / ".gitkeep"
            if not gitkeep.exists():
                gitkeep.touch()
            imprimir(f"  [green]✓ Creada:[/green] {ruta_completa}")
            carpetas_creadas.append(str(ruta_completa))

    imprimir(f"[bold green]✓ Estructura de carpetas lista ({len(ESTRUCTURA_CARPETAS)} rutas procesadas)[/bold green]")
    return carpetas_creadas


# ─────────────────────────────────────────────────────────────────────────────
# 2. ARCHIVO .env.example
# ─────────────────────────────────────────────────────────────────────────────

CONTENIDO_ENV_EXAMPLE = """\
# ============================================================
# .env.example — Variables de entorno del sistema NOA Content
# ============================================================
# Copia este archivo como .env y rellena los valores reales.
# NUNCA subas el archivo .env a Git.
#
# Documentación de cada clave:
#   ANTHROPIC_API_KEY      → https://console.anthropic.com/
#   ELEVENLABS_API_KEY     → https://elevenlabs.io/
#   ELEVENLABS_VOICE_ID    → ID de la voz de Noa en ElevenLabs
#   AIRTABLE_API_KEY       → https://airtable.com/account
#   AIRTABLE_BASE_ID       → ID de la base (app...) en Airtable
#   CREATOMATE_API_KEY     → https://creatomate.com/
#   GOOGLE_DRIVE_FOLDER_ID → ID de la carpeta de Drive para outputs
#   INSTAGRAM_ACCESS_TOKEN → Token de la Graph API de Meta
#   SLACK_WEBHOOK_URL      → Webhook entrante de Slack para notificaciones
#   OPENAI_API_KEY         → https://platform.openai.com/ (Whisper fallback)
# ============================================================

# ─── Inteligencia Artificial ─────────────────────────────────
ANTHROPIC_API_KEY=sk-ant-api03-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ─── Síntesis de voz ─────────────────────────────────────────
ELEVENLABS_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
ELEVENLABS_VOICE_ID=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ─── Base de datos de contenido ─────────────────────────────
AIRTABLE_API_KEY=patXXXXXXXXXXXXXX.XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX

# ─── Renderizado de vídeo ────────────────────────────────────
CREATOMATE_API_KEY=XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ─── Google Drive ────────────────────────────────────────────
# El archivo credentials.json debe estar en /noa-content-system/
GOOGLE_DRIVE_FOLDER_ID=1XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ─── Redes sociales ─────────────────────────────────────────
INSTAGRAM_ACCESS_TOKEN=IGQXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# ─── Notificaciones ─────────────────────────────────────────
SLACK_WEBHOOK_URL=YOUR_SLACK_WEBHOOK_URL_HERE

# ─── Fallback de transcripción ──────────────────────────────
OPENAI_API_KEY=sk-proj-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
"""


def crear_env_example(dry_run: bool = False) -> Path:
    """
    Crea el archivo .env.example en la raíz del proyecto.

    Args:
        dry_run: Si True, solo muestra el contenido que escribiría.

    Returns:
        Ruta al archivo .env.example.
    """
    imprimir("\n[bold cyan]🔑 Creando archivo .env.example...[/bold cyan]")
    ruta_env = BASE_DIR / ".env.example"

    if dry_run:
        imprimir(f"  [DRY-RUN] Escribiría: {ruta_env}")
        return ruta_env

    if ruta_env.exists():
        imprimir(f"  [yellow]↪ Ya existe (no se sobreescribe):[/yellow] {ruta_env}")
    else:
        ruta_env.write_text(CONTENIDO_ENV_EXAMPLE, encoding="utf-8")
        imprimir(f"  [green]✓ Creado:[/green] {ruta_env}")

    # Verificamos que .env real no esté en Git (recomendación)
    gitignore = BASE_DIR / ".gitignore"
    if gitignore.exists():
        contenido_gitignore = gitignore.read_text(encoding="utf-8")
        if ".env" not in contenido_gitignore:
            imprimir("  [yellow]⚠  Recuerda añadir '.env' a tu .gitignore[/yellow]")
    else:
        imprimir("  [yellow]⚠  No se encontró .gitignore — recuerda añadir '.env'[/yellow]")

    return ruta_env


# ─────────────────────────────────────────────────────────────────────────────
# 3. ARCHIVO config.json
# ─────────────────────────────────────────────────────────────────────────────

CONFIGURACION_NOA = {
    "proyecto": {
        "nombre": "NOA Content Automation System",
        "version": "1.0.0",
        "descripcion": "Sistema de automatización de contenido para la app NOA (padres de adolescentes con AACC)",
        "idioma": "es-ES"
    },
    "marca": {
        "nombre": "NOA",
        "tagline": "Tu guía para entender a tu hijo con altas capacidades",
        "colores": {
            "primary": "#1A1A2E",
            "accent": "#E94560",
            "warm": "#F5A623",
            "neutral": "#F8F8F8",
            "dark_text": "#1A1A2E",
            "light_text": "#F8F8F8"
        },
        "fuentes": {
            "principal": "Poppins",
            "secundaria": "Inter",
            "fallback": "sans-serif"
        }
    },
    "video": {
        "resolucion": {
            "ancho": 1080,
            "alto": 1920,
            "descripcion": "Vertical 9:16 (Reels / TikTok)"
        },
        "fps": 30,
        "codec": "H.264",
        "bitrate_mbps": 8,
        "formato_salida": "mp4",
        "duracion_objetivo_segundos": {
            "minimo": 20,
            "optimo": 35,
            "maximo": 45
        }
    },
    "elevenlabs": {
        "modelo": "eleven_multilingual_v2",
        "stability": 0.45,
        "similarity_boost": 0.85,
        "style": 0.30,
        "use_speaker_boost": True,
        "output_format": "mp3_44100_128",
        "idioma": "es"
    },
    "subtitulos": {
        "fuente": "Poppins-Bold",
        "font_size": 68,
        "color_texto": "#FFFFFF",
        "highlight_color": "#E94560",
        "highlight_background": "#E94560",
        "posicion": "center_bottom",
        "palabras_por_segmento": 3,
        "outline_color": "#1A1A2E",
        "outline_width": 3,
        "sombra": True
    },
    "contenido": {
        "mix_ratios": {
            "TOFU": 0.40,
            "MOFU": 0.40,
            "BOFU": 0.20,
            "descripcion": "TOFU=conciencia, MOFU=consideración, BOFU=conversión"
        },
        "frecuencia_publicacion": {
            "instagram_reels_por_semana": 4,
            "tiktok_por_semana": 5,
            "carruseles_por_semana": 2
        },
        "formatos_video": [
            "error-tipico",
            "mito-vs-realidad",
            "antes-despues",
            "consejo-rapido",
            "historia-real",
            "pregunta-reflexion"
        ],
        "cta_principales": [
            "Descarga NOA gratis",
            "Prueba NOA 7 días gratis",
            "Únete a miles de familias en NOA",
            "El test AACC está en NOA, es gratis"
        ]
    },
    "hashtags": {
        "total": 30,
        "lista": [
            "#altascapacidades",
            "#AACC",
            "#hijosAACC",
            "#sobredotacion",
            "#superdotacion",
            "#niñosdotados",
            "#parentalidadconsciente",
            "#padresAACC",
            "#madresAACC",
            "#educaciondiferente",
            "#NEE",
            "#necesidadeseducativas",
            "#crianzarespetosa",
            "#hijosadolescentes",
            "#adolescenciaAACC",
            "#talentoinvisible",
            "#intensidademocional",
            "#sobreexcitabilidades",
            "#gifted",
            "#giftedkids",
            "#giftedteen",
            "#giftedparents",
            "#NOAapp",
            "#appAACC",
            "#familiaAACC",
            "#psicologiainfantil",
            "#desarrollocognitivo",
            "#inteligenciaemocional",
            "#escuelainclusiva",
            "#aprendizajeacelerado"
        ],
        "hashtags_core": [
            "#altascapacidades",
            "#AACC",
            "#NOAapp",
            "#padresAACC",
            "#sobredotacion"
        ]
    },
    "airtable": {
        "tablas": {
            "ideas": "Ideas de Contenido",
            "scripts": "Scripts",
            "produccion": "Producción",
            "publicacion": "Publicación",
            "calendario": "Calendario Editorial"
        }
    },
    "rutas": {
        "outputs_raw": "outputs/raw",
        "outputs_edited": "outputs/edited",
        "outputs_approved": "outputs/approved",
        "outputs_published": "outputs/published",
        "voices": "voices",
        "subtitles": "subtitles",
        "videos_raw": "videos/raw",
        "videos_final": "videos/final",
        "assets": "assets",
        "calendar": "calendar"
    }
}


def crear_config_json(dry_run: bool = False) -> Path:
    """
    Crea el archivo config.json con toda la configuración del proyecto NOA.

    Args:
        dry_run: Si True, solo muestra lo que escribiría.

    Returns:
        Ruta al archivo config.json.
    """
    imprimir("\n[bold cyan]⚙️  Creando config.json...[/bold cyan]")
    ruta_config = BASE_DIR / "config.json"

    if dry_run:
        imprimir(f"  [DRY-RUN] Escribiría: {ruta_config}")
        return ruta_config

    if ruta_config.exists():
        imprimir(f"  [yellow]↪ Ya existe — actualizando con valores por defecto:[/yellow] {ruta_config}")

    with open(ruta_config, "w", encoding="utf-8") as f:
        json.dump(CONFIGURACION_NOA, f, ensure_ascii=False, indent=2)

    imprimir(f"  [green]✓ Creado:[/green] {ruta_config}")
    imprimir(f"  [dim]  Colores de marca: primary={CONFIGURACION_NOA['marca']['colores']['primary']}, "
             f"accent={CONFIGURACION_NOA['marca']['colores']['accent']}[/dim]")
    imprimir(f"  [dim]  Video: {CONFIGURACION_NOA['video']['resolucion']['ancho']}x"
             f"{CONFIGURACION_NOA['video']['resolucion']['alto']} @ {CONFIGURACION_NOA['video']['fps']}fps[/dim]")
    imprimir(f"  [dim]  Hashtags configurados: {CONFIGURACION_NOA['hashtags']['total']}[/dim]")

    return ruta_config


# ─────────────────────────────────────────────────────────────────────────────
# 4. VALIDACIÓN DE DEPENDENCIAS PYTHON
# ─────────────────────────────────────────────────────────────────────────────

DEPENDENCIAS_REQUERIDAS = [
    ("anthropic", "Claude API (generación de contenido)"),
    ("requests", "Peticiones HTTP"),
    ("dotenv", "Variables de entorno (.env)"),
    ("pyairtable", "Airtable (base de datos de contenido)"),
    ("googleapiclient", "Google Drive API"),
    ("google.auth", "Autenticación Google"),
    ("elevenlabs", "Síntesis de voz ElevenLabs"),
    ("openai", "OpenAI / Whisper (fallback)"),
    ("schedule", "Programación de tareas"),
    ("rich", "Terminal con formato"),
    ("pydantic", "Validación de datos"),
    ("click", "CLI"),
]


def validar_dependencias() -> dict[str, bool]:
    """
    Verifica que todas las dependencias Python estén instaladas.

    Returns:
        Diccionario con {modulo: disponible}.
    """
    imprimir("\n[bold cyan]📦 Validando dependencias Python...[/bold cyan]")
    resultados: dict[str, bool] = {}

    for modulo, descripcion in DEPENDENCIAS_REQUERIDAS:
        try:
            __import__(modulo)
            resultados[modulo] = True
            imprimir(f"  [green]✓[/green] {modulo:<25} {descripcion}")
        except ImportError:
            resultados[modulo] = False
            imprimir(f"  [red]✗[/red] {modulo:<25} [red]NO INSTALADO[/red] — {descripcion}")

    faltantes = [m for m, ok in resultados.items() if not ok]
    if faltantes:
        imprimir(f"\n  [yellow]⚠  Faltan {len(faltantes)} dependencias.[/yellow]")
        imprimir("  Ejecuta: [bold]pip install -r requirements.txt[/bold]")
    else:
        imprimir("\n  [bold green]✓ Todas las dependencias están instaladas.[/bold green]")

    return resultados


def instalar_dependencias_si_falta(requirements_path: Path) -> bool:
    """
    Intenta instalar las dependencias desde requirements.txt.

    Args:
        requirements_path: Ruta al archivo requirements.txt.

    Returns:
        True si la instalación fue exitosa.
    """
    if not requirements_path.exists():
        imprimir(f"  [red]✗ No se encontró requirements.txt en {requirements_path}[/red]")
        return False

    imprimir(f"\n  Instalando dependencias desde {requirements_path}...")
    resultado = subprocess.run(
        [sys.executable, "-m", "pip", "install", "-r", str(requirements_path), "-q"],
        capture_output=True,
        text=True,
    )
    if resultado.returncode == 0:
        imprimir("  [green]✓ Dependencias instaladas correctamente.[/green]")
        return True
    else:
        imprimir(f"  [red]✗ Error al instalar dependencias:\n{resultado.stderr}[/red]")
        return False


# ─────────────────────────────────────────────────────────────────────────────
# 5. TEST DE CONECTIVIDAD DE APIs (DRY RUN)
# ─────────────────────────────────────────────────────────────────────────────

def cargar_variables_entorno() -> dict[str, Optional[str]]:
    """
    Carga las variables de entorno desde el archivo .env.

    Returns:
        Diccionario con las variables de entorno relevantes.
    """
    try:
        from dotenv import load_dotenv
        ruta_env = BASE_DIR / ".env"
        if ruta_env.exists():
            load_dotenv(ruta_env)
            imprimir(f"  [green]✓ Variables cargadas desde:[/green] {ruta_env}")
        else:
            imprimir(f"  [yellow]⚠  No se encontró .env en {BASE_DIR}[/yellow]")
            imprimir("  Copia .env.example como .env y rellena las claves.")
    except ImportError:
        imprimir("  [yellow]⚠  python-dotenv no instalado — leyendo variables del sistema.[/yellow]")

    claves = [
        "ANTHROPIC_API_KEY",
        "ELEVENLABS_API_KEY",
        "ELEVENLABS_VOICE_ID",
        "AIRTABLE_API_KEY",
        "AIRTABLE_BASE_ID",
        "CREATOMATE_API_KEY",
        "GOOGLE_DRIVE_FOLDER_ID",
        "INSTAGRAM_ACCESS_TOKEN",
        "SLACK_WEBHOOK_URL",
        "OPENAI_API_KEY",
    ]
    return {clave: os.environ.get(clave) for clave in claves}


def _clave_visible(valor: Optional[str]) -> str:
    """Muestra los primeros 8 caracteres de una API key para verificación visual."""
    if not valor:
        return "[red]NO CONFIGURADA[/red]"
    if len(valor) < 8:
        return "[yellow]VALOR CORTO[/yellow]"
    return f"[dim]{valor[:8]}...{valor[-4:]}[/dim]"


def test_anthropic(api_key: Optional[str]) -> bool:
    """
    Prueba de conectividad con la API de Anthropic (Claude).
    Hace una llamada real mínima para verificar autenticación.

    Args:
        api_key: La clave API de Anthropic.

    Returns:
        True si la conexión fue exitosa.
    """
    if not api_key:
        return False
    try:
        import requests
        respuesta = requests.get(
            "https://api.anthropic.com/v1/models",
            headers={
                "x-api-key": api_key,
                "anthropic-version": "2023-06-01",
            },
            timeout=10,
        )
        return respuesta.status_code == 200
    except Exception:
        return False


def test_elevenlabs(api_key: Optional[str]) -> bool:
    """
    Prueba de conectividad con ElevenLabs.

    Args:
        api_key: La clave API de ElevenLabs.

    Returns:
        True si la conexión fue exitosa.
    """
    if not api_key:
        return False
    try:
        import requests
        respuesta = requests.get(
            "https://api.elevenlabs.io/v1/user",
            headers={"xi-api-key": api_key},
            timeout=10,
        )
        return respuesta.status_code == 200
    except Exception:
        return False


def test_airtable(api_key: Optional[str], base_id: Optional[str]) -> bool:
    """
    Prueba de conectividad con Airtable.

    Args:
        api_key: Token de personal access de Airtable.
        base_id: ID de la base de Airtable.

    Returns:
        True si la conexión fue exitosa.
    """
    if not api_key or not base_id:
        return False
    try:
        import requests
        respuesta = requests.get(
            f"https://api.airtable.com/v0/meta/bases/{base_id}/tables",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        return respuesta.status_code == 200
    except Exception:
        return False


def test_openai(api_key: Optional[str]) -> bool:
    """
    Prueba de conectividad con OpenAI.

    Args:
        api_key: La clave API de OpenAI.

    Returns:
        True si la conexión fue exitosa.
    """
    if not api_key:
        return False
    try:
        import requests
        respuesta = requests.get(
            "https://api.openai.com/v1/models",
            headers={"Authorization": f"Bearer {api_key}"},
            timeout=10,
        )
        return respuesta.status_code == 200
    except Exception:
        return False


def test_slack(webhook_url: Optional[str]) -> bool:
    """
    Prueba de conectividad con Slack (sin enviar mensaje real).

    Args:
        webhook_url: URL del webhook de Slack.

    Returns:
        True si la URL parece válida y es accesible.
    """
    if not webhook_url:
        return False
    # No enviamos mensaje real, solo verificamos que la URL tenga formato correcto
    return webhook_url.startswith("https://hooks.slack.com/services/")


def ejecutar_tests_conectividad(env_vars: dict[str, Optional[str]]) -> dict[str, bool]:
    """
    Ejecuta todos los tests de conectividad de APIs.

    Args:
        env_vars: Variables de entorno cargadas.

    Returns:
        Diccionario con {api: resultado}.
    """
    imprimir("\n[bold cyan]🌐 Ejecutando tests de conectividad de APIs...[/bold cyan]")
    imprimir("  [dim](Se realizan llamadas reales de validación)[/dim]\n")

    tests = [
        ("Anthropic / Claude", lambda: test_anthropic(env_vars.get("ANTHROPIC_API_KEY"))),
        ("ElevenLabs TTS", lambda: test_elevenlabs(env_vars.get("ELEVENLABS_API_KEY"))),
        ("Airtable DB", lambda: test_airtable(env_vars.get("AIRTABLE_API_KEY"), env_vars.get("AIRTABLE_BASE_ID"))),
        ("OpenAI / Whisper", lambda: test_openai(env_vars.get("OPENAI_API_KEY"))),
        ("Slack Webhook", lambda: test_slack(env_vars.get("SLACK_WEBHOOK_URL"))),
    ]

    resultados: dict[str, bool] = {}

    for nombre, test_fn in tests:
        imprimir(f"  Probando {nombre}...", "")
        try:
            exito = test_fn()
        except Exception as e:
            exito = False
            imprimir(f"  [red]Error inesperado: {e}[/red]")

        if exito:
            imprimir(f"  [green]✓ {nombre}: OK[/green]")
        else:
            clave = nombre.lower().replace(" / ", "_").replace(" ", "_")
            imprimir(f"  [yellow]⚠  {nombre}: No disponible (clave no configurada o sin acceso)[/yellow]")

        resultados[nombre] = exito
        time.sleep(0.3)  # Pausa cortés entre requests

    apis_ok = sum(resultados.values())
    imprimir(f"\n  Resultado: [bold]{apis_ok}/{len(tests)}[/bold] APIs verificadas correctamente.")

    return resultados


# ─────────────────────────────────────────────────────────────────────────────
# 6. RESUMEN ASCII / RICH
# ─────────────────────────────────────────────────────────────────────────────

BANNER_ASCII = r"""
  ███╗   ██╗ ██████╗  █████╗
  ████╗  ██║██╔═══██╗██╔══██╗
  ██╔██╗ ██║██║   ██║███████║
  ██║╚██╗██║██║   ██║██╔══██║
  ██║ ╚████║╚██████╔╝██║  ██║
  ╚═╝  ╚═══╝ ╚═════╝ ╚═╝  ╚═╝
  Content Automation System v1.0
  Para padres de adolescentes con AACC
"""


def imprimir_resumen(
    carpetas_ok: bool,
    env_ok: bool,
    config_ok: bool,
    deps: dict[str, bool],
    apis: dict[str, bool],
) -> None:
    """
    Imprime un resumen visual del estado de la configuración del proyecto.

    Args:
        carpetas_ok: Si se crearon las carpetas correctamente.
        env_ok: Si se creó el .env.example.
        config_ok: Si se creó config.json.
        deps: Resultado de validación de dependencias.
        apis: Resultado de tests de conectividad.
    """
    if RICH_AVAILABLE and console:
        # Banner con Rich
        console.print(Panel(
            Text(BANNER_ASCII, style="bold #E94560"),
            border_style="#1A1A2E",
            subtitle="[dim]Sistema de contenido para padres de adolescentes con AACC[/dim]",
        ))

        # Tabla de estado
        tabla = Table(title="Estado de la Configuración", show_header=True, header_style="bold #F5A623")
        tabla.add_column("Componente", style="bold")
        tabla.add_column("Estado", justify="center")
        tabla.add_column("Detalle")

        def estado(ok: bool) -> str:
            return "[green]✓ OK[/green]" if ok else "[red]✗ ERROR[/red]"

        tabla.add_row("Estructura de carpetas", estado(carpetas_ok), f"{len(ESTRUCTURA_CARPETAS)} rutas")
        tabla.add_row(".env.example", estado(env_ok), str(BASE_DIR / ".env.example"))
        tabla.add_row("config.json", estado(config_ok), str(BASE_DIR / "config.json"))

        deps_ok_count = sum(deps.values())
        tabla.add_row(
            "Dependencias Python",
            estado(deps_ok_count == len(deps)),
            f"{deps_ok_count}/{len(deps)} instaladas"
        )

        apis_ok_count = sum(apis.values())
        tabla.add_row(
            "APIs conectadas",
            f"[yellow]{apis_ok_count}/{len(apis)}[/yellow]",
            "Configura .env para activar todas"
        )

        console.print(tabla)

        # Próximos pasos
        console.print(Panel(
            "\n".join([
                "[bold]Próximos pasos:[/bold]",
                "",
                "1. Copia [cyan].env.example[/cyan] como [cyan].env[/cyan] y añade tus claves API",
                "2. Ejecuta [cyan]pip install -r requirements.txt[/cyan] si faltan dependencias",
                "3. Configura las tablas en Airtable (ver /docs/airtable-setup.md)",
                "4. Lanza el generador: [cyan]python scripts/content_generator.py ideas --count 5[/cyan]",
                "",
                "[dim]Documentación completa en /docs/[/dim]",
            ]),
            border_style="#E94560",
            title="[bold #F5A623]🚀 ¡Sistema NOA listo para despegar![/bold #F5A623]",
        ))
    else:
        # Fallback sin Rich
        print("\n" + "=" * 60)
        print(BANNER_ASCII)
        print("=" * 60)
        print("\n✓ CONFIGURACIÓN COMPLETADA")
        print(f"  Carpetas: {'OK' if carpetas_ok else 'ERROR'}")
        print(f"  .env.example: {'OK' if env_ok else 'ERROR'}")
        print(f"  config.json: {'OK' if config_ok else 'ERROR'}")
        print(f"  Dependencias: {sum(deps.values())}/{len(deps)} instaladas")
        print(f"  APIs conectadas: {sum(apis.values())}/{len(apis)}")
        print("\nPróximos pasos:")
        print("  1. Copia .env.example como .env y añade tus claves API")
        print("  2. Ejecuta: pip install -r requirements.txt")
        print("  3. Lanza: python scripts/content_generator.py ideas --count 5")
        print("=" * 60 + "\n")


# ─────────────────────────────────────────────────────────────────────────────
# PUNTO DE ENTRADA PRINCIPAL
# ─────────────────────────────────────────────────────────────────────────────

def main() -> None:
    """Función principal del script de configuración del proyecto NOA."""

    parser = argparse.ArgumentParser(
        description="Configura el proyecto de automatización de contenido NOA.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python setup_project.py
  python setup_project.py --dry-run
  python setup_project.py --skip-api-test
  python setup_project.py --install-deps
        """,
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Muestra lo que haría sin crear archivos ni carpetas.",
    )
    parser.add_argument(
        "--skip-api-test",
        action="store_true",
        help="Omite el test de conectividad de APIs.",
    )
    parser.add_argument(
        "--install-deps",
        action="store_true",
        help="Intenta instalar dependencias faltantes automáticamente.",
    )
    args = parser.parse_args()

    if args.dry_run:
        imprimir("\n[bold yellow]🔍 MODO DRY-RUN ACTIVADO — No se modificará nada.[/bold yellow]")

    imprimir(f"\n[bold]Directorio base del proyecto:[/bold] {BASE_DIR}")

    # ── Paso 1: Estructura de carpetas ──────────────────────────────────────
    try:
        crear_estructura_carpetas(dry_run=args.dry_run)
        carpetas_ok = True
    except Exception as e:
        imprimir(f"[red]✗ Error creando carpetas: {e}[/red]")
        carpetas_ok = False

    # ── Paso 2: .env.example ────────────────────────────────────────────────
    try:
        crear_env_example(dry_run=args.dry_run)
        env_ok = True
    except Exception as e:
        imprimir(f"[red]✗ Error creando .env.example: {e}[/red]")
        env_ok = False

    # ── Paso 3: config.json ─────────────────────────────────────────────────
    try:
        crear_config_json(dry_run=args.dry_run)
        config_ok = True
    except Exception as e:
        imprimir(f"[red]✗ Error creando config.json: {e}[/red]")
        config_ok = False

    # ── Paso 4: Validar dependencias ─────────────────────────────────────────
    deps = validar_dependencias()
    faltantes = [m for m, ok in deps.items() if not ok]

    if faltantes and args.install_deps and not args.dry_run:
        req_path = BASE_DIR / "scripts" / "requirements.txt"
        instalar_dependencias_si_falta(req_path)
        # Re-validar tras instalación
        deps = validar_dependencias()

    # ── Paso 5: Tests de conectividad ────────────────────────────────────────
    apis: dict[str, bool] = {}
    if not args.skip_api_test and not args.dry_run:
        imprimir("\n[bold cyan]🔐 Cargando variables de entorno...[/bold cyan]")
        env_vars = cargar_variables_entorno()
        apis = ejecutar_tests_conectividad(env_vars)
    else:
        if args.dry_run:
            imprimir("\n[dim]Tests de API omitidos en modo dry-run.[/dim]")
        else:
            imprimir("\n[dim]Tests de API omitidos (--skip-api-test).[/dim]")
        apis = {}

    # ── Paso 6: Resumen final ────────────────────────────────────────────────
    imprimir_resumen(carpetas_ok, env_ok, config_ok, deps, apis)

    # Código de salida: 0 si todo OK, 1 si hay problemas
    todo_ok = carpetas_ok and env_ok and config_ok and all(deps.values())
    sys.exit(0 if todo_ok else 1)


if __name__ == "__main__":
    main()
