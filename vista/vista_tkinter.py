# -*- coding: utf-8 -*-
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Callable, Dict, List, Optional
from vista.interfaces import IVistaJuego


class VistaGraficaTkinter(IVistaJuego):
    """Implementación gráfica en Tkinter sin lógica de negocio (Patrón MVC)."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("El Impostor - Proyecto Final POO")
        self.root.geometry("760x640")
        self.root.minsize(700, 580)
        self.root.configure(bg="#181825")

        self._timer_id: Optional[str] = None
        self._configurar_estilos()

        # Encabezado superior fijo
        header = tk.Frame(self.root, bg="#11111b", pady=12)
        header.pack(fill=tk.X)
        tk.Label(
            header,
            text="🕵️ EL IMPOSTOR",
            font=("Segoe UI", 18, "bold"),
            fg="#cba6f7",
            bg="#11111b",
        ).pack()
        tk.Label(
            header,
            text="Juego de Deducción, Creatividad y Engaño",
            font=("Segoe UI", 9),
            fg="#a6adc8",
            bg="#11111b",
        ).pack()

        # Contenedor dinámico central
        self.contenedor = tk.Frame(self.root, bg="#181825", padx=25, pady=15)
        self.contenedor.pack(fill=tk.BOTH, expand=True)

    def _configurar_estilos(self) -> None:
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure(
            "TCombobox",
            fieldbackground="#313244",
            background="#45475a",
            foreground="#cdd6f4",
        )

    def _limpiar_pantalla(self) -> None:
        if self._timer_id is not None:
            self.root.after_cancel(self._timer_id)
            self._timer_id = None
        for widget in self.contenedor.winfo_children():
            widget.destroy()

    def _crear_tarjeta(self, parent: tk.Widget, pady: int = 8) -> tk.Frame:
        card = tk.Frame(
            parent,
            bg="#1e1e2e",
            padx=20,
            pady=15,
            highlightbackground="#313244",
            highlightthickness=1,
        )
        card.pack(fill=tk.X, pady=pady)
        return card

    def _crear_boton(
        self,
        parent: tk.Widget,
        texto: str,
        comando: Callable,
        bg: str = "#89b4fa",
        fg: str = "#11111b",
        width: int = 24,
    ) -> tk.Button:
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=bg,
            fg=fg,
            activebackground="#b4befe",
            activeforeground="#11111b",
            font=("Segoe UI", 10, "bold"),
            relief=tk.FLAT,
            cursor="hand2",
            padx=12,
            pady=7,
            width=width,
        )

    # ---------------- IVistaJuego ----------------

    def iniciar(self) -> None:
        self.root.mainloop()

    def mostrar_error(self, titulo: str, mensaje: str) -> None:
        messagebox.showerror(titulo, mensaje, parent=self.root)

    def mostrar_info(self, titulo: str, mensaje: str) -> None:
        messagebox.showinfo(titulo, mensaje, parent=self.root)

    # ---------------- IVistaRegistro ----------------

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
            text="1. Registro de Jugadores y Configuración",
            font=("Segoe UI", 14, "bold"),
            fg="#cdd6f4",
            bg="#181825",
        ).pack(anchor="w", pady=(0, 8))

        # Tarjeta de jugadores
        card_jug = self._crear_tarjeta(self.contenedor)
        tk.Label(
            card_jug,
            text="Jugadores inscritos (mínimo 3, máximo 10):",
            font=("Segoe UI", 10, "bold"),
            fg="#f9e2af",
            bg="#1e1e2e",
        ).pack(anchor="w", pady=(0, 6))

        fila_input = tk.Frame(card_jug, bg="#1e1e2e")
        fila_input.pack(fill=tk.X, pady=(0, 8))

        entry_nombre = tk.Entry(
            fila_input,
            font=("Segoe UI", 11),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief=tk.FLAT,
        )
        entry_nombre.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5, padx=(0, 8))
        entry_nombre.focus_set()

        def agregar_evento(_event=None):
            nombre = entry_nombre.get()
            entry_nombre.delete(0, tk.END)
            on_agregar_jugador(nombre)

        entry_nombre.bind("<Return>", agregar_evento)

        self._crear_boton(
            fila_input, "+ Agregar", agregar_evento, bg="#a6e3a1", width=12
        ).pack(side=tk.LEFT)

        fila_lista = tk.Frame(card_jug, bg="#1e1e2e")
        fila_lista.pack(fill=tk.X)

        listbox = tk.Listbox(
            fila_lista,
            height=5,
            font=("Segoe UI", 10),
            bg="#313244",
            fg="#cdd6f4",
            selectbackground="#89b4fa",
            selectforeground="#11111b",
            relief=tk.FLAT,
        )
        listbox.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 8))

        for idx, nombre in enumerate(jugadores_actuales, start=1):
            listbox.insert(tk.END, f"  {idx}. {nombre}")

        def eliminar_seleccionado():
            seleccion = listbox.curselection()
            if seleccion:
                on_eliminar_jugador(seleccion[0])

        self._crear_boton(
            fila_lista, "Quitar", eliminar_seleccionado, bg="#f38ba8", width=10
        ).pack(side=tk.LEFT, anchor="n")

        # Tarjeta de configuración (RF-12)
        card_cfg = self._crear_tarjeta(self.contenedor)
        tk.Label(
            card_cfg,
            text="Configuración de la Partida:",
            font=("Segoe UI", 10, "bold"),
            fg="#89dceb",
            bg="#1e1e2e",
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 8))

        tk.Label(card_cfg, text="Categoría:", fg="#cdd6f4", bg="#1e1e2e").grid(
            row=1, column=0, sticky="w", padx=(0, 6), pady=4
        )
        var_cat = tk.StringVar(value=categorias[0] if categorias else "Lugares")
        combo_cat = ttk.Combobox(
            card_cfg, textvariable=var_cat, values=categorias, state="readonly", width=15
        )
        combo_cat.grid(row=1, column=1, sticky="w", padx=(0, 20), pady=4)

        tk.Label(card_cfg, text="Máx. Rondas:", fg="#cdd6f4", bg="#1e1e2e").grid(
            row=1, column=2, sticky="w", padx=(0, 6), pady=4
        )
        var_rondas = tk.IntVar(value=3)
        tk.Spinbox(
            card_cfg,
            from_=1,
            to=10,
            textvariable=var_rondas,
            width=6,
            bg="#313244",
            fg="#cdd6f4",
            relief=tk.FLAT,
        ).grid(row=1, column=3, sticky="w", pady=4)

        tk.Label(card_cfg, text="Debate (seg):", fg="#cdd6f4", bg="#1e1e2e").grid(
            row=2, column=0, sticky="w", padx=(0, 6), pady=4
        )
        var_tiempo = tk.IntVar(value=60)
        tk.Spinbox(
            card_cfg,
            from_=10,
            to=300,
            increment=10,
            textvariable=var_tiempo,
            width=6,
            bg="#313244",
            fg="#cdd6f4",
            relief=tk.FLAT,
        ).grid(row=2, column=1, sticky="w", padx=(0, 20), pady=4)

        tk.Label(card_cfg, text="Máx. letras pista:", fg="#cdd6f4", bg="#1e1e2e").grid(
            row=2, column=2, sticky="w", padx=(0, 6), pady=4
        )
        var_long = tk.IntVar(value=25)
        tk.Spinbox(
            card_cfg,
            from_=5,
            to=60,
            textvariable=var_long,
            width=6,
            bg="#313244",
            fg="#cdd6f4",
            relief=tk.FLAT,
        ).grid(row=2, column=3, sticky="w", pady=4)

        var_ultima = tk.BooleanVar(value=True)
        tk.Checkbutton(
            card_cfg,
            text="Permitir última oportunidad al Impostor para adivinar la palabra",
            variable=var_ultima,
            bg="#1e1e2e",
            fg="#cdd6f4",
            selectcolor="#313244",
            activebackground="#1e1e2e",
            activeforeground="#cdd6f4",
        ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(8, 0))

        # Botón iniciar
        frame_btn = tk.Frame(self.contenedor, bg="#181825")
        frame_btn.pack(pady=14)
        self._crear_boton(
            frame_btn,
            "▶ INICIAR PARTIDA",
            lambda: on_iniciar_partida(
                var_cat.get(),
                var_rondas.get(),
                var_tiempo.get(),
                var_long.get(),
                var_ultima.get(),
            ),
            bg="#cba6f7",
            width=28,
        ).pack()

    # ---------------- IVistaTurno ----------------

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
            text=f"Asignación Secreta de Roles ({numero_jugador}/{total_jugadores})",
            font=("Segoe UI", 13, "bold"),
            fg="#89b4fa",
            bg="#181825",
        ).pack(pady=(5, 10))

        card = self._crear_tarjeta(self.contenedor, pady=15)

        tk.Label(
            card,
            text=f"Pasa el dispositivo a: {nombre_jugador}",
            font=("Segoe UI", 16, "bold"),
            fg="#f9e2af",
            bg="#1e1e2e",
        ).pack(pady=(5, 6))

        tk.Label(
            card,
            text="⚠️ Asegúrate de que los demás jugadores NO miren la pantalla.",
            font=("Segoe UI", 10),
            fg="#f38ba8",
            bg="#1e1e2e",
        ).pack(pady=(0, 15))

        lbl_secreto = tk.Label(
            card,
            text="[ ROL OCULTO ]",
            font=("Segoe UI", 13, "bold"),
            fg="#a6adc8",
            bg="#313244",
            width=38,
            height=4,
            justify=tk.CENTER,
        )
        lbl_secreto.pack(pady=10)

        btn_siguiente = self._crear_boton(
            card,
            "Ocultar y Pasar Turno ➡",
            on_siguiente_jugador,
            bg="#a6e3a1",
            width=26,
        )

        def revelar():
            texto = obtener_texto_rol()
            color = "#f38ba8" if "IMPOSTOR" in texto.upper() else "#a6e3a1"
            lbl_secreto.config(text=texto, fg=color)
            btn_revelar.pack_forget()
            btn_siguiente.pack(pady=(12, 5))

        btn_revelar = self._crear_boton(
            card,
            "👁️ Mostrar mi Rol y Palabra",
            revelar,
            bg="#89b4fa",
            width=26,
        )
        btn_revelar.pack(pady=(12, 5))

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
            text=f"Ronda {numero_ronda} • Fase de Pistas (Categoría: {categoria})",
            font=("Segoe UI", 13, "bold"),
            fg="#cba6f7",
            bg="#181825",
        ).pack(anchor="w", pady=(0, 8))

        # Pistas dadas hasta ahora en la ronda
        card_prev = self._crear_tarjeta(self.contenedor)
        tk.Label(
            card_prev,
            text="Pistas registradas en esta ronda:",
            font=("Segoe UI", 10, "bold"),
            fg="#89dceb",
            bg="#1e1e2e",
        ).pack(anchor="w", pady=(0, 6))

        if not pistas_previas:
            tk.Label(
                card_prev,
                text="Aún no hay pistas en esta ronda. ¡Eres el primero!",
                font=("Segoe UI", 9, "italic"),
                fg="#a6adc8",
                bg="#1e1e2e",
            ).pack(anchor="w")
        else:
            for autor, texto in pistas_previas:
                tk.Label(
                    card_prev,
                    text=f"• {autor}: {texto}",
                    font=("Segoe UI", 10),
                    fg="#cdd6f4",
                    bg="#1e1e2e",
                ).pack(anchor="w", pady=1)

        # Entrada de pista actual
        card_turno = self._crear_tarjeta(self.contenedor)
        tk.Label(
            card_turno,
            text=f"Turno de: {nombre_jugador}",
            font=("Segoe UI", 14, "bold"),
            fg="#f9e2af",
            bg="#1e1e2e",
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            card_turno,
            text=f"Escribe una pista breve relacionada con la palabra (máx. {longitud_maxima} caracteres, sin decir la palabra):",
            font=("Segoe UI", 9),
            fg="#a6adc8",
            bg="#1e1e2e",
        ).pack(anchor="w", pady=(0, 10))

        entry_pista = tk.Entry(
            card_turno,
            font=("Segoe UI", 12),
            bg="#313244",
            fg="#cdd6f4",
            insertbackground="#cdd6f4",
            relief=tk.FLAT,
        )
        entry_pista.pack(fill=tk.X, ipady=6, pady=(0, 12))
        entry_pista.focus_set()

        def enviar(_event=None):
            on_enviar_pista(entry_pista.get())

        entry_pista.bind("<Return>", enviar)

        self._crear_boton(
            card_turno, "Registrar Pista ✔", enviar, bg="#a6e3a1", width=22
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
            text=f"Ronda {numero_ronda} • Fase de Debate (Categoría: {categoria})",
            font=("Segoe UI", 13, "bold"),
            fg="#f9e2af",
            bg="#181825",
        ).pack(anchor="w", pady=(0, 8))

        card_timer = self._crear_tarjeta(self.contenedor)
        lbl_tiempo = tk.Label(
            card_timer,
            text=f"⏱️ Tiempo restante: {segundos_debate}s",
            font=("Segoe UI", 15, "bold"),
            fg="#f38ba8",
            bg="#1e1e2e",
        )
        lbl_tiempo.pack()

        card_pistas = self._crear_tarjeta(self.contenedor)
        tk.Label(
            card_pistas,
            text="Analicen todas las pistas de la ronda y debatan quién es el Impostor:",
            font=("Segoe UI", 10, "bold"),
            fg="#89dceb",
            bg="#1e1e2e",
        ).pack(anchor="w", pady=(0, 8))

        for autor, texto in pistas_ronda:
            fila = tk.Frame(card_pistas, bg="#313244", padx=10, pady=5)
            fila.pack(fill=tk.X, pady=3)
            tk.Label(
                fila,
                text=f"{autor}:",
                font=("Segoe UI", 10, "bold"),
                fg="#f9e2af",
                bg="#313244",
                width=16,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                fila,
                text=texto,
                font=("Segoe UI", 10),
                fg="#cdd6f4",
                bg="#313244",
                anchor="w",
            ).pack(side=tk.LEFT, fill=tk.X, expand=True)

        restante = [segundos_debate]

        def actualizar_reloj():
            restante[0] -= 1
            if restante[0] > 0:
                lbl_tiempo.config(text=f"⏱️ Tiempo restante: {restante[0]}s")
                self._timer_id = self.root.after(1000, actualizar_reloj)
            else:
                lbl_tiempo.config(text="⏱️ ¡Tiempo de debate terminado!")
                self._timer_id = None

        self._timer_id = self.root.after(1000, actualizar_reloj)

        frame_btn = tk.Frame(self.contenedor, bg="#181825")
        frame_btn.pack(pady=12)
        self._crear_boton(
            frame_btn,
            "Ir a Votación Secreta 🗳️",
            on_finalizar_debate,
            bg="#cba6f7",
            width=26,
        ).pack()

    # ---------------- IVistaVotacion ----------------

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
            text=f"Ronda {numero_ronda} • Votación Privada",
            font=("Segoe UI", 13, "bold"),
            fg="#f38ba8",
            bg="#181825",
        ).pack(anchor="w", pady=(0, 8))

        card = self._crear_tarjeta(self.contenedor)
        tk.Label(
            card,
            text=f"Turno de voto de: {nombre_votante}",
            font=("Segoe UI", 14, "bold"),
            fg="#f9e2af",
            bg="#1e1e2e",
        ).pack(anchor="w", pady=(0, 4))

        tk.Label(
            card,
            text="Selecciona al jugador que crees que es el Impostor (no puedes votarte a ti mismo):",
            font=("Segoe UI", 9),
            fg="#a6adc8",
            bg="#1e1e2e",
        ).pack(anchor="w", pady=(0, 10))

        var_elegido = tk.StringVar(value="")

        pistas_dict = dict(pistas_ronda)
        for candidato in candidatos:
            pista_cand = pistas_dict.get(candidato, "")
            texto_opcion = f"{candidato}   (Pista: \"{pista_cand}\")"
            tk.Radiobutton(
                card,
                text=texto_opcion,
                variable=var_elegido,
                value=candidato,
                font=("Segoe UI", 10),
                bg="#1e1e2e",
                fg="#cdd6f4",
                selectcolor="#313244",
                activebackground="#1e1e2e",
                activeforeground="#89b4fa",
            ).pack(anchor="w", pady=3)

        self._crear_boton(
            card,
            "Confirmar Voto 🗳️",
            lambda: on_registrar_voto(var_elegido.get()),
            bg="#f38ba8",
            width=22,
        ).pack(pady=(14, 4))

    def solicitar_ultima_oportunidad(
        self,
        nombre_impostor: str,
        on_adivinar_palabra: Callable[[str], None],
    ) -> None:
        self._limpiar_pantalla()

        card = self._crear_tarjeta(self.contenedor, pady=20)
        tk.Label(
            card,
            text="🎯 ¡EL IMPOSTOR HA SIDO DESCUBIERTO!",
            font=("Segoe UI", 15, "bold"),
            fg="#f38ba8",
            bg="#1e1e2e",
        ).pack(pady=(5, 8))

        tk.Label(
            card,
            text=f"{nombre_impostor}, tienes una ÚLTIMA OPORTUNIDAD para robar la victoria.\nEscribe cuál crees que es la palabra secreta:",
            font=("Segoe UI", 10),
            fg="#cdd6f4",
            bg="#1e1e2e",
            justify=tk.CENTER,
        ).pack(pady=(0, 12))

        entry_adivina = tk.Entry(
            card,
            font=("Segoe UI", 13),
            bg="#313244",
            fg="#f9e2af",
            insertbackground="#f9e2af",
            justify=tk.CENTER,
            relief=tk.FLAT,
        )
        entry_adivina.pack(ipady=6, ipadx=15, pady=(0, 14))
        entry_adivina.focus_set()

        def enviar(_event=None):
            on_adivinar_palabra(entry_adivina.get())

        entry_adivina.bind("<Return>", enviar)

        self._crear_boton(
            card, "Intentar Adivinar 🎲", enviar, bg="#f9e2af", width=24
        ).pack()

    # ---------------- IVistaResultado ----------------

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

        card_res = self._crear_tarjeta(self.contenedor)
        tk.Label(
            card_res,
            text=f"🏆 {ganador.upper()}",
            font=("Segoe UI", 16, "bold"),
            fg="#a6e3a1" if "CIVIL" in ganador.upper() else "#f38ba8",
            bg="#1e1e2e",
        ).pack(pady=(2, 4))

        tk.Label(
            card_res,
            text=detalle,
            font=("Segoe UI", 10),
            fg="#cdd6f4",
            bg="#1e1e2e",
        ).pack(pady=(0, 6))

        tk.Label(
            card_res,
            text=f"🔑 Palabra secreta: {palabra_secreta}",
            font=("Segoe UI", 12, "bold"),
            fg="#f9e2af",
            bg="#1e1e2e",
        ).pack()

        # Tabla de roles revelados y marcador acumulado
        card_tabla = self._crear_tarjeta(self.contenedor)
        tk.Label(
            card_tabla,
            text="Roles Revelados y Marcador Acumulado:",
            font=("Segoe UI", 10, "bold"),
            fg="#89dceb",
            bg="#1e1e2e",
        ).pack(anchor="w", pady=(0, 6))

        for nombre, rol, estado in roles_revelados:
            puntos = marcador_acumulado.get(nombre, 0)
            color_rol = "#f38ba8" if rol == "Impostor" else "#a6e3a1"
            fila = tk.Frame(card_tabla, bg="#313244", padx=10, pady=4)
            fila.pack(fill=tk.X, pady=2)

            tk.Label(
                fila,
                text=nombre,
                font=("Segoe UI", 10, "bold"),
                fg="#cdd6f4",
                bg="#313244",
                width=18,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                fila,
                text=rol,
                font=("Segoe UI", 10, "bold"),
                fg=color_rol,
                bg="#313244",
                width=12,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                fila,
                text=f"Estado: {estado}",
                font=("Segoe UI", 9),
                fg="#a6adc8",
                bg="#313244",
                width=16,
                anchor="w",
            ).pack(side=tk.LEFT)
            tk.Label(
                fila,
                text=f"Puntos: {puntos}",
                font=("Segoe UI", 10, "bold"),
                fg="#f9e2af",
                bg="#313244",
                anchor="e",
            ).pack(side=tk.RIGHT)

        botones = tk.Frame(self.contenedor, bg="#181825")
        botones.pack(pady=12)

        self._crear_boton(
            botones,
            "🔄 Jugar Otra Partida",
            on_nueva_partida,
            bg="#a6e3a1",
            width=22,
        ).pack(side=tk.LEFT, padx=8)

        self._crear_boton(
            botones,
            "👥 Cambiar Jugadores",
            on_volver_registro,
            bg="#89b4fa",
            width=22,
        ).pack(side=tk.LEFT, padx=8)
