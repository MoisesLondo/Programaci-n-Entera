from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, LpMinimize

class Mochila:
    def __init__(self, valores, pesos, capacidad, type) -> None:
        self.valores = valores
        self.pesos = pesos
        self.capacidad = capacidad
        self.num_objetos = len(valores)
        self.variables = self.crear_variables()
        self.definir_problema()
        

        if self.type == "max":
            self.prob = LpProblem("Problema_de_la_Mochila", LpMaximize)
        else:
            self.prob = LpProblem("Problema_de_la_Mochila", LpMinimize)

    def crear_variables(self) -> []:
        return [LpVariable(f"x{i+1}", 0, 1, cat="Integer") for i in range(self.num_objetos)]

    def definir_problema(self) -> None:
        # Función objetivo: maximizar el valor de los objetos seleccionados
        self.prob += lpSum(self.valores[i] * self.variables[i] for i in range(self.num_objetos)), "Valor_Total"
        
        # Restricción: la suma de los pesos de los objetos seleccionados no debe exceder la capacidad
        self.prob += lpSum(self.pesos[i] * self.variables[i] for i in range(self.num_objetos)) <= self.capacidad, "Restriccion_Capacidad"

    def resolver(self) -> None:
        self.prob.solve()

    def mostrar_resultados(self) -> None:
        print(f"Estado de la solución: {LpStatus[self.prob.status]}")
        for i, var in enumerate(self.variables):
            print(f"x{i+1} (objeto {i+1}): {var.varValue}")
        print(f"Valor total máximo: {self.prob.objective.value()}")


valores = [15, 25, 12, 10]
pesos = [3, 6, 5, 5]
capacidad = 12

# Crear una instancia de ProblemaMochila
mochila = Mochila(valores, pesos, capacidad)

# Resolver el problema
mochila.resolver()

# Mostrar los resultados
print("\nResultados:")
mochila.mostrar_resultados()