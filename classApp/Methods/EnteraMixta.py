from pulp import LpMaximize, LpProblem, LpVariable, LpStatus

# Crear un problema de maximización
prob = LpProblem("Programacion_Entera_Mixta", LpMaximize)

# Definir las variables de decisión (mixtas)
x = LpVariable('x', lowBound=0, cat='Integer')  # Entera
y = LpVariable('y', lowBound=0, cat='Continuous')  # Continua

# Definir la función objetivo
prob += 4 * x + 3 * y, "Función Objetivo"

# Definir las restricciones
prob += 3 * x + 2 * y <= 18, "Restriccion_1"

# Resolver el problema
prob.solve()

# Mostrar el estado de la solución
print(f"Estado de la solución: {LpStatus[prob.status]}")

# Mostrar los valores óptimos de las variables
print(f"x = {x.varValue}")
print(f"y = {y.varValue}")

# Mostrar el valor óptimo de la función objetivo
print(f"Valor óptimo de Z = {prob.objective.value()}")
