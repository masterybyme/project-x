from pulp import *
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
        prob = LpProblem("Mitarbeiterplanung", LpMinimize)
        print("1. Problem: ", prob)

        # Entscheidungsvariablen
        x = LpVariable.dicts("Arbeitszeit", [(i, j) for i in mitarbeiter for j in range(4)], 0, 1, LpInteger)
        print("2. x: ", x)

        # Zielfunktion
        prob += lpSum([kosten[i] * lpSum([x[i, j] for j in range(4)]) for i in mitarbeiter])
        print("3. Problem: ", prob)

        # Beschränkungen
        for i in mitarbeiter:
            prob += lpSum([x[i, j] for j in range(4)]) <= max_zeit[i], f"MaxArbeitszeit_{i}"
            for j in range(4):
                prob += x[i, j] <= verfügbarkeit[i][j], f"Verfügbarkeit_{i}_{j}"

        for j in range(4):
            prob += lpSum([x[i, j] for i in mitarbeiter]) >= min_anwesend[j], f"MinAnwesend_{j}"

        print("4. Problem: ", prob)

        # Problem lösen
        prob.solve()

        # Ergebnisse ausgeben
        mitarbeiter_arbeitszeiten = {}
        for i in mitarbeiter:
            mitarbeiter_arbeitszeiten[i] = []
            for j in range(4):
                mitarbeiter_arbeitszeiten[i].append(int(value(x[i, j])))

        print(mitarbeiter_arbeitszeiten)





