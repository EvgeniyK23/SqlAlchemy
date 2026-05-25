from infrastructure.database.models.account import Account
from infrastructure.database.models.transaction import Transaction
from infrastructure.database.repository.base_repository import BaseRepository
from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload


class AccountRepository(BaseRepository[Account]):
    """Репозиторий для работы со счетами."""

    def __init__(self, session: Session):
        super().__init__(session, Account)

    def find_by_name(self, name: str) -> Account | None:
        """WHERE — найти счёт по названию."""
        return self.session.execute(
            select(Account).where(Account.name == name)
        ).scalar_one_or_none()

    def get_with_transactions(self, account_id: int) -> Account | None:
        """JOIN (selectinload) — счёт вместе со всеми транзакциями."""
        return self.session.execute(
            select(Account)
            .where(Account.id == account_id)
            .options(selectinload(Account.transactions))
        ).scalar_one_or_none()

    def get_accounts_with_expenses(self) -> list[Account]:
        """EXISTS / any() — счета, у которых есть хотя бы одна
        транзакция-расход.

        Использует relationship.any() → транслируется в EXISTS подзапрос.
        """
        return (
            self.session
            .execute(
                select(Account).where(
                    Account.transactions.any(Transaction.type == 'expense')
                )
            )
            .scalars()
            .all()
        )

    def update_balance(
        self, account_id: int, new_balance: float
    ) -> Account | None:
        """Обновить баланс счёта."""
        account = self.get(account_id)
        if account:
            account.balance = new_balance
        return account
