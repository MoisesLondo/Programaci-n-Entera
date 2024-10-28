from pulp import LpMaximize, LpProblem, LpVariable, LpStatus

# Crear un problema de maximización
prob = LpProblem("Programacion_Entera_Pura", LpMaximize)

# Definir las variables de decisión (enteras)
x = LpVariable('x', lowBound=0, cat='Integer')
y = LpVariable('y', lowBound=0, cat='Integer')

# Definir la función objetivo
prob += 5 * x + 3 * y, "Función Objetivo"

# Definir las restricciones
prob += 2 * x + 3 * y <= 12, "Restriccion_1"
prob += 2 * x + y <= 8, "Restriccion_2"

# Resolver el problema
prob.solve()

# Mostrar el estado de la solución
print(f"Estado de la solución: {LpStatus[prob.status]}")

# Mostrar los valores óptimos de las variables
print(f"x = {x.varValue}")
print(f"y = {y.varValue}")

# Mostrar el valor óptimo de la función objetivo
print(f"Valor óptimo de Z = {prob.objective.value()}")
