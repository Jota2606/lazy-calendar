from models.horario import Evento


def parsear_celda(texto: str) -> dict:
    """Extrae asignatura, local y docente del texto de una celda."""

    lineas = [
        linea.strip()
        for linea in texto.splitlines()
        if linea.strip()
    ]

    if not lineas:
        return {
            "disciplina": "",
            "local": None,
            "docente": None,
        }

    disciplina = lineas[0]
    local = None
    docente = None

    if len(lineas) >= 2:
        partes = [
            parte.strip()
            for parte in lineas[1].split("|")
        ]

        if len(partes) >= 1 and partes[0]:
            local = partes[0]

        if len(partes) >= 2 and partes[1]:
            docente = partes[1]

    return {
        "disciplina": disciplina,
        "local": local,
        "docente": docente,
    }


def crear_evento(
    curso: str,
    ano: int,
    periodo: str,
    turma: str,
    dia: str,
    inicio: str,
    fim: str,
    texto_celda: str,
) -> Evento:
    """Construye un Evento a partir de los datos de una celda."""

    datos = parsear_celda(texto_celda)

    tipo = "aula"

    if "tutor" in datos["disciplina"].lower():
        tipo = "tutoria"

    return Evento(
        curso=curso,
        ano=ano,
        periodo=periodo,
        turma=turma,
        dia=dia,
        inicio=inicio,
        fim=fim,
        disciplina=datos["disciplina"],
        local=datos["local"],
        docente=datos["docente"],
        tipo=tipo,
    )