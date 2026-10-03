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
        if not hasattr(
            self,
            "marco_tabla",
        ):
            marco = ttk.Frame(
                contenedor
            )

            self.marco_tabla = marco
            self.contenedor_tabla = contenedor

            marco.pack(
                side="top",
                fill="both",
                expand=True,
            )
        else:
            marco = self.marco_tabla

            for widget in marco.winfo_children():
                widget.destroy()

        dias = (
            "SEGUNDA",
            "TERÇA",
            "QUARTA",
            "QUINTA",
            "SEXTA",
        )

        intervalos = {
            (
                evento.inicio,
                evento.fim,
            )
            for evento in self.eventos
        }

        def contiene(
            exterior,
            interior,
        ):
            inicio_exterior = self._hora_a_minutos(
                exterior[0]
            )
            fin_exterior = self._hora_a_minutos(
                exterior[1]
            )

            inicio_interior = self._hora_a_minutos(
                interior[0]
            )
            fin_interior = self._hora_a_minutos(
                interior[1]
            )

            return (
                exterior != interior
                and inicio_exterior <= inicio_interior
                and fin_exterior >= fin_interior
            )

        franjas = [
            intervalo
            for intervalo in intervalos
            if not any(
                contiene(
                    intervalo,
                    otro,
                )
                for otro in intervalos
            )
        ]

        franjas.sort(
            key=lambda franja: self._hora_a_minutos(
                franja[0]
            )
        )

        self.celdas_eventos = {}

        # Encabezado de la tabla

        encabezado = ttk.Label(
            marco,
            text="Franjas horarias",
            anchor="center",
            relief="solid",
            padding=8,
        )

        encabezado.grid(
            row=0,
            column=0,
            sticky="nsew",
        )

        for columna, dia in enumerate(
            dias,
            start=1,
        ):
            encabezado_dia = ttk.Label(
                marco,
                text=dia,
                anchor="center",
                relief="solid",
                padding=8,
                font=(
                    "Segoe UI",
                    10,
                    "bold",
                ),
            )

            encabezado_dia.grid(
                row=0,
                column=columna,
                sticky="nsew",
            )

        # Configuración de columnas

        marco.columnconfigure(
            0,
            weight=0,
            minsize=130,
        )

        for columna in range(1, 6):
            marco.columnconfigure(
                columna,
                weight=1,
                minsize=150,
            )

        # Crear filas de franjas

        for fila, (inicio, fin) in enumerate(
            franjas,
            start=1,
        ):
            texto_franja = ttk.Label(
                marco,
                text=f"{inicio} - {fin}",
                anchor="center",
                relief="solid",
                padding=8,
            )

            texto_franja.grid(
                row=fila,
                column=0,
                sticky="nsew",
            )

        # Colocar eventos

        for indice, evento in enumerate(
            self.eventos
        ):

            columna = dias.index(
                evento.dia
            ) + 1

            fila_inicio = next(
                (
                    indice
                    for indice, franja in enumerate(
                        franjas,
                        start=1,
                    )
                    if franja[0] == evento.inicio
                ),
                None,
            )

            if fila_inicio is None:
                continue

            texto = evento.disciplina

            if evento.tipo == "tutoria":
                texto = (
                    "TUTORÍA\n"
                    f"{evento.disciplina}"
                )

            elif evento.docente:
                texto += (
                    "\n"
                    f"{evento.docente}"
                )

            if evento.local:
                texto += (
                    "\n"
                    f"{evento.local}"
                )

            celda = ttk.Label(
                marco,
                text=texto,
                anchor="center",
                justify="center",
                relief="solid",
                padding=8,
            )

            # Calculamos cuántas franjas ocupa el evento.

            franjas_evento = [
                franja
                for franja in franjas
                if (
                    self._hora_a_minutos(
                        franja[0]
                    )
                    >= self._hora_a_minutos(
                        evento.inicio
                    )
                    and self._hora_a_minutos(
                        franja[1]
                    )
                    <= self._hora_a_minutos(
                        evento.fim
                    )
                )
            ]

            rowspan = max(
                1,
                len(franjas_evento),
            )

            celda.grid(
                row=fila_inicio,
                column=columna,
                rowspan=rowspan,
                sticky="nsew",
            )

            self.celdas_eventos[
                celda
            ] = indice

            celda.bind(
                "<Button-1>",
                self.evento_celda_seleccionada,
            )

        for fila in range(
            1,
            len(franjas) + 1,
        ):
            marco.rowconfigure(
                fila,
                weight=1,
                minsize=90,
            )


    def _hora_a_minutos(
        self,
        hora: str,
    ) -> int:
        horas, minutos = map(
            int,
            hora.split(":"),
        )

        return horas * 60 + minutos


    def evento_celda_seleccionada(
        self,
        evento_click,
    ):
        celda = evento_click.widget

        if celda not in self.celdas_eventos:
            return

        indice = self.celdas_eventos[celda]

        evento = self.eventos[indice]

        self.evento_seleccionado = evento

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
        if not hasattr(
            self,
            "evento_seleccionado",
        ):
            return

        evento = self.evento_seleccionado

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

        self.crear_tabla(
            self.contenedor_tabla
        )

        