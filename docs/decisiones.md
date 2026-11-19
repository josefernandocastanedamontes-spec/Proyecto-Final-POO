# Decisiones de implementación pendientes de confirmación

## Desempate de votación

1. En la votación inicial, cada jugador activo vota por otra persona.
2. Si dos o más participantes obtienen el máximo número de votos, se habilita una segunda votación.
3. En la segunda votación, solo se muestran como candidatos las personas que quedaron empatadas. El votante no puede seleccionarse a sí mismo.
4. Si la segunda votación identifica una mayoría única, ese participante se toma como acusado y se aplican las reglas normales de resolución.
5. Si la segunda votación también queda empatada, la implementación actual concede la victoria de esa ronda al impostor por supervivencia.

**Pendiente académico:** el documento base plantea esta última regla como una alternativa propuesta, no como una instrucción inequívoca. El equipo debe confirmarla con el docente antes de la sustentación. Si se decide otro comportamiento, habrá que actualizar el controlador, sus pruebas y la documentación.
