from infrastructure.database.base import Base  # noqa
from sqlalchemy import Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Account(Base):
    """Финансовый счёт (наличные, карта, вклад)."""

    __tablename__ = 'account'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(20))  # cash / card / deposit
    balance: Mapped[float] = mapped_column(default=0.0)

    # один счёт → много транзакций; при удалении счёта — удаляем транзакции
    transactions: Mapped[list['Transaction']] = relationship(  # noqa
        back_populates='account',
        cascade='all, delete-orphan',
    )

    __table_args__ = (Index('idx_account_type', 'type'),)

    def __repr__(self) -> str:
        return (
            f'Account(id={self.id}, name={self.name!r}, '
            f'balance={self.balance:.2f})'
        )
