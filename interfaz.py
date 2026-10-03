import threading
import tkinter as tk
from tkinter import filedialog, ttk
from pathlib import Path

from parsers.parser import analizar_estructura

from ocr.ocr import (
    ejecutar_ocr,
    guardar_resultado_json,
)


class AplicacionHorario:
    def __init__(self, ventana: tk.Tk):
        self.ventana = ventana

        self.ventana.title("Horario UNIC")
        self.ventana.geometry("700x450")
        self.ventana.minsize(600, 400)

        self.ruta_imagen: Path | None = None
        self.eventos = []

        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = ttk.Frame(
            self.ventana,
            padding=30,
        )
        contenedor.pack(
            fill="both",
            expand=True,
        )

        titulo = ttk.Label(
            contenedor,
            text="HORARIO UNIC",
            font=("Segoe UI", 24, "bold"),
        )
        titulo.pack(pady=(30, 5))

        subtitulo = ttk.Label(
            contenedor,
            text="Generador de horario universitario",
            font=("Segoe UI", 11),
        )
        subtitulo.pack(pady=(0, 40))

        self.boton_seleccionar = ttk.Button(
            contenedor,
            text="Seleccionar horario",
            command=self.seleccionar_imagen,
        )
        self.boton_seleccionar.pack(
            ipadx=20,
            ipady=10,
        )

        self.archivo_label = ttk.Label(
            contenedor,
            text="Ningún horario seleccionado",
        )
        self.archivo_label.pack(pady=20)

        self.boton_analizar = ttk.Button(
            contenedor,
            text="Analizar horario",
            command=self.analizar_horario,
            state="disabled",
        )
        self.boton_analizar.pack(
            ipadx=20,
            ipady=8,
        )

        self.estado_label = ttk.Label(
            contenedor,
            text="Listo.",
        )
        self.estado_label.pack(pady=30)

    def seleccionar_imagen(self):
        ruta = filedialog.askopenfilename(
            title="Seleccionar imagen del horario",
            filetypes=[
                (
                    "Imágenes",
                    "*.jpg *.jpeg *.png *.webp",
                ),
                (
                    "Todos los archivos",
                    "*.*",
                ),
            ],
        )

        if not ruta:
            return

        self.ruta_imagen = Path(ruta)

        self.archivo_label.config(
            text=self.ruta_imagen.name,
        )

        self.boton_analizar.config(
            state="normal",
        )

        self.estado_label.config(
            text="Imagen seleccionada.",
        )

    def analizar_horario(self):
        if self.ruta_imagen is None:
            return

        self.boton_seleccionar.config(
            state="disabled",
        )

        self.boton_analizar.config(
            state="disabled",
        )

        self.estado_label.config(
            text="Analizando horario... Esto puede tardar aproximadamente 1 minuto.",
        )

        hilo = threading.Thread(
            target=self.ejecutar_proceso_ocr,
            daemon=True,
        )

        hilo.start()

    def ejecutar_proceso_ocr(self):
        try:

            print()
            print("=" * 60)
            print("INTERFAZ: INICIO OCR")
            print("=" * 60)

            ruta_salida = (
                Path(__file__).resolve().parent
                / "output"
                / "ocr_resultado.json"
            )

            print("INTERFAZ: Ejecutando OCR...")

            resultado = ejecutar_ocr(
                str(self.ruta_imagen)
            )

            print("INTERFAZ: OCR terminó.")
            print("INTERFAZ: guardando JSON...")

            guardar_resultado_json(
                resultado=resultado,
                ruta_imagen=self.ruta_imagen,
                ruta_salida=ruta_salida,
            )

            print("INTERFAZ: JSON guardado.")

            print("INTERFAZ: analizando estructura...")

            resultado = analizar_estructura(
                ruta_salida
            )

            self.eventos = resultado["eventos"]

            print(
                f"INTERFAZ: parser termino. "
                f"Eventos encontrados: {len(self.eventos)}"
            )

            for numero, evento in  enumerate(
                self.eventos,
                start = 1,
            ):
                print(
                    f"{numero:02d}. "
                    f"{evento.dia:8} "
                    f"{evento.inicio}-{evento.fim} | "
                    f"{evento.tipo:7} | "
                    f"{evento.disciplina}"
                )

            print("INTERFAZ: proceso OCR terminado.")
            print("=" * 60)

        except Exception as error:
            self.ventana.after(
                0,
                self.mostrar_error,
                error,
            )
            return

        self.ventana.after(
            0,
            self.ocr_completado,
        )

    def ocr_completado(self):
        self.boton_seleccionar.config(
            state="normal",
        )

        self.estado_label.config(
            text="OCR completado correctamente.",
        )

    def mostrar_error(self, error):
        self.boton_seleccionar.config(
            state="normal",
        )

        self.boton_analizar.config(
            state="normal",
        )

        self.estado_label.config(
            text=f"Error durante el OCR: {error}",
        )


def iniciar_aplicacion():
    ventana = tk.Tk()

    AplicacionHorario(ventana)

    ventana.mainloop()


if __name__ == "__main__":
    iniciar_aplicacion()