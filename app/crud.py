from sqlalchemy.orm import Session
from passlib.context import CryptContext

# ACTION: Make sure to import your schema and models
from . import models, schema
from .database import SessionLocal

# Password hashing utility
pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")


# ---------------- PREDICTION CRUD ----------------
# FIXED: Updated the function to accept the new payload and predicted price
def create_prediction(db: Session, payload: schema.PredictionRequest, predicted_price: float):
    """
    Insert a new prediction record into the database using the Kaggle features.
    """
    # Create the database model instance using data from the payload
    db_pred = models.Prediction(
        OverallQual=payload.OverallQual,
        GrLivArea=payload.GrLivArea,
        GarageCars=payload.GarageCars,
        TotalBsmtSF=payload.TotalBsmtSF,
        YearBuilt=payload.YearBuilt,
        predicted_price=predicted_price
    )
    db.add(db_pred)
    db.commit()
    db.refresh(db_pred)
    return db_pred


# ---------------- USER CRUD (No changes needed here) ----------------
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, username: str, password: str):
    hashed = pwd_ctx.hash(password)
    user = models.User(username=username, hashed_password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_ctx.verify(plain_password, hashed_password)


# ---------------- DB SESSION DEPENDENCY (No changes needed here) ----------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()