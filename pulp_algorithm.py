from ortools.linear_solver import pywraplp
from data_processing import DataProcessing

class PulpAlgorithm:
    def __init__(self, dp: DataProcessing):
        # Attribute von DataProcessing zuweisen
        self.current_user_id = dp.current_user_id
        self.user_availability = dp.user_availability
        self.opening_hours = dp.opening_hours
        self.laden_oeffnet = dp.laden_oeffnet
        self.laden_schliesst = dp.laden_schliesst
        self.binary_availability = dp.binary_availability

    def run(self):
        self.algorithm()

    def algorithm(self):
        mitarbeiter = [f"MA{i+1}" for i in range(len(self.binary_availability))]

        verfügbarkeit = {}
        for i, (user_id, availabilities) in enumerate(self.binary_availability.items()):
            # Nehmen wir an, dass wir uns nur für die Verfügbarkeit am ersten Tag interessieren
            date, binary_list = availabilities[0]
            verfügbarkeit[mitarbeiter[i]] = binary_list

        kosten = {ma: 20 for ma in mitarbeiter}  # Kosten pro Stunde
        max_zeit = {ma: 8 for ma in mitarbeiter}  # Maximale Arbeitszeit pro Tag
        min_anwesend = [1, 1, 1, 1]  # Mindestanzahl an Mitarbeitern pro Stunde

        # Problem
        solver = pywraplp.Solver.CreateSolver('GLOP')

        # Entscheidungsvariablen
        x = {}
        for i in mitarbeiter:
            for j in range(4):
               x[i, j] = solver.IntVar(0, 1, 'x[%s, %s]' % (i, j))


        # Zielfunktion
        solver.Minimize(solver.Sum([kosten[i] * x[i, j] for i in mitarbeiter for j in range(4)]))

        # Beschränkungen
        for i in mitarbeiter:
            solver.Add(solver.Sum([x[i, j] for j in range(4)]) <= max_zeit[i])
            for j in range(4):
                solver.Add(x[i, j] <= verfügbarkeit[i][j])

        for j in range(4):
            solver.Add(solver.Sum([x[i, j] for i in mitarbeiter]) >= min_anwesend[j])

        # Problem lösen
        status = solver.Solve()

        # Ergebnisse ausgeben
        if status == pywraplp.Solver.OPTIMAL:
            mitarbeiter_arbeitszeiten = {}
            for i in mitarbeiter:
                mitarbeiter_arbeitszeiten[i] = []
                for j in range(4):
                    mitarbeiter_arbeitszeiten[i].append(int(x[i, j].solution_value()))
            print(mitarbeiter_arbeitszeiten)
        else:
            print('Das Problem konnte nicht optimal gelöst werden.')
        

