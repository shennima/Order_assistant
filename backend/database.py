from sqlalchemy.orm import Session
from .models import Order
from datetime import datetime, date
from typing import Optional


def get_db_session():
    """获取数据库会话"""
    from .models import SessionLocal
    return SessionLocal()


def create_order(db: Session, order_data: dict):
    """
    创建订单

    Args:
        db: 数据库会话
        order_data: 订单数据字典

    Returns:
        新创建的订单对象

    Raises:
        ValueError: 如果订单号已存在
    """
    # 检查订单号是否已存在
    existing_order = get_order_by_number(db, order_data.get('order_number'))
    if existing_order:
        raise ValueError(f"订单号 '{order_data.get('order_number')}' 已存在")

    # 处理日期字符串转换为date对象
    for key in ['expected_delivery_date', 'input_date', 'audit_date', 'production_date', 'delivery_date']:
        if key in order_data and isinstance(order_data[key], str):
            try:
                order_data[key] = datetime.strptime(order_data[key], '%Y-%m-%d').date()
            except ValueError:
                order_data[key] = None

    # 创建订单实例
    db_order = Order(**order_data)
    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order_by_id(db: Session, order_id: int):
    """
    根据ID获取订单

    Args:
        db: 数据库会话
        order_id: 订单ID

    Returns:
        订单对象或None
    """
    return db.query(Order).filter(Order.id == order_id).first()


def get_order_by_number(db: Session, order_number: str):
    """
    根据订单号获取订单

    Args:
        db: 数据库会话
        order_number: 订单号

    Returns:
        订单对象或None
    """
    return db.query(Order).filter(Order.order_number == order_number).first()


def update_order(db: Session, order_id: int, order_data: dict):
    """
    更新订单

    Args:
        db: 数据库会话
        order_id: 订单ID
        order_data: 要更新的订单数据字典

    Returns:
        更新后的订单对象或None
    """
    db_order = get_order_by_id(db, order_id)
    if not db_order:
        return None

    # 处理日期字符串转换为date对象
    for key in ['expected_delivery_date', 'input_date', 'audit_date', 'production_date', 'delivery_date']:
        if key in order_data and isinstance(order_data[key], str):
            try:
                order_data[key] = datetime.strptime(order_data[key], '%Y-%m-%d').date()
            except ValueError:
                order_data[key] = None

    # 更新订单字段
    for key, value in order_data.items():
        setattr(db_order, key, value)

    # 更新updated_at字段
    db_order.updated_at = datetime.utcnow()

    db.commit()
    db.refresh(db_order)
    return db_order
