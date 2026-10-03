from models.horario import Evento


NORMALIZACIONES_DISCIPLINA = {
    "EspanholI": "Espanhol I",
    "Espanholl": "Espanhol I",
    "MatematicaI": "Matemática I",
    "Fisical": "Física I",
    "Lingua Portuiguesan": "Língua Portuguesa",
}


def normalizar_disciplina(disciplina: str) -> str:
    texto = disciplina.strip()

    if texto in NORMALIZACIONES_DISCIPLINA:
        return NORMALIZACIONES_DISCIPLINA[texto]

    return texto


def normalizar_evento(evento: Evento) -> Evento:
    evento.disciplina = normalizar_disciplina(
        evento.disciplina
    )

    return evento


def normalizar_eventos(
    eventos: list[Evento],
) -> list[Evento]:
    return [
        normalizar_evento(evento)
        for evento in eventos
    ]