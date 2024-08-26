#Implementear quicksorting y mergesorting
from threading import Thread
#Thread modificado, en lugar de asociarle una funcion se le cambia el metodo run()
class My(Thread):
    def __init__(self, nombre, lista):
        super().__init__()
        self.name = nombre
    #Acepta modificaciones en 2 metodos unicamente __init__ y run(). Leer documentacion de threads

    def run(self):
        pass

def mergeSort(lista):
    size_of_list = len(lista)//2
    if len(lista)<=1:
        return lista
    
    sub_A_ordenada = mergeSort(lista[:size_of_list])
    sub_B_ordenada = mergeSort(lista[size_of_list:])

    return merge(sub_A_ordenada, sub_B_ordenada)

def merge(sublista_a, sublista_b):
    result = []
    i, j = 0, 0

    while i < len(sublista_a) and j < len(sublista_b):
        if sublista_a[i] < sublista_b[j]:
            result.append(sublista_a[i])
            i += 1
        else:
            result.append(sublista_b[j])
            j += 1

    result.extend(sublista_a[i:])
    result.extend(sublista_b[j:])

    return result


foo = [6,4,1,67,89,1,3,5,-1, -5]
lista_foo = mergeSort(foo) 
print(foo)
print(lista_foo)
