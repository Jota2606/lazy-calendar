from models.horario import (
    DIAS_VALIDOS,
    Evento,
    hora_a_minutos,
)


def validar_hora(hora: str) -> bool:
    """Comprueba si una hora tiene formato HH:MM válido."""

    try:
        horas, minutos = map(int, hora.split(":"))

        return (
            0 <= horas <= 23
            and 0 <= minutos <= 59
        )

    except (ValueError, AttributeError):
        return False


def validar_evento(evento: Evento) -> list[str]:
    """Devuelve una lista de errores encontrados en un evento."""

    errores = []

    # --------------------------------------------------------
    # Validar día
    # --------------------------------------------------------

    if evento.dia not in DIAS_VALIDOS:
        errores.append(
            f"Día inválido: {evento.dia}"
        )

    # --------------------------------------------------------
    # Validar hora de inicio
    # --------------------------------------------------------

    inicio_valido = validar_hora(evento.inicio)

    if not inicio_valido:
        errores.append(
            f"Hora de inicio inválida: {evento.inicio}"
        )

    # --------------------------------------------------------
    # Validar hora de fin
    # --------------------------------------------------------

    fim_valido = validar_hora(evento.fim)

    if not fim_valido:
        errores.append(
            f"Hora de fin inválida: {evento.fim}"
        )

    # --------------------------------------------------------
    # Comprobar que la hora final sea posterior a la inicial
    # --------------------------------------------------------

    if inicio_valido and fim_valido:

        inicio = hora_a_minutos(evento.inicio)
        fim = hora_a_minutos(evento.fim)

        if fim <= inicio:
            errores.append(
                f"La hora de fin debe ser posterior a "
                f"la hora de inicio: "
                f"{evento.inicio} - {evento.fim}"
            )

    # --------------------------------------------------------
    # Validar disciplina
    # --------------------------------------------------------

    if not evento.disciplina.strip():
        errores.append(
            "La disciplina está vacía"
        )

    # --------------------------------------------------------
    # Validar turma
    # --------------------------------------------------------

    if not evento.turma.strip():
        errores.append(
            "La turma está vacía"
        )

    return errores