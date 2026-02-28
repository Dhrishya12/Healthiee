from database import engine, Base, SessionLocal
from models import Product, Ingredient, ProductIngredient, Country, Ban

Base.metadata.create_all(bind=engine)

db = SessionLocal()

# ---------- Countries ----------
eu = Country(name="European Union")
canada = Country(name="Canada")
india = Country(name="India")

db.add_all([eu, canada, india])
db.commit()

# ---------- Ingredients ----------
hydroquinone = Ingredient(
    name="Hydroquinone",
    risk_level="High",
    description="May cause skin irritation and cancer risk."
)

titanium = Ingredient(
    name="Titanium Dioxide",
    risk_level="Moderate",
    description="Possible inhalation risk in powder form."
)

db.add_all([hydroquinone, titanium])
db.commit()

# ---------- Product ----------
cream = Product(name="SkinGlow Cream", category="Cosmetics")
db.add(cream)
db.commit()

# ---------- Mapping ----------
db.add(ProductIngredient(product_id=cream.id, ingredient_id=hydroquinone.id))
db.add(ProductIngredient(product_id=cream.id, ingredient_id=titanium.id))
db.commit()

# ---------- Bans ----------
db.add(Ban(
    ingredient_id=hydroquinone.id,
    country_id=eu.id,
    reason="Banned due to carcinogenic risk",
    severity="High"
))

db.add(Ban(
    ingredient_id=hydroquinone.id,
    country_id=canada.id,
    reason="Skin damage and long-term toxicity",
    severity="High"
))

db.commit()
db.close()