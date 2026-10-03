import os

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