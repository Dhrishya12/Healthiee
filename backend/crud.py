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
        db_banned = models.BannedCountry(
            country=banned.country,
            reason=banned.reason,
            product_id=db_product.id
        )
        db.add(db_banned)

    db.commit()
    return db_product


def get_products(db: Session):
    return db.query(models.Product).all()