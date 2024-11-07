import time
import random
import threading

lock_terminado = threading.Lock()

# Clase que representa una rana como hilo
class Anfibio(threading.Thread):
    def __init__(self, nombre, posicion_inicial, carretera):
        threading.Thread.__init__(self)  # Inicializar la clase base Thread
        self.nombre = nombre
        self.posicion = posicion_inicial
        self.carretera = carretera
        self.lock = threading.Lock()  # Agregar un lock para evitar que 2 anfibios se muevan al mismo lugar

    def run(self):
        while True:
            with self.lock:  # Proteger todo el bloque de verificación y movimiento
                # Priorizar movimiento de ranas y sapos específicos
                if self.nombre == "🐸":
                    if self.puede_avanzar():
                        self.posicion += 1  # Se mueve hacia adelante
                    elif self.puede_saltar():
                        self.posicion += 2  # Salta sobre el sapo
                    elif self.puede_retroceder():
                        # tirar dado de 0 a 2
                        dado = random.randint(0, 2)
                        # si dado es 0 no hace nada y sale, si es 1 o 2 retrocede
                        if dado > 0:
                            self.posicion -= 1  # Retrocede uno

                elif self.nombre == "🐱":
                    if self.puede_retroceder():
                        self.posicion -= 1  # Se mueve hacia atrás
                    elif self.puede_saltar():
                        self.posicion -= 2  # Salta sobre la rana
                    elif self.puede_avanzar():
                        # tirar dado de 0 a 2
                        dado = random.randint(0, 2)
                        # si dado es 0 no hace nada y sale, si es 1 o 2 avanza
                        if dado > 0:
                            self.posicion += 1  # Avanza uno

            self.carretera.mostrar_pista()
            time.sleep(0.5)

            if self.carretera.debe_terminar():
                if not self.carretera.anfibio_gano:
                    self.carretera.anfibio_gano = True
                    print("¡El juego ha terminado!")
                    break
                else:
                    break


    def puede_avanzar(self):
        # Verificar si puede moverse hacia adelante
        return self.posicion < self.carretera.longitud_pista - 1 and self.carretera.pista[self.posicion + 1] == " _ "

    def puede_retroceder(self):
        # Verificar si puede moverse hacia atrás
        return self.posicion > 0 and self.carretera.pista[self.posicion - 1] == " _ "

    def puede_saltar(self):
        # Verificar si puede saltar (hay un espacio vacío dos posiciones adelante o atrás)
        if self.nombre == "🐸":
            return (self.posicion < self.carretera.longitud_pista - 2 and
                    self.carretera.pista[self.posicion + 1] == "🐱" and
                    self.carretera.pista[self.posicion + 2] == " _ ")
        else:  # Sapo
            return (self.posicion > 1 and
                    self.carretera.pista[self.posicion - 1] == "🐸" and
                    self.carretera.pista[self.posicion - 2] == " _ ")


# Clase que representa la carretera
class Pista:
    def __init__(self, longitud_pista):
        self.longitud_pista = longitud_pista
        self.pista = [" _ "] * longitud_pista
        self.ranas = []
        self.lock = threading.Lock()  # Agregar un lock para evitar colisiones al mostrar la pista
        self.pista_inicial = []
        self.anfibio_gano = False

    def agregar_rana(self, rana):
        self.ranas.append(rana)

    def iniciar(self):
        # Mostrar la pista inicial antes de que comiencen los movimientos5

        self.mostrar_pista()

        for rana in self.ranas:
            rana.start()  # Iniciar cada hilo (cada rana)

        for rana in self.ranas:
            rana.join()  # Esperar a que todos los hilos terminen


    def armar_pista(self):
        self.pista = [" _ "] * self.longitud_pista
        for rana in self.ranas:
            if 0 <= rana.posicion < self.longitud_pista:
                self.pista[rana.posicion] = rana.nombre
            if len(self.pista_inicial) == 0:
                self.pista_inicial = self.pista

    def mostrar_pista(self):
        with self.lock:  # Proteger la salida con un lock para evitar conflictos entre hilos
            self.armar_pista()
            print(self.pista)
            print("")

    def debe_terminar(self):
        return self.pista == self.pista_inicial[::-1]


if __name__ == "__main__":
    cantidad_ranas = int(input("Ingrese una cantidad de ranas: "))
    cantidad_sapos = int(input("Ingrese una cantidad de sapos: "))
    longitud_pista = cantidad_ranas + cantidad_sapos + 1
    pista = Pista(longitud_pista)
    # Crear ranas (se mueven hacia la derecha)
    for i in range(cantidad_ranas):
        pista.agregar_rana(Anfibio("🐸", i, pista))  # Ranas en posiciones 0, 1, 2

    # Crear sapos (se mueven hacia la izquierda)
    for i in range(cantidad_sapos):
        pista.agregar_rana(Anfibio("🐱", longitud_pista - 1 - i, pista))  # Sapos en posiciones 4, 5, 6

    start = time.time()
    pista.iniciar()
    finish = time.time()

    print(f'Tiempo de ejecucion : {finish - start:.2f}s')
