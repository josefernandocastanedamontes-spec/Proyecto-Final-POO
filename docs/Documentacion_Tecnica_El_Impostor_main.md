# El Impostor — Documentación técnica de la implementación

**Repositorio:** `josefernandocastanedamontes-spec/Proyecto-Final-POO`  
**Base:** rama `main`  
**Lenguaje:** Python 3  
**Interfaz:** Tkinter  
**Arquitectura:** Modelo–Vista–Controlador (MVC)

## Propósito y alcance

Este documento describe el código de la rama `main` con las correcciones de cierre preparadas para la entrega. Conserva el diseño inicial del equipo y distingue entre las reglas implementadas y las decisiones que requieren confirmación académica.

El Impostor es un juego de deducción social para grupos de 3 a 10 participantes. En cada ronda, el sistema selecciona una palabra de una categoría y asigna un impostor. Los civiles conocen la palabra secreta; el impostor no. Los participantes registran pistas, debaten y votan por quien consideran impostor. El resultado actualiza un marcador durante la partida.

La aplicación funciona localmente en un computador compartido. No incluye cuentas, persistencia de datos, salas en línea ni sincronización entre dispositivos.

## 1. Arquitectura y organización

| Capa | Ruta / componentes | Responsabilidad |
|---|---|---|
| Modelo | `modelos/` | Jugador, Rol, Civil, Impostor, Partida, Ronda, Pista, Voto, PalabraSecreta, Categoria, ConfiguracionPartida, ResultadoPartida, enumeraciones y excepciones. |
| Servicios | `servicios/` | Asignación de roles, consulta del banco de palabras, validación de pistas y conteo de votos. |
| Controlador | `controlador/` | Coordina el ciclo de la partida, las rondas, la votación y la resolución. |
| Vista | `vista/` | Contratos de interacción e interfaz de escritorio desarrollada con Tkinter. |
| Pruebas | `test/` | Pruebas unitarias sobre servicios, modelos y desempate. |
| Entrada | `main.py` | Construye las dependencias e inicia la aplicación. |

La vista captura acciones y las comunica mediante callbacks. `ControladorPartida` coordina el flujo y delega tareas específicas a `ControladorRonda` y `ControladorVotacion`. Los servicios encapsulan algoritmos intercambiables.

## 2. Flujo de una ronda

1. Se comprueba el registro de entre 3 y 10 jugadores y se valida la configuración.
2. Se selecciona una palabra de la categoría configurada.
3. Se asigna exactamente un impostor; el resto recibe el rol Civil.
4. Cada participante consulta su rol de manera privada. Los civiles ven la palabra y el impostor no.
5. Cada jugador activo registra una pista, validada por longitud y por la palabra prohibida.
6. Se presentan las pistas y se ejecuta el debate con temporizador. Al llegar a cero, la vista inicia la votación; el botón manual usa la misma protección para evitar una segunda ejecución.
7. Cada jugador activo vota por otro participante. La lista no incluye al votante.
8. Si hay empate, se realiza una segunda votación limitada a los candidatos empatados.
9. Se determina el ganador, se registra el resultado y se actualiza el marcador.
10. Si quedan rondas, se seleccionan una palabra y unos roles nuevos y se repite la revelación privada.

Los estados de jugadores se restablecen al preparar una nueva ronda; la eliminación por una acusación incorrecta se aplica a esa ronda, no se conserva automáticamente en las rondas posteriores.

## 3. Componentes principales

- `ControladorPartida`: registra jugadores, valida la configuración, crea la partida, prepara cada ronda y calcula el marcador.
- `ControladorRonda`: administra la revelación privada, el registro de pistas y el debate.
- `ControladorVotacion`: solicita votos, excluye al votante y ejecuta el segundo desempate cuando corresponde.
- `AsignadorRolesAleatorio`: asigna aleatoriamente un impostor y roles civiles.
- `RepositorioPalabrasMemoria`: mantiene palabras organizadas en Lugares, Comida y Animales.
- `ContadorVotosMayoria`: determina una mayoría única y devuelve los candidatos empatados cuando hay empate.
- `ValidadorPistaCompuesto`: combina los validadores de longitud y palabra prohibida.
- `VistaGraficaTkinter`: construye las pantallas de registro, revelación, pistas, debate, votación, última oportunidad y resultado.

