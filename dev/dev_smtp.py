import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).resolve().parent.parent)
)

from exportadores.correo import enviar_correo


enviar_correo(
    "output/horario.ics"
)

print(
    "SMTP: horario enviado correctamente."
)