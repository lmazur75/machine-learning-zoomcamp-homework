import pickle
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any, Literal, Optional
from pydantic import BaseModel, Field, ConfigDict
import uvicorn
import pandas as pd


class Engine(BaseModel):
    engine_rpm: int = Field(..., ge=0, le=100000)
    lub_oil_pressure: Optional[float] = Field(0.0, ge=0.0, le=1000.0)  # Default to 0.0
    fuel_pressure: Optional[float] = Field(0.0, ge=0.0, le=1000.0)
    coolant_pressure: Optional[float] = Field(0.0, ge=0.0, le=1000.0)
    lub_oil_temp: Optional[float] = Field(0, ge=0, le=1000.0)
    coolant_temp: Optional[float] = Field(0.0, ge=0.0, le=1000.0)


class PredictResponse(BaseModel):
    condition_probability: float
    condition: bool

app = FastAPI(title="engine-condition-prediction")

# ✅ CORS must be added immediately after app initialization
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or ["http://localhost:5500"] if hosting locally
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

with open('model.bin', 'rb') as f_in:
    pipeline = pickle.load(f_in)


def predict_single(engine_dict):
    default_values = {
        'engine_rpm': 0,
        'lub_oil_pressure': 0.0,
        'fuel_pressure': 0.0,
        'coolant_pressure': 0.0,
        'lub_oil_temp': 0,
        'coolant_temp': 0.0
    }
    
    # Update defaults with provided values
    default_values.update(engine_dict)
    df = pd.DataFrame([default_values])
    result = pipeline.predict_proba(df)[0, 1]
    return float(result)


@app.post("/predict")
def predict(engine: Engine) -> PredictResponse:
    prob = predict_single(engine.model_dump())

    return PredictResponse(
        condition_probability=prob,
        condition=prob >= 0.5
    )


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=9696)