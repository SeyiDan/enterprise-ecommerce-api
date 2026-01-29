from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import text
from sqlalchemy.orm import Session
from typing import List
from app.db.base import get_db
from app.core.dependencies import get_current_user
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.schemas.order import OrderCreate, OrderResponse, OrderSummary

router = APIRouter()


@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new order."""
    total_amount = 0.0
    order_items = []
    
    # Validate products and calculate total
    for item in order_data.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {item.product_id} not found"
            )
        
        if product.stock_quantity < item.quantity:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Insufficient stock for product {product.name}"
            )
        
        item_total = product.price * item.quantity
        total_amount += item_total
        
        order_items.append({
            "product_id": product.id,
            "quantity": item.quantity,
            "price_at_purchase": product.price
        })
        
        # Update stock
        product.stock_quantity -= item.quantity
    
    # Create order
    new_order = Order(
        user_id=current_user.id,
        total_amount=total_amount
    )
    db.add(new_order)
    db.flush()  # Get order ID before adding items
    
    # Add order items
    for item_data in order_items:
        order_item = OrderItem(
            order_id=new_order.id,
            **item_data
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(new_order)
    
    return new_order


@router.get("/", response_model=List[OrderResponse])
def list_orders(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get all orders for the current user."""
    query = db.query(Order).filter(Order.user_id == current_user.id)
    
    # If admin, show all orders
    if current_user.is_admin:
        query = db.query(Order)
    
    orders = query.offset(skip).limit(limit).all()
    return orders


@router.get("/summary", response_model=List[OrderSummary])
def get_order_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get order summary using raw SQL (performance optimization)."""
    # This demonstrates using raw SQL for complex queries
    raw_query = text("""
        SELECT 
            o.id as order_id,
            u.email as user_email,
            o.total_amount,
            COUNT(oi.id) as item_count,
            o.status,
            o.created_at
        FROM orders o
        JOIN users u ON o.user_id = u.id
        LEFT JOIN order_items oi ON o.id = oi.order_id
        WHERE (:is_admin = true OR o.user_id = :user_id)
        GROUP BY o.id, u.email, o.total_amount, o.status, o.created_at
        ORDER BY o.created_at DESC
    """)
    
    result = db.execute(
        raw_query,
        {"is_admin": current_user.is_admin, "user_id": current_user.id}
    )
    
    summaries = []
    for row in result:
        summaries.append(OrderSummary(
            order_id=row.order_id,
            user_email=row.user_email,
            total_amount=row.total_amount,
            item_count=row.item_count,
            status=row.status,
            created_at=row.created_at
        ))
    
    return summaries


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get a specific order by ID."""
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    
    # Check if user owns the order or is admin
    if order.user_id != current_user.id and not current_user.is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to view this order"
        )
    
    return order
