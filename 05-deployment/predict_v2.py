import pickle
from fastapi import FastAPI
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict
import uvicorn


class Customer(BaseModel):
    model_config = ConfigDict(extra="forbid")
    number_of_courses_viewed: int = Field(..., ge=0, le=9)
    lead_source: Literal["organic_search", "social_media", "paid_ads", "referral", "events"]
    annual_income: Optional[float] = Field(None, ge=13929.0, le=109899.0)
    interaction_count: Optional[int] = Field(None, ge=0, le=11)
    lead_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    industry: Optional[Literal["retail", "finance", "other", "education", "healthcare", "technology", "manufacturing"]] = None
    employment_status: Optional[Literal["self_employed", "student", "unemployed", "employed"]] = None
    location: Optional[Literal["north_america", "europe", "middle_east", "asia", "south_america", "africa", "australia"]] = None


class PredictResponse(BaseModel):
    convert_probability: float
    convert: bool

app = FastAPI(title="customer-convert-prediction")

with open('pipeline_v2.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)


def predict_single(customer):
    result = pipeline.predict_proba(customer)[0, 1]
    return float(result)


@app.post("/predict")
def predict(customer: Customer) -> PredictResponse:
    prob = predict_single(customer.model_dump())

    return PredictResponse(
        convert_probability=prob,
        convert=prob >= 0.5
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)
