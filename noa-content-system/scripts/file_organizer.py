#!/usr/bin/env python3
"""
file_organizer.py — NOA Content System
Organiza, renombra y sube archivos de producción de contenido.
Convención de nombres: NOA_YYYYMMDD_TEMA_HOOK_ESTADO
"""

import os
import re
import sys
import json
import shutil
import argparse
import logging
from pathlib import Path
from datetime import datetime
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

# ─── Configuración ────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
VOICES_DIR = BASE_DIR / "voices"
SUBTITLES_DIR = BASE_DIR / "subtitles"
VIDEOS_DIR = BASE_DIR / "videos"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)
log = logging.getLogger("file_organizer")

# Extensiones por tipo
TIPO_POR_EXTENSION = {
    ".mp3": "voice",
    ".wav": "voice",
    ".srt": "subtitle",
    ".ass": "subtitle",
    ".mp4": "video",
    ".mov": "video",
    ".json": "data",
    ".md": "script",
    ".txt": "script",
    ".png": "image",
    ".jpg": "image",
    ".jpeg": "image",
}

ESTADOS_VALIDOS = ["IDEA", "SCRIPT", "VOICE", "SUBS", "VIDEO", "APPROVED", "PUBLISHED", "RECYCLED"]

CARPETA_POR_ESTADO = {
    "IDEA": OUTPUTS_DIR / "raw",
    "SCRIPT": OUTPUTS_DIR / "raw",
    "VOICE": VOICES_DIR,
    "SUBS": SUBTITLES_DIR,
    "VIDEO": OUTPUTS_DIR / "edited",
    "APPROVED": OUTPUTS_DIR / "approved",
    "PUBLISHED": OUTPUTS_DIR / "published",
    "RECYCLED": BASE_DIR / "recycled-content",
}


# ─── Funciones principales ────────────────────────────────────────────────────

def detectar_tipo(file: Path) -> str:
    return TIPO_POR_EXTENSION.get(file.suffix.lower(), "unknown")


def sanitizar_segmento(texto: str) -> str:
    """Convierte texto libre a segmento válido para nombre de archivo."""
    texto = texto.upper().strip()
    texto = re.sub(r"[áàä]", "A", texto)
    texto = re.sub(r"[éèë]", "E", texto)
    texto = re.sub(r"[íìï]", "I", texto)
    texto = re.sub(r"[óòö]", "O", texto)
    texto = re.sub(r"[úùü]", "U", texto)
    texto = re.sub(r"[ñ]", "N", texto)
    texto = re.sub(r"[^A-Z0-9\-]", "-", texto)
    texto = re.sub(r"-{2,}", "-", texto)
    return texto.strip("-")[:30]


def construir_nombre(fecha: str, tema: str, hook: str, estado: str, extension: str) -> str:
    """
    Construye el nombre de archivo según la convención NOA.
    NOA_YYYYMMDD_TEMA_HOOK_ESTADO.ext
    """
    tema_san = sanitizar_segmento(tema)
    hook_san = sanitizar_segmento(hook)
    estado_san = estado.upper()
    if estado_san not in ESTADOS_VALIDOS:
        raise ValueError(f"Estado no válido: {estado_san}. Válidos: {ESTADOS_VALIDOS}")
    return f"NOA_{fecha}_{tema_san}_{hook_san}_{estado_san}{extension}"


def detectar_estado_desde_nombre(nombre: str) -> Optional[str]:
    """Intenta extraer el estado del nombre de archivo si ya sigue la convención."""
    partes = nombre.upper().split("_")
    for estado in reversed(ESTADOS_VALIDOS):
        if any(estado in p for p in partes):
            return estado
    return None


def destino_para_archivo(file: Path, estado: str) -> Path:
    """Determina la carpeta destino basándose en el estado."""
    tipo = detectar_tipo(file)

    if tipo == "voice":
        carpeta = VOICES_DIR
    elif tipo == "subtitle":
        carpeta = SUBTITLES_DIR
    elif tipo == "video":
        if estado == "PUBLISHED":
            carpeta = OUTPUTS_DIR / "published"
        elif estado == "APPROVED":
            carpeta = OUTPUTS_DIR / "approved"
        else:
            carpeta = OUTPUTS_DIR / "edited"
    else:
        carpeta = CARPETA_POR_ESTADO.get(estado, OUTPUTS_DIR / "raw")

    semana = f"W{datetime.now().isocalendar()[1]:02d}"
    anio = datetime.now().year
    carpeta_final = carpeta / str(anio) / semana
    return carpeta_final


