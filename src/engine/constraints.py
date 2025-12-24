def apply_constraints(solver, df, vars, cfg, params):
    for c in cfg:
        if c["type"] == "sum_equals":
            solver.Add(
                sum(vars[c["var"]][i] * df.loc[i, c["multiplier"]] for i in df.index)
                == params[c["value"]]
            )
        elif c["type"] == "sum_le":
            solver.Add(
                sum(vars[c["var"]][i] * df.loc[i, c["multiplier"]] for i in df.index)
                <= params[c["value"]]
            )
        elif c["type"] == "eligibility":
            for i in df.index:
                if not eval(c["condition"], {}, {**df.loc[i].to_dict(), **params}):
                    solver.Add(vars[c["var"]][i] == 0)