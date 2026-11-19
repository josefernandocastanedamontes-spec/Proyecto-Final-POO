# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Dict, List, Optional
from vista.interfaces import IVistaJuego


class VistaGraficaTkinter(IVistaJuego):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("El Impostor - POO")
        self.root.geometry("740x620")
        self.root.minsize(680, 560)
        self.root.configure(bg="#f0f2f5")

        self._timer_id: Optional[str] = None
        self._configurar_estilos()

        header = tk.Frame(self.root, bg="#2c3e50", pady=12)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="EL IMPOSTOR",
            font=("Arial", 16, "bold"),
            fg="#ffffff",
            bg="#2c3e50",
        ).pack()
        tk.Label(
            header,
            text="Juego de deduccion y palabras secretas",
            font=("Arial", 9),
            fg="#d0d7de",
            bg="#2c3e50",
        ).pack()

        self.contenedor = tk.Frame(self.root, bg="#f0f2f5", padx=24, pady=16)
        self.contenedor.pack(fill=tk.BOTH, expand=True)

    def _configurar_estilos(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass

    def _limpiar_pantalla(self) -> None:
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def _crear_panel(self, parent: tk.Widget, pady: int = 8) -> tk.Frame:
        panel = tk.Frame(
            parent,
            bg="#ffffff",
            padx=18,
            pady=14,
            highlightbackground="#d0d7de",
            highlightthickness=1,
        )
        panel.pack(fill=tk.X, pady=pady)
        return panel

    def _crear_boton(
        self,
        parent: tk.Widget,
        texto: str,
        comando: Callable,
        bg: str = "#2980b9",
        fg: str = "#ffffff",
        width: int = 22,
    ) -> tk.Button:
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=bg,
            fg=fg,
            activebackground="#1f6391",
            activeforeground="#ffffff",
            font=("Arial", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=10,
            pady=6,
            width=width,
        )

    def iniciar(self) -> None:
        self.root.mainloop()

    def mostrar_error(self, titulo: str, mensaje: str) -> None:
        messagebox.showerror(titulo, mensaje, parent=self.root)

    def mostrar_info(self, titulo: str, mensaje: str) -> None:
        messagebox.showinfo(titulo, mensaje, parent=self.root)

    def mostrar_registro(
        self,
        categorias: List[str],
        jugadores_actuales: List[str],
        on_agregar_jugador: Callable[[str], None],
        on_eliminar_jugador: Callable[[int], None],
        on_iniciar_partida: Callable[[str, int, int, int, bool], None],
    ) -> None:
        self._limpiar_pantalla()

        tk.Label(
            self.contenedor,
            text="Registro de Jugadores y Configuracion",
            font=("Arial", 13, "bold"),
            fg="#1f2328",
            bg="#f0f2f5",
        ).pack(anchor="w", pady=(0, 6))

        panel_jug = self._crear_panel(self.contenedor)
        tk.Label(
            panel_jug,
            text="Jugadores inscritos (3 a 10 jugadores):",
            font=("Arial", 10, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 6))

        fila_input = tk.Frame(panel_jug, bg="#ffffff")
        fila_input.pack(fill=tk.X, pady=(0, 8))

        entry_nombre = tk.Entry(
            fila_input,
            font=("Arial", 10),
            bg="#f6f8fa",
            fg="#1f2328",
            relief=tk.SOLID,
            bd=1,
        )
        entry_nombre.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=4, padx=(0, 8))
        entry_nombre.focus_set()

        def agregar_evento(_event=None):
            nombre = entry_nombre.get()
            entry_nombre.delete(0, tk.END)
            on_agregar_jugador(nombre)

        entry_nombre.bind("<Return>", agregar_evento)

        self._crear_boton(
            fila_input, "Agregar", agregar_evento, bg="#27ae60", width=12
        ).pack(side=tk.LEFT)

        fila_lista = tk.Frame(panel_jug, bg="#ffffff")
        fila_lista.pack(fill=tk.X)

        listbox = tk.Listbox(
            fila_lista,
            height=5,
            font=("Arial", 10),
            bg="#f6f8fa",
            fg="#1f2328",
            selectbackground="#2980b9",
            selectforeground="#ffffff",
            relief=tk.SOLID,
            bd=1,
        )
        listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        for idx, nombre in enumerate(jugadores_actuales, start=1):
            listbox.insert(tk.END, f" {idx}. {nombre}")

        def eliminar_seleccionado():
            seleccion = listbox.curselection()
            if seleccion:
                on_eliminar_jugador(seleccion[0])

        self._crear_boton(
            fila_lista, "Eliminar", eliminar_seleccionado, bg="#c0392b", width=12
        ).pack(side=tk.LEFT, anchor="n")

        panel_cfg = self._crear_panel(self.contenedor)
        tk.Label(
            panel_cfg,
            text="Parametros de la partida:",
            font=("Arial", 10, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        tk.Label(panel_cfg, text="Categoria:", fg="#1f2328", bg="#ffffff").grid(
            row=1, column=0, sticky="w", padx=(0, 6), pady=4
        )
        var_cat = tk.StringVar(value=categorias[0] if categorias else "Lugares")
        combo_cat = ttk.Combobox(
            panel_cfg, textvariable=var_cat, values=categorias, state="readonly", width=16
        )
        combo_cat.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=4)

        tk.Label(panel_cfg, text="Numero de rondas:", fg="#1f2328", bg="#ffffff").grid(
            row=1, column=2, sticky="w", padx=(0, 6), pady=4
        )
        var_rondas = tk.IntVar(value=3)
        tk.Spinbox(
            panel_cfg,
            from_=1,
            to=10,
            textvariable=var_rondas,
            width=6,
            relief=tk.SOLID,
            bd=1,
        ).grid(row=1, column=3, sticky="w", pady=4)

        tk.Label(panel_cfg, text="Tiempo debate (seg):", fg="#1f2328", bg="#ffffff").grid(
            row=2, column=0, sticky="w", padx=(0, 6), pady=4
        )
        var_tiempo = tk.IntVar(value=60)
        tk.Spinbox(
            panel_cfg,
            from_=10,
            to=300,
            increment=10,
            textvariable=var_tiempo,
            width=6,
            relief=tk.SOLID,
            bd=1,
        ).grid(row=2, column=1, sticky="w", padx=(0, 20), pady=4)

        tk.Label(panel_cfg, text="Max. caracteres pista:", fg="#1f2328", bg="#ffffff").grid(
            row=2, column=2, sticky="w", padx=(0, 6), pady=4
        )
        var_long = tk.IntVar(value=25)
        tk.Spinbox(
            panel_cfg,
            from_=5,
            to=60,
            textvariable=var_long,
            width=6,
            relief=tk.SOLID,
            bd=1,
        ).grid(row=2, column=3, sticky="w", pady=4)

        var_ultima = tk.BooleanVar(value=True)
        tk.Checkbutton(
            panel_cfg,
            text="Permitir ultima oportunidad al Impostor para adivinar la palabra",
            variable=var_ultima,
            bg="#ffffff",
            fg="#1f2328",
            activebackground="#ffffff",
        ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 0))

        frame_btn = tk.Frame(self.contenedor, bg="#f0f2f5")
        frame_btn.pack(pady=12)
        self._crear_boton(
            frame_btn,
            "Iniciar Partida",
            lambda: on_iniciar_partida(
                var_cat.get(),
                var_rondas.get(),
                var_tiempo.get(),
                var_long.get(),
                var_ultima.get(),
            ),
            bg="#2c3e50",
            width=24,
        ).pack()

    def mostrar_asignacion_privada(
        self,
        nombre_jugador: str,
        numero_jugador: int,
        total_jugadores: int,
        obtener_texto_rol: Callable[[], str],
        on_siguiente_jugador: Callable[[], None],
    ) -> None:
        self._limpiar_pantalla()

        tk.Label(
            self.contenedor,
            text=f"Asignacion de Roles ({numero_jugador} de {total_jugadores})",
            font=("Arial", 13, "bold"),
            fg="#1f2328",
            bg="#f0f2f5",
        ).pack(pady=(4, 8))

        panel = self._crear_panel(self.contenedor, pady=12)

        tk.Label(
            panel,
            text=f"Turno de: {nombre_jugador}",
            font=("Arial", 15, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
        ).pack(pady=(6, 4))

        tk.Label(
            panel,
            text="Asegurate de que los demas jugadores no miren la pantalla.",
            font=("Arial", 9),
            fg="#c0392b",
            bg="#ffffff",
        ).pack(pady=(0, 14))

        lbl_secreto = tk.Label(
            panel,
            text="ROL OCULTO",
            font=("Arial", 12, "bold"),
            fg="#57606a",
            bg="#f6f8fa",
            width=40,
            height=4,
            relief=tk.SOLID,
            bd=1,
            justify=tk.CENTER,
        )
        lbl_secreto.pack(pady=8)

        btn_siguiente = self._crear_boton(
            panel,
            "Ocultar y Continuar",
            on_siguiente_jugador,
            bg="#27ae60",
            width=24,
        )

        def revelar():
            texto = obtener_texto_rol()
            color = "#c0392b" if "IMPOSTOR" in texto.upper() else "#1e7e34"
            lbl_secreto.config(text=texto, fg=color)
            btn_revelar.pack_forget()
            btn_siguiente.pack(pady=(12, 4))

        btn_revelar = self._crear_boton(
            panel,
            "Mostrar mi Rol",
            revelar,
            bg="#2980b9",
            width=24,
        )
        btn_revelar.pack(pady=(12, 4))

    def mostrar_turno_pista(
        self,
        numero_ronda: int,
        categoria: str,
        nombre_jugador: str,
        pistas_previas: List[tuple],
        longitud_maxima: int,
        on_enviar_pista: Callable[[str], None],
    ) -> None:
        self._limpiar_pantalla()

        tk.Label(
            self.contenedor,
            text=f"Ronda {numero_ronda} - Fase de Pistas (Categoria: {categoria})",
            font=("Arial", 13, "bold"),
            fg="#1f2328",
            bg="#f0f2f5",
        ).pack(anchor="w", pady=(0, 6))

        panel_prev = self._crear_panel(self.contenedor)
        tk.Label(
            panel_prev,
            text="Pistas registradas en la ronda:",
            font=("Arial", 10, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 6))

        if not pistas_previas:
            tk.Label(
                panel_prev,
                text="Aun no hay pistas registradas.",
                font=("Arial", 9, "italic"),
                fg="#57606a",
                bg="#ffffff",
            ).pack(anchor="w")
        else:
            for autor, texto in pistas_previas:
                tk.Label(
                    panel_prev,
                    text=f"- {autor}: {texto}",
                    font=("Arial", 10),
                    fg="#1f2328",
                    bg="#ffffff",
                ).pack(anchor="w", pady=1)

        panel_turno = self._crear_panel(self.contenedor)
        tk.Label(
            panel_turno,
            text=f"Turno de: {nombre_jugador}",
            font=("Arial", 13, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            panel_turno,
            text=f"Escribe una pista relacionada (maximo {longitud_maxima} caracteres, sin escribir la palabra secreta):",
            font=("Arial", 9),
            fg="#57606a",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 10))

        entry_pista = tk.Entry(
            panel_turno,
            font=("Arial", 11),
            bg="#f6f8fa",
            fg="#1f2328",
            relief=tk.SOLID,
            bd=1,
        )
        entry_pista.pack(fill=tk.X, ipady=5, pady=(0, 12))
        entry_pista.focus_set()

        def enviar(_event=None):
            on_enviar_pista(entry_pista.get())

        entry_pista.bind("<Return>", enviar)

        self._crear_boton(
            panel_turno, "Enviar Pista", enviar, bg="#27ae60", width=20
        ).pack()

    def mostrar_debate(
        self,
        numero_ronda: int,
        categoria: str,
        pistas_ronda: List[tuple],
        segundos_debate: int,
        on_finalizar_debate: Callable[[], None],
    ) -> None:
        self._limpiar_pantalla()

        tk.Label(
            self.contenedor,
            text=f"Ronda {numero_ronda} - Fase de Debate (Categoria: {categoria})",
            font=("Arial", 13, "bold"),
            fg="#1f2328",
            bg="#f0f2f5",
        ).pack(anchor="w", pady=(0, 6))

        panel_timer = self._crear_panel(self.contenedor)
        lbl_tiempo = tk.Label(
            panel_timer,
            text=f"Tiempo restante: {segundos_debate} segundos",
            font=("Arial", 13, "bold"),
            fg="#c0392b",
            bg="#ffffff",
        )
        lbl_tiempo.pack()

        panel_pistas = self._crear_panel(self.contenedor)
        tk.Label(
            panel_pistas,
            text="Pistas de todos los jugadores:",
            font=("Arial", 10, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 8))

        for autor, texto in pistas_ronda:
            fila = tk.Frame(panel_pistas, bg="#f6f8fa", padx=10, pady=5)
            fila.pack(fill=tk.X, pady=2)
            tk.Label(
                fila,
                text=f"{autor}:",
                font=("Arial", 10, "bold"),
                fg="#2c3e50",
                bg="#f6f8fa",
                width=16,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                fila,
                text=texto,
                font=("Arial", 10),
                fg="#1f2328",
                bg="#f6f8fa",
                anchor="w",
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        restante = [segundos_debate]

        def actualizar_reloj():
            restante[0] -= 1
            if restante[0] > 0:
                lbl_tiempo.config(text=f"Tiempo restante: {restante[0]} segundos")
                self._timer_id = self.root.after(1000, actualizar_reloj)
            else:
                lbl_tiempo.config(text="Tiempo de debate finalizado")
                self._timer_id = None

        self._timer_id = self.root.after(1000, actualizar_reloj)

        frame_btn = tk.Frame(self.contenedor, bg="#f0f2f5")
        frame_btn.pack(pady=12)
        self._crear_boton(
            frame_btn,
            "Pasar a Votacion",
            on_finalizar_debate,
            bg="#2c3e50",
            width=24,
        ).pack()

    def mostrar_votacion_privada(
        self,
        numero_ronda: int,
        nombre_votante: str,
        candidatos: List[str],
        pistas_ronda: List[tuple],
        on_registrar_voto: Callable[[str], None],
    ) -> None:
        self._limpiar_pantalla()

        tk.Label(
            self.contenedor,
            text=f"Ronda {numero_ronda} - Votacion",
            font=("Arial", 13, "bold"),
            fg="#1f2328",
            bg="#f0f2f5",
        ).pack(anchor="w", pady=(0, 6))

        panel = self._crear_panel(self.contenedor)
        tk.Label(
            panel,
            text=f"Voto de: {nombre_votante}",
            font=("Arial", 13, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            panel,
            text="Selecciona al jugador sospechoso (no puedes votarte a ti mismo):",
            font=("Arial", 9),
            fg="#57606a",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 10))

        var_elegido = tk.StringVar(value="")
        pistas_dict = dict(pistas_ronda)

        for candidato in candidatos:
            pista_cand = pistas_dict.get(candidato, "")
            texto_opcion = f"{candidato} (Pista: {pista_cand})"
            tk.Radiobutton(
                panel,
                text=texto_opcion,
                variable=var_elegido,
                value=candidato,
                font=("Arial", 10),
                bg="#ffffff",
                fg="#1f2328",
                activebackground="#ffffff",
            ).pack(anchor="w", pady=3)

        self._crear_boton(
            panel,
            "Confirmar Voto",
            lambda: on_registrar_voto(var_elegido.get()),
            bg="#c0392b",
            width=20,
        ).pack(pady=(14, 4))

    def solicitar_ultima_oportunidad(
        self,
        nombre_impostor: str,
        on_adivinar_palabra: Callable[[str], None],
    ) -> None:
        self._limpiar_pantalla()

        panel = self._crear_panel(self.contenedor, pady=16)
        tk.Label(
            panel,
            text="El Impostor ha sido descubierto",
            font=("Arial", 14, "bold"),
            fg="#c0392b",
            bg="#ffffff",
        ).pack(pady=(4, 8))

        tk.Label(
            panel,
            text=f"{nombre_impostor}, tienes una ultima oportunidad.\nEscribe cual crees que es la palabra secreta:",
            font=("Arial", 10),
            fg="#1f2328",
            bg="#ffffff",
            justify=tk.CENTER,
        ).pack(pady=(0, 12))

        entry_adivina = tk.Entry(
            panel,
            font=("Arial", 12),
            bg="#f6f8fa",
            fg="#1f2328",
            justify=tk.CENTER,
            relief=tk.SOLID,
            bd=1,
        )
        entry_adivina.pack(ipady=5, ipadx=15, pady=(0, 14))
        entry_adivina.focus_set()

        def enviar(_event=None):
            on_adivinar_palabra(entry_adivina.get())

        entry_adivina.bind("<Return>", enviar)

        self._crear_boton(
            panel, "Adivinar Palabra", enviar, bg="#2980b9", width=22
        ).pack()

    def mostrar_resultado_final(
        self,
        ganador: str,
        detalle: str,
        palabra_secreta: str,
        roles_revelados: List[tuple],
        marcador_acumulado: Dict[str, int],
        on_nueva_partida: Callable[[], None],
        on_volver_registro: Callable[[], None],
    ) -> None:
        self._limpiar_pantalla()

        panel_res = self._crear_panel(self.contenedor)
        tk.Label(
            panel_res,
            text=ganador.upper(),
            font=("Arial", 15, "bold"),
            fg="#1e7e34" if "CIVIL" in ganador.upper() else "#c0392b",
            bg="#ffffff",
        ).pack(pady=(2, 4))

        tk.Label(
            panel_res,
            text=detalle,
            font=("Arial", 10),
            fg="#1f2328",
            bg="#ffffff",
        ).pack(pady=(0, 6))

        tk.Label(
            panel_res,
            text=f"Palabra secreta: {palabra_secreta}",
            font=("Arial", 11, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
        ).pack()

        panel_tabla = self._crear_panel(self.contenedor)
        tk.Label(
            panel_tabla,
            text="Roles Revelados y Marcador Acumulado:",
            font=("Arial", 10, "bold"),
            fg="#2c3e50",
            bg="#ffffff",
        ).pack(anchor="w", pady=(0, 6))

        for nombre, rol, estado in roles_revelados:
            puntos = marcador_acumulado.get(nombre, 0)
            color_rol = "#c0392b" if rol == "Impostor" else "#1e7e34"
            fila = tk.Frame(panel_tabla, bg="#f6f8fa", padx=10, pady=4)
            fila.pack(fill=tk.X, pady=2)

            tk.Label(
                fila,
                text=nombre,
                font=("Arial", 10, "bold"),
                fg="#1f2328",
                bg="#f6f8fa",
                width=18,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                fila,
                text=rol,
                font=("Arial", 10, "bold"),
                fg=color_rol,
                bg="#f6f8fa",
                width=12,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                fila,
                text=f"Estado: {estado}",
                font=("Arial", 9),
                fg="#57606a",
                bg="#f6f8fa",
                width=16,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                fila,
                text=f"Puntos: {puntos}",
                font=("Arial", 10, "bold"),
                fg="#2c3e50",
                bg="#f6f8fa",
                anchor="e",
            ).pack(side=tk.RIGHT)

        botones = tk.Frame(self.contenedor, bg="#f0f2f5")
        botones.pack(pady=12)

        self._crear_boton(
            botones,
            "Nueva Partida",
            on_nueva_partida,
            bg="#27ae60",
            width=20,
        ).pack(side=tk.LEFT, padx=8)

        self._crear_boton(
            botones,
            "Volver al Registro",
            on_volver_registro,
            bg="#2980b9",
            width=20,
        ).pack(side=tk.LEFT, padx=8)
