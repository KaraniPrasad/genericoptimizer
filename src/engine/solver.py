from ortools.linear_solver import pywraplp

def create_solver():
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        raise RuntimeError("SCIP solver unavailable")
    return solver