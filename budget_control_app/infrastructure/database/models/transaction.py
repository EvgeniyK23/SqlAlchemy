from datetime import datetime

from infrastructure.database.base import Base  # noqa
from sqlalchemy import DateTime, ForeignKey, Index, String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Transaction(Base):
    """Финансовая транзакция (доход / расход / перевод)."""

    __tablename__ = 'transaction'

    id: Mapped[int] = mapped_column(primary_key=True)
    account_id: Mapped[int] = mapped_column(ForeignKey('account.id'))
    category_id: Mapped[int] = mapped_column(ForeignKey('category.id'))
    # recipient необязателен: расход в магазине может не иметь получателя
    recipient_id: Mapped[int | None] = mapped_column(
        ForeignKey('recipient.id', ondelete='SET NULL'), nullable=True
    )
    amount: Mapped[float]
    type: Mapped[str] = mapped_column(
        String(10)
    )  # income / expense / transfer
    date: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    comment: Mapped[str | None] = mapped_column(String(255))

    account: Mapped['Account'] = relationship(back_populates='transactions')  # noqa
    category: Mapped['Category'] = relationship(back_populates='transactions')  # noqa
    recipient: Mapped['Recipient | None'] = relationship(  # noqa
        back_populates='transactions'
    )

    # many-to-many с Check через TransactionCheck
    check_links: Mapped[list['TransactionCheck']] = relationship(  # noqa
        back_populates='transaction',
        cascade='all, delete-orphan',
    )

    __table_args__ = (
        Index('idx_transaction_type', 'type'),
        Index('idx_transaction_date', 'date'),
        Index('idx_transaction_account', 'account_id'),
    )

    def __repr__(self) -> str:
        return (
            f'Transaction(id={self.id}, amount={self.amount:.2f}, '
            f'type={self.type!r}, date={self.date.date()})'
        )
