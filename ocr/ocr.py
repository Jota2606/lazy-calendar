import json
import os
from pathlib import Path
os.environ["PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT"] = "0"

from paddleocr import PPStructureV3


_ocr = None


def obtener_ocr():
    """Obtiene la instancia compartida de PP-StructureV3."""
    global _ocr

    if _ocr is None:
        print("Cargando modelo OCR...")

        _ocr = PPStructureV3(
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
            use_seal_recognition=False,
            use_formula_recognition=False,
            use_chart_recognition=False,
            use_region_detection=False,
            enable_mkldnn=False,
            cpu_threads=6,
            
            text_detection_model_name="PP-OCRv5_mobile_det",
            text_recognition_model_name="PP-OCRv5_mobile_rec",
        )

        print("Modelo OCR cargado.")

    return _ocr


def ejecutar_ocr(ruta_imagen: str):
    """Ejecuta PP-StructureV3 sobre una imagen."""
    ocr = obtener_ocr()

    resultado = ocr.predict(
        ruta_imagen,
        use_doc_orientation_classify=False,
        use_doc_unwarping=False,
        use_textline_orientation=False,
        use_seal_recognition=False,
        use_formula_recognition=False,
        use_chart_recognition=False,
        use_region_detection=False,
    )

    return resultado


def extraer_tablas(resultado: list) -> list:
    """Extrae las tablas detectadas del resultado de OCR."""
    if not resultado:
        return []

    pagina = resultado[0]

    return pagina["table_res_list"]

def convertir_a_lista(valor):
    """Convierte arrays NumPy y estructuras similares a listas normales."""
    if hasattr(valor, "tolist"):
        return valor.tolist()

    return valor


def guardar_resultado_json(
    resultado: list,
    ruta_imagen: str | Path,
    ruta_salida: str | Path,
) -> None:
    """
    Guarda el resultado OCR en el formato JSON utilizado por los parsers.
    """
    tablas = extraer_tablas(resultado)

    datos_exportados = {
        "imagen": Path(ruta_imagen).name,
        "tablas": [],
    }

    for numero, tabla in enumerate(tablas, start=1):
        ocr = tabla["table_ocr_pred"]

        datos_exportados["tablas"].append(
            {
                "numero": numero,
                "rec_texts": ocr["rec_texts"],
                "rec_scores": convertir_a_lista(
                    ocr["rec_scores"]
                ),
                "rec_boxes": convertir_a_lista(
                    ocr["rec_boxes"]
                ),
                "rec_polys": convertir_a_lista(
                    ocr["rec_polys"]
                ),
            }
        )

    ruta_salida = Path(ruta_salida)

    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ruta_salida.open(
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(
            datos_exportados,
            archivo,
            ensure_ascii=False,
            indent=2,
        )