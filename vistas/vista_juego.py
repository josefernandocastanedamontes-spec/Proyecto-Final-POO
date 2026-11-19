import tkinter as tk
from tkinter import ttk, messagebox

from controladores.controlador_partida import ControladorPartida


class VistaJuego:
    """Interfaz Tkinter. Solo presenta datos y comunica acciones al controlador."""

    def __init__(self, root=None, controlador=None):
        self.root = root or tk.Tk()
        self.controlador = controlador or ControladorPartida()
        self.root.title("El Impostor | Juego de deducción")
        self.root.geometry("760x600")
        self.root.minsize(650, 500)
        self._after_id = None
        self._tiempo_restante = 0
        self._indice_revelacion = 0
        self._indice_pista = 0
        self._indice_voto = 0
        self._indice_desempate = 0
        self._mostrar_inicio()

    def _limpiar(self):
        if self._after_id:
            self.root.after_cancel(self._after_id)
            self._after_id = None
        for widget in self.root.winfo_children():
            widget.destroy()

    def _contenedor(self, titulo, subtitulo=None):
        self._limpiar()
        marco = ttk.Frame(self.root, padding=24)
        marco.pack(fill="both", expand=True)
        ttk.Label(marco, text=titulo, font=("Segoe UI", 22, "bold")).pack(anchor="w", pady=(0, 6))
        if subtitulo:
            ttk.Label(marco, text=subtitulo, font=("Segoe UI", 10)).pack(anchor="w", pady=(0, 18))
        return marco

    def _mostrar_inicio(self):
        marco = self._contenedor("🎭 El Impostor", "Registra a los participantes y configura una partida.")
        ttk.Label(marco, text="Nombres (uno por línea, de 3 a 10 jugadores)").pack(anchor="w")
        self.txt_nombres = tk.Text(marco, height=8, width=50, font=("Segoe UI", 11))
        self.txt_nombres.pack(fill="x", pady=(4, 14))
        self.txt_nombres.insert("1.0", "Ana\nJuan\nSofía\nPedro")

        fila = ttk.Frame(marco)
        fila.pack(fill="x", pady=5)
        ttk.Label(fila, text="Número de rondas:").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.var_rondas = tk.StringVar(value="3")
        ttk.Entry(fila, textvariable=self.var_rondas, width=8).grid(row=0, column=1, sticky="w", padx=(0, 20))
        ttk.Label(fila, text="Debate (segundos):").grid(row=0, column=2, sticky="w", padx=(0, 6))
        self.var_tiempo = tk.StringVar(value="60")
        ttk.Entry(fila, textvariable=self.var_tiempo, width=8).grid(row=0, column=3, sticky="w")

        fila2 = ttk.Frame(marco)
        fila2.pack(fill="x", pady=8)
        ttk.Label(fila2, text="Categoría:").grid(row=0, column=0, sticky="w", padx=(0, 6))
        self.var_categoria = tk.StringVar(value="Lugares")
        ttk.Combobox(fila2, textvariable=self.var_categoria, values=["Lugares", "Comida", "Animales"],
                     state="readonly", width=18).grid(row=0, column=1, sticky="w", padx=(0, 20))
        self.var_ultima = tk.BooleanVar(value=True)
        ttk.Checkbutton(fila2, text="Última oportunidad del impostor", variable=self.var_ultima).grid(row=0, column=2, sticky="w")
        ttk.Label(marco, text="Longitud máxima de pista: 40 caracteres").pack(anchor="w", pady=5)
        ttk.Button(marco, text="Iniciar partida", command=self._iniciar).pack(anchor="e", pady=14)

    def _iniciar(self):
        try:
            nombres = self.txt_nombres.get("1.0", "end").splitlines()
            self.controlador.iniciar_partida(
                nombres, numero_rondas=int(self.var_rondas.get()),
                tiempo_debate=int(self.var_tiempo.get()), categoria=self.var_categoria.get(),
                ultima_oportunidad=self.var_ultima.get(), longitud_max_pista=40,
            )
            self._indice_revelacion = 0
            self._mostrar_revelacion()
        except Exception as exc:
            messagebox.showerror("No se pudo iniciar", str(exc), parent=self.root)

    def _mostrar_revelacion(self):
        jugadores = self.controlador.jugadores
        if self._indice_revelacion >= len(jugadores):
            self.controlador.confirmar_revelacion()
            self._indice_pista = 0
            self._mostrar_pistas()
            return
        jugador = jugadores[self._indice_revelacion]
        marco = self._contenedor("Revelación privada", f"Ronda {self.controlador.ronda.numero} de {self.controlador.partida.configuracion.numero_rondas}")
        ttk.Label(marco, text=f"Pasa el dispositivo a {jugador.nombre}.", font=("Segoe UI", 16)).pack(pady=30)
        ttk.Label(marco, text="Asegúrate de que nadie más esté mirando.").pack(pady=4)
        etiqueta = ttk.Label(marco, text="", font=("Segoe UI", 16, "bold"), justify="center")
        etiqueta.pack(pady=35)
        boton = ttk.Button(marco, text="Mostrar mi rol")
        boton.pack(pady=12)

        def revelar():
            etiqueta.config(text=self.controlador.informacion_privada(jugador))
            boton.config(text="Ocultar y pasar", command=ocultar)

        def ocultar():
            etiqueta.config(text="")
            self._indice_revelacion += 1
            self._mostrar_revelacion()

        boton.config(command=revelar)

    def _mostrar_pistas(self):
        jugador = self.controlador.jugador_turno_pista()
        marco = self._contenedor("Ronda de pistas", f"Turno {self._indice_pista + 1} | Jugador: {jugador.nombre}")
        ttk.Label(marco, text="Escribe una pista relacionada con la palabra, sin mencionarla.").pack(anchor="w", pady=10)
        entrada = ttk.Entry(marco, font=("Segoe UI", 13))
        entrada.pack(fill="x", pady=8)
        contador = ttk.Label(marco, text="Máximo 40 caracteres")
        contador.pack(anchor="w")
        entrada.bind("<KeyRelease>", lambda _e: contador.config(text=f"{len(entrada.get())}/40 caracteres"))

        def enviar():
            try:
                completo = self.controlador.registrar_pista(entrada.get())
                self._indice_pista += 1
                if completo:
                    self._mostrar_debate()
                else:
                    self._mostrar_pistas()
            except Exception as exc:
                messagebox.showerror("Pista no válida", str(exc), parent=self.root)

        ttk.Button(marco, text="Registrar pista", command=enviar).pack(anchor="e", pady=20)

    def _mostrar_debate(self):
        marco = self._contenedor("Debate", "Analicen las pistas y conversen antes de votar.")
        lista = "\n".join(f"• {p.autor.nombre}: {p.texto}" for p in self.controlador.ronda.pistas)
        ttk.Label(marco, text=lista, font=("Segoe UI", 13), justify="left").pack(anchor="w", pady=15)
        self._tiempo_restante = self.controlador.partida.configuracion.tiempo_debate
        self.lbl_tiempo = ttk.Label(marco, text="", font=("Segoe UI", 20, "bold"))
        self.lbl_tiempo.pack(pady=20)
        ttk.Button(marco, text="Finalizar debate y votar", command=self._finalizar_debate).pack(anchor="e", pady=20)
        self._actualizar_reloj()

    def _actualizar_reloj(self):
        if not hasattr(self, "lbl_tiempo") or not self.lbl_tiempo.winfo_exists():
            return
        self.lbl_tiempo.config(text=f"Tiempo: {self._tiempo_restante} s")
        if self._tiempo_restante <= 0:
            self._finalizar_debate()
            return
        self._tiempo_restante -= 1
        self._after_id = self.root.after(1000, self._actualizar_reloj)

    def _finalizar_debate(self):
        try:
            if self.controlador.ronda.fase.name != "DEBATE":
                return
            self.controlador.finalizar_debate()
            self._indice_voto = 0
            self._mostrar_votacion()
        except Exception as exc:
            messagebox.showerror("Error", str(exc), parent=self.root)

    def _mostrar_votacion(self):
        jugadores = self.controlador.jugadores
        if self._indice_voto >= len(jugadores):
            return
        votante = jugadores[self._indice_voto]
        marco = self._contenedor("Votación", f"Voto {self._indice_voto + 1} de {len(jugadores)}")
        ttk.Label(marco, text=f"Pasa el dispositivo a {votante.nombre}.", font=("Segoe UI", 15)).pack(pady=20)
        ttk.Label(marco, text="Selecciona a quién consideras el impostor.").pack(anchor="w")
        opciones = [j.nombre for j in jugadores if j is not votante]
        variable = tk.StringVar(value=opciones[0])
        ttk.Combobox(marco, textvariable=variable, values=opciones, state="readonly").pack(fill="x", pady=10)

        def votar():
            try:
                acusado = next(j for j in jugadores if j.nombre == variable.get())
                respuesta = self.controlador.registrar_voto(votante, acusado)
                self._indice_voto += 1
                if respuesta["estado"] == "votando":
                    self._mostrar_votacion()
                elif respuesta["estado"] == "desempate":
                    self._indice_desempate = 0
                    self._mostrar_desempate()
                else:
                    self._procesar_respuesta_final(respuesta)
            except Exception as exc:
                messagebox.showerror("Voto no válido", str(exc), parent=self.root)

        ttk.Button(marco, text="Confirmar voto", command=votar).pack(anchor="e", pady=20)

    def _mostrar_desempate(self):
        jugadores = self.controlador.jugadores
        candidatos = self.controlador.ronda.candidatos_desempate
        if self._indice_desempate >= len(jugadores):
            return
        votante = jugadores[self._indice_desempate]
        opciones = [j for j in candidatos if j is not votante]
        if not opciones:
            respuesta = {"estado": "resultado", "resultado": self.controlador.partida.determinar_ganador(empate=True)}
            self._procesar_respuesta_final(respuesta)
            return
        marco = self._contenedor("Desempate", "Hubo un empate. Voten únicamente entre los jugadores empatados.")
        ttk.Label(marco, text=f"Turno de {votante.nombre}", font=("Segoe UI", 15)).pack(pady=20)
        variable = tk.StringVar(value=opciones[0].nombre)
        ttk.Combobox(marco, textvariable=variable, values=[j.nombre for j in opciones], state="readonly").pack(fill="x", pady=10)

        def votar():
            try:
                acusado = next(j for j in opciones if j.nombre == variable.get())
                respuesta = self.controlador.registrar_voto_desempate(votante, acusado)
                self._indice_desempate += 1
                if respuesta["estado"] == "desempate_votando":
                    self._mostrar_desempate()
                else:
                    self._procesar_respuesta_final(respuesta)
            except Exception as exc:
                messagebox.showerror("Voto no válido", str(exc), parent=self.root)

        ttk.Button(marco, text="Confirmar desempate", command=votar).pack(anchor="e", pady=20)

    def _procesar_respuesta_final(self, respuesta):
        if respuesta["estado"] == "ultima_oportunidad":
            self._mostrar_ultima_oportunidad()
        else:
            self._mostrar_resultado(respuesta["resultado"])

    def _mostrar_ultima_oportunidad(self):
        marco = self._contenedor("Última oportunidad", "El impostor puede intentar adivinar la palabra secreta una sola vez.")
        ttk.Label(marco, text="Impostor: escribe tu respuesta.").pack(anchor="w", pady=12)
        entrada = ttk.Entry(marco, font=("Segoe UI", 13))
        entrada.pack(fill="x", pady=10)

        def enviar():
            try:
                resultado = self.controlador.resolver_ultima_oportunidad(entrada.get())
                self._mostrar_resultado(resultado)
            except Exception as exc:
                messagebox.showerror("Error", str(exc), parent=self.root)

        ttk.Button(marco, text="Enviar intento", command=enviar).pack(anchor="e", pady=20)

    def _mostrar_resultado(self, resultado):
        marco = self._contenedor("Resultado de la ronda", resultado.generar_resumen())
        ttk.Label(marco, text="Roles revelados", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 8))
        for nombre, rol in resultado.roles_revelados.items():
            ttk.Label(marco, text=f"{nombre}: {rol}").pack(anchor="w")
        ttk.Label(marco, text="Marcador", font=("Segoe UI", 14, "bold")).pack(anchor="w", pady=(20, 8))
        for nombre, puntos in self.controlador.partida.marcador.items():
            ttk.Label(marco, text=f"{nombre}: {puntos} punto(s)").pack(anchor="w")
        if self.controlador.hay_mas_rondas():
            ttk.Button(marco, text="Siguiente ronda", command=self._siguiente_ronda).pack(anchor="e", pady=22)
        else:
            ttk.Button(marco, text="Finalizar partida", command=self._mostrar_final).pack(anchor="e", pady=22)

    def _siguiente_ronda(self):
        try:
            self.controlador.siguiente_ronda()
            self._indice_revelacion = 0
            self._indice_pista = 0
            self._indice_voto = 0
            self._indice_desempate = 0
            self._mostrar_revelacion()
        except Exception as exc:
            messagebox.showerror("Error", str(exc), parent=self.root)

    def _mostrar_final(self):
        marco = self._contenedor("Partida finalizada", "Gracias por jugar El Impostor.")
        ttk.Label(marco, text="Marcador final", font=("Segoe UI", 16, "bold")).pack(anchor="w", pady=15)
        for nombre, puntos in sorted(self.controlador.partida.marcador.items(), key=lambda x: x[1], reverse=True):
            ttk.Label(marco, text=f"{nombre}: {puntos} punto(s)", font=("Segoe UI", 12)).pack(anchor="w")
        ttk.Button(marco, text="Volver al inicio", command=self._mostrar_inicio).pack(anchor="e", pady=25)

    def ejecutar(self):
        self.root.mainloop()