def renombrar_y_mover(
    file: Path,
    tema: str,
    hook: str,
    estado: str,
    fecha: Optional[str] = None,
    dry_run: bool = False,
    verbose: bool = False
) -> Path:
    """
    Renombra el archivo a la convención NOA y lo mueve a la carpeta correcta.
    Retorna la ruta final del archivo.
    """
    if fecha is None:
        fecha = datetime.now().strftime("%Y%m%d")

    nuevo_nombre = construir_nombre(fecha, tema, hook, estado, file.suffix)
    carpeta_destino = destino_para_archivo(file, estado)
    ruta_destino = carpeta_destino / nuevo_nombre

    # Resolver conflictos
    if ruta_destino.exists():
        base = ruta_destino.stem
        suffix = ruta_destino.suffix
        contador = 2
        while ruta_destino.exists():
            ruta_destino = carpeta_destino / f"{base}_v{contador}{suffix}"
            contador += 1

    if verbose:
        log.info(f"  Origen:  {file}")
        log.info(f"  Destino: {ruta_destino}")

    if not dry_run:
        carpeta_destino.mkdir(parents=True, exist_ok=True)
        shutil.move(str(file), str(ruta_destino))
        log.info(f"✓ Movido: {ruta_destino.name}")
    else:
        log.info(f"[DRY RUN] Movería: {file.name} → {ruta_destino}")

    return ruta_destino


def escanear_nuevos_archivos(directorio: Path, extension_filtro: Optional[str] = None) -> list[Path]:
    """Escanea un directorio buscando archivos que no siguen la convención de nombres."""
    archivos = []
    pattern = f"*{extension_filtro}" if extension_filtro else "*"

    for file in directorio.glob(pattern):
        if file.is_file() and not file.name.startswith("."):
            if not file.name.startswith("NOA_"):
                archivos.append(file)

    return sorted(archivos)


def subir_a_gdrive(file: Path, folder_id: str) -> str:
    """
    Sube un archivo a Google Drive y retorna el ID del archivo subido.
    Requiere credenciales configuradas en .env y google-api-python-client instalado.
    """
    try:
        from google.oauth2 import service_account
        from googleapiclient.discovery import build
        from googleapiclient.http import MediaFileUpload

        credentials_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH")
        if not credentials_path:
            log.warning("GOOGLE_SERVICE_ACCOUNT_PATH no configurado. Saltando subida a Drive.")
            return ""

        creds = service_account.Credentials.from_service_account_file(
            credentials_path,
            scopes=["https://www.googleapis.com/auth/drive.file"]
        )
        service = build("drive", "v3", credentials=creds)

        file_metadata = {
            "name": file.name,
            "parents": [folder_id]
        }
        media = MediaFileUpload(str(file), resumable=True)
        uploaded = service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id, webViewLink"
        ).execute()

        log.info(f"✓ Subido a Drive: {uploaded.get('webViewLink', '')}")
        return uploaded.get("id", "")

    except ImportError:
        log.error("google-api-python-client no instalado. Ejecuta: pip install google-api-python-client google-auth")
        return ""
    except Exception as e:
        log.error(f"Error subiendo a Drive: {e}")
        return ""


def actualizar_airtable(record_id: str, campo: str, valor: str) -> bool:
    """Actualiza un campo en un registro de Airtable."""
    try:
        import requests
        api_key = os.getenv("AIRTABLE_API_KEY")
        base_id = os.getenv("AIRTABLE_BASE_ID")
        if not api_key or not base_id:
            log.warning("AIRTABLE_API_KEY o AIRTABLE_BASE_ID no configurados.")
            return False

        url = f"https://api.airtable.com/v0/{base_id}/Contenido/{record_id}"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {"fields": {campo: valor}}
        response = requests.patch(url, json=payload, headers=headers)
        response.raise_for_status()
        return True

    except Exception as e:
        log.error(f"Error actualizando Airtable: {e}")
        return False


