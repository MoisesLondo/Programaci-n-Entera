from pulp import LpMaximize, LpProblem, LpVariable, lpSum, LpStatus, LpMinimize

class Mochila:

    _resultTxt:str
    def __init__(self, valores:int=[], pesos:int=[], capacidad:int=0, type:str="max") -> None:
        self.valores = valores
        self.pesos = pesos
        self.capacidad = capacidad
        self.type= type

    def pre_solve(self):
        if self.type == "max":
            self.problema_mochila = LpProblem("Problema_de_la_Mochila", LpMaximize)
        else:
            self.problema_mochila = LpProblem("Problema_de_la_Mochila", LpMinimize)

        self.n = len(self.pesos)  # Número de objetos
        self.x = [LpVariable(f"x_{i+1}", cat='Binary') for i in range(self.n)]
        print("Variables de decisión definidas (0 = no seleccionado, 1 = seleccionado):")
        for i in range(self.n):
            print(f"x_{i+1} -> Objeto {i+1}")
        self.definir_problema()


    def definir_problema(self) -> None:
        self.problema_mochila += sum(self.valores[i] * self.x[i] for i in range(self.n)), "Valor_total"
        self.problema_mochila += sum(self.pesos[i] * self.x[i] for i in range(self.n)) <= self.capacidad, "Capacidad_mochila"


    def resolver(self) -> None:
        self.problema_mochila.solve()

    def mostrar_resultados(self) -> None:
        print(f"Estado de la solución: {LpStatus[self.problema_mochila.status]}")
        list_str=[]
        for i in range(self.n):
            list_str.append(f"Objeto {i+1}: {'Seleccionado' if self.x[i].varValue == 1 else 'No seleccionado'} (Peso: {self.pesos[i]}, Valor: {self.valores[i]})")

        # Paso 7: Calcular y mostrar el valor total en la mochila y el peso total
        valor_total = sum(self.valores[i] * self.x[i].varValue for i in range(self.n))
        peso_total = sum(self.pesos[i] * self.x[i].varValue for i in range(self.n))
        print(f"Valor total en la mochila: {valor_total}")
        print(f"Peso total en la mochila: {peso_total}")
        str_list = ''
        for i in list_str:
            print(i)
            str_list += f'{i} \n'

        self._resultTxt=f"""Estado de la solución: {LpStatus[self.problema_mochila.status]}
{str_list}
Valor total en la mochila: {valor_total}
Peso total en la mochila: {peso_total}
        """

    def set_atr(self, valores:int=[], pesos:int=[], capacidad:int=0, type:str="max") -> None:
        self.valores = valores
        self.pesos = pesos
        self.capacidad = capacidad
        self.type= type
        self.pre_solve()

    def getResult(self) -> None:
        return self._resultTxt


if __name__ == "__main__":
    valores = [15, 25, 12, 10]
    pesos = [3, 6, 5, 5]
    capacidad = 12

    # Crear una instancia de ProblemaMochila
    mochila = Mochila()
    mochila.set_atr(valores, pesos, capacidad)

    # Resolver el problema
    mochila.resolver()

    # Mostrar los resultados
    print("\nResultados:")
    mochila.mostrar_resultados()