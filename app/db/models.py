from sqlalchemy import BigInteger, Column, Index, Integer, Numeric, String
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class PriceTick(Base):
    __tablename__ = "price_ticks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String, nullable=False)
    price = Column(Numeric(30, 18), nullable=False)
    ts_unix = Column(BigInteger, nullable=False)

    __table_args__ = (Index("ix_price_ticks_ticker_ts", "ticker", "ts_unix"),)
