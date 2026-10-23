# backend/agents/waste_agent.py
"""Waste Diagnosis Agent
Calculates waste rate and provides a short analysis.
"""
from ..schemas import WasteRequest, WasteResponse

def waste_diagnosis(req: WasteRequest):
    if req.prepared_portions == 0:
        waste_rate = 0.0
        analysis = "No portions were prepared, so no waste."
    else:
        waste_rate = max(0.0, (req.prepared_portions - req.consumed_portions) / req.prepared_portions) * 100
        if waste_rate < 5:
            level = "low"
        elif waste_rate < 20:
            level = "moderate"
        else:
            level = "high"
        analysis = f"Waste rate is {waste_rate:.1f}% ({level})."
    return WasteResponse(waste_rate_pct=waste_rate, analysis=analysis)
