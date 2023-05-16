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

    def run(self):
        self.algorithm()

    def algorithm(self):
        mitarbeiter = [f"MA{i+1}" for i in range(len(self.binary_availability))]

        verfügbarkeit = {}
        for i, (user_id, availabilities) in enumerate(self.binary_availability.items()):
            verfügbarkeit[mitarbeiter[i]] = []
            for day_availability in availabilities:
                date, binary_list = day_availability
                verfügbarkeit[mitarbeiter[i]].append(binary_list)
        
        print(verfügbarkeit)

        kosten = {ma: 20 for ma in mitarbeiter}  # Kosten pro Stunde
        max_zeit = {ma: 5 for ma in mitarbeiter}  # Maximale Arbeitszeit pro Tag

        min_anwesend = [1] * 24  # Mindestanzahl an Mitarbeitern pro Stunde

        # Problem 
        # GLOP = Simplex Verfahren
        # CBC =  branch-and-bound- und branch-and-cut-Verfahren
        # SCIP = Framework für die Lösung gemischt-ganzzahliger Programmierungsproblem
        # GLPK = Vielzahl von Algorithmen, einschließlich des Simplex-Verfahrens und des branch-and-bound-Verfahrens
        solver = pywraplp.Solver.CreateSolver('SCIP')


        # Entscheidungsvariablen ------------------------------------------------------------------------------------------------
        x = {}
        for i in mitarbeiter:
            for j in range(7):  # Für jeden Tag der Woche
                for k in range(len(verfügbarkeit[i][j])):  # Für jede Stunde des Tages, an dem das Café geöffnet ist
                    x[i, j, k] = solver.IntVar(0, 1, 'x[%s, %s, %s]' % (i, j, k))

        print(x)

        # Zielfunktion ----------------------------------------------------------------------------------------------------------
        objective = solver.Objective()
        for i in mitarbeiter:
            for j in range(7):
                for k in range(len(verfügbarkeit[i][j])):
                    objective.SetCoefficient(x[i, j, k], kosten[i])
        objective.SetMinimization()


        # Beschränkungen --------------------------------------------------------------------------------------------------------
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

        # Constraint makes sure that the user works at least 4 hours in a row - doesn't work yet
        for i in mitarbeiter:
            for j in range(7):
                for k in range(len(verfügbarkeit[i][j]) - 4):
                    # Check if the Mitarbeiter is planned at the current hour and the next 3 hours
                    is_planned = [x[i, j, k + n] for n in range(4)]
                    # Add a constraint to ensure at least one of the four hours is planned
                    solver.Add(solver.Sum(is_planned) >= 0)


        # Problem lösen ---------------------------------------------------------------------------------------------------------
        status = solver.Solve()

        # Ergebnisse ausgeben
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

