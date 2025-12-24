from fastapi import FastAPI
import pandas as pd
import yaml
from services.scenario_service import run_scenario

app = FastAPI()

@app.post("/optimize")
def optimize(data: dict):
    df = pd.DataFrame(data["rows"])
    config = yaml.safe_load(open(data["config"]))
    return run_scenario(df, config, data["params"])