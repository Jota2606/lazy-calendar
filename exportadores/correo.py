import os
import smtplib
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


def enviar_correo(
    ruta_adjunto: str | Path,
) -> None:
    correo = os.getenv("SMTP_EMAIL")
    password = os.getenv("SMTP_PASSWORD")
    destino = os.getenv("DESTINO_EMAIL")

    if not correo:
        raise ValueError(
            "No se encontró SMTP_EMAIL en el archivo .env."
        )

    if not password:
        raise ValueError(
            "No se encontró SMTP_PASSWORD en el archivo .env."
        )

    if not destino:
        raise ValueError(
            "No se encontró DESTINO_EMAIL en el archivo .env."
        )

    ruta_adjunto = Path(ruta_adjunto)

    if not ruta_adjunto.exists():
        raise FileNotFoundError(
            f"No existe el archivo: {ruta_adjunto}"
        )

    mensaje = EmailMessage()

    mensaje["Subject"] = "Horario UNIC"
    mensaje["From"] = correo
    mensaje["To"] = destino

    mensaje.set_content(
        "Adjunto encontrarás tu horario de la UNIC "
        "en formato compatible con calendario."
    )

    with ruta_adjunto.open("rb") as archivo:
        contenido = archivo.read()

    mensaje.add_attachment(
        contenido,
        maintype="text",
        subtype="calendar",
        filename=ruta_adjunto.name,
    )

    with smtplib.SMTP(
        "smtp.gmail.com",
        587,
    ) as servidor:
        servidor.starttls()

        servidor.login(
            correo,
            password,
        )

        servidor.send_message(
            mensaje
        )