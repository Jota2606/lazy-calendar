def normalizar_dia(texto: str) -> str | None:
    """Normaliza el nombre de un día reconocido por OCR."""
    equivalencias = {
        "SEGUNDA": "SEGUNDA",
        "TERCA": "TERÇA",
        "TERÇA": "TERÇA",
        "QUARTA": "QUARTA",
        "QUINTA": "QUINTA",
        "SEXTA": "SEXTA",
    }

    return equivalencias.get(texto.strip().upper())


def es_hora(texto: str) -> bool:
    """Indica si un texto tiene formato HH:MM-HH:MM."""
    partes = texto.split("-")

    if len(partes) != 2:
        return False

    for parte in partes:
        valores = parte.strip().split(":")

        if len(valores) != 2:
            return False

        try:
            hora = int(valores[0])
            minuto = int(valores[1])
        except ValueError:
            return False

        if not (0 <= hora <= 23 and 0 <= minuto <= 59):
            return False

    return True


def extraer_dias(tabla: dict) -> dict[str, float]:
    """Extrae los días y su posición horizontal."""
    dias = {}

    textos = tabla["rec_texts"]
    scores = tabla["rec_scores"]
    cajas = tabla["rec_boxes"]

    for texto, score, caja in zip(textos, scores, cajas):
        if score < 0.80:
            continue

        dia = normalizar_dia(texto)

        if dia is None:
            continue

        x1, _, x2, _ = caja
        centro_x = (x1 + x2) / 2

        dias[dia] = centro_x

    return dias


def extraer_franjas(tabla: dict) -> list[dict]:
    """Extrae las franjas horarias detectadas en la tabla."""
    franjas = []

    textos = tabla["rec_texts"]
    scores = tabla["rec_scores"]
    cajas = tabla["rec_boxes"]

    for texto, score, caja in zip(textos, scores, cajas):
        if score < 0.80:
            continue

        texto = texto.strip()

        if not es_hora(texto):
            continue

        x1, y1, x2, y2 = caja

        franjas.append(
            {
                "hora": texto,
                "x": (x1 + x2) / 2,
                "y": (y1 + y2) / 2,
            }
        )

    franjas.sort(key=lambda franja: franja["y"])

    return franjas


def extraer_franjas_matutinas(tabla: dict) -> list[dict]:
    """Extrae únicamente las franjas del horario matutino."""
    franjas = extraer_franjas(tabla)

    return [
        franja
        for franja in franjas
        if franja["y"] < 1200
    ]


def centro_x(caja) -> float:
    x1, _, x2, _ = caja
    return (x1 + x2) / 2


def centro_y(caja) -> float:
    _, y1, _, y2 = caja
    return (y1 + y2) / 2


def obtener_dia_mas_cercano(
    x: float,
    dias: dict[str, float],
) -> str:
    """Devuelve el día cuya columna está más cerca de X."""
    return min(
        dias,
        key=lambda dia: abs(x - dias[dia]),
    )


def extraer_contenido_matutino(
    tabla: dict,
    dias: dict[str, float],
) -> list[dict]:
    """
    Extrae los textos que pertenecen a las columnas
    del horario matutino.
    """
    contenidos = []

    textos = tabla["rec_texts"]
    scores = tabla["rec_scores"]
    cajas = tabla["rec_boxes"]

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

        dia = obtener_dia_mas_cercano(x, dias)

        distancia = abs(
            x - dias[dia]
        )

        # Evita asignar textos alejados de cualquier día.
        if distancia > 450:
            continue

        # Los encabezados ya fueron utilizados para
        # detectar las columnas y no son contenido.
        if texto.upper() in {
            "SEGUNDA",
            "TERCA",
            "TERÇA",
            "QUARTA",
            "QUINTA",
            "SEXTA",
        }:
            continue

        contenidos.append(
            {
                "texto": texto,
                "score": score,
                "x": x,
                "y": y,
                "dia": dia,
            }
        )

    contenidos.sort(
        key=lambda contenido: (
            contenido["dia"],
            contenido["y"],
        )
    )

    return contenidos


def extraer_metadata(tabla: dict) -> dict:
    """
    Extrae la metadata principal del horario matutino.
    Conserva el primer valor encontrado para cada campo.
    """
    import re

    metadata = {
        "curso": None,
        "ano": None,
        "periodo": None,
        "turma": None,
    }

    textos = tabla["rec_texts"]

    for texto in textos:
        texto = texto.strip()

        if not texto:
            continue

        # CURSO
        if metadata["curso"] is None:
            match = re.search(
                r"CURSO:\s*(.*?)(?=\s+ANO:|$)",
                texto,
                re.IGNORECASE,
            )

            if match:
                metadata["curso"] = match.group(1).strip()

        # ANO
        if metadata["ano"] is None:
            match = re.search(
                r"ANO:\s*(\d+)",
                texto,
                re.IGNORECASE,
            )

            if match:
                metadata["ano"] = int(
                    match.group(1)
                )

        # PERIODO
        if metadata["periodo"] is None:
            match = re.search(
                r"PERIODO:\s*(MATUTINO|NOTURNO)",
                texto.upper(),
                re.IGNORECASE,
            )

            if match:
                metadata["periodo"] = (
                    match.group(1).strip()
                )

        # TURMA
        if metadata["turma"] is None:
            match = re.search(
                r"T(?:H)?URMA:\s*([A-Z0-9]+)",
                texto.upper(),
                re.IGNORECASE,
            )

            if match:
                metadata["turma"] = (
                    match.group(1).strip()
                )

    return metadata