# El Impostor — Proyecto final POO

Juego de deducción social desarrollado en Python 3 con interfaz de escritorio Tkinter. Participan entre 3 y 10 jugadores: los civiles conocen una palabra secreta y el impostor debe disimular que la desconoce.

## Requisitos
- Python 3.10 o superior.
- Tkinter disponible en la instalación de Python.
- No se requieren paquetes externos para la ejecución básica.

## Ejecución
Desde la raíz del repositorio:

```bash
python main.py
```

## Pruebas

```bash
python -m unittest discover -s test -v
```

La suite actual contiene 9 pruebas unitarias sobre asignación de roles, banco de palabras, validación de pistas, conteo y desempate, transiciones de fase, configuración y resultados.

## Estructura
- `modelos/`: entidades, roles, estados, configuración, resultados y excepciones.
- `servicios/`: asignación, consulta de palabras, validación y conteo de votos.
- `controlador/`: coordinación de partida, rondas y votación.
- `vista/`: contratos de la vista e interfaz Tkinter.
- `test/`: pruebas unitarias.
- `docs/`: documentación técnica y diagramas.

## Documentación y UML
- [Documentación técnica (Markdown)](docs/Documentacion_Tecnica_El_Impostor_main.md)
- [Diagrama de clases actualizado (Mermaid)](docs/diagrama_clases_main.mmd)
- [Decisión de desempate y regla provisional](docs/decisiones.md)

La entrega editable Word y PDF, con la fotografía original del UML manuscrito en el Anexo A, se adjunta en los archivos compartidos junto con esta actualización. Esos binarios no están almacenados directamente en GitHub en esta rama.

## Reglas de desempate
Si la votación inicial termina empatada, se realiza una segunda votación entre los candidatos empatados. Si el empate persiste, la implementación asigna la victoria de esa ronda al impostor por supervivencia. Esta última decisión es provisional y debe confirmarse con el docente.
