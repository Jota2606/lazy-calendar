from pathlib import Path

from parsers.entrada import (
    cargar_ocr,
    obtener_tabla_matutina,
)

from parsers.estructura import (
    extraer_dias,
    extraer_franjas_matutinas,
    extraer_contenido_matutino,
    extraer_metadata,
)

from parsers.celdas import (
    agrupar_contenido_por_dia,
    extraer_datos_de_celdas,
    obtener_franjas_por_celda,
)

from parsers.eventos import crear_eventos

DIAS_VALIDOS = {
    "SEGUNDA",
    "TERÇA",
    "QUARTA",
    "QUINTA",
    "SEXTA",
}


def analizar_estructura(ruta: str | Path) -> dict:
    """
    Carga el JSON del OCR y extrae la estructura básica
    necesaria para reconstruir el horario.
    """
    datos_ocr = cargar_ocr(ruta)
    tabla = obtener_tabla_matutina(datos_ocr)

    dias = extraer_dias(tabla)
    franjas = extraer_franjas_matutinas(tabla)
    metadata = extraer_metadata(tabla)

    contenidos = extraer_contenido_matutino(
        tabla,
        dias,
    )

    celdas = agrupar_contenido_por_dia(
        contenidos
    )

    franjas_por_celda = obtener_franjas_por_celda(
        celdas,
        franjas,
    )

    datos_celdas = extraer_datos_de_celdas(celdas)

    eventos = crear_eventos(
        celdas,
        franjas_por_celda,
        datos_celdas,
        curso=metadata["curso"] or "",
        ano=metadata["ano"] or 0,
        periodo=metadata["periodo"] or "",
        turma=metadata["turma"] or "",
    )

    return {
        "tabla": tabla,
        "dias": dias,
        "franjas": franjas,
        "contenidos": contenidos,
        "celdas": celdas,
        "franjas_por_celda": franjas_por_celda,
        "datos_celdas": datos_celdas,
        "metadata": metadata,
        "eventos": eventos,
    }


