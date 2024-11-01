from pulp import LpMinimize, LpProblem, LpVariable, LpStatus

class BinariaEstaciones:
    def __init__(self) -> None:
        """Inicialización de la clase sin requerir parámetros."""
        self.num_ciudades = 0
        self.distancias = []
        self.tiempo_max = 40  # Valor predeterminado
        self._resultTxt = ""
        self.prob = None

    def set_parameters(self, num_ciudades: int, distancias: list, tiempo_max: int = 40) -> None:
        """
        Configura los parámetros para el problema de ubicación de estaciones.
        :param num_ciudades: Número total de ciudades.
        :param distancias: Matriz de distancias entre ciudades.
        :param tiempo_max: Tiempo máximo permitido para cubrir cada ciudad.
        """
        self.num_ciudades = num_ciudades
        self.distancias = distancias
        self.tiempo_max = tiempo_max
        self.prob = LpProblem("Ubicacion_Estaciones", LpMinimize)

    def pre_solve(self) -> None:
        if self.prob is None:
            raise ValueError("Parámetros no configurados. Use set_parameters() antes de resolver.")

        # Definir variables de decisión (si se coloca una estación en cada ciudad i)
        self.x = [LpVariable(f'x_{i}', cat='Binary') for i in range(self.num_ciudades)]
        
        # Definir la función objetivo (minimizar la cantidad de estaciones)
        self.prob += sum(self.x), "Minimizar estaciones"
        
        # Definir restricciones de cobertura para cada ciudad
        for j in range(self.num_ciudades):
            # Asegurar que cada ciudad j tenga al menos una estación a menos de 40 minutos
            self.prob += sum(self.x[i] for i in range(self.num_ciudades) if self.distancias[i][j] <= self.tiempo_max) >= 1, f"Restriccion_cobertura_{j}"

    def solve(self) -> None:
        # Resolver el problema
        if self.prob is not None:
            self.prob.solve()

    def result(self) -> None:
        # Mostrar el estado de la solución
        if self.prob is None:
            self._resultTxt = "No se ha configurado ni resuelto el problema."
            return

        self._resultTxt = f"Estado de la solución: {LpStatus[self.prob.status]}\n"
        print(self._resultTxt)

        # Mostrar las ciudades en las que se colocan estaciones
        estaciones = []
        for i in range(self.num_ciudades):
            estaciones.append(f"Ciudad {i}: {'Sí' if self.x[i].varValue == 1 else 'No'}")
        
        # Guardar el resultado en _resultTxt
        self._resultTxt += f"Cantidad mínima de estaciones: {self.prob.objective.value()}\nEstaciones ubicadas:\n" + "\n".join(estaciones)

    def getResult(self) -> str:
        return self._resultTxt
