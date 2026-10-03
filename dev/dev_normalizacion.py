import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(RAIZ_PROYECTO),
)

from parsers.parser import analizar_estructura
from normalizadores.normalizador import normalizar_eventos


def main():
    ruta_ocr = (
        RAIZ_PROYECTO
        / "output"
        / "ocr_resultado.json"
    )

    resultado = analizar_estructura(
        ruta_ocr
    )

    eventos = resultado["eventos"]

    print()
    print("=" * 70)
    print("ANTES DE NORMALIZAR")
    print("=" * 70)

    for numero, evento in enumerate(
        eventos,
        start=1,
    ):
        print(
            f"{numero:02d}. "
            f"{evento.dia:8} "
            f"{evento.inicio}-{evento.fim} | "
            f"{evento.disciplina}"
        )

    eventos_normalizados = normalizar_eventos(
        eventos
    )

    print()
    print("=" * 70)
    print("DESPUÉS DE NORMALIZAR")
    print("=" * 70)

    for numero, evento in enumerate(
        eventos_normalizados,
        start=1,
    ):
        print(
            f"{numero:02d}. "
            f"{evento.dia:8} "
            f"{evento.inicio}-{evento.fim} | "
            f"{evento.disciplina}"
        )


if __name__ == "__main__":
    main()