from ortools.linear_solver import pywraplp
from data_processing import DataProcessing

class ORAlgorithm:
    def __init__(self, dp: DataProcessing):
        self.current_user_id = dp.current_user_id
        self.user_availability = dp.user_availability
        self.opening_hours = dp.opening_hours
        self.laden_oeffnet = dp.laden_oeffnet
        self.laden_schliesst = dp.laden_schliesst
        self.binary_availability = dp.binary_availability
        self.time_req = dp.time_req

    def run(self):
        self.algorithm()

    def algorithm(self):
        # List-Comprehensions
        mitarbeiter = [f"MA{i+1}" for i in range(len(self.binary_availability))]

        # Aus dem binary_availability dict. die Verfügbarkeits-Informationen ziehen
        verfügbarkeit = {}
        for i, (user_id, availabilities) in enumerate(self.binary_availability.items()):
            verfügbarkeit[mitarbeiter[i]] = []
            for day_availability in availabilities:
                date, binary_list = day_availability
                verfügbarkeit[mitarbeiter[i]].append(binary_list)

        # Kosten für jeden MA noch gleich, ebenfalls die max Zeit bei allen gleich
        kosten = {ma: 20 for ma in mitarbeiter}  # Kosten pro Stunde
        max_zeit = {ma: 5 for ma in mitarbeiter}  # Maximale Arbeitszeit pro Tag

        # Diese Daten werden später noch aus der Datenbank gezogen
        min_anwesend = [1] * 24  # Mindestanzahl an Mitarbeitern pro Stunde

        # Problem 
        # GLOP = Simplex Verfahren
        # CBC =  branch-and-bound- und branch-and-cut-Verfahren
        # SCIP = Framework für die Lösung gemischt-ganzzahliger Programmierungsproblem
        # GLPK = Vielzahl von Algorithmen, einschließlich des Simplex-Verfahrens und des branch-and-bound-Verfahrens
        solver = pywraplp.Solver.CreateSolver('SCIP')


        # Entscheidungsvariablen ------------------------------------------------------------------------------------------------

        # solver.NumVar() <-- kontinuierliche Variabeln
        # solver.BoolVar() <-- boolesche Variabeln
        # solver.IntVar() <-- Int Variabeln
        x = {}
        for i in mitarbeiter:
            for j in range(7):  # Für jeden Tag der Woche
                for k in range(len(verfügbarkeit[i][j])):  # Für jede Stunde des Tages, an dem das Café geöffnet ist
                    x[i, j, k] = solver.IntVar(0, 1, f'x[{i}, {j}, {k}]') # Variabeln können nur die Werte 0 oder 1 annehmen

        print(x)

        # Zielfunktion ----------------------------------------------------------------------------------------------------------
        objective = solver.Objective()
        for i in mitarbeiter:
            for j in range(7):
                for k in range(len(verfügbarkeit[i][j])):
                    # Die Kosten werden multipliziert
                    objective.SetCoefficient(x[i, j, k], kosten[i])
        # Es wird veruscht, eine Kombination von Werten für die x[i, j, k] zu finden, die die Summe kosten[i]*x[i, j, k] minimiert            
        objective.SetMinimization()


        # Beschränkungen --------------------------------------------------------------------------------------------------------
        # (Die solver.Add() Funktion nimmt eine Bedingung als Argument und fügt sie dem Optimierungsproblem hinzu.)

        # MA darf nur eingeteilt werden, sofern er auch verfügbar ist.
        for i in mitarbeiter:
            for j in range(7):
                for k in range(len(verfügbarkeit[i][j])):
                    solver.Add(x[i, j, k] <= verfügbarkeit[i][j][k])


        # Mindestanzahl MA zu jeder Stunde an jedem Tag anwesend 
        for j in range(7):
            for k in range(len(verfügbarkeit[mitarbeiter[0]][j])):  # Wir nehmen an, dass alle Mitarbeiter die gleichen Öffnungszeiten haben
                solver.Add(solver.Sum([x[i, j, k] for i in mitarbeiter]) >= min_anwesend[k])


        # Constraint only allows solutions where the max planned summed hour is 25
        total_hours = {ma: solver.Sum([x[ma, j, k] for j in range(7) for k in range(len(verfügbarkeit[ma][j]))]) for ma in mitarbeiter}
        for ma in mitarbeiter:
            solver.Add(total_hours[ma] <= 25)


        # Constraint makes sure that the user works at least 3 hours in a row - doesn't work yet
        for i in mitarbeiter:
            for j in range(7):
                for k in range(len(verfügbarkeit[i][j]) - 3):
                    # Check if the Mitarbeiter is planned at the current hour and the next 2 hours
                    is_planned = [x[i, j, k + n] for n in range(3)]
                    # Add a constraint to ensure at least one of the tree hours is planned
                    solver.Add(solver.Sum(is_planned) >= 3)


        # Problem lösen ---------------------------------------------------------------------------------------------------------
        status = solver.Solve()



        # Ergebnisse ausgeben ----------------------------------------------------------------------------------------------------
        if status == pywraplp.Solver.OPTIMAL:
            mitarbeiter_arbeitszeiten = {}
            for i in mitarbeiter:
                mitarbeiter_arbeitszeiten[i] = []
                for j in range(7):
                    arbeitszeit_pro_tag = []
                    for k in range(len(verfügbarkeit[i][j])):
                        arbeitszeit_pro_tag.append(int(x[i, j, k].solution_value()))
                    mitarbeiter_arbeitszeiten[i].append(arbeitszeit_pro_tag)
            print(mitarbeiter_arbeitszeiten)
        else:
            print('Das Problem konnte nicht optimal gelöst werden.')

