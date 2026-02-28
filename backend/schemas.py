from pydantic import BaseModel
from typing import List, Optional

class BannedCountryBase(BaseModel):
    country: str
    reason: str

class BannedCountryCreate(BannedCountryBase):
    pass

class BannedCountry(BannedCountryBase):
    id: int

    class Config:
        orm_mode = True


class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProductCreate(ProductBase):
    banned_countries: List[BannedCountryCreate] = []

class Product(ProductBase):
    id: int
    banned_countries: List[BannedCountry] = []

    class Config:
        orm_mode = True