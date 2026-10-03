import json


def cargar_resultado():
    with open(
        "ocr_resultado.json",
        "r",
        encoding="utf-8",
    ) as archivo:
        return json.load(archivo)


def centro_y(box):
    return (box[1] + box[3]) / 2


def es_metadata_matutina(texto):
    texto = texto.upper()
    return "PERIODO:" in texto and "MATUTINO" in texto


def es_inicio_curso(texto):
    return texto.upper().startswith("CURSO:")


def obtener_bloque_matutino(tabla):
    textos = tabla["rec_texts"]
    boxes = tabla["rec_boxes"]
    scores = tabla["rec_scores"]

    inicio = None
    fin = len(textos)

    # Buscar metadata MATUTINO
    for i, texto in enumerate(textos):
        if es_metadata_matutina(texto):
            inicio = centro_y(boxes[i])
            break

    if inicio is None:
        return []

    # Buscar el siguiente CURSO después del bloque matutino
    for i, texto in enumerate(textos):
        if centro_y(boxes[i]) <= inicio:
            continue

        if es_inicio_curso(texto):
            fin = centro_y(boxes[i])
            break

    bloque = []

    for texto, box, score in zip(textos, boxes, scores):
        y = centro_y(box)

        if inicio <= y < fin:
            bloque.append({
                "texto": texto,
                "box": box,
                "score": score,
            })

    return bloque


def main():
    datos = cargar_resultado()

    # La tabla 1 contiene el bloque matutino.
    tabla = datos[0]

    bloque = obtener_bloque_matutino(tabla)

    print("\n" + "=" * 80)
    print("BLOQUE MATUTINO")
    print("=" * 80)

    for i, elemento in enumerate(bloque):
        box = elemento["box"]

        print(
            f"{i:03d} | "
            f"X={box[0]:7.1f}-{box[2]:7.1f} | "
            f"Y={box[1]:7.1f}-{box[3]:7.1f} | "
            f"{elemento['score']:.2f} | "
            f"{elemento['texto']}"
        )


if __name__ == "__main__":
    main()