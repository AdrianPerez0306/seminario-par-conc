"""
CONSIGNA:
2. En pseudocódigo, usando semáforos, resolver el problema del "rendez-vous" (o encuentro). Consiste en tener dos procesos, tales que uno de ellos mientras ejecuta deberá alcanzar un punto (o marca) dentro de su código, y lo mismo con otro proceso. El primero de ambos que llegue a la marca correspondiente deberá quedarse esperando a que el otro proceso llegue a su marca, y recién en el momento en que el otro haya llegado, ambos podrán continuar ejecutando su código a partir de allí. Escribir o discutir luego una solución análoga del rendez-vous para para 3 o más procesos, cada uno con su código y su marca dada. (Opcionalmente, implementarlo en Python u otro lenguaje, imprimiendo mensajes que informen cuando los procesos lleguen a las marcas dadas. En este caso, dentro del código podrían utilizar algún paquete o clase existente que implemente semáforos...)

Solucion para N procesos, determinados por la varible <cantidad>, 

ALUMNO
Perez, Adrian Maximiliano
"""
 
import threading

# Contador para tener en cuenta cuantos procesos estan a la espera del resto.
counter = 0

# Semaforo para condicion de carrera sobre la variable <counter = 0> definida arriba
counter_sem = threading.Semaphore(1)

class ProcesoRendezVous(threading.Thread):
    # Acepta modificaciones en 2 metodos unicamente __init__ y run(). Leer documentacion de threads
    def __init__(self, nombre, semaphore:threading.Semaphore):
        super().__init__()
        self.name = nombre
        self.semaphore = semaphore

    def run(self):
        print(f'Process {self.name}: Empieza a ejecutar')
        # Hace cosas
        print(f'Process {self.name}: Marca de espera alcanzada')
        with counter_sem:
            global counter
            counter += 1
            if counter == cantidad: #Si estan todos a esperando, se liberan los semaforos.
                for semaforo in semaforos:
                    semaforo.release()
        self.semaphore.acquire()
        print(f'Proceso {self.name}: Continua')


class RendezVous:
    def __init__(self, procesos:[]):
        self.procesos = procesos

    #COmienza ejecucion de todos los threads. Sera necesario el join? Ya que corta ejecucion con el ganador
    def comenzar(self):
        for proceso in self.procesos:
            proceso.start()
        for proceso in self.procesos:
            proceso.join()
        return


if __name__ == "__main__":
    #Cantidad de procesos y semaforos
    cantidad = 3

    #Cantida de semaforos, igual a la cantidad de procesos. Inicia en 0 asi pueden ejecutar
    semaforos = [threading.Semaphore(0) for i in range(cantidad)]
    #Procesos creados en base a los semaforos definidos arriba
    procesos = [ProcesoRendezVous(i+1, semaforo) for i, semaforo in enumerate(semaforos)]

    encuentro = RendezVous(procesos=procesos)
    encuentro.comenzar()