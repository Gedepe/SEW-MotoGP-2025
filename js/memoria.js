"use strict";

class Memoria {
    constructor() {
    }

    voltearCarta(carta) {
        carta.dataset.estado = "volteada";
    }
}

const juegoMemoria = new Memoria();