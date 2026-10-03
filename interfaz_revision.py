import tkinter as tk
from tkinter import ttk

from models.horario import Evento


class VentanaRevision:
    def __init__(
        self,
        ventana_padre: tk.Tk,
        eventos: list[Evento],
    ):
        self.ventana_padre = ventana_padre
        self.eventos = eventos

        self.ventana = tk.Toplevel(
            ventana_padre
        )

        self.ventana.title(
            "Revisar horario"
        )

        self.ventana.geometry(
            "1200x750"
        )

        self.ventana.minsize(
            950,
            600,
        )

        self.crear_interfaz()

    def crear_interfaz(self):
        contenedor = ttk.Frame(
            self.ventana,
            padding=20,
        )

        contenedor.pack(
            fill="both",
            expand=True,
        )

        titulo = ttk.Label(
            contenedor,
            text="Revisar horario",
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

        aviso = ttk.Label(
            contenedor,
            text=(
                "La aplicación puede cometer errores "
                "durante el reconocimiento del horario. "
                "Revise cuidadosamente todos los eventos "
                "antes de continuar."
            ),
            wraplength=1100,
        )

        aviso.pack(
            anchor="w",
            pady=(0, 20),
        )

        contenido = ttk.Frame(
            contenedor
        )

        contenido.pack(
            fill="both",
            expand=True,
        )

        self.crear_tabla(
            contenido
        )

        self.crear_panel_edicion(
            contenido
        )

    def crear_tabla(
        self,
        contenedor: ttk.Frame,
    ):
        marco = ttk.Frame(
            contenedor
        )

        marco.pack(
            side="top",
            fill="both",
            expand=True,
        )

        columnas = (
            "dia",
            "inicio",
            "fin",
            "disciplina",
            "docente",
            "local",
            "tipo",
        )

        self.tabla = ttk.Treeview(
            marco,
            columns=columnas,
            show="headings",
        )

        encabezados = {
            "dia": "Día",
            "inicio": "Inicio",
            "fin": "Fin",
            "disciplina": "Disciplina",
            "docente": "Docente",
            "local": "Local",
            "tipo": "Tipo",
        }

        for columna in columnas:
            self.tabla.heading(
                columna,
                text=encabezados[columna],
            )

        anchos = {
            "dia": 100,
            "inicio": 80,
            "fin": 80,
            "disciplina": 180,
            "docente": 180,
            "local": 220,
            "tipo": 100,
        }

        for columna, ancho in anchos.items():
            self.tabla.column(
                columna,
                width=ancho,
            )

        for indice, evento in enumerate(
            self.eventos
        ):
            self.tabla.insert(
                "",
                "end",
                iid=str(indice),
                values=(
                    evento.dia,
                    evento.inicio,
                    evento.fim,
                    evento.disciplina,
                    evento.docente or "",
                    evento.local or "",
                    evento.tipo,
                ),
            )

        scrollbar_vertical = ttk.Scrollbar(
            marco,
            orient="vertical",
            command=self.tabla.yview,
        )

        self.tabla.configure(
            yscrollcommand=scrollbar_vertical.set
        )

        self.tabla.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar_vertical.pack(
            side="right",
            fill="y",
        )

        self.tabla.bind(
            "<<TreeviewSelect>>",
            self.evento_seleccionado,
        )

    def crear_panel_edicion(
        self,
        contenedor: ttk.Frame,
    ):
        separador = ttk.Separator(
            contenedor,
            orient="horizontal",
        )

        separador.pack(
            fill="x",
            pady=15,
        )

        marco = ttk.LabelFrame(
            contenedor,
            text="Evento seleccionado",
            padding=15,
        )

        marco.pack(
            fill="x",
        )

        self.dia_var = tk.StringVar()
        self.inicio_var = tk.StringVar()
        self.fin_var = tk.StringVar()
        self.disciplina_var = tk.StringVar()
        self.docente_var = tk.StringVar()
        self.local_var = tk.StringVar()
        self.tipo_var = tk.StringVar()

        campos = [
            ("Día", self.dia_var),
            ("Inicio", self.inicio_var),
            ("Fin", self.fin_var),
            ("Disciplina", self.disciplina_var),
            ("Docente", self.docente_var),
            ("Local", self.local_var),
            ("Tipo", self.tipo_var),
        ]

        for fila, (nombre, variable) in enumerate(
            campos
        ):
            etiqueta = ttk.Label(
                marco,
                text=f"{nombre}:",
            )

            etiqueta.grid(
                row=fila,
                column=0,
                sticky="w",
                padx=(0, 10),
                pady=4,
            )

            entrada = ttk.Entry(
                marco,
                textvariable=variable,
            )

            entrada.grid(
                row=fila,
                column=1,
                sticky="ew",
                pady=4,
            )

        boton_guardar = ttk.Button(
            marco,
            text="Guardar Cambios",
            command=self.guardar_cambios,
        )

        boton_guardar.grid(
            row=len(campos),
            column=0,
            columnspan=2,
            pady=(15,0),
        )

        marco.columnconfigure(
            1,
            weight=1,
        )

    def evento_seleccionado(
        self,
        _evento,
    ):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        indice = int(
            seleccion[0]
        )

        evento = self.eventos[indice]

        self.dia_var.set(
            evento.dia
        )

        self.inicio_var.set(
            evento.inicio
        )

        self.fin_var.set(
            evento.fim
        )

        self.disciplina_var.set(
            evento.disciplina
        )

        self.docente_var.set(
            evento.docente or ""
        )

        self.local_var.set(
            evento.local or ""
        )

        self.tipo_var.set(
            evento.tipo
        )
    def guardar_cambios(self):
        seleccion = self.tabla.selection()

        if not seleccion:
            return

        indice = int(
            seleccion[0]
        )

        evento = self.eventos[indice]

        evento.dia = self.dia_var.get().strip()
        evento.inicio = self.inicio_var.get().strip()
        evento.fim = self.fin_var.get().strip()
        evento.disciplina = (
            self.disciplina_var.get().strip()
        )
        evento.docente = (
            self.docente_var.get().strip()
            or None
        )
        evento.local = (
            self.local_var.get().strip()
            or None
        )
        evento.tipo = self.tipo_var.get().strip()

        self.tabla.item(
            seleccion[0],
            values=(
                evento.dia,
                evento.inicio,
                evento.fim,
                evento.disciplina,
                evento.docente or "",
                evento.local or "",
                evento.tipo,
            ),
        )