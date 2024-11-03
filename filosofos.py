
from snakes.nets import *
TOKEN_VALUE = 1
TOKEN = Value(TOKEN_VALUE)



n = PetriNet("N")
n.add_place(Place("src", [TOKEN_VALUE]))
n.add_place(Place("tgt", []))
t = Transition("t")
n.add_transition(t)
n.add_input("src", "t", TOKEN)
n.add_output("tgt", "t", TOKEN)

print(n.node())
print(t.modes())
t.fire(t.modes()[0])
print(n.node())

