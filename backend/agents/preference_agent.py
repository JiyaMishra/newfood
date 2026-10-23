# backend/agents/preference_agent.py
"""Food Preference Agent
Computes a preference score for a dish using deterministic aggregation.
"""
from ..schemas import PreferenceRequest, PreferenceResponse
import pandas as pd
import os

CSV_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'messwise_full_august_2026_menu_dataset.csv'))

def load_data():
    return pd.read_csv(CSV_PATH)

def food_preference(req: PreferenceRequest):
    df = load_data()
    # Filter rows for the given food_item and meal
    mask = (df['food_item'] == req.food_item) & (df['meal'] == req.meal)
    relevant = df[mask]
    if relevant.empty:
        score = 0.0
        evidence = f"No historical records found for {req.food_item} ({req.meal})."
    else:
        # Simple average of synthetic_liking_score weighted by historical_demand_rate
        weighted = (relevant['synthetic_liking_score'] * relevant['historical_demand_rate']).mean()
        score = float(round(weighted, 3))
        avg_consumers = relevant['expected_consumers'].mean()
        evidence = f"Based on {len(relevant)} past servings, avg expected consumers {avg_consumers:.1f}, weighted liking {score}."
    return score, evidence
