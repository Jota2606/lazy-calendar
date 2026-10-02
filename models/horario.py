from dataclasses import dataclass


DIAS_VALIDOS = {
    "SEGUNDA",
    "TERÇA",
    "QUARTA",
    "QUINTA",
    "SEXTA",
}

DIAS_ES = {
    "SEGUNDA": "lunes",
    "TERÇA": "martes",
    "QUARTA": "miércoles",
    "QUINTA": "jueves",
    "SEXTA": "viernes",
}

ORDEN_DIAS = {
    "SEGUNDA": 0,
    "TERÇA": 1,
    "QUARTA": 2,
    "QUINTA": 3,
    "SEXTA": 4,
}

@dataclass
class Evento:
    curso: str
    ano: int
    periodo: str
    turma: str
    dia: str
    inicio: str
    fim: str
    disciplina: str
    local: str | None = None
    docente: str | None = None
    tipo: str = "aula"


def hora_a_minutos(hora: str) -> int:
    """Convierte HH:MM a minutos desde medianoche."""

    horas, minutos = map(int, hora.split(":"))

    return horas * 60 + minutos


def obtener_franjas(eventos: list[Evento]) -> list[tuple[str, str]]:
    """Obtiene las franjas horarias presentes y las ordena por hora de inicio."""

    franjas = {
        (evento.inicio, evento.fim)
        for evento in eventos
    }

    return sorted(
        franjas,
        key=lambda franja: hora_a_minutos(franja[0])
    )


def obtener_dias(eventos: list[Evento]) -> list[str]:
    """Obtiene los días presentes en el horario en orden semanal."""

    dias = {
        evento.dia
        for evento in eventos
    }

    return sorted(
        dias,
        key=lambda dia: ORDEN_DIAS[dia]
    )


def crear_tabla(eventos: list[Evento]) -> dict[str, list[Evento]]:
    """Organiza los eventos por día y los ordena cronológicamente."""

    tabla = {
        dia: []
        for dia in DIAS_VALIDOS
    }

    for evento in eventos:
        tabla[evento.dia].append(evento)

    key=lambda item: ORDEN_DIAS[item[0]]

    tabla = dict(
        sorted(
            tabla.items(),
            key=lambda item: ORDEN_DIAS[item[0]]
        )
    )

    for dia in tabla:
        tabla[dia].sort(
            key=lambda evento: hora_a_minutos(evento.inicio)
        )

    return tabla


def dia_para_calendario(dia: str) -> str:
    """Convierte el día portugués al equivalente en español."""

    return DIAS_ES[dia]