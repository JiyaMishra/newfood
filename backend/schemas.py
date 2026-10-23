from pydantic import BaseModel
from typing import Optional, List

class DemandRequest(BaseModel):
    date: str
    meal: str
    attendance_estimate: int
    exam_intensity: float
    temperature_c: float
    rainfall_mm: float
    historical_demand_rate: float
    # additional features as needed

class DemandResponse(BaseModel):
    predicted_consumers: int
    model_version: str
    input: DemandRequest

class PreferenceRequest(BaseModel):
    food_item: str
    meal: str
    date: str

class PreferenceResponse(BaseModel):
    preference_score: float
    evidence: str

class WasteRequest(BaseModel):
    prepared_portions: int
    leftover_portions: int
    food_item: str
    meal: str
    date: str

class WasteResponse(BaseModel):
    waste_rate_pct: float
    analysis: str

class KitchenPlanRequest(BaseModel):
    predicted_consumers: int
    food_item: str
    portion_size: float  # assumed kg or pieces per consumer

class KitchenPlanResponse(BaseModel):
    initial_batch: int
    reserve_quantity: int
    replenishment_needed: bool
    notes: str

class FeedbackRecord(BaseModel):
    date: str
    meal: str
    food_item: str
    predicted_consumers: Optional[int] = None
    actual_consumers: Optional[int] = None
    prepared_portions: Optional[int] = None
    leftover_portions: Optional[int] = None

class FeedbackResponse(BaseModel):
    message: str
    stats: dict

class ChatMessage(BaseModel):
    content: str
    user_id: Optional[str] = None

class ChatResponse(BaseModel):
    reply: str

class WeatherResponse(BaseModel):
    temperature_c: float
    rainfall_mm: float
    description: str

class SmartSuggestionResponse(BaseModel):
    suggestions: List[str]
