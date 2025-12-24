def generate_explanations(df, vars):
    out = []
    for i in df.index:
        for v in vars:
            if vars[v][i].solution_value() > 0:
                out.append({
                    "Entity": df.loc[i,"Supplier"],
                    "Variable: x = number of order blocks": v,
                    "Reason": "Selected under optimal feasible constraint set"
                })
    return out