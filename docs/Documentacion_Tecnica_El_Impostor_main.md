# El Impostor — Documentación técnica de la rama main

**Versión:** 1.0 — 19 de noviembre de 2026  
**Repositorio:** `josefernandocastanedamontes-spec/Proyecto-Final-POO`  
**Rama documentada:** `main`  
**Tecnología:** Python 3, Tkinter, unittest  
**Arquitectura:** Modelo–Vista–Controlador (MVC)

## Control del documento

Este informe describe el código publicado en `main`. El diseño inicial del equipo se conserva como referencia en el diagrama UML manuscrito (Anexo A en el documento de entrega editable). Las rutas y nombres de módulos de este informe corresponden a `controlador/` y `vista/`, tal como aparecen en la rama `main`.

La revisión fue estática sobre los archivos del repositorio. Las pruebas no se ejecutaron en este entorno y no se afirma que la GUI haya sido probada en tiempo de ejecución.

## 1. Descripción general

El Impostor es un juego grupal de deducción social. Entre tres y diez participantes reciben roles: los civiles conocen una palabra secreta y el impostor intenta disimular que la desconoce. Los jugadores registran pistas, debaten y votan por quien consideran que es el impostor. La aplicación presenta el resultado y un marcador acumulado durante la sesión.

La versión actual es una aplicación de escritorio ejecutada localmente en un computador compartido. No se identifican cuentas, persistencia en una base de datos, conexión por Internet ni sincronización entre dispositivos.

## 2. Arquitectura y organización

| Capa | Ruta / componentes | Responsabilidad |
|---|---|---|
| Modelo | `modelos/` | Entidades del dominio: Jugador, Rol, Civil, Impostor, Partida, Ronda, Pista, Voto, PalabraSecreta, Categoria, ConfiguracionPartida y ResultadoPartida; además de enumeraciones y excepciones. |
| Servicios | `servicios/` | Algoritmos de asignación de roles, selección de palabras, conteo de votos y validación de pistas. |
| Controlador | `controlador/` | Coordina el ciclo de partida, las fases de ronda y la votación. |
| Vista | `vista/` | Contratos de interacción y aplicación gráfica construida con Tkinter. |
| Pruebas | `test/` | Pruebas unitarias sobre servicios. |
| Entrada | `main.py` | Construye dependencias e inicia la aplicación. |

La vista recibe acciones de los jugadores y las comunica mediante callbacks. `ControladorPartida` coordina el flujo y delega tareas específicas en `ControladorRonda` y `ControladorVotacion`. Los servicios encapsulan operaciones especializadas.

## 3. Componentes principales

- **ControladorPartida:** registra jugadores, valida la configuración, crea la partida, inicia la asignación, coordina rondas y presenta resultados.
- **ControladorRonda:** revela roles en privado, solicita pistas y presenta la fase de debate.
- **ControladorVotacion:** solicita un voto por jugador activo y utiliza el contador para determinar el resultado.
- **AsignadorRolesAleatorio:** mezcla los jugadores y asigna un impostor; el resto recibe el rol Civil.
- **RepositorioPalabrasMemoria:** mantiene palabras organizadas en Lugares, Comida y Animales.
- **ContadorVotosMayoria:** determina una mayoría única; devuelve `None` cuando hay empate o no hay votos.
- **ValidadorPistaCompuesto:** combina validadores de longitud y palabra prohibida.
- **VistaGraficaTkinter:** presenta registro, asignación privada, pistas, debate, votación, última oportunidad y resultados.

## 4. Flujo de juego observado

| Etapa | Comportamiento en el código |
|---|---|
| Registro | Permite agregar y retirar jugadores. Valida nombres vacíos, duplicados y un máximo de diez; exige al menos tres para iniciar. |
| Configuración | Permite elegir categoría, rondas, tiempo de debate, longitud máxima de pista y última oportunidad. |
| Asignación privada | Cada participante consulta su rol por turnos. Los civiles ven la palabra; el impostor recibe un mensaje sin ella. |
| Pistas | Cada jugador activo registra una pista. Se valida texto vacío, longitud y presencia de la palabra secreta según el validador actual. |
| Debate | Se presenta la lista de pistas y una cuenta regresiva. El avance a votación se realiza actualmente con el botón de la vista. |
| Votación | Cada participante activo registra un voto. El controlador rechaza voto vacío, voto a sí mismo y candidato no válido. |
| Resolución | Si se señala al impostor, puede habilitarse el intento final. Si se señala a un civil, se marca eliminado y se evalúa la continuidad. |
| Resultado | Se muestran ganador, palabra, roles, estado de jugadores y marcador acumulado. |

**Limitación importante:** el código consultado asigna palabra y roles al comenzar la partida, no al iniciar cada ronda. Por tanto, en rondas posteriores no se renuevan como plantea el documento base.

## 5. POO y principios SOLID

