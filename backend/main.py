from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
import models, schemas, crud
from database import engine, SessionLocal
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Healthiee API")

# Allow ALL CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- ADDED: Schema for the incoming search request ---
class ProductCheckRequest(BaseModel):
    name: str

# --- ADDED: The endpoint the frontend is looking for ---
@app.post("/check-product")
def check_product(request: ProductCheckRequest, db: Session = Depends(get_db)):
    # 1. Search for an exact or partial match of the product name
    product = db.query(models.Product).filter(models.Product.name.ilike(f"%{request.name}%")).first()
    
    # If it's not a product, check if the user searched for an ingredient directly
    if not product:
        ingredient = db.query(models.Ingredient).filter(models.Ingredient.name.ilike(f"%{request.name}%")).first()
        if ingredient:
            bans = db.query(models.Ban).filter(models.Ban.ingredient_id == ingredient.id).all()
            banned_countries = [db.query(models.Country).filter(models.Country.id == b.country_id).first().name for b in bans]
            
            return {
                "name": ingredient.name,
                "risk_level": ingredient.risk_level,
                "banned": len(bans) > 0,
                "banned_countries": banned_countries,
                "reason": bans[0].reason if bans else "No restriction"
            }
        return {"error": "Product or ingredient not found in database."}

    # 2. If product is found, fetch its associated ingredients
    product_ingredients = db.query(models.ProductIngredient).filter(models.ProductIngredient.product_id == product.id).all()
    ingredient_ids = [pi.ingredient_id for pi in product_ingredients]
    ingredients = db.query(models.Ingredient).filter(models.Ingredient.id.in_(ingredient_ids)).all()
    
    # 3. Calculate highest risk level among ingredients
    risk_level = "Low"
    for i in ingredients:
        if i.risk_level == "High":
            risk_level = "High"
            break
        elif i.risk_level in ["Medium", "Moderate"] and risk_level != "High":
            risk_level = "Medium"
            
    # 4. Find if any of these ingredients or the product itself is banned
    bans = db.query(models.Ban).filter(
        (models.Ban.product_id == product.id) | 
        (models.Ban.ingredient_id.in_(ingredient_ids))
    ).all()
    
    banned_countries = []
    reason = "No restriction"
    
    if bans:
        for ban in bans:
            country = db.query(models.Country).filter(models.Country.id == ban.country_id).first()
            if country and country.name not in banned_countries:
                banned_countries.append(country.name)
        reason = bans[0].reason

    return {
        "name": product.name,
        "risk_level": risk_level,
        "banned": len(bans) > 0,
        "banned_countries": banned_countries,
        "reason": reason
    }

# --- KEPT: Your existing endpoints ---

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=list[schemas.Product])
def read_products(db: Session = Depends(get_db)):
    return crud.get_products(db=db)

@app.get("/")
def root():
    return {"message": "Healthiee API Running"}