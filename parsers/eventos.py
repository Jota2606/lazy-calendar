from models.horario import Evento, ORDEN_DIAS


def obtener_intervalo_franjas(
    franjas_celda: list[dict],
) -> tuple[str, str]:
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
            es_tutoria = (
                inicio == "11:45"
                and fim == "12:30"
            )

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