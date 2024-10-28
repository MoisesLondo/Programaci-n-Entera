# Importar la biblioteca de PuLP
from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, PULP_CBC_CMD

# Crear un problema de maximización
prob = LpProblem("Ejemplo_Programacion_Entera", LpMaximize)

# Definir variables (enteras)
x = LpVariable('x', lowBound=0, cat='Integer')
y = LpVariable('y', lowBound=0, cat='Integer')

# Definir la función objetivo
prob += 3 * x + 2 * y, "Función Objetivo"

# Definir las restricciones
prob += x + y <= 4, "Restriccion_1"
prob += x - y >= 0, "Restriccion_2"

# Resolver el problema utilizando el solucionador por defecto (CBC)
prob.solve(PULP_CBC_CMD(msg=True))

# Mostrar el estado de la solución
print(f"Estado de la solución: {LpStatus[prob.status]}")

# Mostrar los valores óptimos de las variables
print(f"x = {x.varValue}")
print(f"y = {y.varValue}")

# Mostrar el valor óptimo de la función objetivo
print(f"Valor óptimo de Z = {prob.objective.value()}")
