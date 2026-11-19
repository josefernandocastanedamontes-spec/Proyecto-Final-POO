# El Impostor — Proyecto final POO

Juego de deducción social desarrollado en Python 3 con interfaz de escritorio Tkinter. Entre 3 y 10 participantes reciben roles: los civiles conocen una palabra secreta y el impostor debe disimular que la desconoce.

## Requisitos y ejecución
- Python 3.10 o superior.
- Tkinter disponible en la instalación.
- No se requieren paquetes externos para la ejecución básica.

Desde la raíz del repositorio:

```bash
python main.py
```

## Pruebas

```bash
python -m unittest discover -s test -v
```

Actualmente hay cuatro pruebas unitarias enfocadas en asignación de roles, consulta de palabras, validación de pistas y conteo por mayoría. No constituyen una prueba de integración de una partida completa.

## Estructura
- `modelos/`: entidades, roles, estados, configuración y resultados.
- `servicios/`: asignación, consulta de palabras, validación y conteo.
- `controlador/`: coordinación de partida, rondas y votación.
- `vista/`: contratos de vista e interfaz Tkinter.
- `test/`: pruebas unitarias.
- `docs/`: documentación y diagramas.

## Documentación
- [Documentación técnica ajustada a main](docs/Documentacion_Tecnica_El_Impostor_main.md)
- [Diagrama de clases de la implementación](docs/diagrama_clases_main.mmd)

La documentación separa las funciones existentes de los pendientes técnicos detectados en la revisión estática.