def generar_reporte_diario(directorio: Path) -> str:
    """Genera un resumen de los archivos organizados hoy."""
    hoy = datetime.now().strftime("%Y%m%d")
    archivos_hoy = list(directorio.rglob(f"NOA_{hoy}_*"))

    por_estado = {}
    for f in archivos_hoy:
        estado = detectar_estado_desde_nombre(f.stem) or "DESCONOCIDO"
        por_estado.setdefault(estado, []).append(f.name)

    lineas = [f"\n📊 REPORTE DIARIO NOA — {datetime.now().strftime('%d/%m/%Y')}"]
    lineas.append(f"Total archivos hoy: {len(archivos_hoy)}\n")
    for estado, archivos in sorted(por_estado.items()):
        lineas.append(f"  {estado}: {len(archivos)} archivo(s)")
        for a in archivos:
            lineas.append(f"    · {a}")

    return "\n".join(lineas)


# ─── CLI ──────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description="NOA File Organizer — Organiza y renombra archivos de producción",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python file_organizer.py organizar --tema "ERROR-TIPICO" --hook "ARGUMENTAR" --estado SCRIPT
  python file_organizer.py organizar --directorio outputs/raw --dry-run
  python file_organizer.py escanear --directorio outputs/raw
  python file_organizer.py reporte
        """
    )
    subparsers = parser.add_subparsers(dest="comando")

    # Subcomando: organizar
    p_org = subparsers.add_parser("organizar", help="Renombra y mueve un archivo")
    p_org.add_argument("archivo", nargs="?", help="Archivo a organizar")
    p_org.add_argument("--directorio", "-d", help="Directorio a organizar (todos los archivos sin convención)")
    p_org.add_argument("--tema", required=False, help="Tema del contenido (ej: EXPLOSION-EMOCIONAL)")
    p_org.add_argument("--hook", required=False, help="Hook resumido (ej: NO-ES-RABIA)")
    p_org.add_argument("--estado", choices=ESTADOS_VALIDOS, default="SCRIPT")
    p_org.add_argument("--fecha", help="Fecha YYYYMMDD (por defecto: hoy)")
    p_org.add_argument("--drive", action="store_true", help="Subir a Google Drive después")
    p_org.add_argument("--dry-run", action="store_true", help="Solo mostrar qué haría, sin mover")
    p_org.add_argument("--verbose", "-v", action="store_true")

    # Subcomando: escanear
    p_scan = subparsers.add_parser("escanear", help="Lista archivos que no siguen la convención")
    p_scan.add_argument("--directorio", "-d", default="outputs/", help="Directorio a escanear")

    # Subcomando: reporte
    subparsers.add_parser("reporte", help="Genera reporte diario de archivos")

    args = parser.parse_args()

    if args.comando == "escanear":
        directorio = Path(args.directorio)
        if not directorio.exists():
            log.error(f"Directorio no encontrado: {directorio}")
            sys.exit(1)
        archivos = escanear_nuevos_archivos(directorio)
        if archivos:
            log.info(f"\n{len(archivos)} archivo(s) sin convención NOA en {directorio}:")
            for f in archivos:
                log.info(f"  · {f.name}  ({detectar_tipo(f)})")
        else:
            log.info("✓ Todos los archivos siguen la convención NOA.")

    elif args.comando == "organizar":
        if args.archivo:
            file = Path(args.archivo)
            if not file.exists():
                log.error(f"Archivo no encontrado: {file}")
                sys.exit(1)
            tema = args.tema or "CONTENIDO"
            hook = args.hook or "HOOK"
            ruta_final = renombrar_y_mover(
                file, tema, hook, args.estado,
                fecha=args.fecha,
                dry_run=args.dry_run,
                verbose=args.verbose
            )
            if args.drive and not args.dry_run:
                folder_id = os.getenv("GOOGLE_DRIVE_FOLDER_ID", "")
                if folder_id:
                    subir_a_gdrive(ruta_final, folder_id)

        elif args.directorio:
            directorio = Path(args.directorio)
            archivos = escanear_nuevos_archivos(directorio)
            log.info(f"Organizando {len(archivos)} archivo(s) en {directorio}...")
            for file in archivos:
                tema = args.tema or file.stem.split("-")[0] or "CONTENIDO"
                hook = args.hook or "HOOK"
                renombrar_y_mover(
                    file, tema, hook, args.estado,
                    fecha=args.fecha,
                    dry_run=args.dry_run,
                    verbose=args.verbose
                )
        else:
            log.error("Especifica --archivo o --directorio")
            sys.exit(1)

    elif args.comando == "reporte":
        print(generar_reporte_diario(BASE_DIR))

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
