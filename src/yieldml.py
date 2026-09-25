"""Feature cases and data loading shared by the modelling notebooks."""
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, r2_score

# yield rasters are in bu/ac; 1 bu/ac of wheat = 62.77 kg/ha
Y_MULT = 62.77
TARGET = "yield"

ASP_FIELDS = ["S2", "S4", "S5", "S6", "SB1", "SB4", "SB5", "SB7", "SCD2", "SCD3", "SCD5", "SCD6"]
BAU_FIELDS = ["S3", "S7", "SB3", "SB6", "SCD4", "SCD7"]

# year classes from the 25th/75th percentiles of Oct-Jun precipitation, 1993-2022 (notebook 02)
YEAR_CLASS = {"2019": "Normal", "2020": "Dry", "2021": "Normal",
              "2022": "Dry", "2023": "Wet", "2024": "Normal"}

SOIL = ["Carbon (0-15 cm)", "Carbon (15-30 cm)",
        "Clay (0-15 cm)", "Clay (15-30 cm)", "Clay (30-60 cm)", "Clay (60-90 cm)", "Clay (90-120 cm)",
        "Sand (0-15 cm)", "Sand (15-30 cm)", "Sand (30-60 cm)", "Sand (60-90 cm)", "Sand (90-120 cm)",
        "Silt (0-15 cm)", "Silt (15-30 cm)", "Silt (30-60 cm)", "Silt (60-90 cm)", "Silt (90-120 cm)",
        "OM (0-15 cm)", "OM (15-30 cm)", "pH (0-15 cm)", "pH (15-30 cm)"]
TOPO_N = ["Elevation", "Aspect", "Curvature", "Slope", "TPI", "Nitrogen"]
SM = ["SM 30 cm", "SM 60 cm", "SM 90 cm"]

# the column order is kept exactly as in the runs behind the paper
CASES = {
    "Case1": SOIL + TOPO_N + ["Precipitation"],
    "Case2": SOIL + TOPO_N + SM,
    "Case3": SOIL + TOPO_N + ["ETa"],
    "Case4": SOIL + TOPO_N + ["Precipitation", "ETa"],
    "Case5": SOIL + TOPO_N + SM + ["Precipitation"],
    "Case6": SOIL + TOPO_N + SM + ["ETa"],
    "Case7": SOIL + TOPO_N + SM + ["ETa", "Precipitation"],
    "Case8": SM + ["ETa", "Precipitation", "Nitrogen", "Elevation", "Aspect", "Curvature", "Slope", "TPI"],
}
CASE_LABELS = {
    "Case1": "Case 1: P", "Case2": "Case 2: SM", "Case3": "Case 3: ETa",
    "Case4": "Case 4: P + ETa", "Case5": "Case 5: P + SM", "Case6": "Case 6: SM + ETa",
    "Case7": "Case 7: P + SM + ETa", "Case8": "Case 8: no soil properties",
}


def load_group(folder):
    """Read every field-year csv in a folder (sorted by name) and add Field, FieldName and Year."""
    frames = []
    for f in sorted(Path(folder).glob("*.csv")):
        df = pd.read_csv(f)
        parts = f.stem.split("_")                       # e.g. S2_2022_Wheat
        df = df.assign(Field=f.stem, FieldName=parts[0], Year=parts[1])
        frames.append(df)
    return pd.concat(frames, ignore_index=True)


def load_all(model_dir="../data/model_input"):
    asp = load_group(Path(model_dir) / "ASP")
    bau = load_group(Path(model_dir) / "BAU")
    return {"ASP": asp, "BAU": bau, "ASP+BAU": pd.concat([asp, bau], ignore_index=True)}


def by_year_class(df, cls):
    """cls is 'All', 'Dry', 'Normal' or 'Wet'."""
    if cls == "All":
        return df
    years = [y for y, c in YEAR_CLASS.items() if c == cls]
    return df[df["Year"].isin(years)].copy()


def scores(y_true, y_pred):
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    return {"R2": r2_score(y_true, y_pred), "RMSE": rmse, "RRMSE": rmse / np.mean(y_true) * 100}
