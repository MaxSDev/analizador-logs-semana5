from datetime import datetime
import re


NIVELES = ("INFO", "WARNING", "ERROR")
PATRON_FECHA = re.compile(r"[0-9]{4}-[0-9]{2}-[0-9]{2}(?: [0-9]{2}:[0-9]{2}:[0-9]{2})?")
PATRON_SEVERIDAD = re.compile(r"\[([^\[\]]*)\]")


def validar_fecha(texto):
    # Comprueba el formato exacto y la existencia de la fecha y hora.
    if not PATRON_FECHA.fullmatch(texto):
        return False
    formato = "%Y-%m-%d %H:%M:%S" if " " in texto else "%Y-%m-%d"
    try:
        datetime.strptime(texto, formato)
    except ValueError:
        return False
    return True


def separar_fecha_mensaje(texto):
    # Separa la fecha inicial y su hora opcional del mensaje restante.
    campos = texto.split(maxsplit=1)
    if not campos:
        return "", ""
    # Si comienza con palabras, falta la fecha; esas palabras son el mensaje.
    if not re.match(r"[0-9]", campos[0]):
        return "", texto
    fecha = campos[0]
    mensaje = campos[1] if len(campos) == 2 else ""
    if mensaje:
        partes = mensaje.split(maxsplit=1)
        if ":" in partes[0]:
            fecha += " " + partes[0]
            mensaje = partes[1] if len(partes) == 2 else ""
    return fecha, mensaje


def analizar_linea(linea):
    # Devuelve la severidad reconocida y todos los motivos de invalidez.
    texto = linea.strip()
    if not texto:
        return None, ["Línea vacía"]

    motivos = []
    # strip() permite espacios iniciales; match() exige la etiqueta al inicio.
    coincidencia = PATRON_SEVERIDAD.match(texto)
    nivel = None
    if coincidencia:
        etiqueta = coincidencia.group(1)
        if etiqueta in NIVELES:
            nivel = etiqueta
        else:
            motivos.append(f"severidad desconocida: [{etiqueta}]")
        fecha, mensaje = separar_fecha_mensaje(texto[coincidencia.end():].strip())
    else:
        motivos.append("severidad ausente o sin corchetes válidos")
        # Sin etiqueta, se examina la fecha inicial sin inventar un nivel.
        campos = texto.split(maxsplit=1)
        fecha = campos[0]
        mensaje = campos[1] if len(campos) == 2 else ""
        if mensaje and re.match(r"[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\s|$)", mensaje):
            partes = mensaje.split(maxsplit=1)
            fecha += " " + partes[0]
            mensaje = partes[1] if len(partes) == 2 else ""

    if not fecha:
        motivos.append("fecha ausente")
    elif not validar_fecha(fecha):
        motivos.append("fecha inválida: formato incorrecto o fecha/hora inexistente")
    if not mensaje:
        motivos.append("mensaje ausente o vacío")
    return nivel, motivos


def analizar_archivo(ruta):
    # Lee línea por línea; propaga errores de lectura para tratarlos en main.
    resultado = {
        "lineas": 0,
        "eventos": 0,
        "severidades": dict.fromkeys(NIVELES, 0),
        "malformadas": [],
    }
    # utf-8-sig también admite UTF-8 sin BOM; no oculta bytes ilegibles.
    with open(ruta, encoding="utf-8-sig") as archivo:
        for numero, linea in enumerate(archivo, start=1):
            resultado["lineas"] += 1
            if linea.strip():
                resultado["eventos"] += 1
            nivel, motivos = analizar_linea(linea)
            # La severidad se conserva aunque la fecha o el mensaje fallen.
            if nivel is not None:
                resultado["severidades"][nivel] += 1
            if motivos:
                resultado["malformadas"].append((numero, motivos))
    return resultado
