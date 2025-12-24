from src.engine.solver import create_solver
from src.engine.variables import create_variables
from src.engine.objective import apply_objective
from src.engine.constraints import apply_constraints
from src.engine.explainability import generate_explanations
from src.engine.validation import validate_schema
from ortools.linear_solver import pywraplp
import streamlit as st
import pandas as pd

def run_scenario(df, config, params):
    validate_schema(df, config)

    solver = create_solver()
    vars = create_variables(solver, df, config["variables"])
    apply_objective(solver, df, vars, config["objective"], params)
    apply_constraints(solver, df, vars, config["constraints"], params)
    status=solver.Solve()

    if 'error' in st.session_state:
        del st.session_state['error']

    if status == pywraplp.Solver.INFEASIBLE:
        print('Problem is infeasible (no valid solution found).')
        st.session_state['error'] = 'Problem is infeasible (no valid solution found).'
    elif status == pywraplp.Solver.UNBOUNDED:
        print('Problem is unbounded.')
        st.session_state['error'] = 'Problem is unbounded.'

    results = []
    for i in df.index:
        qty = vars["x"][i].solution_value() * df.loc[i, "SOQ"]
        if qty > 0:
            results.append({"Supplier": df.loc[i,"Supplier"], "AwardedQty": qty})

    return {"results": pd.DataFrame(results), "explanations": generate_explanations(df, vars)}

def compare_scenarios(df, config, params, param, values):
    rows = []
    for v in values:
        params[param] = v
        r = run_scenario(df, config, params)
        rows.append({"scenario": v, "suppliers": len(r["results"])})
    return pd.DataFrame(rows)