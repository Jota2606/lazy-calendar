from pathlib import Path

from openpyxl import Workbook

from models.horario import Evento


def exportar_excel(
    eventos: list[Evento],
    ruta_salida: str | Path,
) -> None:
    """
    Exporta una lista de eventos a un archivo Excel.
    """
    libro = Workbook()
    hoja = libro.active
    hoja.title = "Horario"

    encabezados = [
        "Día",
        "Inicio",
        "Fin",
        "Disciplina",
        "Docente",
        "Local",
        "Tipo",
    ]

    hoja.append(encabezados)

    for evento in eventos:
        hoja.append([
            evento.dia,
            evento.inicio,
            evento.fim,
            evento.disciplina,
            evento.docente or "",
            evento.local or "",
            evento.tipo,
        ])

    ruta_salida = Path(ruta_salida)

    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    libro.save(ruta_salida)