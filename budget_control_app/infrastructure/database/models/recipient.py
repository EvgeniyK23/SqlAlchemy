from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.base import Base


class Recipient(Base):
    """Получатель перевода (человек, магазин, сервис)."""

    __tablename__ = 'recipient'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str | None] = mapped_column(String(20))
    note: Mapped[str | None] = mapped_column(String(255))

    # при удалении получателя — транзакции остаются, recipient_id → NULL
    transactions: Mapped[list['Transaction']] = relationship(
        back_populates='recipient',
    )

    def __repr__(self) -> str:
        return f'Recipient(id={self.id}, name={self.name!r})'
