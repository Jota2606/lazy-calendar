import sys
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(RAIZ_PROYECTO),
)

from parsers.parser import analizar_estructura
from exportadores.excel import exportar_excel


resultado = analizar_estructura(
    RAIZ_PROYECTO / "output" / "ocr_resultado.json"
)

eventos = resultado["eventos"]

ruta_salida = RAIZ_PROYECTO / "output" / "horario.xlsx"

exportar_excel(
    eventos=eventos,
    ruta_salida=ruta_salida,
)

print()
print("=" * 60)
print("EXPORTACIÓN EXCEL")
print("=" * 60)

print(f"Eventos exportados: {len(eventos)}")
print("Archivo: output/horario.xlsx")

print()
print("EVENTOS")
print("=" * 60)

for numero, evento in enumerate(eventos, start=1):
    print(
        f"{numero:02d}. "
        f"{evento.dia:8} "
        f"{evento.inicio}-{evento.fim} | "
        f"{evento.disciplina}"
    )

print()
print("Exportación completada correctamente.")