


import time
from random import randint
from threading import Thread, Lock

lock = Lock() 
common_var = 1

#Thread modificado, en lugar de asociarle una funcion se le cambia el metodo run()
class Proceso(Thread):
    def __init__(self,nombre, mensaje, local_var = 0):
        super().__init__()
        self.name = nombre
        self.mensaje = mensaje
        self.local_var = local_var
    #Acepta modificaciones en 2 metodos unicamente __init__ y run(). Leer documentacion de threads

    def run(self):
        global common_var
        time.sleep(randint(1, 5))
        with lock:
            print("\n")
            print(f"Lock adquirido por {self.name}")
            print(f"{self.mensaje}")
            print(f"COMMON_VAR = {common_var}")
            common_var += 1
            print(f"COMMON_VAR = {common_var}")
            print(f"Lock liberado por {self.name}")
            print("\n")


class Prueba:
    def __init__(self, cantidad_procesos):
        self.cantidad_procesos = cantidad_procesos
        
    def crear_procesos(self):
        procesos = [
            Proceso(nombre=f'Proceso {i+1}', mensaje="Proceso ejecutando")
            for i in range(self.cantidad_procesos)
        ]
        return procesos
    #COmienza ejecucion de todos los threads. Sera necesario el join? Ya que corta ejecucion con el ganador
    def comenzar(self):
        procesos = self.crear_procesos()
        for proceso in procesos:
            proceso.start()
        for proceso in procesos:
            proceso.join()
        return


#Para ejecucion en IDE
ejecucion = Prueba(cantidad_procesos=10)
ejecucion.comenzar()
