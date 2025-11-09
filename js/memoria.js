"use strict";

class Memoria {
    constructor() {
        this.tablero_bloqueado = false;
        this.primera_carta = null;
        this.segunda_carta = null;

        const parrafoCrono = document.querySelector("main p.cronometro");
        this.cronometro = new Cronometro(parrafoCrono);

        this.cronometro.arrancar();
    }

    voltearCarta(carta) {
        if (this.tablero_bloqueado || carta.dataset.estado === "revelada" || carta === this.primera_carta) return;

        // Marcar visualmente como "volteada"
        carta.dataset.estado = "volteada";

        if (!this.primera_carta) {
            this.primera_carta = carta;
            return;
        }

        this.segunda_carta = carta;
        this.tablero_bloqueado = true;

        this.compararCartas();
    }

    compararCartas() {
        const esPareja =
            this.primera_carta.querySelector("img").src ===
            this.segunda_carta.querySelector("img").src;

        setTimeout(() => {
            if (esPareja) {
                this.deshabilitarCartas();
            } else {
                this.volverACubrir();
            }
        }, 1000);
    }

    deshabilitarCartas() {
        // Marcar visualmente como "revelada"
        this.primera_carta.dataset.estado = "volteada";
        this.segunda_carta.dataset.estado = "volteada";

        // Marcar lógicamente como "revelada" para bloquear
        this.primera_carta.dataset.revelada = "true";
        this.segunda_carta.dataset.revelada = "true";

        this.comprobarJuego();
        this.reiniciarAtributos();
    }

    volverACubrir() {
        // Solo cubrir si no están "reveladas"
        if (!this.primera_carta.dataset.revelada) this.primera_carta.dataset.estado = "";
        if (!this.segunda_carta.dataset.revelada) this.segunda_carta.dataset.estado = "";

        this.reiniciarAtributos();
    }

    reiniciarAtributos() {
        this.primera_carta = null;
        this.segunda_carta = null;
        this.tablero_bloqueado = false;
    }

    barajarCartas() {
        const contenedor = document.querySelector("main");
        const cartas = Array.from(contenedor.querySelectorAll("article"));

        for (let i = cartas.length - 1; i > 0; i--) {
            const j = Math.floor(Math.random() * (i + 1));
            [cartas[i], cartas[j]] = [cartas[j], cartas[i]];
        }

        cartas.forEach(carta => contenedor.appendChild(carta));
    }

    comprobarJuego() {
        const cartas = document.querySelectorAll("main article");
        const todasReveladas = Array.from(cartas).every(
            carta => carta.dataset.revelada === "true"
        );

        if (todasReveladas) {
            alert("Juego completado.");
            this.cronometro.parar();
        }
    }
}

const juegoMemoria = new Memoria();
window.addEventListener("load", () => juegoMemoria.barajarCartas());
