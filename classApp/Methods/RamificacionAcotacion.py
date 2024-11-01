# Importar la biblioteca de PuLP
from pulp import LpMaximize, LpProblem, LpVariable, LpStatus, PULP_CBC_CMD, LpMinimize

class RamificacionAcotacion:
    _resultTxt:str
    def __init__(self, value1:int=0, value2:int=0,res1:int=0, res2:int=0, valorxRes1:int=0,valorxRes2:int=0, valoryRes1:int=0, valoryRes2:int=0,type:str="max") -> None:
        self.value1 = value1
        self.value2 = value2
        self.res1 = res1
        self.res2 = res2
        self.valorXre1= valorxRes1
        self.valorXre2= valorxRes2
        self.valorYre1= valoryRes1
        self.valorYre2= valoryRes2
        self.type = type

    def pre_solve(self) -> None:
        
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
        self.prob += self.valorXre1 * self.x +  self.valorYre1 * self.y <= self.res1, "Restriccion_1"
        self.prob += self.valorXre2 * self.x +  self.valorYre2 * self.y <= self.res2, "Restriccion_2"

    def solve(self) -> None:
        # Resolver el problema
        self.prob.solve(PULP_CBC_CMD(msg=True))

    def result(self) -> None:
        # Mostrar el estado de la solución
        print(f"Estado de la solución: {LpStatus[self.prob.status]}")

        # Mostrar los valores óptimos de las variables
        print(f"x = {self.x.varValue}")
        print(f"y = {self.y.varValue}")

        # Mostrar el valor óptimo de la función objetivo
        print(f"Valor óptimo de Z = {self.prob.objective.value()}")
        str_list =''
        list_str =[]
        print("\nRamificaciones:")
        for var in self.prob.variables():
            if var.cat == 'Integer':
                list_str.append(f"{var.name} = {var.varValue}, Ramificación: {'Toma' if var.varValue > 0 else 'No toma'}")

        for i in list_str:
            str_list += f'{i} \n'
        
        self._resultTxt=f"""Estado de la solución: {LpStatus[self.prob.status]}
    x = {self.x.varValue}
    y = {self.y.varValue}
Valor óptimo de Z = {self.prob.objective.value()}
Ramificaciones:
{str_list}
        """

    def set_atr(self, value1:int, value2:int,res1:int, res2:int,type:str,valorxRes1:int,valorxRes2:int, valoryRes1:int, valoryRes2:int) -> None:
        self.value1 = value1
        self.value2 = value2
        self.res1 = res1
        self.res2 = res2
        self.type = type
        self.valorXre1= valorxRes1
        self.valorXre2= valorxRes2
        self.valorYre1= valoryRes1
        self.valorYre2= valoryRes2
        self.pre_solve()

    def getResult(self) -> None:
        return self._resultTxt

if __name__ == "__main__":
    test = RamificacionAcotacion(5, 4, 6, 4, "max")
    test.solve()
    test.result()