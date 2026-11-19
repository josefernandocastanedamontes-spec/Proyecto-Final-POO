# 🎭 El Impostor

Juego de deducción social desarrollado en **Python 3** con Programación Orientada a Objetos. Todos los participantes reciben una palabra secreta menos uno: el impostor. Los civiles dan pistas para descubrirlo y el impostor intenta pasar desapercibido.

## Integrantes
- Jose Fernando Castañeda Montes
- Santiago Aonso Restrepo Diaz
- Alejandro Caballero

## Requisitos
- Python 3.10 o superior.
- Tkinter (incluido normalmente en las instalaciones de Python para Windows).

No se necesitan paquetes externos.

## Ejecutar
Desde la carpeta raíz del proyecto:

```bash
py main.py
```

En otros sistemas puede utilizarse:

```bash
python3 main.py
```

## Ejecutar las pruebas

```bash
py -m unittest discover -s test -v
```

## Cómo se juega
1. Registra entre 3 y 10 participantes.
2. Selecciona la cantidad de rondas, categoría, tiempo de debate y si se permite una última oportunidad.
3. Cada persona ve su rol en privado. Los civiles también ven la palabra secreta.
4. Cada participante escribe una pista breve sin revelar la palabra.
5. El grupo debate y vota por quien sospecha que es el impostor.
6. Si hay empate, se realiza una segunda votación entre los empatados.
7. Si se descubre al impostor y está habilitada la última oportunidad, este puede intentar adivinar la palabra una sola vez.
8. Se muestran los roles y se actualiza el marcador.

## Estructura

```text
EL_IMPOSTOR/
├── modelos/          # Entidades, roles, estados y reglas de dominio
├── servicios/        # Asignación, palabras, validación y conteo de votos
├── controladores/    # Coordinación de los casos de uso
├── vistas/           # Interfaz de escritorio Tkinter
├── test/             # Pruebas unitarias
└── main.py           # Punto de entrada
```

## Arquitectura y diseño
- **MVC:** los modelos no dependen de Tkinter; la vista presenta información y recoge acciones; el controlador coordina el flujo.
- **SRP:** modelos y servicios mantienen responsabilidades separadas.
- **OCP:** la asignación, el repositorio, el contador y los validadores se pueden sustituir mediante contratos.
- **LSP:** `Civil` e `Impostor` implementan el contrato abstracto `Rol` sin exponer al impostor la palabra.
- **ISP:** los contratos de asignación, repositorio, conteo y validación son independientes.
- **DIP:** `Partida` recibe sus servicios por constructor.
- **Strategy:** el asignador y los servicios se pueden intercambiar.
- **Composite:** `ValidadorPistaCompuesto` combina validadores de reglas individuales.

## Reglas implementadas
- Entre 3 y 10 jugadores con nombres únicos.
- Exactamente un impostor por ronda.
- La palabra se entrega a los civiles, no al impostor.
- Una pista por participante y por ronda.
- Rechazo de pistas vacías, demasiado largas o que contengan la palabra secreta como término completo.
- Un voto por participante; no se permite votar por sí mismo.
- Desempate entre los candidatos empatados; si persiste, el impostor gana por supervivencia.
- Última oportunidad configurable, con un único intento real de adivinanza.
- Marcador acumulado entre rondas.

## Alcance y limitaciones
La primera versión funciona en un solo computador compartido. La privacidad de los roles depende de que cada participante oculte la pantalla al pasar el dispositivo. No incluye salas en línea ni multijugador por red.
