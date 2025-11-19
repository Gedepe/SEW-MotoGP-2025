import xml.etree.ElementTree as ET

# Namespace usado en el XML
NS = {'u': 'http://www.uniovi.es'}

class Kml:
    def __init__(self):
        self.raiz = ET.Element('kml', xmlns="http://www.opengis.net/kml/2.2")
        self.doc = ET.SubElement(self.raiz, 'Document')

    def addPlacemark(self, nombre, descripcion, lon, lat, alt, modoAltitud="absolute"):
        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre
        ET.SubElement(pm, 'description').text = descripcion
        punto = ET.SubElement(pm, 'Point')
        ET.SubElement(punto, 'coordinates').text = f"{lon},{lat},{alt}"
        ET.SubElement(punto, 'altitudeMode').text = modoAltitud

    def addLineString(self, nombre, coordenadas, color='#ff0000ff', ancho='4'):
        pm = ET.SubElement(self.doc, 'Placemark')
        ET.SubElement(pm, 'name').text = nombre
        estilo = ET.SubElement(pm, 'Style')
        linea = ET.SubElement(estilo, 'LineStyle')
        ET.SubElement(linea, 'color').text = color
        ET.SubElement(linea, 'width').text = ancho
        ls = ET.SubElement(pm, 'LineString')
        ET.SubElement(ls, 'extrude').text = '1'
        ET.SubElement(ls, 'tessellation').text = '1'
        ET.SubElement(ls, 'altitudeMode').text = 'absolute'
        ET.SubElement(ls, 'coordinates').text = coordenadas

    def escribir(self, nombreArchivo):
        arbol = ET.ElementTree(self.raiz)
        arbol.write(nombreArchivo, encoding='utf-8', xml_declaration=True)

def procesarCircuito(xmlPath, kmlPath):
    try:
        tree = ET.parse(xmlPath)
        root = tree.getroot()
    except Exception as e:
        print(f"Error al leer el archivo XML: {e}")
        return

    kml = Kml()
    coordenadas_str = ""
    coordenadas_lista = []

    # Recorremos todos los tramos del circuito
    tramos = root.findall('.//u:tramo', NS)

    for idx, tramo in enumerate(tramos, start=1):
        coord = tramo.find('u:coordenadas', NS)
        lat = coord.find('u:latitud', NS).attrib['grados']
        lon = coord.find('u:longitud', NS).attrib['grados']
        alt = coord.find('u:altitud', NS).attrib['metros']

        # Añadimos un Placemark por punto
        kml.addPlacemark(f"Punto {idx}", f"Sector {idx}", lon, lat, alt)

        # Guardamos coordenadas para LineString
        coordenadas_lista.append(f"{lon},{lat},{alt}")

    # Cerramos el circuito añadiendo el primer punto al final
    if coordenadas_lista:
        coordenadas_lista.append(coordenadas_lista[0])

    # Concatenamos todas las coordenadas para LineString
    coordenadas_str = " ".join(coordenadas_lista)

    # Añadimos la línea del circuito completo
    kml.addLineString("Circuito Completo", coordenadas_str.strip())

    # Escribimos el archivo KML
    kml.escribir(kmlPath)
    print(f"Archivo {kmlPath} generado correctamente.")

def main():
    procesarCircuito("circuitoEsquema.xml", "circuito.kml")

if __name__ == "__main__":
    main()