## 4. Diseño orientado a objetos y SOLID

`Rol` es una abstracción común especializada por `Civil` e `Impostor`. `Jugador` mantiene identificador, nombre, rol y estado. `Ronda` conserva pistas, votos iniciales, votos de desempate, fase y resultado. `Partida` administra jugadores, rondas y resultados.

| Principio | Evidencia y observación |
|---|---|
| SRP | Modelos, servicios, controladores y vista separan responsabilidades. `ControladorPartida` sigue coordinando varias decisiones de flujo y puntuación. |
| OCP | Las interfaces de asignación, conteo y consulta de palabras permiten reemplazar implementaciones. |
| LSP | `Civil` e `Impostor` implementan el contrato `Rol`; la última oportunidad se consume únicamente para el impostor. |
| ISP | `vista/interfaces.py` separa contratos de registro, turnos, votación y resultado. |
| DIP | El controlador recibe vista, repositorio, asignador y contador mediante inyección de dependencias. |

**Patrones:** `ValidadorPistaCompuesto` aplica Composite al ejecutar una colección de validadores. Las interfaces de asignación, conteo y consulta de palabras permiten utilizar Strategy.

## 5. Validaciones y reglas

- Entre 3 y 10 jugadores; nombres obligatorios y únicos sin distinguir mayúsculas y minúsculas.
- Número de rondas entre 1 y 10.
- Tiempo de debate entre 10 y 300 segundos.
- Longitud máxima de pista entre 5 y 60 caracteres.
- La pista no puede estar vacía, exceder el límite ni incluir la palabra secreta como término completo.
- No se permite votar por uno mismo ni seleccionar un candidato fuera de la votación habilitada.
- El impostor dispone de un único intento para adivinar la palabra cuando la última oportunidad está activada.

**Decisión provisional de empate:** si la segunda votación también termina empatada, el código asigna la victoria de esa ronda al impostor por supervivencia. El documento base presenta esta opción como una propuesta que se debe validar con el docente.

## 6. Pruebas y verificación

La suite actual contiene 9 pruebas unitarias ejecutadas correctamente en la copia de trabajo: asignación de roles, consulta de palabras, validación de pistas, conteo y empate, transiciones de fase, validación de configuración, comparación de palabra completa, registro de resultados y segunda votación. No equivale a una prueba automatizada de toda la interfaz gráfica.

Para ejecutar desde la raíz del repositorio:

```bash
python -m unittest discover -s test -v
python main.py
```

La GUI debe probarse manualmente en el equipo que se usará para la sustentación, especialmente el temporizador y el recorrido completo de una partida.

## 7. Diagramas y anexos

El repositorio conserva el diagrama de clases actualizado en [diagrama_clases_main.mmd](./diagrama_clases_main.mmd), que representa las clases de la implementación actual. También se incorpora por separado la fotografía del diagrama UML manuscrito original elaborado por el equipo: [diagrama_clases_original_equipo.jpg](./diagrama_clases_original_equipo.png).

El UML manuscrito documenta el diseño inicial y se conserva como evidencia del trabajo original. El diagrama Mermaid representa las clases de la versión actual; ambos cumplen funciones distintas.

### 7.1 Video de demostración del funcionamiento

La demostración audiovisual del juego está disponible en YouTube: [Ver demostración del funcionamiento de El Impostor](https://youtu.be/2-C16hEieo8?si=wfyZLq3YzCOQ-uqD). El video complementa la documentación y permite observar el recorrido de la aplicación.

## 8. Conclusión

La implementación separa el dominio, los servicios, los controladores y la interfaz Tkinter. Las correcciones incorporan transiciones de fase, un segundo desempate, nueva palabra y roles por ronda, validación por término completo, validaciones de configuración y avance automático al finalizar el temporizador. La suite unitaria ejecutada tiene nueve pruebas. Antes de la entrega, el equipo debe confirmar la regla de segundo empate y realizar una prueba manual integral de la interfaz.
