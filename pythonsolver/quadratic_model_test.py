import dimod

qm = dimod.QuadraticModel()
qm.add_variable('BINARY', "x")
qm.add_variable('BINARY', "y")

qm.add_linear("x", 5)
qm.add_linear("y", 2)
print(qm.linear["x"])
