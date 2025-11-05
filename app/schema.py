from pydantic import BaseModel,Field
from typing import Optional

class PredictionRequest(BaseModel):
    OverallQual: int      # Overall material and finish quality (1-10)
    GrLivArea: int        # Above grade (ground) living area square feet
    GarageCars: int       # Size of garage in car capacity
    TotalBsmtSF: int      # Total square feet of basement area
    YearBuilt: int        # Original construction date
    
    # Add any other features your model requires...
    # Example: FullBath: int, TotRmsAbvGrd: int, etc.


class PredictionResponse(BaseModel):
    predicted_price: float


class UserCreate(BaseModel):
    username: str
    password: str = Field(..., min_length=8, max_length=72)


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None