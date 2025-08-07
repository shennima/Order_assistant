from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Mapped, mapped_column
from sqlalchemy.types import Date as SQLDate
from typing import Optional
from datetime import date, datetime

# 数据库配置
DATABASE_URL = "mysql+pymysql://root:Aacbbc6.@localhost:3306/order_management_system"
Base = declarative_base()


class Order(Base):
    """订单基础模型"""
    __tablename__ = "orders"

    # 使用 SQLAlchemy 2.0 的 Mapped 类型注解
    id: Mapped[int] = mapped_column("order_id", Integer, primary_key=True, index=True, autoincrement=True)
    order_number: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    customer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    product_name: Mapped[str] = mapped_column(String(100), nullable=False)
    specification: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    quantity: Mapped[float] = mapped_column(Float, nullable=False)
    sale_price: Mapped[float] = mapped_column(Float, nullable=False)
    sale_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    contract_number: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    expected_delivery_date: Mapped[Optional[date]] = mapped_column(SQLDate, nullable=True)
    input_date: Mapped[Optional[date]] = mapped_column(SQLDate, nullable=True)
    audit_date: Mapped[Optional[date]] = mapped_column(SQLDate, nullable=True)
    production_date: Mapped[Optional[date]] = mapped_column(SQLDate, nullable=True)
    delivery_date: Mapped[Optional[date]] = mapped_column(SQLDate, nullable=True)
    finished_weight: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    transport_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    destination: Mapped[Optional[str]] = mapped_column(String(200), nullable=True)
    payment_method: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    remark: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


# 创建数据库引擎
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)
