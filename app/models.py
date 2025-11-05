from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Prediction(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    
    # --- Features from your PredictionRequest schema ---
    OverallQual = Column(Integer)
    GrLivArea = Column(Integer)
    GarageCars = Column(Integer)
    TotalBsmtSF = Column(Integer)
    YearBuilt = Column(Integer)

    # --- The predicted price ---
    predicted_price = Column(Float)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    full_name = Column(String)
    hashed_password = Column(String)


