import pulp
import numpy as np

# Función para agregar un corte de Gomory
def agregar_corte(prob, vars, tableau):
    filas, columnas = tableau.shape
    for i in range(filas):
        # Buscar filas fraccionarias (donde el término independiente no sea entero)
        if not np.isclose(tableau[i, -1], np.floor(tableau[i, -1])):
            # Generar un corte basado en la parte fraccionaria
            corte = np.floor(tableau[i, -1]) - tableau[i, -1]
            for j in range(columnas - 1):
                if not np.isclose(tableau[i, j], 0):
                    corte += (tableau[i, j] - np.floor(tableau[i, j])) * vars[j]

            # Agregar el corte como una restricción adicional
            prob += corte <= 0, f"Corte_Gomory_{i}"
            return True  # Se agregó un corte
    return False  # No se encontraron cortes

# Crear el problema de maximización
prob = pulp.LpProblem("Ejemplo_Cortes_Gomory", pulp.LpMaximize)

# Definir variables (continuas para la relajación inicial)
x1 = pulp.LpVariable("x1", lowBound=0)
x2 = pulp.LpVariable("x2", lowBound=0)

# Definir la función objetivo
prob += 5 * x1 + 4 * x2, "Función Objetivo"

# Definir las restricciones
prob += 6 * x1 + 4 * x2 <= 24, "Restriccion_1"
prob += x1 + 2 * x2 <= 6, "Restriccion_2"
prob += -x1 + x2 <= 1, "Restriccion_3"

# Resolver el problema relajado inicialmente
prob.solve()
print(f"Estado de la solución: {pulp.LpStatus[prob.status]}")
print(f"x1 = {x1.varValue}, x2 = {x2.varValue}")

# Obtener la tabla simplex (conceptual, usando valores directos)
# En un caso real, aquí deberías obtener la tabla de resultados del solucionador LP
tableau = np.array([
    [6, 4, 0, 24],  # Restricción 1
    [1, 2, 0, 6],   # Restricción 2
    [-1, 1, 0, 1]   # Restricción 3
])

# Aplicar el algoritmo de cortes iterativamente
while True:
    # Agregar un corte de Gomory si se encuentra
    if not agregar_corte(prob, [x1, x2], tableau):
        break
    # Resolver el problema con los nuevos cortes
    prob.solve()
    print(f"Estado de la solución: {pulp.LpStatus[prob.status]}")
    print(f"x1 = {x1.varValue}, x2 = {x2.varValue}")

# Mostrar la solución final
print(f"Solución óptima entera: x1 = {x1.varValue}, x2 = {x2.varValue}")
