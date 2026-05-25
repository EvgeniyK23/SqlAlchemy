from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class Check(Base):
    """Кассовый чек из магазина."""

    __tablename__ = 'check'

    id: Mapped[int] = mapped_column(primary_key=True)
    store_name: Mapped[str] = mapped_column(String(100))
    purchased_at: Mapped[datetime] = mapped_column(DateTime)

    # many-to-many с Transaction через TransactionCheck
    transaction_links: Mapped[list['TransactionCheck']] = relationship(
        back_populates='check',
        cascade='all, delete-orphan',
    )

    # один чек → много позиций; при удалении чека — удаляем позиции
    items: Mapped[list['CheckProductAssociation']] = relationship(
        back_populates='check',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return f'Check(id={self.id}, store={self.store_name!r}, date={self.purchased_at.date()})'
