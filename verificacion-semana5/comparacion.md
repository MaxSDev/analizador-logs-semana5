# Verificación de Semana 5

Se ejecutó cada ejemplo con `python analizador.py <ruta>` antes y después.

| Ejemplo | stdout | stderr | Código | Líneas | Eventos | INFO | WARNING | ERROR | Malformadas |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| logs_correctos.txt | Idéntica byte a byte | Vacía en ambas | 0 | 5 | 5 | 3 | 1 | 1 | 0 |
| logs_correctos2.log | Idéntica byte a byte | Vacía en ambas | 0 | 10 | 10 | 4 | 3 | 3 | 0 |
| logs_errores.txt | Idéntica byte a byte | Vacía en ambas | 0 | 10 | 9 | 3 | 2 | 2 | 7 |
| logs_errores2.log | Idéntica byte a byte | Vacía en ambas | 0 | 16 | 15 | 5 | 3 | 4 | 12 |

Los SHA-256 coinciden en los cuatro ejemplos, las pruebas, las tres imágenes de evidencias/, README.md y .gitignore.

Las 23 pruebas pasan en ambas ejecuciones. El diff se generó contra la copia de analizador.py guardada antes de editar, pues el repositorio aún carece de un commit inicial.
