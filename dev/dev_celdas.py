import json


DIAS = [
    "SEGUNDA",
    "TERÇA",
    "QUARTA",
    "QUINTA",
    "SEXTA",
]

COLUMNAS = {
    "SEGUNDA": 874.0,
    "TERÇA": 1632.0,
    "QUARTA": 2348.0,
    "QUINTA": 3045.0,
    "SEXTA": 3708.5,
}

FRANJAS_MATUTINAS = [
    {
        "hora": "7:30-9:30",
        "inicio_contenido": 480.0,
    },
    {
        "hora": "9:40-11:40",
        "inicio_contenido": 780.0,
    },
    {
        "hora": "11:45-12:30",
        "inicio_contenido": 1020.0,
    },
]

DISTANCIA_MAX_COLUMNA = 450
DISTANCIA_MAXIMA_ENTRE_LINEAS = 100


def centro_x(caja):
    x1, _, x2, _ = caja
    return (x1 + x2) / 2


def centro_y(caja):
    _, y1, _, y2 = caja
    return (y1 + y2) / 2


def obtener_dia_mas_cercano(x):
    return min(
        COLUMNAS,
        key=lambda dia: abs(x - COLUMNAS[dia]),
    )


def obtener_franja_inicial(y):
    """
    Determina en qué fila comienza una celda según
    la posición de su primera línea de OCR.
    """

    for indice in range(
        len(FRANJAS_MATUTINAS) - 1,
        -1,
        -1,
    ):
        if y >= FRANJAS_MATUTINAS[indice]["inicio_contenido"]:
            return indice

    return None


def obtener_franjas_que_cubre(y_inicio, y_fin):
    """
    Determina las filas que ocupa una celda.

    La fila se determina por el lugar donde comienza
    el contenido. Una celda solo se considera fusionada
    con la siguiente si su contenido continúa claramente
    después del inicio de esa siguiente fila.
    """

    fila_inicial = obtener_franja_inicial(y_inicio)

    if fila_inicial is None:
        return []

    franjas = [
        FRANJAS_MATUTINAS[fila_inicial]["hora"]
    ]

    for indice in range(
        fila_inicial + 1,
        len(FRANJAS_MATUTINAS),
    ):
        inicio_siguiente = (
            FRANJAS_MATUTINAS[indice]["inicio_contenido"]
        )

        if y_fin >= inicio_siguiente:
            franjas.append(
                FRANJAS_MATUTINAS[indice]["hora"]
            )

    return franjas


def agrupar_por_celda(elementos):
    if not elementos:
        return []

    elementos = sorted(
        elementos,
        key=lambda item: item["y"],
    )

    grupos = []
    grupo_actual = [elementos[0]]

    for elemento in elementos[1:]:

        anterior = grupo_actual[-1]

        distancia = elemento["y"] - anterior["y"]

        if distancia <= DISTANCIA_MAXIMA_ENTRE_LINEAS:
            grupo_actual.append(elemento)
        else:
            grupos.append(grupo_actual)
            grupo_actual = [elemento]

    grupos.append(grupo_actual)

    return grupos


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

    columnas = {
        dia: []
        for dia in DIAS
    }

    for texto, score, caja in zip(
        textos,
        scores,
        cajas,
    ):
        if score < 0.80:
            continue

        texto = texto.strip()

        if not texto:
            continue

        x = centro_x(caja)
        y = centro_y(caja)

        # Solo zona matutina.
        if y < 480 or y >= 1200:
            continue

        dia = obtener_dia_mas_cercano(x)

        distancia = abs(
            x - COLUMNAS[dia]
        )

        if distancia > DISTANCIA_MAX_COLUMNA:
            continue

        # Ignorar encabezados.
        if texto.upper() in {
            "SEGUNDA",
            "TERCA",
            "TERÇA",
            "QUARTA",
            "QUINTA",
            "SEXTA",
        }:
            continue

        columnas[dia].append(
            {
                "texto": texto,
                "score": score,
                "x": x,
                "y": y,
            }
        )

    print()
    print("=" * 100)
    print("RECONSTRUCCIÓN GEOMÉTRICA DE CELDAS MATUTINAS")
    print("=" * 100)

    for dia in DIAS:

        print()
        print("#" * 100)
        print(dia)
        print("#" * 100)

        grupos = agrupar_por_celda(
            columnas[dia]
        )

        for numero, grupo in enumerate(
            grupos,
            start=1,
        ):
            y_inicio = grupo[0]["y"]
            y_fin = grupo[-1]["y"]

            franjas = obtener_franjas_que_cubre(
                y_inicio,
                y_fin,
            )

            print()
            print(
                f"CELDA {numero}"
                f" | Y={y_inicio:.1f}-{y_fin:.1f}"
            )

            if franjas:
                print(
                    "   FRANJAS QUE CUBRE:"
                    f" {', '.join(franjas)}"
                )
            else:
                print(
                    "   FRANJAS QUE CUBRE: ninguna"
                )

            for elemento in grupo:
                print(
                    f"   Y={elemento['y']:7.1f}"
                    f" | score={elemento['score']:.2f}"
                    f" | {elemento['texto']}"
                )


if __name__ == "__main__":
    main()