import tkinter as tk
from tkinter import ttk
from tkcalendar import Calendar
from tkinter import messagebox
from validators.validator import validar_evento
from pathlib import Path
from exportadores.ical import exportar_ical
from exportadores.excel import exportar_excel
from exportadores.correo import enviar_correo

class VentanaExportacion:
    def __init__(
        self,
        ventana_padre: tk.Toplevel,
        eventos,
    ):
        self.ventana_padre = ventana_padre
        self.eventos = eventos

        self.ventana = tk.Toplevel(
            ventana_padre
        )

        self.ventana.title(
            "Exportar horario"
        )

        self.ventana.geometry(
            "500x350"
        )

        self.ventana.minsize(
            450,
            300,
        )

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
            text="Exportar horario",
            font=(
                "Segoe UI",
                20,
                "bold",
            ),
        )

        titulo.pack(
            anchor="w",
            pady=(0, 10),
        )

        descripcion = ttk.Label(
            contenedor,
            text=(
                "Seleccione el lunes de inicio del semestre "
                "y el numero de semanas que desea generar."
            ),
            wraplength=420,
        )

        descripcion.pack(
            anchor="w",
            pady=(0, 25),
        )

        etiqueta_fecha = ttk.Label(
            contenedor,
            text="Lunes de inicio:",
        )

        etiqueta_fecha.pack(
            anchor="w",
            pady=(0, 5),
        )

        self.calendario = Calendar(
            contenedor,
            selectmode="day",
            date_pattern="dd/mm/yyyy",
        )

        self.calendario.pack(
            pady=(0, 10),
        )

        etiqueta_semanas = ttk.Label(
            contenedor,
            text="Número de semanas",
        )

        etiqueta_semanas.pack(
            anchor="w",
            pady=(10,5)
        )

        self.semanas_var = tk.IntVar(
            value=16
        )

        self.semanas_spinbox = ttk.Spinbox(
            contenedor,
            from_=1,
            to=52,
            textvariable=self.semanas_var,
            width=10,
        )

        self.semanas_spinbox.pack(
            anchor="w",
        )

        boton_exportar = ttk.Button(
            contenedor,
            text="Exportar horario",
            command=self.exportar,
        )

        boton_exportar.pack(
            pady=(30, 0),
        )

        self.boton_correo = ttk.Button(
            contenedor,
            text="Enviar calendario por correo",
            command=self.enviar_calendario_por_correo,
            state="disabled",
        )

        self.boton_correo.pack(
            pady=(10, 0)
        )

    def exportar(self):
        fecha = self.calendario.selection_get()

        if fecha.weekday() != 0:
            messagebox.showerror(
                "Fecha inválida",
                "Debe seleccionar un lunes.",
                parent=self.ventana,
            )
            return

        errores = []

        for numero, evento in enumerate(
            self.eventos,
            start=1,
        ):
            errores_evento = validar_evento(
                evento
            )

            if errores_evento:
                errores.append(
                    f"Evento {numero}: "
                    + "; ".join(errores_evento)
                )

        if errores:
            messagebox.showerror(
                "Horario inválido",
                "No se puede exportar el horario porque "
                "se encontraron errores:\n\n"
                + "\n".join(errores),
                parent=self.ventana,
            )
            return

        ruta_salida = (
            Path(__file__).resolve().parent
            / "output"
        )

        ruta_ical = (
            ruta_salida
            / "horario.ics"
        )

        ruta_excel = (
            ruta_salida
            / "horario.xlsx"
        )

        self.ruta_ical = ruta_ical

        exportar_ical(
            eventos=self.eventos,
            fecha_inicio=fecha,
            semanas=self.semanas_var.get(),
            ruta_salida=ruta_ical,
        )

        exportar_excel(
            eventos=self.eventos,
            ruta_salida=ruta_excel,
        )

        self.boton_correo.config(
            state="normal"
        )

        print(
            "EXPORTACIÓN: archivos generados"
        )

        print(
            "ICS:",
            ruta_ical,
        )

        print(
            "Excel:",
            ruta_excel,
        )

        messagebox.showinfo(
            "Exportación completada",
            "El horario se exportó correctamente.\n\n"
            f"Calendario: {ruta_ical}\n"
            f"Excel: {ruta_excel}",
            parent=self.ventana,
        )

    def enviar_calendario_por_correo(self):
        try:
            enviar_correo(
                self.ruta_ical
            )

        except Exception as error:
            messagebox.showerror(
                "Error al enviar",
                (
                    "No se pudo enviar el calendario "
                    "por correo.\n\n"
                    f"Detalles: {error}"
                ),
                parent=self.ventana,
            )

            return

        messagebox.showinfo(
            "Correo enviado",
            (
                "El calendario se envió correctamente "
                "por correo electrónico."
            ),
            parent=self.ventana,
        )