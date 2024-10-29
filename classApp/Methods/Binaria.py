from pulp import LpMinimize, LpProblem, LpVariable, LpStatus, LpMaximize


class Binaria:
    def __init__(self, value1, value2, value3, res1, res2, type) -> None:
        self.value1 = value1
        self.value2 = value2
        self.value3 = value3
        self.res1 = res1
        self.res2 = res2
        self.type = type

        if self.type == "max":
            self.prob = LpProblem("Programacion_Binaria", LpMaximize)
        else:
            self.prob = LpProblem("Programacion_Binaria", LpMinimize)
    
    # Definir las variables de decisión (binarias)
        self.x = LpVariable('x', cat='Binary')
        self.y = LpVariable('y', cat='Binary')
        self.z = LpVariable('z', cat='Binary')

    # Definir la función objetivo
        self.prob += self.value1 * self.x + self.value2 * self.y + self.value3 * self.z, "Función Objetivo"
    
    # Definir las restricciones
        self.prob += self.x + self.y >= self.res1, "Restriccion_1"
        self.prob += self.y + self.z >= self.res2, "Restriccion_2"

    # Resolver el problema
    def solve(self) -> None:
        self.prob.solve()
    
    def result(self) -> None:
        # Mostrar el estado de la solución
        print(f"Estado de la solución: {LpStatus[self.prob.status]}")

        # Mostrar los valores óptimos de las variables
        print(f"x = {self.x.varValue}")
        print(f"y = {self.y.varValue}")
        print(f"z = {self.z.varValue}")

        # Mostrar el valor óptimo de la función objetivo
        print(f"Valor óptimo de Z = {self.prob.objective.value()}")


    