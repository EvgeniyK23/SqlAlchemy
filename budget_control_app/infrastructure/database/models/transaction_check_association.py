from infrastructure.database.base import Base  # noqa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TransactionCheck(Base):
    """Ассоциативная таблица: Транзакция ↔ Чек (many-to-many).

    Один чек может соответствовать нескольким транзакциям
    (например, оплата разными способами), и одна транзакция
    может иметь несколько чеков.
    """

    __tablename__ = 'transaction_check'

    transaction_id: Mapped[int] = mapped_column(
        ForeignKey('transaction.id', ondelete='CASCADE'), primary_key=True
    )
    check_id: Mapped[int] = mapped_column(
        ForeignKey('check.id', ondelete='CASCADE'), primary_key=True
    )

    transaction: Mapped['Transaction'] = relationship(  # noqa
        back_populates='check_links'
    )
    check: Mapped['Check'] = relationship(back_populates='transaction_links')  # noqa

    def __repr__(self) -> str:
        return (
            f'TransactionCheck(txn={self.transaction_id}, '
            f'check={self.check_id})'
        )
