class Cronometro {
    constructor(elemento) {
        this.elemento = elemento; // elemento donde se muestra el cronómetro
        this.acumulado = 0;
        this.corriendo = null;
        try {
            this.tiempo = Temporal.Duration.from({ seconds: 0 });
            this.usandoTemporal = true;
        } catch {
            this.tiempo = 0;
            this.usandoTemporal = false;
        }
    }

    arrancar() {
        if (this.corriendo) return; 

        try {
            if (this.usandoTemporal) {
                this.inicio = Temporal.Now.plainDateTimeISO();
            } else {
                this.inicio = new Date();
            }
            this.corriendo = setInterval(this.actualizar.bind(this), 100);
            this.mostrar();
        } catch (error) {
            console.error("Error al iniciar el cronómetro:", error);
        }
    }

    actualizar() {
        try {
            if (this.usandoTemporal) {
                const ahora = Temporal.Now.plainDateTimeISO();
                const dur = ahora.since(this.inicio).round({ smallestUnit: "milliseconds" });
                this.tiempo = dur.add(Temporal.Duration.from({ seconds: this.acumulado }));
            } else {
                const ahora = this.acumulado + new Date() .getTime();
                const dif = ahora - this.inicio;
                this.tiempo = dif;
            }
            this.mostrar();
        } catch (error) {
            console.error("Error al actualizar el cronómetro:", error);
        }
    }

    parar() {
        if (this.corriendo) {
            clearInterval(this.corriendo);
            this.corriendo = null;
        }
        if (this.usandoTemporal) {
            this.acumulado = this.tiempo.total({ unit: "seconds" });
        } else {
            this.acumulado = this.tiempo;
        }
    }

    reiniciar() {
        try {
            if (this.usandoTemporal) {
                this.tiempo = Temporal.Duration.from({ seconds: 0 });
            } else {
                this.tiempo = 0;
            }
            this.acumulado = 0;
            this.parar();
            this.mostrar();
        } catch (error) {
            console.error("Error al reiniciar el cronómetro:", error);
        }
    }

    mostrar() {
        let stringMinutos = "00", stringSegundos = "00", stringDecimas = "0";
        if (this.usandoTemporal) {
            totalMs = this.tiempo.total({ unit: "milliseconds" });
        }

        const dur = this.tiempo;

        stringMinutos = String(parseInt(dur / 60000)).padStart(2, '0');
        stringSegundos = String(parseInt((dur % 60000) / 1000)).padStart(2, '0');
        stringDecimas = String(parseInt((dur % 1000) / 100));

        const stringCronometro = stringMinutos + ":" + stringSegundos + "." + stringDecimas;
        let parrafo = document.querySelector("main p");
        if (parrafo) {
            parrafo.textContent = stringCronometro;
        }
        this.elemento.textContent = `${minutos}:${segundos}.${decimas}`;
    }

}
