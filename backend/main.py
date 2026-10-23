import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import os

from . import config
from .db import get_db, init_db
from .schemas import DemandRequest, DemandResponse, PreferenceRequest, PreferenceResponse, WasteRequest, WasteResponse, KitchenPlanRequest, KitchenPlanResponse, FeedbackRecord, FeedbackResponse, ChatMessage, ChatResponse, WeatherResponse, SmartSuggestionResponse
from .agents.demand_agent import demand_forecast
from .agents.preference_agent import food_preference
from .agents.waste_agent import waste_diagnosis
from .agents.kitchen_agent import kitchen_plan
from .agents.feedback_agent import record_feedback, get_feedback_stats
from .utils import fetch_weather, get_smart_suggestions

app = FastAPI(title="MessWise Backend")

# Allow frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.post("/api/predict-demand", response_model=DemandResponse)
async def predict_demand(req: DemandRequest):
    try:
        pred, version = demand_forecast(req)
        return DemandResponse(predicted_consumers=pred, model_version=version, input=req)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/food-preference", response_model=PreferenceResponse)
async def preference(req: PreferenceRequest):
    score, evidence = food_preference(req)
    return PreferenceResponse(preference_score=score, evidence=evidence)

@app.post("/api/waste-diagnosis", response_model=WasteResponse)
async def waste(req: WasteRequest):
    rate, analysis = waste_diagnosis(req)
    return WasteResponse(waste_rate_pct=rate, analysis=analysis)

@app.post("/api/kitchen-plan", response_model=KitchenPlanResponse)
async def plan(req: KitchenPlanRequest):
    plan = kitchen_plan(req)
    return KitchenPlanResponse(**plan)

@app.post("/api/feedback", response_model=FeedbackResponse)
async def feedback(record: FeedbackRecord, db=Depends(get_db)):
    try:
        record_feedback(db, record)
        stats = get_feedback_stats(db)
        return FeedbackResponse(message="Feedback recorded", stats=stats)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/weather", response_model=WeatherResponse)
async def weather():
    data = await fetch_weather()
    return data

@app.get("/api/smart-suggestions", response_model=SmartSuggestionResponse)
async def suggestions():
    sugg = await get_smart_suggestions()
    return SmartSuggestionResponse(suggestions=sugg)

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    # Simple deterministic fallback if OpenAI key missing
    if not config.OPENAI_API_KEY:
        # fallback: echo the message
        return ChatResponse(reply=f"You said: {message.content}")
    # Otherwise call OpenAI (omitted for brevity)
    return ChatResponse(reply="[OpenAI response not implemented in this demo]")

if __name__ == "__main__":
    uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=True)
