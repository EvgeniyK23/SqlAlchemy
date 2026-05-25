from datetime import datetime

from infrastructure.database.models.account import Account
from infrastructure.database.models.category import Category
from infrastructure.database.models.recipient import Recipient
from infrastructure.database.models.transaction import Transaction
from infrastructure.database.repository.base_repository import BaseRepository
from sqlalchemy import func, select
from sqlalchemy.orm import Session, joinedload


class TransactionRepository(BaseRepository[Transaction]):
    """Репозиторий для работы с транзакциями."""

    def __init__(self, session: Session):
        super().__init__(session, Transaction)

    # ──────────────────────────────────────────
    # WHERE
    # ──────────────────────────────────────────

    def find_by_type(self, txn_type: str) -> list[Transaction]:
        """WHERE — найти транзакции по типу (income / expense / transfer)."""
        return (
            self.session
            .execute(
                select(Transaction)
                .where(Transaction.type == txn_type)
                .order_by(Transaction.date.desc())
            )
            .scalars()
            .all()
        )

    def find_by_date_range(
        self, start: datetime, end: datetime
    ) -> list[Transaction]:
        """WHERE — транзакции за указанный период, свежие первыми."""
        return (
            self.session
            .execute(
                select(Transaction)
                .where(Transaction.date >= start, Transaction.date <= end)
                .order_by(Transaction.date.desc())
            )
            .scalars()
            .all()
        )

    def find_expenses_above(self, amount: float) -> list[Transaction]:
        """WHERE + ORDER BY — расходы дороже указанной суммы."""
        return (
            self.session
            .execute(
                select(Transaction)
                .where(
                    Transaction.type == 'expense', Transaction.amount > amount
                )
                .order_by(Transaction.amount.desc())
            )
            .scalars()
            .all()
        )

    # ──────────────────────────────────────────
    # JOIN
    # ──────────────────────────────────────────

    def get_all_with_details(self) -> list[tuple]:
        """JOIN — все транзакции с данными счёта, категории и получателя.

        Используем joinedload для eager-загрузки связей.
        Возвращает: (id, сумма, тип, дата, счёт, категория, получатель).
        """
        return self.session.execute(
            select(
                Transaction.id,
                Transaction.amount,
                Transaction.type,
                Transaction.date,
                Transaction.comment,
                Account.name.label('account'),
                Category.name.label('category'),
                Recipient.name.label('recipient'),
            )
            .join(Account, Transaction.account_id == Account.id)
            .join(Category, Transaction.category_id == Category.id)
            .outerjoin(Recipient, Transaction.recipient_id == Recipient.id)
            .order_by(Transaction.date.desc())
        ).all()

    def get_with_relations(self, txn_id: int) -> Transaction | None:
        """JOIN (joinedload) — одна транзакция со всеми связанными
        объектами."""
        return self.session.execute(
            select(Transaction)
            .where(Transaction.id == txn_id)
            .options(
                joinedload(Transaction.account),
                joinedload(Transaction.category),
                joinedload(Transaction.recipient),
            )
        ).scalar_one_or_none()

    # ──────────────────────────────────────────
    # GROUP BY + ORDER BY
    # ──────────────────────────────────────────

    def get_monthly_summary(self) -> list[tuple]:
        """GROUP BY + ORDER BY — сводка доходов и расходов по месяцам.

        Возвращает: (год, месяц, тип, общая сумма).
        """
        return self.session.execute(
            select(
                func.strftime('%Y', Transaction.date).label('year'),
                func.strftime('%m', Transaction.date).label('month'),
                Transaction.type,
                func.sum(Transaction.amount).label('total'),
            )
            .group_by('year', 'month', Transaction.type)
            .order_by('year', 'month', Transaction.type)
        ).all()

    # ──────────────────────────────────────────
    # EXISTS / has()
    # ──────────────────────────────────────────

    def find_transactions_with_expense_category(self) -> list[Transaction]:
        """EXISTS / has() — транзакции, категория которых является расходной.

        relationship.has() → транслируется в EXISTS подзапрос.
        """
        return (
            self.session
            .execute(
                select(Transaction).where(
                    Transaction.category.has(Category.type == 'expense')
                )
            )
            .scalars()
            .all()
        )

    def update_comment(self, txn_id: int, comment: str) -> Transaction | None:
        """Обновить комментарий к транзакции."""
        txn = self.get(txn_id)
        if txn:
            txn.comment = comment
        return txn
