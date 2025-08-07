from sqlalchemy.orm import Session
from . import models, database
from typing import Optional
from datetime import date, datetime


class OrderService:
    """订单服务类"""

    def __init__(self, db: Session):
        self.db = db

    def create_order(self, order_data: dict) -> models.Order:
        """
        创建订单

        Args:
            order_data: 订单数据

        Returns:
            创建的订单对象
        """
        # 确保创建和更新时间被设置
        if 'created_at' not in order_data:
            order_data['created_at'] = datetime.utcnow()
        if 'updated_at' not in order_data:
            order_data['updated_at'] = datetime.utcnow()

        return database.create_order(self.db, order_data)

    def get_order(self, order_id: int) -> Optional[models.Order]:
        """
        根据ID获取订单

        Args:
            order_id: 订单ID

        Returns:
            订单对象或None
        """
        return database.get_order_by_id(self.db, order_id)

    def get_order_by_number(self, order_number: str) -> Optional[models.Order]:
        """
        根据订单号获取订单

        Args:
            order_number: 订单号

        Returns:
            订单对象或None
        """
        return database.get_order_by_number(self.db, order_number)
