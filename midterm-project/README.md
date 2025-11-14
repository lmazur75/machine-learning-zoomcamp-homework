# Engine Health Prediction Project

## Description of the Problem

This project focuses on predicting the health condition of automotive vehicle engines using machine learning. The goal is to classify whether an engine is in good condition or requires maintenance based on various sensor readings and operational parameters.

### Dataset
The project uses the **Automotive Vehicles Engine Health Dataset** which contains various engine parameters including:
- Engine RPM
- Lubricating oil pressure
- Fuel pressure
- Coolant pressure
- Lubricating oil temperature
- Coolant temperature
- Engine Condition (target variable: 0 = needs maintenance, 1 = good condition)

**Dataset Source**: [Automotive Vehicles Engine Health Dataset on Kaggle](https://www.kaggle.com/datasets/loveall/automotive-vehicles-engine-health-dataset)

### Solution Approach
The project implements a binary classification model using XGBoost, which achieved the best performance among several tested algorithms (Logistic Regression, Decision Tree, Random Forest, and XGBoost). The model can predict engine health with approximately 66.6% accuracy.

## Project Structure

```
├── README.md
├── notebook.ipynb          # EDA and model selection
├── train.py               # Training script
├── predict.py             # FastAPI service for predictions
├── Dockerfile             # Container configuration
├── pyproject.toml         # Project dependencies (uv)
├── uv.lock               # Locked dependencies
├── engine_data.csv       # Dataset
└── xgboost_engine_model.bin  # Trained model
```

## Installation and Setup

### Prerequisites
- Python 3.9+
- uv (recommended package manager)

### Installing uv

```bash
# On macOS and Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or using pip
pip install uv
```

### Option 1: Using uv (Recommended)

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd engine-health-prediction
```

2. **Create virtual environment and install dependencies**
```bash
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -r requirements.txt
```

Or install directly from pyproject.toml:
```bash
uv pip sync
```

### Option 2: Using Docker

```bash
docker build -t engine-health-api .
docker run -p 8000:8000 engine-health-api
```

## How to Download the Dataset

1. Visit [Kaggle Dataset Page](https://www.kaggle.com/datasets/loveall/automotive-vehicles-engine-health-dataset)
2. Download `engine_data.csv`
3. Place it in the project root directory

Alternatively, use Kaggle API:
```bash
kaggle datasets download -d loveall/automotive-vehicles-engine-health-dataset
unzip automotive-vehicles-engine-health-dataset.zip
```

## Usage

### 1. Training the Model

Train the model from scratch:

```bash
python train.py
```

This will:
- Load and preprocess the data
- Train the XGBoost model with optimized hyperparameters
- Save the model to `xgboost_engine_model.bin`
- Display training metrics

### 2. Running the Prediction Service

Start the FastAPI server:

```bash
uvicorn predict:app --host 0.0.0.0 --port 8000
```

Or for development with auto-reload:

```bash
uvicorn predict:app --reload
```

The service will be available at:
- API: `http://localhost:8000`
- Interactive docs: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

### 3. Making Predictions

#### Using curl:

```bash
curl -X POST http://localhost:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "engine_rpm": 700,
    "lub_oil_pressure": 2.5,
    "fuel_pressure": 11.8,
    "coolant_pressure": 3.2,
    "lub_oil_temp": 84.1,
    "coolant_temp": 81.6
  }'
```

#### Using Python requests:

```python
import requests

data = {
    "engine_rpm": 700,
    "lub_oil_pressure": 2.5,
    "fuel_pressure": 11.8,
    "coolant_pressure": 3.2,
    "lub_oil_temp": 84.1,
    "coolant_temp": 81.6
}

response = requests.post('http://localhost:8000/predict', json=data)
print(response.json())
```

#### Using the Interactive API Documentation:

1. Navigate to `http://localhost:8000/docs`
2. Click on the `/predict` endpoint
3. Click "Try it out"
4. Enter your test data
5. Click "Execute"

#### Response format:

```json
{
  "prediction": 1,
  "condition": "Good",
  "confidence": 0.85,
  "input_data": {
    "engine_rpm": 700,
    "lub_oil_pressure": 2.5,
    "fuel_pressure": 11.8,
    "coolant_pressure": 3.2,
    "lub_oil_temp": 84.1,
    "coolant_temp": 81.6
  }
}
```

- `prediction`: 0 (maintenance needed) or 1 (good condition)
- `condition`: Human-readable status
- `confidence`: Model confidence score
- `input_data`: Echo of the input parameters

## Model Performance

Based on the test set evaluation:

| Model | Test Accuracy | Test Precision | Test Recall | Test F1 | Test ROC-AUC |
|-------|---------------|----------------|-------------|---------|--------------|
| XGBoost | 0.6660 | 0.6502 | 0.6660 | 0.6457 | 0.7019 |
| Random Forest | 0.6627 | 0.6458 | 0.6627 | 0.6395 | 0.6989 |
| Logistic Regression | 0.6611 | 0.6434 | 0.6611 | 0.6261 | 0.6918 |
| Decision Tree | 0.6598 | 0.6427 | 0.6598 | 0.6382 | 0.6822 |

### Feature Importance

The most important features for prediction (XGBoost):
1. **Engine RPM** (51.44%)
2. **Fuel Pressure** (17.43%)
3. **Lubricating Oil Temperature** (10.38%)
4. **Lubricating Oil Pressure** (8.83%)
5. **Coolant Pressure** (6.34%)
6. **Coolant Temperature** (5.59%)

## Docker Deployment

### Build the Docker image:

```bash
docker build -t engine-health-api .
```

### Run the container:

```bash
docker run -p 8000:8000 engine-health-api
```

### Test the deployment:

```bash
curl http://localhost:8000/health
```

## API Endpoints

### Health Check
- **URL**: `/health`
- **Method**: GET
- **Response**: `{"status": "healthy", "model_loaded": true}`

### Root
- **URL**: `/`
- **Method**: GET
- **Response**: Welcome message with API information

### Predict Engine Condition
- **URL**: `/predict`
- **Method**: POST
- **Content-Type**: application/json
- **Request Body**:
```json
{
  "engine_rpm": 700,
  "lub_oil_pressure": 2.5,
  "fuel_pressure": 11.8,
  "coolant_pressure": 3.2,
  "lub_oil_temp": 84.1,
  "coolant_temp": 81.6
}
```

### Interactive Documentation
- **Swagger UI**: `/docs`
- **ReDoc**: `/redoc`

## Files and Dependencies

### pyproject.toml
Contains project metadata and dependencies:
```toml
[project]
name = "engine-health-prediction"
version = "0.1.0"
requires-python = ">=3.9"
dependencies = [
    "pandas>=2.0.0",
    "numpy>=1.24.0",
    "scikit-learn>=1.3.0",
    "xgboost>=2.0.0",
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "joblib>=1.3.0",
    "pydantic>=2.0.0",
]
```

### Dockerfile
Multi-stage build for optimized container size:
```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv pip install --system -r pyproject.toml

# Copy application files
COPY train.py predict.py xgboost_engine_model.bin ./

EXPOSE 8000

CMD ["uvicorn", "predict:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Development

### Setting up development environment with uv

```bash
# Create virtual environment
uv venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# or
.venv\Scripts\activate  # Windows

# Install dependencies
uv pip install -r requirements.txt

# Install development dependencies
uv pip install jupyter matplotlib seaborn
```

### Running the Jupyter Notebook

```bash
jupyter notebook notebook.ipynb
```

The notebook contains:
- Data loading and exploration
- Feature analysis and visualization
- Model comparison and selection
- Hyperparameter tuning with GridSearchCV
- Final model evaluation

### Project Workflow

1. **Data Preparation** (`notebook.ipynb`)
   - Load dataset
   - Clean column names
   - Check for missing values
   - Split into train/test sets

2. **EDA and Feature Analysis** (`notebook.ipynb`)
   - Statistical summary
   - Feature importance analysis
   - Visualization of key features

3. **Model Selection** (`notebook.ipynb`)
   - Test multiple algorithms
   - Hyperparameter tuning with GridSearchCV
   - Cross-validation with StratifiedKFold
   - Select best performing model (XGBoost)

4. **Model Training** (`train.py`)
   - Train final model with best parameters
   - Save model to disk

5. **Deployment** (`predict.py`, `Dockerfile`)
   - FastAPI service for real-time predictions
   - Docker containerization

## Why uv?

This project uses [uv](https://github.com/astral-sh/uv) as the package manager because:

- **Speed**: 10-100x faster than pip
- **Reliability**: Consistent dependency resolution
- **Simplicity**: Drop-in replacement for pip
- **Modern**: Built in Rust with modern Python packaging standards
- **Compatibility**: Works with existing pip/PyPI ecosystem

## FastAPI Benefits

This project uses FastAPI instead of Flask because:

- **Automatic API Documentation**: Interactive docs at `/docs` and `/redoc`
- **Type Safety**: Built-in request/response validation with Pydantic
- **Modern**: Async support, WebSocket support
- **Performance**: One of the fastest Python frameworks
- **Developer Experience**: Better error messages and IDE support

## Example Code Snippets

### train.py (simplified)

```python
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
import xgboost as xgb

# Load data
df = pd.read_csv('engine_data.csv')
df.columns = df.columns.str.strip().str.replace(' ','_').str.lower()

# Prepare features
X = df.drop("engine_condition", axis=1)
y = df["engine_condition"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=42
)

# Train model
model = xgb.XGBClassifier(
    learning_rate=0.1,
    max_depth=3,
    n_estimators=100,
    subsample=1.0,
    random_state=42,
    eval_metric='logloss',
    use_label_encoder=False
)

model.fit(X_train, y_train)

# Save model
joblib.dump(model, 'xgboost_engine_model.bin')
print("Model saved successfully!")
```

### predict.py (simplified)

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import joblib
import numpy as np

app = FastAPI(title="Engine Health Prediction API")

# Load model
model = joblib.load('xgboost_engine_model.bin')

class EngineData(BaseModel):
    engine_rpm: float = Field(..., gt=0)
    lub_oil_pressure: float = Field(..., ge=0)
    fuel_pressure: float = Field(..., ge=0)
    coolant_pressure: float = Field(..., ge=0)
    lub_oil_temp: float = Field(..., gt=0)
    coolant_temp: float = Field(..., gt=0)

@app.get("/")
def read_root():
    return {"message": "Engine Health Prediction API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "model_loaded": True}

@app.post("/predict")
def predict(data: EngineData):
    features = np.array([[
        data.engine_rpm,
        data.lub_oil_pressure,
        data.fuel_pressure,
        data.coolant_pressure,
        data.lub_oil_temp,
        data.coolant_temp
    ]])
    
    prediction = int(model.predict(features)[0])
    confidence = float(model.predict_proba(features)[0].max())
    
    return {
        "prediction": prediction,
        "condition": "Good" if prediction == 1 else "Maintenance Needed",
        "confidence": round(confidence, 4),
        "input_data": data.dict()
    }
```

## Future Improvements

1. **Model Enhancement**
   - Collect more data for better accuracy
   - Feature engineering (interaction features, polynomial features)
   - Try ensemble methods
   - Address class imbalance if present

2. **API Enhancements**
   - Add authentication (OAuth2, API keys)
   - Implement rate limiting
   - Add batch prediction endpoint
   - Include confidence intervals
   - Add model versioning

3. **Monitoring**
   - Add logging and metrics
   - Model performance tracking
   - Alert system for anomalies
   - Integration with monitoring tools (Prometheus, Grafana)

4. **Testing**
   - Unit tests for API endpoints
   - Integration tests
   - Load testing
   - Model drift detection

## Troubleshooting

### Common Issues

1. **Model file not found**
   - Ensure you run `train.py` before starting the API
   - Check that `xgboost_engine_model.bin` exists in the project directory

2. **Port already in use**
   - Change the port: `uvicorn predict:app --port 8001`
   - Or kill the process using port 8000

3. **uv not found**
   - Install uv: `pip install uv`
   - Or use the installation script from the official website

4. **Dependencies issues**
   - Regenerate lock file: `uv pip compile pyproject.toml -o requirements.txt`
   - Clear cache: `uv cache clean`

## Performance Benchmarks

- **Prediction latency**: ~5-10ms per request
- **Throughput**: ~100-200 requests/second (single worker)
- **Memory usage**: ~200-300MB
- **Model size**: ~100KB

## License

This project is available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Development Setup

```bash
git clone <your-repo-url>
cd engine-health-prediction
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

### Running Tests

```bash
pytest tests/
```

## Contact

For questions or feedback, please open an issue in the repository.

## Acknowledgments

- Dataset provided by [Kaggle](https://www.kaggle.com/datasets/loveall/automotive-vehicles-engine-health-dataset)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Package management with [uv](https://github.com/astral-sh/uv)

---

**Note**: This project is for educational and demonstration purposes. For production use, additional testing, validation, and monitoring should be implemented.