import argparse
from pathlib import Path
import sys

# Conserva los nombres disponibles para quienes importan analizador.
from logica_analisis import (
    NIVELES,
    PATRON_FECHA,
    PATRON_SEVERIDAD,
    analizar_archivo,
    analizar_linea,
    separar_fecha_mensaje,
    validar_fecha,
)


def mostrar_resumen(resultado, ruta):
    # Presenta los resultados sin modificar los contadores del análisis.
    separador = "-" * 64
    print("=" * 64)
    print("ANALIZADOR DE LOGS".center(64))
    print("=" * 64)
    print(f"Archivo: {Path(ruta).name}")
    print(separador)
    print("RESUMEN GENERAL")
    print(separador)
    print(f"{'Líneas leídas':<28} {resultado['lineas']:>10}")
    print(f"{'Total de eventos':<28} {resultado['eventos']:>10}")
    print(f"{'Líneas malformadas':<28} {len(resultado['malformadas']):>10}")
    if resultado["lineas"] == 0:
        print("El archivo está vacío.")
    print(separador)
    print("CLASIFICACIÓN POR SEVERIDAD")
    print(separador)
    print(f"{'Nivel':<28} {'Cantidad':>10}")
    for nivel, cantidad in resultado["severidades"].items():
        print(f"{nivel:<28} {cantidad:>10}")
    print(separador)
    print("DETALLES DE LÍNEAS MALFORMADAS")
    print(separador)
    if resultado["malformadas"]:
        print(f"{'Línea':>6}  Motivo(s)")
        for numero, motivos in resultado["malformadas"]:
            print(f"{numero:>6}  {'; '.join(motivos)}")
    else:
        print("Sin inconsistencias: no se encontraron líneas malformadas.")
    print("=" * 64)


def seleccionar_archivo():
    # Devuelve una ruta, "" al cancelar o None para usar la consola.
    # La importación local evita cargar tkinter al ejecutar con argumentos.
    try:
        import tkinter as tk
        from tkinter import filedialog
    except ImportError:
        print("El selector no está disponible. Ingresa la ruta en consola.")
        return None

    ventana = None
    try:
        ventana = tk.Tk()
        ventana.withdraw()
        return filedialog.askopenfilename(
            parent=ventana,
            title="Seleccionar archivo de logs",
            filetypes=(
                ("Archivos de logs (.txt y .log)", ("*.txt", "*.log")),
                ("Todos los archivos", "*"),
            ),
        )
    except tk.TclError:
        print("No se pudo abrir el selector. Ingresa la ruta en consola.")
        return None
    finally:
        # Se destruye la ventana oculta incluso si el diálogo falla.
        if ventana is not None:
            try:
                ventana.destroy()
            except tk.TclError:
                pass  # La ventana ya no está disponible.


def main(argumentos=None):
    # Obtiene la ruta, maneja fallos de lectura y devuelve el código de salida.
    parser = argparse.ArgumentParser(description="Analizador de archivos de logs UTF-8")
    parser.add_argument("ruta", nargs="?", help="Ruta relativa o absoluta del log UTF-8")
    opciones = parser.parse_args(argumentos)
    ruta = opciones.ruta
    if ruta is None:
        ruta = seleccionar_archivo()
        if ruta == "":
            print("Selección cancelada. No se analizó ningún archivo.")
            return 0
    if ruta is None:
        try:
            ruta = input("Ruta del archivo de logs: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nNo se recibió una ruta.", file=sys.stderr)
            return 1
    if not ruta:
        print("Error: la ruta está vacía.", file=sys.stderr)
        return 1
    try:
        resultado = analizar_archivo(ruta)
    except FileNotFoundError:
        print(f"Error: el archivo no existe: {ruta}", file=sys.stderr)
        return 1
    except PermissionError:
        print(f"Error: no hay permiso para leer: {ruta}", file=sys.stderr)
        return 1
    except UnicodeError:
        print("Error: el archivo no contiene texto UTF-8 válido.", file=sys.stderr)
        return 1
    except OSError as error:
        print(f"Error al leer el archivo: {error}", file=sys.stderr)
        return 1
    mostrar_resumen(resultado, ruta)
    return 0


if __name__ == "__main__":
    sys.exit(main())
