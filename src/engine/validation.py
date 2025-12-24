def validate_schema(df, config):
    required_cols = set()

    # objective terms
    for t in config["objective"]["terms"]:
        required_cols.add(t["column"])

    # variable bounds
    for v in config["variables"]:
        if isinstance(v.get("upper"), str):
            required_cols |= set(
                k for k in df.columns if k in v["upper"]
            )

    # constraints
    for c in config["constraints"]:
        if "multiplier" in c and c["multiplier"] in df.columns:
            required_cols.add(c["multiplier"])

    missing = required_cols - set(df.columns)
    if missing:
        raise ValueError(
            f"CSV is missing required columns: {sorted(missing)}"
        )
