from infrastructure.database.models.recipient import Recipient
from infrastructure.database.models.transaction import Transaction
from infrastructure.database.repository.base_repository import BaseRepository
from sqlalchemy import func, select
from sqlalchemy.orm import Session


class RecipientRepository(BaseRepository[Recipient]):
    """Репозиторий для работы с получателями переводов."""

    def __init__(self, session: Session):
        super().__init__(session, Recipient)

    def find_by_name(self, name: str) -> Recipient | None:
        """WHERE — найти получателя по имени."""
        return self.session.execute(
            select(Recipient).where(Recipient.name == name)
        ).scalar_one_or_none()

    def get_top_recipients_by_amount(self, limit: int = 5) -> list[tuple]:
        """GROUP BY + ORDER BY + JOIN — топ получателей по сумме переводов.

        Возвращает: (имя, кол-во переводов, общая сумма).
        """
        return self.session.execute(
            select(
                Recipient.name,
                func.count(Transaction.id).label('txn_count'),
                func.sum(Transaction.amount).label('total'),
            )
            .join(Transaction, Transaction.recipient_id == Recipient.id)
            .group_by(Recipient.id, Recipient.name)
            .order_by(func.sum(Transaction.amount).desc())
            .limit(limit)
        ).all()

    def get_recipients_with_transfers(self) -> list[Recipient]:
        """EXISTS / any() — получатели, которым был хотя бы один перевод."""
        return (
            self.session
            .execute(
                select(Recipient).where(
                    Recipient.transactions.any(Transaction.type == 'transfer')
                )
            )
            .scalars()
            .all()
        )
