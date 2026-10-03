import json

from ocr.ocr import ejecutar_ocr, extraer_tablas


def convertir_para_json(tablas):
    datos = []

    for tabla in tablas:
        pred = tabla["table_ocr_pred"]

        datos.append({
            "table_region_id": tabla["table_region_id"],
            "rec_boxes": [
                [float(valor) for valor in box]
                for box in pred["rec_boxes"]
            ],
            "rec_texts": pred["rec_texts"],
            "rec_scores": [
                float(score)
                for score in pred["rec_scores"]
            ],
        })

    return datos


def main():
    print("Ejecutando OCR...")

    resultado = ejecutar_ocr("horario.jpeg")
    tablas = extraer_tablas(resultado)

    datos = convertir_para_json(tablas)

    with open(
        "ocr_resultado.json",
        "w",
        encoding="utf-8",
    ) as archivo:
        json.dump(
            datos,
            archivo,
            ensure_ascii=False,
            indent=2,
        )

    print("\nResultado OCR guardado en ocr_resultado.json")
    print(f"Tablas guardadas: {len(datos)}")


if __name__ == "__main__":
    main()