from models.horario import Evento, crear_tabla
from parsers.parser import parsear_celda, crear_evento
from validators.validator import validar_evento


def mostrar_evento(evento: Evento) -> None:
    """Muestra toda la información disponible de un evento."""

    print(f"   {evento.inicio}-{evento.fim}")
    print(f"      Asignatura: {evento.disciplina}")
    print(f"      Local: {evento.local or 'No indicado'}")
    print(f"      Docente: {evento.docente or 'No indicado'}")
    print(f"      Tipo: {evento.tipo}")


def mostrar_horario(eventos: list[Evento]) -> None:
    """Muestra los eventos organizados por día."""

    tabla = crear_tabla(eventos)

    print("\nHORARIO:\n")

    for dia, eventos_del_dia in tabla.items():
        print(f"{dia}:")

        if not eventos_del_dia:
            print("   —")
            continue

        for evento in eventos_del_dia:
            mostrar_evento(evento)


def mostrar_errores(evento: Evento) -> None:
    """Muestra los errores encontrados en un evento."""

    errores = validar_evento(evento)

    if not errores:
        return

    print(f"\nERRORES EN {evento.disciplina}:")

    for error in errores:
        print(f"   - {error}")


def main() -> None:
    """Punto de entrada principal del programa."""

    horario = [
        Evento(
            curso="ENGENHARIA INFORMÁTICA",
            ano=3,
            periodo="VESPERTINO",
            turma="ENGINF-A3V1",
            dia="SEGUNDA",
            inicio="12:30",
            fim="14:30",
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

    # Validar eventos
    for evento in horario:
        mostrar_errores(evento)

    # Mostrar horario
    mostrar_horario(horario)

    # Probar parser de una celda
    texto_celda = """Estrutura de Dados e Algoritmos II
Luei 1.5 | Isabel Acosta"""

    datos = parsear_celda(texto_celda)

    print("\nCELDA PARSEADA:\n")

    print(f"Asignatura: {datos['disciplina']}")
    print(f"Local: {datos['local']}")
    print(f"Docente: {datos['docente']}")

    # Probar creación automática de evento
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


if __name__ == "__main__":
    main()