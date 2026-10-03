import sys
from datetime import date
from pathlib import Path

RAIZ_PROYECTO = Path(__file__).resolve().parent.parent

sys.path.insert(
    0,
    str(RAIZ_PROYECTO),
)

from parsers.parser import analizar_estructura
from exportadores.ical import exportar_ical


resultado = analizar_estructura(
    RAIZ_PROYECTO / "output" / "ocr_resultado.json"
)

eventos = resultado["eventos"]

fecha_inicio = date(2026, 10, 5)

exportar_ical(
    eventos=eventos,
    fecha_inicio=fecha_inicio,
    ruta_salida=RAIZ_PROYECTO / "output" / "horario.ics",
)

print()
print("=" * 60)
print("EXPORTACIÓN iCAL")
print("=" * 60)

print(f"Eventos exportados: {len(eventos)}")
print(f"Semana iniciada: {fecha_inicio}")
print("Archivo: output/horario.ics")

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