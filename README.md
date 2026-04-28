# Compilador Python

## Descripción

Este proyecto es un compilador/interprete simple para un lenguaje de programación personalizado, implementado en Python con una interfaz gráfica de usuario (GUI) usando Tkinter. El lenguaje permite operaciones básicas como impresión, asignaciones de variables, operaciones aritméticas, y control de un juego de la serpiente.

## Características

- Análisis léxico y sintáctico
- Interpretación de código
- GUI con editor de código, salida y análisis
- Integración con un juego de la serpiente
- Temas claro y oscuro
- Guardar y cargar código

## Requisitos

- Python 3.x
- Tkinter (incluido en la instalación estándar de Python)

## Instalación

1. Clona o descarga el repositorio.
2. Asegúrate de tener Python instalado.
3. Ejecuta el script: `python final.py`

## Uso

1. Abre la aplicación ejecutando `python final.py`.
2. Escribe código en el panel de código.
3. Haz clic en "Ejecutar" para interpretar el código.
4. Usa "Análisis Léxico/Sintáctico" para ver tokens y árbol sintáctico.
5. El juego de la serpiente se puede controlar con comandos del lenguaje.

## Sintaxis del Lenguaje

- `print expresión`: Imprime el valor de la expresión.
- `variable = expresión`: Asigna valor a una variable.
- Operadores: +, -, *, /, %, ^
- Comandos de juego: MOVER_ARRIBA, MOVER_ABAJO, MOVER_IZQUIERDA, MOVER_DERECHA, INICIAR_JUEGO, DETENER_JUEGO

## Ejemplos

```
print "Hola Mundo"
x = 5 + 3
print x
INICIAR_JUEGO
MOVER_DERECHA
```

## Contribución

Si deseas contribuir, por favor abre un issue o envía un pull request.

## Licencia

Este proyecto está bajo la licencia MIT.
