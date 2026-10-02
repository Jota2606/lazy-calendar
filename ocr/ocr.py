import os

os.environ["PADDLE_PDX_ENABLE_MKLDNN_BYDEFAULT"] = "0"

from paddleocr import PPStructureV3


def ejecutar_ocr(ruta_imagen: str):
    """Ejecuta PP-StructureV3 sobre una imagen."""
    ocr = PPStructureV3()
    resultado = ocr.predict(ruta_imagen)
    return resultado


def extraer_tablas(resultado: list) -> list:
    """Extrae las tablas detectadas del resultado de OCR."""
    if not resultado:
        return []

    pagina = resultado[0]

    return pagina["table_res_list"]