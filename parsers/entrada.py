import json
from pathlib import Path


def cargar_ocr(ruta: str | Path) -> dict:
    """Carga el resultado bruto generado por el OCR."""
    ruta = Path(ruta)

    with ruta.open("r", encoding="utf-8") as archivo:
        return json.load(archivo)


def obtener_tabla_matutina(datos_ocr: dict) -> dict:
    """Obtiene la primera tabla, que corresponde al horario principal."""
    tablas = datos_ocr["tablas"]

    if not tablas:
        raise ValueError("El OCR no encontró ninguna tabla.")

    return tablas[0]