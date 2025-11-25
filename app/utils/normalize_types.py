import numpy as np
import pandas as pd

def normalize(o):
    """Convierte numpy, pandas y otros tipos no JSON a tipos nativos."""
    if isinstance(o, (np.integer,)):
        return int(o)
    if isinstance(o, (np.floating,)):
        return round(float(o), 2)
    if isinstance(o, (pd.Timestamp,)):
        return o.isoformat()
    if isinstance(o, (pd.Timedelta,)):
        return o.total_seconds()
    if isinstance(o, dict):
        return {normalize(k): normalize(v) for k, v in o.items()}
    if isinstance(o, list):
        return [normalize(v) for v in o]
    if isinstance(o, set):
        return [normalize(v) for v in o]
    return o
