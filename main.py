from models.horario import Evento, crear_tabla

def mostrar_evento(evento: Evento) -> None:
    """Muestra toda la información disponible de un evento."""

    print(f"   {evento.inicio}-{evento.fim}")
    print(f"      Asignatura: {evento.disciplina}")
    print(f"      Local: {evento.local or 'No indicado'}")
    print(f"      Docente: {evento.docente or 'No indicado'}")
    print(f"      Tipo: {evento.tipo}")

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

horario = [
    Evento(
        curso="ENGENHARIA INFORMÁTICA",
        ano=3,
        periodo="VESPERTINO",
        turma="ENGINF-A3V1",
        dia="SEGUNDA",
        inicio="12:30",
        fim="14:300",
        disciplina="Estrutura de Dados e Algoritmos II",
        local="Luei 1.5",
        docente="Isabel Acosta",
    ),

    Evento(
        curso="ENGENHARIA INFORMÁTICA",
        ano=3,
        periodo="VESPERTINO",
        turma="ENGINF-A3V1",
        dia="TERÇA",
        inicio="14:40",
        fim="16:40",
        disciplina="Programação",
        local="Laboratório de Sistemas",
        docente="Luis Pimentel",
    ),

    Evento(
        curso="ENGENHARIA INFORMÁTICA",
        ano=3,
        periodo="VESPERTINO",
        turma="ENGINF-A3V1",
        dia="QUARTA",
        inicio="16:45",
        fim="17:30",
        disciplina="Tutorias",
        local="Luei 1.8",
        docente="Miguel Farias",
        tipo="tutoria",
    ),
]


# ============================================================
# PRUEBA DEL PROGRAMA
# ============================================================

tabla = crear_tabla(horario)

print("\nHORARIO:\n")

for dia, eventos in tabla.items():

    print(f"{dia}:")

    if not eventos:
        print("   —")
        continue

    for evento in eventos:
        mostrar_evento(evento)

texto_celda = """Estrutura de Dados e Algoritmos II
Luei 1.5 | Isabel Acosta"""

datos = parsear_celda(texto_celda)

print("\nCELDA PARSEADA:\n")

print(f"Asignatura: {datos['disciplina']}")
print(f"Local: {datos['local']}")
print(f"Docente: {datos['docente']}")

evento_prueba = crear_evento(
    curso="ENGENHARIA INFORMÁTICA",
    ano=3,
    periodo="VESPERTINO",
    turma="ENGINF-A3V1",
    dia="SEGUNDA",
    inicio="12:30",
    fim="14:30",
    texto_celda="""Estrutura de Dados e Algoritmos II
Luei 1.5 | Isabel Acosta""",
)

print("\nEVENTO CREADO AUTOMÁTICAMENTE:\n")

mostrar_evento(evento_prueba)