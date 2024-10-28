from pulp import LpMinimize, LpProblem, LpVariable, LpStatus

# Crear un problema de minimización
prob = LpProblem("Programacion_Binaria", LpMinimize)

# Definir las variables de decisión (binarias)
x = LpVariable('x', cat='Binary')
y = LpVariable('y', cat='Binary')
z = LpVariable('z', cat='Binary')

# Definir la función objetivo
prob += 2 * x + 3 * y + 4 * z, "Función Objetivo"

# Definir las restricciones
prob += x + y >= 1, "Restriccion_1"
prob += y + z >= 1, "Restriccion_2"

# Resolver el problema
prob.solve()

# Mostrar el estado de la solución
print(f"Estado de la solución: {LpStatus[prob.status]}")

# Mostrar los valores óptimos de las variables
print(f"x = {x.varValue}")
print(f"y = {y.varValue}")
print(f"z = {z.varValue}")

# Mostrar el valor óptimo de la función objetivo
print(f"Valor óptimo de Z = {prob.objective.value()}")
