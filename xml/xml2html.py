#!/usr/bin/env python3
import xml.etree.ElementTree as ET
from pathlib import Path

# Namespace para tu XML
NS = {'xs': 'http://www.uniovi.es'}

class Html:
    def __init__(self):
        self.partes = []

    def add(self, txt):
        self.partes.append(txt)

    def render(self):
        return "\n".join(self.partes)

def xml2html(xml_in, html_out):
    # Leer XML
    tree = ET.parse(xml_in)
    root = tree.getroot()

    # Extraer datos del circuito
    nombre = root.get('nombre')  # atributo del elemento <circuito>
    pais = root.find('xs:pais', NS)
    localidad = root.find('xs:localidad_mas_proxima', NS)
    longitud_elem = root.find('xs:longitud_circuito', NS)
    anchura_elem = root.find('xs:anchura', NS)
    fecha = root.find('xs:fecha', NS)
    hora = root.find('xs:hora_española', NS)
    num_vueltas = root.find('xs:num_vueltas', NS)
    patrocinador = root.find('xs:patrocinador', NS)

    # Función utilidad para obtener texto
    def texto(elem):
        return elem.text.strip() if elem is not None and elem.text else ""

    # Utilidad para atributos
    def atributo(elem, attr):
        return elem.get(attr) if elem is not None and elem.get(attr) else ""

    # Construir HTML
    h = Html()
    h.add('<!DOCTYPE html>')
    h.add('<html lang="es">')
    h.add('<head>')
    h.add('  <meta charset="UTF-8">')
    h.add('  <meta name="viewport" content="width=device-width, initial-scale=1.0">')
    h.add('  <link rel="stylesheet" href="estilo.css">')
    h.add(f'  <title>Información - {nombre}</title>')
    h.add('</head>')
    h.add('<body>')
    h.add('  <main>')
    h.add(f'    <h1>{nombre}</h1>')
    h.add('    <section>')
    if pais is not None:
        h.add(f'      <p><strong>País:</strong> {texto(pais)}</p>')
    if localidad is not None:
        h.add(f'      <p><strong>Localidad más próxima:</strong> {texto(localidad)}</p>')
    if longitud_elem is not None:
        m = atributo(longitud_elem, 'metros')
        h.add(f'      <p><strong>Longitud del circuito:</strong> {m} m</p>')
    if anchura_elem is not None:
        m2 = atributo(anchura_elem, 'metros')
        h.add(f'      <p><strong>Anchura:</strong> {m2} m</p>')
    if fecha is not None:
        h.add(f'      <p><strong>Fecha:</strong> {texto(fecha)}</p>')
    if hora is not None:
        h.add(f'      <p><strong>Hora (española):</strong> {texto(hora)}</p>')
    if num_vueltas is not None:
        h.add(f'      <p><strong>Número de vueltas:</strong> {texto(num_vueltas)}</p>')
    if patrocinador is not None:
        h.add(f'      <p><strong>Patrocinador:</strong> {texto(patrocinador)}</p>')
    h.add('    </section>')
    h.add('  </main>')
    h.add('</body>')
    h.add('</html>')

    # Escribir HTML
    with open(html_out, 'w', encoding='utf-8') as f:
        f.write(h.render())

    print(f"HTML generado: {html_out}")

def main():
    xml2html("circuitoEsquema.xml", "InfoCircuito.html")

if __name__ == "__main__":
    main()
