DISTANCIA_MAXIMA_ENTRE_LINEAS = 100


def agrupar_por_celda(
    elementos: list[dict],
) -> list[list[dict]]:
    """
    Agrupa líneas de OCR que probablemente pertenecen
    a la misma celda de la tabla.
    """
    if not elementos:
        return []

    elementos = sorted(
        elementos,
        key=lambda elemento: elemento["y"],
    )

    grupos = []
    grupo_actual = [elementos[0]]

    for elemento in elementos[1:]:
        anterior = grupo_actual[-1]

        distancia = (
            elemento["y"] - anterior["y"]
        )

        if distancia <= DISTANCIA_MAXIMA_ENTRE_LINEAS:
            grupo_actual.append(elemento)
        else:
            grupos.append(grupo_actual)
            grupo_actual = [elemento]

    grupos.append(grupo_actual)

    return grupos


def agrupar_contenido_por_dia(
    contenidos: list[dict],
) -> dict[str, list[list[dict]]]:
    """
    Agrupa el contenido OCR por día y posteriormente
    por celda.
    """
    por_dia = {}

    for contenido in contenidos:
        dia = contenido["dia"]

        por_dia.setdefault(
            dia,
            [],
        ).append(contenido)

    resultado = {}

    for dia, elementos in por_dia.items():
        resultado[dia] = agrupar_por_celda(
            elementos
        )

    return resultado


def extraer_datos_celda(
    celda: list[dict],
) -> dict:
    """
    Separa el contenido textual de una celda en
    disciplina, docente, local y otros textos.
    """
    disciplina = None
    docente = None
    local = None
    otros = []

    for elemento in celda:
        texto = elemento["texto"].strip()

        if not texto:
            continue

        texto_lower = texto.lower()

        # Docente
        if texto_lower.startswith("prof:"):
            docente = texto.split(":", 1)[1].strip()
            continue

        # Local
        if texto_lower.startswith("cutato"):
            local = texto
            continue

        # Primer texto que no sea docente/local:
        # lo consideramos la disciplina.
        if disciplina is None:
            disciplina = texto
            continue

        # Todo texto adicional queda conservado.
        otros.append(texto)

    return {
        "disciplina": disciplina,
        "docente": docente,
        "local": local,
        "otros": otros,
    }


def extraer_datos_de_celdas(
    celdas: dict[str, list[list[dict]]],
) -> dict[str, list[dict]]:
    """
    Extrae los datos semánticos de todas las celdas.
    """
    resultado = {}

    for dia, grupos in celdas.items():
        resultado[dia] = []

        for celda in grupos:
            datos = extraer_datos_celda(celda)

            resultado[dia].append(datos)

    return resultado


def franjas_de_celda(
    celda: list[dict],
    franjas: list[dict],
) -> list[dict]:
    """
    Determina qué franjas horarias cubre una celda
    utilizando su posición y altura vertical.
    """
    if not celda or not franjas:
        return []

    franjas = sorted(
        franjas,
        key=lambda franja: franja["y"],
    )

    y_min = min(
        elemento["y"]
        for elemento in celda
    )

    y_max = max(
        elemento["y"]
        for elemento in celda
    )

    altura = y_max - y_min

    # Las celdas normales del horario tienen
    # aproximadamente esta altura.
    altura_normal = 130

    # CELDA NORMAL
    if altura <= altura_normal:
        centro = (y_min + y_max) / 2

        indice = min(
            range(len(franjas)),
            key=lambda indice: abs(
                centro - franjas[indice]["y"]
            ),
        )

        return [franjas[indice]]

    # CELDA FUSIONADA
    indice_inicio = min(
        range(len(franjas)),
        key=lambda indice: abs(
            y_min - franjas[indice]["y"]
        ),
    )

    indice_fin = min(
        range(len(franjas)),
        key=lambda indice: abs(
            y_max - franjas[indice]["y"]
        ),
    )

    inicio = min(
        indice_inicio,
        indice_fin,
    )

    fin = max(
        indice_inicio,
        indice_fin,
    )

    return franjas[inicio:fin + 1]


def obtener_franjas_por_celda(
    celdas: dict[str, list[list[dict]]],
    franjas: list[dict],
) -> dict[str, list[list[dict]]]:
    """
    Determina las franjas horarias de cada celda.
    """
    resultado = {}

    for dia, grupos in celdas.items():
        resultado[dia] = []

        for celda in grupos:
            resultado[dia].append(
                franjas_de_celda(
                    celda,
                    franjas,
                )
            )

    return resultado