from pathlib import Path

from models.horario import Evento, ORDEN_DIAS
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

def obtener_intervalo_franjas(franjas_celda: list[dict]) -> tuple[str, str]:
    """
    Convierte una o varias franjas horarias en un intervalo
    de inicio y fin.
    """

    if not franjas_celda:
        raise ValueError(
            "No se encontraron franjas para la celda."
        )

    primera = franjas_celda[0]["hora"]
    ultima = franjas_celda[-1]["hora"]

    inicio = primera.split("-", 1)[0].strip()
    fim = ultima.split("-", 1)[1].strip()

    return inicio, fim

def crear_eventos(
    celdas: dict[str, list[list[dict]]],
    franjas_por_celda: dict[str, list[list[dict]]],
    datos_celdas: dict[str, list[dict]],
    curso: str,
    ano: int,
    periodo: str,
    turma: str,
) -> list[Evento]:
    """
    Convierte las celdas detectadas en objetos Evento.
    """

    eventos = []

    dias_ordenados = sorted(
        celdas,
        key=lambda dia: ORDEN_DIAS[dia],
    )

    for dia in dias_ordenados:
        grupos = celdas[dia]
        franjas_dia = franjas_por_celda[dia]
        datos_dia = datos_celdas[dia]

        for indice, celda in enumerate(grupos):

            franjas_celda = franjas_dia[indice]
            datos = datos_dia[indice]

            if not franjas_celda:
                continue

            inicio, fim = obtener_intervalo_franjas(
                franjas_celda
            )

            # La última celda de cada día corresponde
            # a la fila de tutorías.
            es_tutoria = indice == len(grupos) - 1

            evento = Evento(
                curso=curso,
                ano=ano,
                periodo=periodo,
                turma=turma,
                dia=dia,
                inicio=inicio,
                fim=fim,
                disciplina=datos["disciplina"] or "",
                local=datos["local"],
                docente=datos["docente"],
                tipo="tutoria" if es_tutoria else "aula",
            )

            eventos.append(evento)

    return eventos