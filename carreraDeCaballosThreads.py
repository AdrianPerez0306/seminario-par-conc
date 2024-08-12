"""
Implementar una "carrera de caballos" usando threads, donde cada "caballo" es un Thread
o bien un objeto de una clase que sea sub clase de Thread, y contendrá una posición dada
por un número entero. El ciclo de vida de este objeto es incrementar la posición en variados
instantes de tiempo, mientras no haya llegado a la meta, la cual es simplemente un entero prefijado.
Una vez que un caballo llegue a la meta, se debe informar en pantalla cuál fue el ganador, luego de
lo cual los demás caballos no deberán seguir corriendo. Imprimir durante todo el ciclo las posiciones
de los caballos, o bien de alguna manera el camino que va recorriendo cada uno (usando símbolos Ascii).
El programa podría producir un ganador disitnto cada vez que se corra. Opcionalmente, extender el
funcionamiento a un array de n caballos, donde n puede ser un parámetro.
"""

import time
from random import randint
from threading import Thread, Lock

lock_ganador = Lock() #Si hay un ganador, se toma el recurso y bloquea ejecucion para otros threads
ganador = None

#Thread modificado, en lugar de asociarle una funcion se le cambia el metodo run()
class ThreadCaballo(Thread):
    def __init__(self, nombre, distancia_carrera):
        super().__init__()
        self.name = nombre
        self.distancia_a_recorrer = distancia_carrera
        self.distancia_recorrida = 0
    #Acepta modificaciones en 2 metodos unicamente __init__ y run(). Leer documentacion de threads

    def run(self):
        global ganador
        while ((self.distancia_recorrida < self.distancia_a_recorrer) and
               (ganador is None)):
            #Avanzan enteros aleatorios entre (a,b)
            self.distancia_recorrida += randint(1,2)
            self.normalizar_distancia_recorrida()
            # Verifica si algun caballo ha ganado antes de imprimir
            with lock_ganador: #Esto implica un lock.acquire() y lock.release()
                print(f"{self.name} - Distancia recorrida: {self.distancia_recorrida}")
                if self.distancia_recorrida == self.distancia_a_recorrer:
                    ganador = self.name
                    print(f"{ganador} ha llegado a la meta y es el ganador!")
                    break  # Corta ejecucion una vez hay ganador
            time.sleep(0.2)

    def normalizar_distancia_recorrida(self):
        if self.distancia_recorrida > self.distancia_a_recorrer:
            self.distancia_recorrida = self.distancia_a_recorrer


class CarreraCaballos:
    def __init__(self, distancia, numero_competidores):
        self.distancia_carrera = distancia
        self.numero_caballos = numero_competidores
        self.ganador = None

    def crear_caballos(self):
        caballos = [
            ThreadCaballo(nombre=f'Caballo {i+1}',
                          distancia_carrera = self.distancia_carrera
                          )
            for i in range(self.numero_caballos)
        ]
        return caballos
    #COmienza ejecucion de todos los threads. Sera necesario el join? Ya que corta ejecucion con el ganador
    def comenzar(self):
        caballos = self.crear_caballos()
        for caballo in caballos:
            caballo.start()
        for caballo in caballos:
            caballo.join()
        return

#Para ejecucion en IDE
carrera = CarreraCaballos(distancia=10, numero_competidores=5)
carrera.comenzar()

#Para ejecucion de consola
if __name__ == "__main__":
    carrera = CarreraCaballos(distancia=10, numero_competidores=5)
    carrera.comenzar()
