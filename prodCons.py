"""
CONSIGNA:
1. Describir en pseudocódigo una solución al problema de productor-consumidor, para el caso de 2 productores y 1 consumidor, todos sobre un mismo buffer. Escribir todas las aclaraciones que sean necesarias.

ALUMNO
Perez, Adrian Maximiliano

SOLO IMPLEMENTADO EN PsEUDO CODIGO. ARCHIVO DE PYTHON SOLO PARA COMENTAR
"""

'''
// Buffer compartido de dimension N espacios
buffer: array[N]

// Semaphores
    #Empty representa el numero de espacios disponible. Tiene N espacios
empty: threading.Semaphore(N) 

    #Para que el consumidor no consuma si esta vacio. Por default con buffer vacio.
notEmpty: threading.Semaphore(0)

    #Para exclusion mutua, que un solo proceso produzca o consuma. No varios a la vez
mutex: threading.Semaphore(1) 


// PRODUCTOR
#Produce siempre y cuando haya espacio. Sino, espera.

while true:
  item = Item()
  wait(empty) # Si empty=0, esta lleno. Se duerme y espera un signal del Consumidor
  wait(mutex) // Adquiere el mutex UNICO
  buffer.add(item)
  signal(mutex) // Libera mutex para que otro proceso pueda tomarlo. Evita inanicion
  signal(notEmpty) // Incrementa notEmpty, que representa la cantidad de items en el buffer


// CONSUMIDOR
#Produce siempre y cuando haya items en el buffer. Sino, espera.

while true:
  wait(notEmpty) // Si esta vacio, queda a la espera de un signal del Productor
  wait(mutex)   // Adquiere el mutex UNICO
  buffer.remove(item)
  signal(mutex) // Libera mutex para que otro proceso pueda tomarlo. Evita inanicion
  signal(empty) // Indica que se consumio un item, por ende hay espacio disponible. 
  consume item


NOTA: 
wait() decrementa. Toma recurso si puede, si no se duerme a la espera de un signal()
signal() incrementa. Libera recurso y permite el paso a otro proceso.

ACLARACIONES:
No es necesario agregar el codigo del otro productor, ya que es identico y el buffer es comun.
En caso de haber otro productor, respetaria los waits y signals respectivos del Productor
'''