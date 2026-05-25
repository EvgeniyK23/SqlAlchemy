from sqlalchemy import func, select
from sqlalchemy.orm import Session

from infrastructure.database.models.category import Category
from infrastructure.database.models.transaction import Transaction
from infrastructure.database.repository.base_repository import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    """Репозиторий для работы с категориями."""

    def __init__(self, session: Session):
        super().__init__(session, Category)

    def find_by_type(self, category_type: str) -> list[Category]:
        """WHERE — найти категории по типу (income / expense)."""
        return (
            self.session.execute(
                select(Category).where(Category.type == category_type)
            )
            .scalars()
            .all()
        )

    def get_spending_by_category(self) -> list[tuple]:
        """GROUP BY + ORDER BY + JOIN — расходы по категориям.

        Возвращает: (название, тип, сумма, кол-во транзакций),
        отсортированные по убыванию суммы.
        """
        return self.session.execute(
            select(
                Category.name,
                Category.type,
                func.sum(Transaction.amount).label('total'),
                func.count(Transaction.id).label('txn_count'),
            )
            .join(Transaction, Transaction.category_id == Category.id)
            .group_by(Category.id, Category.name, Category.type)
            .order_by(func.sum(Transaction.amount).desc())
        ).all()

    def get_categories_with_transactions(self) -> list[Category]:
        """EXISTS / any() — категории, у которых есть хотя бы одна транзакция."""
        return (
            self.session.execute(
                select(Category).where(Category.transactions.any())
            )
            .scalars()
            .all()
        )

    def get_expense_categories_above(self, min_total: float) -> list[tuple]:
        """GROUP BY + HAVING (WHERE на агрегат) — категории расходов,
        суммарная трата по которым превышает min_total.
        """
        return self.session.execute(
            select(
                Category.name,
                func.sum(Transaction.amount).label('total'),
            )
            .join(Transaction, Transaction.category_id == Category.id)
            .where(Transaction.type == 'expense')
            .group_by(Category.id, Category.name)
            .having(func.sum(Transaction.amount) > min_total)
            .order_by(func.sum(Transaction.amount).desc())
        ).all()
