from datetime import date, datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from icalendar import Calendar, Event as ICalEvent

from models.horario import Evento


DIAS_A_OFFSET = {
    "SEGUNDA": 0,
    "TERÇA": 1,
    "QUARTA": 2,
    "QUINTA": 3,
    "SEXTA": 4,
}


def convertir_dia_a_fecha(
    dia: str,
    fecha_inicio: date,
) -> date:
    """
    Convierte el día del horario en una fecha concreta
    tomando como referencia el lunes de la semana.
    """
    if dia not in DIAS_A_OFFSET:
        raise ValueError(
            f"Día inválido para calendario: {dia}"
        )

    return fecha_inicio + timedelta(
        days=DIAS_A_OFFSET[dia]
    )


def convertir_hora(hora: str) -> tuple[int, int]:
    """
    Convierte una hora HH:MM en horas y minutos.
    """
    horas, minutos = map(
        int,
        hora.split(":"),
    )

    return horas, minutos


def crear_evento_ical(
    evento: Evento,
    fecha_inicio: date,
) -> ICalEvent:
    """
    Convierte un Evento del horario en un evento iCalendar.
    """
    fecha = convertir_dia_a_fecha(
        evento.dia,
        fecha_inicio,
    )

    hora_inicio = convertir_hora(
        evento.inicio
    )

    hora_fin = convertir_hora(
        evento.fim
    )

    zona_horaria = ZoneInfo("Africa/Luanda")

    inicio = datetime(
        fecha.year,
        fecha.month,
        fecha.day,
        hora_inicio[0],
        hora_inicio[1],
        tzinfo=zona_horaria,
    )

    fin = datetime(
        fecha.year,
        fecha.month,
        fecha.day,
        hora_fin[0],
        hora_fin[1],
        tzinfo=zona_horaria,
    )

    evento_ical = ICalEvent()

    evento_ical.add(
        "summary",
        evento.disciplina,
    )

    evento_ical.add(
        "dtstart",
        inicio,
    )

    evento_ical.add(
        "dtend",
        fin,
    )

    if evento.local:
        evento_ical.add(
            "location",
            evento.local,
        )

    descripcion = []

    if evento.docente:
        descripcion.append(
            f"Docente: {evento.docente}"
        )

    descripcion.append(
        f"Turma: {evento.turma}"
    )

    descripcion.append(
        f"Curso: {evento.curso}"
    )

    descripcion.append(
        f"Tipo: {evento.tipo}"
    )

    evento_ical.add(
        "description",
        "\n".join(descripcion),
    )

    return evento_ical


def exportar_ical(
    eventos: list[Evento],
    fecha_inicio: date,
    ruta_salida: str | Path,
) -> None:
    """
    Exporta una lista de eventos a un archivo iCalendar.

    fecha_inicio debe corresponder al lunes de la semana
    representada por el horario.
    """
    if fecha_inicio.weekday() != 0:
        raise ValueError(
            "La fecha de inicio del horario debe ser un lunes."
        )

    calendario = Calendar()

    calendario.add(
        "prodid",
        "-//Horario UNIC//Horario Universitario//ES",
    )

    calendario.add(
        "version",
        "2.0",
    )

    calendario.add(
        "calscale",
        "GREGORIAN",
    )

    calendario.add(
        "x-wr-calname",
        "Horario UNIC",
    )

    for evento in eventos:
        evento_ical = crear_evento_ical(
            evento,
            fecha_inicio,
        )

        calendario.add_component(
            evento_ical
        )

    ruta_salida = Path(ruta_salida)

    ruta_salida.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with ruta_salida.open(
        "wb"
    ) as archivo:
        archivo.write(
            calendario.to_ical()
        )