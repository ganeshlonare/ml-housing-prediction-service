import pandas as pd
import joblib
import os
from sklearn.linear_model import LinearRegression

# Import the schema to use it for type hinting
from . import schema
from .config import settings

# Define the path to the model from your settings
MODEL_PATH = settings.MODEL_PATH

# IMPORTANT: These features MUST match the fields in your schema.PredictionRequest
FEATURES = [
    'OverallQual',
    'GrLivArea',
    'GarageCars',
    'TotalBsmtSF',
    'YearBuilt'
]

TARGET = 'SalePrice'


def train_model(csv_path: str = "data/train.csv"):
    """
    Trains a new linear regression model on the Kaggle dataset.
    """
    print(f"Loading dataset from {csv_path}...")
    df = pd.read_csv(csv_path)

    # --- Basic Data Cleaning ---
    # For this example, we'll fill missing values in our feature columns with the mean.
    # A real project would have more advanced feature engineering.
    for col in FEATURES:
        if df[col].isnull().any():
            df[col] = df[col].fillna(df[col].mean())
    
    print("Selecting features and target...")
    X = df[FEATURES]
    y = df[TARGET]

    print("Training Linear Regression model...")
    model = LinearRegression()
    model.fit(X, y)

    # Ensure the model directory exists before saving
    model_dir = os.path.dirname(MODEL_PATH)
    os.makedirs(model_dir, exist_ok=True)
    
    print(f"Saving model to {MODEL_PATH}...")
    joblib.dump(model, MODEL_PATH)
    
    return MODEL_PATH


def load_model():
    """
    Loads the trained model from the file.
    """
    try:
        model = joblib.load(MODEL_PATH)
        return model
    except FileNotFoundError:
        print(f"Error: Model file not found at {MODEL_PATH}")
        return None


def prepare_features(payload: schema.PredictionRequest):
    """
    Converts the API payload into a model-ready DataFrame.
    """
    # Create a dictionary from the pydantic model
    data = payload.model_dump()
    
    # Convert the dictionary to a pandas DataFrame
    df = pd.DataFrame([data])
    
    # Ensure the column order is the same as it was during training
    df = df[FEATURES]
    
    return df