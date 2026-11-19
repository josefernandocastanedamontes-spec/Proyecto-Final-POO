# -*- coding: utf-8 -*-
from controlador.controlador_partida import ControladorPartida
from servicios.asignacion import AsignadorRolesAleatorio
from servicios.conteo import ContadorVotosMayoria
from servicios.palabras import RepositorioPalabrasMemoria
from vista.vista_tkinter import VistaGraficaTkinter


def main() -> None:
    vista = VistaGraficaTkinter()
    repositorio = RepositorioPalabrasMemoria()
    asignador = AsignadorRolesAleatorio()
    contador = ContadorVotosMayoria()

    controlador = ControladorPartida(
        vista=vista,
        repositorio_palabras=repositorio,
        asignador_roles=asignador,
        contador_votos=contador,
    )
    controlador.iniciar_aplicacion()


if __name__ == "__main__":
    main()