La clase abstracta `Rol` define un contrato común y `Civil` e `Impostor` lo especializan. `Jugador` conserva identificador, nombre, rol y estado, además de crear pistas y votos. `Ronda` agrupa pistas, votos y fase.

| Principio | Evidencia y observación |
|---|---|
| SRP | La separación en modelos, servicios, controladores y vista distribuye responsabilidades. `ControladorPartida` todavía concentra decisiones de flujo y puntuación. |
| OCP | `IAsignadorRoles` e `IContadorVotos` permiten sustituir implementaciones. El repositorio de palabras se declara como clase concreta en el controlador. |
| LSP | `Civil` e `Impostor` implementan `Rol`; debe revisarse la semántica de `intentar_adivinar` para mantener contratos coherentes. |
| ISP | `vista/interfaces.py` separa contratos de registro, turnos, votación y resultado y los agrupa en `IVistaJuego`. |
| DIP | El controlador recibe vista, asignador y contador por constructor. Conviene depender también de la abstracción `IRepositorioPalabras`. |

**Patrones:** Composite aparece en `ValidadorPistaCompuesto`, que ejecuta varios validadores. Strategy se refleja en las interfaces de asignación, conteo y consulta de palabras, que permiten cambiar algoritmos.

## 6. Pruebas y verificación

`test/test_juego_completo.py` contiene cuatro pruebas unitarias: asignación de un único impostor, consulta de palabras por categoría, validación de pistas y conteo por mayoría. El nombre del archivo no implica que exista una prueba de integración del juego completo.

Para ejecutar localmente desde la raíz:

```bash
python -m unittest discover -s test -v
python main.py
```

## 7. Hallazgos y pendientes técnicos

| Prioridad | Hallazgo estático en `main` | Acción recomendada |
|---|---|---|
| Alta | `Partida.determinar_ganador()` devuelve siempre un resultado pendiente. | Implementar la determinación del resultado o retirar el método hasta definir su responsabilidad. |
| Alta | `Ronda.avanzar_fase()` contiene `pass`; controladores modifican `_fase` directamente. | Implementar transiciones válidas y encapsularlas. |
| Alta | El empate no activa segunda votación entre empatados. | Implementar el desempate indicado en el documento base y definir qué ocurre si persiste. |
| Alta | Palabra y roles no se renuevan en cada ronda. | Elegir otra palabra y volver a asignar roles al iniciar cada ronda. |
| Media | El temporizador actualiza el texto, pero no dispara por sí solo el avance a votación. | Conectar el fin del temporizador con el callback y evitar dobles ejecuciones. |
| Media | La palabra prohibida se busca como subcadena, lo que puede generar falsos positivos. | Comparar términos completos con normalización. |
| Media | La lista visual de candidatos incluye al votante, aunque el controlador rechaza ese voto. | Excluir al votante de las opciones. |
| Media | La configuración no valida todos los límites, por ejemplo el tiempo de debate. | Completar las validaciones de parámetros. |
| Media | Las pruebas cubren servicios, no controladores ni flujo integrado. | Agregar pruebas de ronda, empate, última oportunidad y marcador. |
| Baja | El README anterior no documentaba instalación, ejecución ni pruebas. | Mantener estas instrucciones actualizadas. |

**Decisión pendiente:** el documento base propone una segunda votación entre los empatados y plantea como alternativa que, si el empate persiste, gane el impostor por supervivencia. Esa segunda regla debe ser confirmada por el equipo o por el docente antes de tratarla como requisito definitivo.

## 8. Instalación y uso

1. Instalar Python 3.10 o superior y verificar que Tkinter esté disponible.
2. Abrir una terminal en la raíz del repositorio.
3. Ejecutar `python -m unittest discover -s test -v` para correr las pruebas disponibles.
4. Ejecutar `python main.py` para iniciar la aplicación.
5. Registrar entre tres y diez participantes, escoger la configuración y seguir las indicaciones de la pantalla.

## 9. Conclusión

La rama `main` contiene una aplicación de escritorio organizada en capas y una interfaz Tkinter para recorrer las etapas centrales del juego. Ofrece una base para explicar POO, herencia, abstracción, interfaces, MVC y separación de servicios. Antes de considerar cerrada la entrega deben completarse las transiciones de ronda, el desempate, la renovación de palabra y roles, el avance automático del temporizador y las pruebas de integración.

## Anexo A. Diagrama UML original del equipo

La fotografía del diagrama manuscrito elaborado por el equipo se conserva como referencia del diseño inicial y debe incluirse junto al documento de entrega. El diagrama de clases de la implementación actual se encuentra en [`diagrama_clases_main.mmd`](diagrama_clases_main.mmd). El UML manuscrito y el diagrama sincronizado con el código cumplen propósitos distintos: el primero documenta el diseño inicial y el segundo representa la estructura de la versión publicada.
