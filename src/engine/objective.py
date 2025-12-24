from src.engine.expression import resolve_weight, resolve_scale

def apply_objective(solver, df, vars, obj_cfg, params):
    scale = resolve_scale(obj_cfg.get("scale"), df, params)

    solver.Maximize(
        solver.Sum(
            (
                sum(
                    resolve_weight(term["weight"], params)
                    * df.loc[i, term["column"]]
                    for term in obj_cfg["terms"]
                )
                * (df.loc[i, scale] if isinstance(scale, str) else scale)
                * vars[obj_cfg["var"]][i]
            )
            for i in df.index
        )
    )

