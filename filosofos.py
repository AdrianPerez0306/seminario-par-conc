from snakes.nets import *


TOKEN_VALUE = 1
TOKEN = Value(TOKEN_VALUE)
n = PetriNet("N")

####################################################################
##############       Cubiertos -> Place()   ########################
####################################################################

cubiertos = []
for i in range(5):
    cubierto = Place(f'cubierto_{i+1}',[TOKEN_VALUE])
    cubiertos.append(cubierto)
    n.add_place(cubierto)

mode = lambda transition: transition.modes()[0]

####################################################################
##############          FILOSOFO_1          ########################
####################################################################

#Cada filosofo tiene un place para ocupar los cubiertos, este recibe 1 token
#   de la transicion de agarrar cubiertos
filosofo_1_ocupar_cubiertos = Place('f1_comiendo')
n.add_place(filosofo_1_ocupar_cubiertos)

# Transicion de agarrar cubiertos. Toma 2 tokens, 1 por cada cubierto(2 maximo),
# y devuelve un token al Place('f1_comiendo')
filosofo_1_agarrar_cubiertos = Transition("f1_agarrar_cubiertos")
n.add_transition(filosofo_1_agarrar_cubiertos)
n.add_input("cubierto_1", "f1_agarrar_cubiertos", TOKEN)
n.add_input("cubierto_2", "f1_agarrar_cubiertos", TOKEN)
n.add_output("f1_comiendo", "f1_agarrar_cubiertos", TOKEN)

# Luego que el Place('f1_comiendo') tiene el token, el filosofo f1 tiene otra transicio,
# f1_liberar_cubiertos, que toma 1 token del Place('f1_comiendo'), y devuelve un TOKEN ,
# a cada Place('cubierto') que tomo originalmente
filosofo_1_liberar_cubiertos = Transition("f1_liberar_cubiertos")
n.add_transition(filosofo_1_liberar_cubiertos)
n.add_input("f1_comiendo", "f1_liberar_cubiertos", TOKEN)
n.add_output("cubierto_1", "f1_liberar_cubiertos", TOKEN)
n.add_output("cubierto_2", "f1_liberar_cubiertos", TOKEN)

####################################################################
##############          FILOSOFO_2          ########################
####################################################################

#Cada filosofo tiene un place para ocupar los cubiertos, este recibe 1 token
#   de la transicion de agarrar cubiertos
filosofo_2_ocupar_cubiertos = Place('f2_comiendo')
n.add_place(filosofo_2_ocupar_cubiertos)

# Transicion de agarrar cubiertos.
filosofo_2_agarrar_cubiertos = Transition("f2_agarrar_cubiertos")
n.add_transition(filosofo_2_agarrar_cubiertos)
n.add_input("cubierto_2", "f2_agarrar_cubiertos", TOKEN)
n.add_input("cubierto_3", "f2_agarrar_cubiertos", TOKEN)
n.add_output("f2_comiendo", "f2_agarrar_cubiertos", TOKEN)

# Transicion de liberar cubiertos
filosofo_2_liberar_cubiertos = Transition("f2_liberar_cubiertos")
n.add_transition(filosofo_2_liberar_cubiertos)
n.add_input("f2_comiendo", "f2_liberar_cubiertos", TOKEN)
n.add_output("cubierto_2", "f2_liberar_cubiertos", TOKEN)
n.add_output("cubierto_3", "f2_liberar_cubiertos", TOKEN)




# EJemplo de transicion y tokens.
# Se dispara la Transition("f1_agarrar_cubiertos") y cubiertos_2, los deja en Place("f1_comiendo")
# y luego de ejecutar  Transition("f1_liberar_cubiertos")
def snapshot():
    for place in n.place():
        print(f'{place}: {"sin TOKEN" if place.tokens.size() == 0 else "con TOKEN"}')


print('''
#######################
##### ESTADO INICIAL.##
####################### ''')
snapshot()

print('''
####################################
Filosofo 1. Agarra cubiertos 1 y 2.#
####################################''')
filosofo_1_mode = mode(filosofo_1_agarrar_cubiertos)
filosofo_1_agarrar_cubiertos.fire(filosofo_1_mode)
snapshot()

print('''
####################################
Filosofo 1. Libera cubiertos 1 y 2.#
####################################''')
filosofo_1_mode = mode(filosofo_1_liberar_cubiertos)
filosofo_1_liberar_cubiertos.fire(filosofo_1_mode)
snapshot()

print('''
####################################
Filosofo 2. Agarra cubiertos 2 y 3..#
####################################''')
filosofo_2_mode = mode(filosofo_2_agarrar_cubiertos)
filosofo_2_agarrar_cubiertos.fire(filosofo_2_mode)
snapshot()

print('''
####################################
Filosofo 2. Libera cubiertos 2 y 3..#
####################################''')
filosofo_2_mode = mode(filosofo_2_liberar_cubiertos)
filosofo_2_liberar_cubiertos.fire(filosofo_2_mode)
snapshot()

print('''
####################################
Filosofo 1. Agarra cubiertos 1 y 2.#
####################################''')
print("Filosofo 1. Agarra cubiertos 1 y 2. ")
filosofo_1_mode = mode(filosofo_1_agarrar_cubiertos)
filosofo_1_agarrar_cubiertos.fire(filosofo_1_mode)
snapshot()

print('''
#################################################
Filosofo 2. Intenta agarrar cubiertos 2 y 3.    #
El cubierto 2 esta ocupado por el Filosofo 1    #
#################################################''')
try:
    filosofo_2_mode = mode(filosofo_2_agarrar_cubiertos)
    filosofo_2_agarrar_cubiertos.fire(filosofo_2_mode)
except IndexError:
    print('\n')
    print("Cubierto no disponible")
    print('\n')
snapshot()
