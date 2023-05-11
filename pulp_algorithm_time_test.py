import pulp
import time
import random

# Anzahl der Mitarbeiter und Tage
num_workers = 2000
num_days = 21

# Zufällige Verfügbarkeit generieren
availability = [[random.choice([True, False]) for _ in range(num_days)] for _ in range(num_workers)]

# Problem erstellen
problem = pulp.LpProblem("worker_scheduling", pulp.LpMinimize)

# Variablen erstellen
x = [[pulp.LpVariable(f"x_{i}_{j}", cat='Binary') if availability[i][j] else 0
      for j in range(num_days)] for i in range(num_workers)]

# Constraints hinzufügen
for i in range(num_workers):
    problem += pulp.lpSum(x[i][j] for j in range(num_days)) <= 5  # Jeder Mitarbeiter arbeitet höchstens 5 Tage

for j in range(num_days):
    problem += pulp.lpSum(x[i][j] if isinstance(x[i][j], pulp.LpVariable) else 0 for i in range(num_workers)) >= 20  # An jedem Tag müssen mindestens 20 Mitarbeiter arbeiten


# Zielfunktion (könnte auf Ihre spezielle Anforderung angepasst werden)
problem += pulp.lpSum(x)

# Constraints (könnten auf Ihre spezielle Anforderung angepasst werden)
for i in range(num_workers):
    problem += pulp.lpSum(x[i][j] for j in range(num_days)) <= 5  # Jeder Mitarbeiter arbeitet höchstens 5 Tage

# Problem lösen und Zeit messen
start_time = time.time()
problem.solve()
end_time = time.time()

# Ausführungszeit ausgeben
print("Execution time: ", end_time - start_time)

# Lösung in Matrixform ausgeben
solution = [[pulp.value(var) if isinstance(var, pulp.LpVariable) else 0 for var in worker] for worker in x]
for row in solution:
    print(row)
