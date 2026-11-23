# Verificación directa de la entrega

Ejecutada en la sesión de entrega del 22 de noviembre de 2026, desde la raíz del proyecto.

- `python -B -m unittest -v` devolvió `0`. 23/23 pruebas aprobadas. [Salida](unittest.txt).
- Los casos de selector usan simulaciones. La ejecución con argumento se comprobó en procesos reales de consola. La comprobación gráfica queda pendiente.

Totales en el orden líneas, eventos, INFO, WARNING, ERROR y malformadas.

| Comando | Observados | Esperados en README | Código | stderr | Diferencias con README / stdout anterior |
| --- | --- | --- | ---: | --- | --- |
| [`python analizador.py logs_correctos.txt`](logs_correctos.txt.stdout.txt) | 5, 5, 3, 1, 1, 0 | 5, 5, 3, 1, 1, 0 | 0 | Vacío | Ninguna / idéntica byte a byte |
| [`python analizador.py logs_errores.txt`](logs_errores.txt.stdout.txt) | 10, 9, 3, 2, 2, 7 | 10, 9, 3, 2, 2, 7 | 0 | Vacío | Ninguna / idéntica byte a byte |
| [`python analizador.py logs_correctos2.log`](logs_correctos2.log.stdout.txt) | 10, 10, 4, 3, 3, 0 | 10, 10, 4, 3, 3, 0 | 0 | Vacío | Ninguna / idéntica byte a byte |
| [`python analizador.py logs_errores2.log`](logs_errores2.log.stdout.txt) | 16, 15, 5, 3, 4, 12 | 16, 15, 5, 3, 4, 12 | 0 | Vacío | Ninguna / idéntica byte a byte |

**Estado de esta ejecución directa: APROBADA.**

En la [refactorización previa](../comparacion.md) constan 23/23 pruebas antes y después. Se cotejaron nuevamente sus archivos guardados, que contienen salidas estándar idénticas entre sí para los cuatro ejemplos, errores vacíos y códigos de salida 0.
