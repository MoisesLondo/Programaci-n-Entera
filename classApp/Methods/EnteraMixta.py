from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, LpMinimize

class EnteraMixta:
    def __init__(self, value1, value2, valueRes1, valueRes2, res, type):
        self.value1 = value1
        self.value2 = value2
        self.valueRes1 = valueRes1
        self.valueRes2 = valueRes2
        self.res = res
        self.type = type

        if self.type == "max":
            self.prob = LpProblem("Programacion_Entera_Mixta", LpMaximize)
        else:
            self.prob = LpProblem("Programacion_Entera_Mixta", LpMinimize)

        # Definir las variables de decisión (mixtas)
        self.x = LpVariable('x', lowBound=0, cat='Integer')
        self.y = LpVariable('y', lowBound=0, cat='Continuous')

        # Definir la función objetivo
        self.prob += self.value1 * self.x + self.value2 * self.y, "Función Objetivo"

        # Definir las restricciones
        self.prob += self.valueRes1 * self.x + self.valueRes2 * self.y <= self.res, "Restriccion_1"

    def solve(self):
        # Resolver el problema
        self.prob.solve()

    def result(self):
        # Mostrar el estado de la solución
        print(f"Estado de la solución: {LpStatus[self.prob.status]}")

        # Mostrar los valores óptimos de las variables
        print(f"x = {self.x.varValue}")
        print(f"y = {self.y.varValue}")

        # Mostrar el valor óptimo de la función objetivo
        print(f"Valor óptimo de Z = {self.prob.objective.value()}")