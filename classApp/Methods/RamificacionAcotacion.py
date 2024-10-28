# Importar la biblioteca de PuLP
from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, PULP_CBC_CMD, LpMinimize

class RamificacionAcotacion:
    def __init__(self, value1, value2,res1, res2, type):
        self.value1 = value1
        self.value2 = value2
        self.res1 = res1
        self.res2 = res2
        self.type = type

        if self.type == "max":
            self.prob = LpProblem("Ejemplo_Programacion_Entera", LpMaximize)
        else:
            self.prob = LpProblem("Ejemplo_Programacion_Entera", LpMinimize)

        # Definir las variables de decisión (binarias)
        self.x = LpVariable('x', lowBound=0, cat='Integer')
        self.y = LpVariable('y', lowBound=0, cat='Integer')

        # Definir la función objetivo
        self.prob += self.value1 * self.x + self.value2 * self.y, "Función Objetivo"

        # Definir las restricciones
        self.prob += self.x + self.y <= self.res1, "Restriccion_1"
        self.prob += self.x - self.y >= self.res2, "Restriccion_2"

    def solve(self):
        # Resolver el problema
        self.prob.solve(PULP_CBC_CMD(msg=True))

    def result(self):
        # Mostrar el estado de la solución
        print(f"Estado de la solución: {LpStatus[self.prob.status]}")

        # Mostrar los valores óptimos de las variables
        print(f"x = {self.x.varValue}")
        print(f"y = {self.y.varValue}")

        # Mostrar el valor óptimo de la función objetivo
        print(f"Valor óptimo de Z = {self.prob.objective.value()}")

test = RamificacionAcotacion(5, 4, 6, 4, "max")
test.solve()
test.result()