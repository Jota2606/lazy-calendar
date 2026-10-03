import json
from pathlib import Path

from ocr.ocr import ejecutar_ocr, extraer_tablas


def convertir_a_lista(valor):
    """Convierte arrays NumPy y estructuras similares a listas normales."""
    if hasattr(valor, "tolist"):
        return valor.tolist()

    return valor


def main():
    print("Ejecutando OCR una última vez para generar el JSON...")

    resultado = ejecutar_ocr("horario.jpeg")
    tablas = extraer_tablas(resultado)

    datos_exportados = {
        "imagen": "horario.jpeg",
        "tablas": [],
    }

    for numero, tabla in enumerate(tablas, start=1):
        ocr = tabla["table_ocr_pred"]

        datos_exportados["tablas"].append(
            {
                "numero": numero,
                "rec_texts": ocr["rec_texts"],
                "rec_scores": convertir_a_lista(ocr["rec_scores"]),
                "rec_boxes": convertir_a_lista(ocr["rec_boxes"]),
                "rec_polys": convertir_a_lista(ocr["rec_polys"]),
            }
        )

    carpeta_salida = Path("output")
    carpeta_salida.mkdir(exist_ok=True)

    ruta = carpeta_salida / "ocr_resultado.json"

    with ruta.open("w", encoding="utf-8") as archivo:
        json.dump(
            datos_exportados,
            archivo,
            ensure_ascii=False,
            indent=2,
        )

    print()
    print("=" * 80)
    print("OCR EXPORTADO")
    print("=" * 80)
    print(f"Tablas: {len(tablas)}")
    print(f"Archivo: {ruta}")
    print("=" * 80)


if __name__ == "__main__":
    main()