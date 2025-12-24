def create_variables(solver, df, var_cfg):
    vars = {}
    for v in var_cfg:
        if v["type"] == "integer":
            vars[v["name"]] = {
                i: solver.IntVar(
                    v["lower"],
                    eval(v["upper"], {}, df.loc[i].to_dict()),
                    f"{v['name']}_{i}"
                ) for i in df.index
            }
        elif v["type"] == "binary":
            vars[v["name"]] = {i: solver.BoolVar(f"{v['name']}_{i}") for i in df.index}
    return vars