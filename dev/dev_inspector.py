import json


def cargar_resultado():
    with open(
        "ocr_resultado.json",
        "r",
        encoding="utf-8",
    ) as archivo:
        return json.load(archivo)


def main():
    datos = cargar_resultado()

    print(f"Tablas encontradas: {len(datos)}")

    for tabla in datos:
        print("\n" + "=" * 70)
        print(f"TABLA {tabla['table_region_id']}")
        print("=" * 70)

        textos = tabla["rec_texts"]
        boxes = tabla["rec_boxes"]
        scores = tabla["rec_scores"]

        for i, (texto, box, score) in enumerate(
            zip(textos, boxes, scores)
        ):
            x1, y1, x2, y2 = box

            print(
                f"{i:03d} | "
                f"X={x1:7.1f}-{x2:7.1f} | "
                f"Y={y1:7.1f}-{y2:7.1f} | "
                f"{score:.2f} | "
                f"{texto}"
            )


if __name__ == "__main__":
    main()