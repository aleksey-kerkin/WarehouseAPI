from datetime import datetime
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import engine, get_db
from models import Base
from models import Order as DBOrder
from models import OrderItem as DBOrderItem
from models import Product as DBProduct
from schemas import Order, OrderCreate, OrderStatus, Product, ProductCreate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Warehouse API",
    description="API для управления складом и заказами",
    version="1.0.0",
)

# Products CRUD


@app.post("/products/", response_model=Product, tags=["Products"])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = DBProduct(
        name=product.name,
        description=product.description,
        price=product.price,
        quantity=product.quantity,
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.get("/products/", response_model=List[Product], tags=["Products"])
def read_products(db: Session = Depends(get_db)):
    products = db.query(DBProduct).all()
    return products


@app.get("/products/{product_id}", response_model=Product, tags=["Products"])
def read_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    return db_product


@app.put("/products/{product_id}", response_model=Product, tags=["Products"])
def update_product(
    product_id: int, product: ProductCreate, db: Session = Depends(get_db)
):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    for var, value in vars(product).items():
        setattr(db_product, var, value)
    db.commit()
    db.refresh(db_product)
    return db_product


@app.delete("/products/{product_id}", response_model=Product, tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(DBProduct).filter(DBProduct.id == product_id).first()
    if db_product is None:
        raise HTTPException(status_code=404, detail="Продукт не найден")
    db.delete(db_product)
    db.commit()
    return db_product


# Orders CRUD


@app.post("/orders/", response_model=Order, tags=["Orders"])
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    db_order = DBOrder(created_at=datetime.now(), status="в процессе")
    db.add(db_order)
    db.flush()

    for item in order.items:
        product = (
            db.query(DBProduct).filter(DBProduct.id == item.product_id).first()
        )
        if product is None:
            raise HTTPException(
                status_code=404,
                detail=f"Продукт с id {item.product_id} не найден",
            )
        if product.quantity < item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Недостаточное количество для продукта {product.name}",
            )

        product.quantity -= item.quantity
        db_order_item = DBOrderItem(
            order_id=db_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
        )
        db.add(db_order_item)

    db.commit()
    db.refresh(db_order)
    return db_order


@app.get("/orders/", response_model=List[Order], tags=["Orders"])
def read_orders(
    status: Optional[OrderStatus] = None, db: Session = Depends(get_db)
):
    query = db.query(DBOrder)
    if status:
        query = query.filter(DBOrder.status == status.value)
    orders = query.all()
    return orders


@app.get("/orders/{order_id}", response_model=Order, tags=["Orders"])
def read_order(order_id: int, db: Session = Depends(get_db)):
    db_order = db.query(DBOrder).filter(DBOrder.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")
    return db_order


@app.patch("/orders/{order_id}/status", response_model=Order, tags=["Orders"])
def update_order_status(
    order_id: int, status: OrderStatus, db: Session = Depends(get_db)
):
    db_order = db.query(DBOrder).filter(DBOrder.id == order_id).first()
    if db_order is None:
        raise HTTPException(status_code=404, detail="Заказ не найден")

    db_order.status = status.value
    db.commit()
    db.refresh(db_order)
    return db_order
