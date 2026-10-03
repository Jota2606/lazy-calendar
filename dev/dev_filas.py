import json


def centro_x(caja):
    x1, _, x2, _ = caja
    return (x1 + x2) / 2


def centro_y(caja):
    _, y1, _, y2 = caja
    return (y1 + y2) / 2


def normalizar_dia(texto):
    texto = texto.upper().strip()

    equivalencias = {
        "SEGUNDA": "SEGUNDA",
        "TERCA": "TERÇA",
        "TERÇA": "TERÇA",
        "QUARTA": "QUARTA",
        "QUINTA": "QUINTA",
        "SEXTA": "SEXTA",
    }

    return equivalencias.get(texto)


def es_hora(texto):
    partes = texto.split("-")

    if len(partes) != 2:
        return False

    def validar_parte(parte):
        valores = parte.strip().split(":")

        if len(valores) != 2:
            return False

        try:
            hora = int(valores[0])
            minuto = int(valores[1])
        except ValueError:
            return False

        return (
            0 <= hora <= 23
            and 0 <= minuto <= 59
        )

    return validar_parte(partes[0]) and validar_parte(partes[1])


def main():
    with open(
        "output/ocr_resultado.json",
        "r",
        encoding="utf-8",
    ) as archivo:
        datos_ocr = json.load(archivo)

    tabla = datos_ocr["tablas"][0]

    textos = tabla["rec_texts"]
    scores = tabla["rec_scores"]
    cajas = tabla["rec_boxes"]

    print("\n" + "=" * 80)
    print("COLUMNAS")
    print("=" * 80)

    columnas = {}

    for texto, score, caja in zip(textos, scores, cajas):
        if score < 0.80:
            continue

        dia = normalizar_dia(texto)

        if dia is None:
            continue

        columnas[dia] = centro_x(caja)

    for dia, x in sorted(columnas.items(), key=lambda item: item[1]):
        print(f"{dia:8} -> X={x:.1f}")

    print("\n" + "=" * 80)
    print("FRANJAS HORARIAS")
    print("=" * 80)

    franjas = []

    for texto, score, caja in zip(textos, scores, cajas):
        if score < 0.80:
            continue

        if not es_hora(texto):
            continue

        franjas.append(
            {
                "hora": texto,
                "x": centro_x(caja),
                "y": centro_y(caja),
            }
        )

    franjas.sort(key=lambda item: item["y"])

    for franja in franjas:
        print(
            f"{franja['hora']:15} "
            f"X={franja['x']:6.1f} "
            f"Y={franja['y']:6.1f}"
        )


if __name__ == "__main__":
    main()