from dataclasses import dataclass


# ============================================================
# CONFIGURACIÓN DEL HORARIO
# ============================================================

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


# ============================================================
# MODELO DE DATOS
# ============================================================

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


# ============================================================
# FUNCIONES AUXILIARES DE HORA
# ============================================================

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

    orden_dias = {
        "SEGUNDA": 0,
        "TERÇA": 1,
        "QUARTA": 2,
        "QUINTA": 3,
        "SEXTA": 4,
    }

    dias = {
        evento.dia
        for evento in eventos
    }

    return sorted(
        dias,
        key=lambda dia: orden_dias[dia]
    )

def crear_tabla(eventos: list[Evento]) -> dict[str, list[Evento]]:
    """Organiza los eventos por día y los ordena cronológicamente."""

    tabla = {
        dia: []
        for dia in DIAS_VALIDOS
    }

    for evento in eventos:
        tabla[evento.dia].append(evento)

    orden_dias = {
        "SEGUNDA": 0,
        "TERÇA": 1,
        "QUARTA": 2,
        "QUINTA": 3,
        "SEXTA": 4,
    }

    tabla = dict(
        sorted(
            tabla.items(),
            key=lambda item: orden_dias[item[0]]
        )
    )

    for dia in tabla:
        tabla[dia].sort(
            key=lambda evento: hora_a_minutos(evento.inicio)
        )

    return tabla

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


# ============================================================
# FUNCIONES DE VALIDACIÓN
# ============================================================

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


# ============================================================
# TRADUCCIÓN PARA EL CALENDARIO
# ============================================================

def dia_para_calendario(dia: str) -> str:
    """Convierte el día portugués al equivalente en español."""

    return DIAS_ES[dia]


# ============================================================
# DATOS DE PRUEBA
# ============================================================

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