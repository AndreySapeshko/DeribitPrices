from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import BigInteger, Numeric, Text, Index

class Base(DeclarativeBase):
    pass

class PriceTick(Base):
    __tablename__ = "price_ticks"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    ticker: Mapped[str] = mapped_column(Text, nullable=False)
    price: Mapped[float] = mapped_column(Numeric(20, 10), nullable=False)
    ts_unix: Mapped[int] = mapped_column(BigInteger, nullable=False)

    __table_args__ = (
        Index("ix_price_ticks_ticker_ts", "ticker", "ts_unix"),
    )
