from sqlalchemy.orm import Session
import models, schemas

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(
        name=product.name,
        description=product.description
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    for banned in product.banned_countries:
        # First, find or create the country to get its ID
        db_country = db.query(models.Country).filter(models.Country.name == banned.country).first()
        if not db_country:
            db_country = models.Country(name=banned.country)
            db.add(db_country)
            db.commit()
            db.refresh(db_country)

        # Use models.Ban instead of models.BannedCountry
        db_ban = models.Ban(
            country_id=db_country.id, # Map to the ID, not the string
            reason=banned.reason,
            product_id=db_product.id,
            severity="High" # Provide a default or pass it from the schema
        )
        db.add(db_ban)

    db.commit()
    return db_product

def get_products(db: Session):
    return db.query(models.Product).all()