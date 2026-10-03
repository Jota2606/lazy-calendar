from parsers.parser import analizar_estructura
from validators.validator import validar_evento

resultado = analizar_estructura(
    "output/ocr_resultado.json"
)

print("\nDÍAS")
print("=" * 40)

for dia, x in resultado["dias"].items():
    print(f"{dia:8} -> X={x:.1f}")


print("\nFRANJAS")
print("=" * 40)

for franja in resultado["franjas"]:
    print(
        f"{franja['hora']:15}"
        f" X={franja['x']:.1f}"
        f" Y={franja['y']:.1f}"
    )

print("\nCONTENIDO MATUTINO")
print("=" * 80)

for contenido in resultado["contenidos"]:
    print(
        f"{contenido['dia']:8}"
        f" Y={contenido['y']:7.1f}"
        f" score={contenido['score']:.2f}"
        f" | {contenido['texto']}"
    )

print("\nCELDAS DETECTADAS")
print("=" * 80)

for dia, grupos in resultado["celdas"].items():
    print(f"\n{dia}")

    for numero, grupo in enumerate(
        grupos,
        start=1,
    ):
        print(
            f"\n  CELDA {numero}"
            f" | Y={grupo[0]['y']:.1f}"
            f"-{grupo[-1]['y']:.1f}"
        )

        for elemento in grupo:
            print(
                f"    Y={elemento['y']:7.1f}"
                f" | {elemento['texto']}"
            )

print("\nFRANJAS POR CELDA")
print("=" * 80)

for dia, grupos in resultado["celdas"].items():
    print(f"\n{dia}")

    franjas_dia = resultado["franjas_por_celda"][dia]

    for numero, franjas_celda in enumerate(
        franjas_dia,
        start=1,
    ):
        if franjas_celda:
            texto_franjas = ", ".join(
                franja["hora"]
                for franja in franjas_celda
            )
        else:
            texto_franjas = "NINGUNA"

        print(
            f"  CELDA {numero}"
            f" -> {texto_franjas}"
        )

print()
print("DATOS DE LAS CELDAS")
print("=" * 80)

for dia, celdas in resultado["datos_celdas"].items():
    print()
    print(dia)

    for numero, datos in enumerate(celdas, start=1):
        print(f"  CELDA {numero}")
        print(f"    disciplina -> {datos['disciplina']}")
        print(f"    docente    -> {datos['docente']}")
        print(f"    local      -> {datos['local']}")
        print(f"    otros      -> {datos['otros']}")

print()
print("METADATA")
print("=" * 80)

for clave, valor in resultado["metadata"].items():
    print(f"{clave:10} -> {valor}")

print()
print("EVENTOS")
print("=" * 100)

for numero, evento in enumerate(
    resultado["eventos"],
    start=1,
):
    print(
        f"{numero:02d}. "
        f"{evento.dia:8} "
        f"{evento.inicio}-{evento.fim} | "
        f"{evento.tipo:7} | "
        f"{evento.disciplina}"
    )

print()
print("VALIDACIÓN")
print("=" * 80)

errores_totales = 0

for numero, evento in enumerate(
    resultado["eventos"],
    start=1,
):
    errores = validar_evento(evento)

    if errores:
        errores_totales += len(errores)

        print()
        print(
            f"EVENTO {numero:02d} "
            f"{evento.dia} "
            f"{evento.inicio}-{evento.fim}"
        )

        for error in errores:
            print(f"  ERROR: {error}")

    else:
        print(
            f"{numero:02d}. OK"
        )

print()
print(
    f"Errores encontrados: {errores_totales}"
)