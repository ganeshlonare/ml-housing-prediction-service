import os, subprocess, zipfile
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import timedelta

from . import models, schema, ml_model, crud
from .database import engine
from .config import settings
from .auth import create_access_token, get_current_user
from .crud import get_db

# create tables in the database
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI app
app = FastAPI()


# Load the ML model on startup (optional but good practice)
model = None
try:
    model = ml_model.load_model()
    print("Model loaded successfully on startup.")
except Exception as e:
    print(f"Model loading failed on startup: {e}")
    model = None


# -------- This endpoint is for your old, simpler dataset --------
# @app.post("/train")
# def train(csv_path: str = "data/housing.csv"):
#     path = ml_model.train_model(csv_path)
#     global model
#     model = ml_model.load_model() # This correctly reloads the model
#     return {"status": "trained", "path": path}


# -------- AUTH ENDPOINT --------
# FIXED: Used PascalCase for the schema class (schema.Token)
@app.post("/token", response_model=schema.Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not crud.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# -------- KAGGLE TRAINING ENDPOINT --------
@app.post("/train/kaggle")
def train_from_kaggle():
    data_path = "data/"
    train_csv_path = os.path.join(data_path, "train.csv")
    zip_path = os.path.join(data_path, "house-prices-advanced-regression-techniques.zip")

    if not os.path.exists(train_csv_path):
        print(f"'{train_csv_path}' not found. Downloading and extracting data...")
        os.makedirs(data_path, exist_ok=True)
        subprocess.run(
            ["kaggle", "competitions", "download", "-c", "house-prices-advanced-regression-techniques", "-p", data_path],
            check=True
        )
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(data_path)
        print("Data downloaded and extracted successfully.")
    else:
        print(f"'{train_csv_path}' already exists. Skipping download.")

    print("Training model from Kaggle dataset...")
    path = ml_model.train_model(train_csv_path)
    
    # FIXED: Reload the newly trained model so /predict can use it
    global model
    model = ml_model.load_model()
    print("Model training complete and reloaded.")
    
    return {"status": "trained_from_kaggle", "path": path}


# -------- USER REGISTRATION --------
@app.post("/users", status_code=201)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    created = crud.create_user(db, user.username, user.password)
    return {"username": created.username}


# -------- PREDICTION ENDPOINT --------

@app.post("/predict", response_model=schema.PredictionResponse)
def predict(
    payload: schema.PredictionRequest,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db)
):
    global model
    if model is None:
        raise HTTPException(status_code=500, detail="Model not trained or loaded yet. Please call /train or /train/kaggle first.")

    try:
        feature_vector = ml_model.prepare_features(payload)
        pred = float(model.predict(feature_vector)[0])
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to create prediction. Check input data. Error: {e}")

    crud.create_prediction(db, payload, pred)
    return {"predicted_price": pred}


# -------- PROFILE ENDPOINT --------
@app.get("/me")
def read_me(current_user=Depends(get_current_user)):
    return {"username": current_user.username}