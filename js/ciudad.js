"use strict";

class Ciudad {
    constructor(nombre, pais, gentilicio) {
        this.nombre = nombre;
        this.pais = pais;
        this.gentilicio = gentilicio;
        this.poblacion = 0;
        this.coordenadas = { lat: 0, lon: 0 };
    }

    inicializar(poblacion, coordenadas) {
        this.poblacion = poblacion;
        this.coordenadas = coordenadas;
    }

    getNombre() {
        return `Ciudad: ${this.nombre}`;
    }

    getPais() {
        return `País: ${this.pais}`;
    }

    getInfoSecundaria() {
        return `
            <ul>
                <li>Gentilicio: ${this.gentilicio}</li>
                <li>Población: ${this.poblacion.toLocaleString()} habitantes</li>
            </ul>
        `;
    }

    mostrarCoordenadas() {
        document.write(`<p>Coordenadas de ${this.nombre}: lat=${this.coordenadas.lat}, lon=${this.coordenadas.lon}</p>`);
    }
}
