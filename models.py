import datetime

from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from db import Base


class Brands(Base):
    __tablename__ = 'brands'

    brand_id = Column(Integer, primary_key=True, autoincrement=True)
    brand_name = Column(String, nullable=True)


class Product(Base):
    __tablename__ = 'products'

    product_id = Column(Integer, primary_key=True, autoincrement=True)
    product_name = Column(String, nullable=True)
    product_quantity = Column(Integer, nullable=True)
    product_price = Column(Integer, nullable=True)
    date_updated = Column(Date, nullable=True, default=datetime.date.today())
    brand_id = Column(Integer, ForeignKey('brands.brand_id'), nullable=False)

    brand = relationship("Brands", lazy='joined')

    def __repr__(self):
        brand_name = self.brand.brand_name if self.brand else "No Brand"
        return (f"Product Details: "
                f"\n\tid: {self.product_id}, "
                f"\n\tname: {self.product_name}, "
                f"\n\tprice: ${int(self.product_price) / 100}, "
                f"\n\tquantity: {self.product_quantity}"
                f"\n\tdate updated: {self.date_updated}"
                f"\n\tbrand id: {self.brand_id}"
                f"\n\tbrand name: {brand_name}"
                )

