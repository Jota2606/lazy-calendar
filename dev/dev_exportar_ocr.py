import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(RAIZ_PROYECTO),
)

from ocr.ocr import ejecutar_ocr, guardar_resultado_json


def main():
    ruta_imagen = RAIZ_PROYECTO / "horario.jpeg"
    ruta_salida = (
        RAIZ_PROYECTO
        / "output"
        / "ocr_resultado.json"
    )

    print("Ejecutando OCR...")

    resultado = ejecutar_ocr(
        ruta_imagen
    )

    guardar_resultado_json(
        resultado=resultado,
        ruta_imagen=ruta_imagen,
        ruta_salida=ruta_salida,
    )

    print()
    print("=" * 80)
    print("OCR EXPORTADO")
    print("=" * 80)
    print(f"Archivo: {ruta_salida}")
    print("=" * 80)


if __name__ == "__main__":
    main()