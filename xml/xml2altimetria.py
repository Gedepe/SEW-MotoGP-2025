#!/usr/bin/env python3
# xml2altimetria.py
# Versión simplificada: sin relleno, sin colores, sin puntos, sin rayas internas

import xml.etree.ElementTree as ET
from pathlib import Path

SVG_WIDTH = 1000
SVG_HEIGHT = 400
MARGIN_LEFT = 60
MARGIN_RIGHT = 20
MARGIN_TOP = 20
MARGIN_BOTTOM = 60

NS = {'u': 'http://www.uniovi.es'}

def leer_puntos(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    tramos = root.findall('.//u:tramo', NS)
    distancias = []
    altitudes = []

    for tramo in tramos:
        dist_elem = tramo.find('u:dist_tramo', NS)
        alt_elem = tramo.find('u:coordenadas/u:altitud', NS)

        dist_m = (dist_elem.get('metros') 
                  if dist_elem is not None and dist_elem.get('metros') 
                  else (dist_elem.text or "0"))

        alt_m = (alt_elem.get('metros') 
                 if alt_elem is not None and alt_elem.get('metros') 
                 else (alt_elem.text or "0"))

        try: d = float(dist_m)
        except: d = 0.0

        try: a = float(alt_m)
        except: a = 0.0

        distancias.append(d)
        altitudes.append(a)

    return distancias, altitudes


def acumular_distancias(distancias):
    xs = [0.0]
    total = 0.0
    for d in distancias:
        total += d
        xs.append(total)
    return xs


def generar_puntos_svg(xs, alturas):
    min_x = min(xs)
    max_x = max(xs)
    min_h = min(alturas)
    max_h = max(alturas)

    inner_w = SVG_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    inner_h = SVG_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

    scale_x = inner_w / (max_x - min_x) if max_x != min_x else 1
    scale_y = inner_h / (max_h - min_h) if max_h != min_h else 1

    puntos = []
    for x, h in zip(xs, alturas):
        x_svg = MARGIN_LEFT + (x - min_x) * scale_x
        y_svg = MARGIN_TOP + (max_h - h) * scale_y
        puntos.append((round(x_svg,2), round(y_svg,2)))

    return puntos, (min_x, max_x, min_h, max_h)


def crear_svg(puntos, rango, salida_path):
    min_x, max_x, min_h, max_h = rango
    inner_w = SVG_WIDTH - MARGIN_LEFT - MARGIN_RIGHT
    inner_h = SVG_HEIGHT - MARGIN_TOP - MARGIN_BOTTOM

    coords_str = " ".join(f"{x},{y}" for x,y in puntos)

    svg = []
    svg.append('<?xml version="1.0" encoding="UTF-8"?>')
    svg.append(f'<svg width="{SVG_WIDTH}" height="{SVG_HEIGHT}" '
               'xmlns="http://www.w3.org/2000/svg">')
    svg.append('<rect x="0" y="0" width="100%" height="100%" fill="white"/>')

    # Eje X
    svg.append(f'<line x1="{MARGIN_LEFT}" y1="{SVG_HEIGHT-MARGIN_BOTTOM}" '
               f'x2="{SVG_WIDTH-MARGIN_RIGHT}" y2="{SVG_HEIGHT-MARGIN_BOTTOM}" '
               'stroke="black" stroke-width="1"/>')

    # Eje Y
    svg.append(f'<line x1="{MARGIN_LEFT}" y1="{MARGIN_TOP}" '
               f'x2="{MARGIN_LEFT}" y2="{SVG_HEIGHT-MARGIN_BOTTOM}" '
               'stroke="black" stroke-width="1"/>')

    # Etiquetas X
    for i in range(11):
        frac = i / 10
        x = MARGIN_LEFT + frac * inner_w
        dist = min_x + frac * (max_x - min_x)
        svg.append(f'<text x="{x}" y="{SVG_HEIGHT-MARGIN_BOTTOM+20}" '
                   f'font-size="10" text-anchor="middle">{dist:.0f}</text>')

    # Etiquetas Y
    for i in range(11):
        frac = i / 10
        y = MARGIN_TOP + frac * inner_h
        alt = max_h - frac * (max_h - min_h)
        svg.append(f'<text x="{MARGIN_LEFT-10}" y="{y+4}" '
                   f'font-size="10" text-anchor="end">{alt:.0f}</text>')

    # Polylínea del perfil — solo línea negra, sin puntos, sin rellenos
    svg.append(f'<polyline points="{coords_str}" fill="none" '
               'stroke="black" stroke-width="2"/>')

    svg.append('</svg>')

    with open(salida_path, "w", encoding="utf-8") as f:
        f.write("\n".join(svg))


def main():
    xml_path = Path("circuitoEsquema.xml")
    salida = Path("altimetria.svg")

    if not xml_path.exists():
        print("ERROR: No existe circuitoEsquema.xml")
        return

    distancias, altitudes = leer_puntos(xml_path)
    if not distancias:
        print("No hay tramos en el XML.")
        return

    xs = acumular_distancias(distancias)

    alturas_vertices = [altitudes[0]] + altitudes

    puntos, rango = generar_puntos_svg(xs, alturas_vertices)

    crear_svg(puntos, rango, salida)

    print(f"SVG generado: {salida}")


if __name__ == "__main__":
    main()
