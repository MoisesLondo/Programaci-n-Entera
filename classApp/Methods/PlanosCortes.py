import pulp
import numpy as np

class PlanosCortes:
    def __init__(self, obj_coef, constraints, constraint_values) -> None:
        # Initialize attributes
        self.obj_coef = obj_coef  # Coefficients for the objective function
        self.constraints = constraints  # Coefficients for each constraint
        self.constraint_values = constraint_values  # RHS values for each constraint
        self.prob = pulp.LpProblem("Ejemplo_Cortes_Gomory", pulp.LpMaximize)

        # Define variables (continuous for initial relaxation)
        self.vars = [pulp.LpVariable(f"x{i+1}", lowBound=0) for i in range(len(obj_coef))]

        # Set up the objective function
        self.prob += pulp.lpSum([self.obj_coef[i] * self.vars[i] for i in range(len(self.vars))]), "Función Objetivo"

        # Add constraints to the problem
        for i, (coef, val) in enumerate(zip(self.constraints, self.constraint_values)):
            self.prob += (pulp.lpSum([coef[j] * self.vars[j] for j in range(len(self.vars))]) <= val), f"Restriccion_{i+1}"

        # Initialize solution status and tableau (for demonstration purposes, it's predefined here)
        self.tableau = np.array([coef + [val] for coef, val in zip(self.constraints, self.constraint_values)])
        self.solution_status = None
        self.optimal_values = {}

    def agregar_corte(self) -> bool:
        """Adds a Gomory cut based on the current tableau."""
        filas, columnas = self.tableau.shape
        for i in range(filas):
            # Look for fractional rows where the independent term is not integer
            if not np.isclose(self.tableau[i, -1], np.floor(self.tableau[i, -1])):
                corte = np.floor(self.tableau[i, -1]) - self.tableau[i, -1]
                for j in range(columnas - 1):
                    if not np.isclose(self.tableau[i, j], 0):
                        corte += (self.tableau[i, j] - np.floor(self.tableau[i, j])) * self.vars[j]

                # Add cut as an additional constraint
                self.prob += corte <= 0, f"Corte_Gomory_{i}"
                return True  # Cut added
        return False  # No fractional cuts found

    def solve(self) -> None:
        """Iteratively solves the problem by adding Gomory cuts."""
        while True:
            # Solve the relaxed problem
            self.prob.solve()
            self.solution_status = pulp.LpStatus[self.prob.status]
            self.optimal_values = {v.name: v.varValue for v in self.vars}

            # Add Gomory cuts iteratively
            if not self.agregar_corte():
                break  # Stop if no new cuts are found

    def result(self) -> None:
        """Prints the final integer optimal solution."""
        print(f"Estado de la solución: {self.solution_status}")
        for var_name, var_value in self.optimal_values.items():
            print(f"{var_name} = {var_value}")
        print(f"Valor óptimo de Z = {self.prob.objective.value()}")
        
        self._resultTxt = f"Estado de la solución: {self.solution_status}\n"
        for var_name, var_value in self.optimal_values.items():
            self._resultTxt += f"{var_name} = {var_value}\n"
        self._resultTxt += f"Valor óptimo de Z = {self.prob.objective.value()}"
    
    def set_atr(self, obj_coef:int=[], constraints:int=[], constraint_values:int=[]) -> None:
        self.obj_coef = obj_coef
        self.constraints = constraints
        self.constraint_values = constraint_values

    def getResult(self) -> str:
        """Returns the final integer optimal solution as a string."""
        return self._resultTxt

