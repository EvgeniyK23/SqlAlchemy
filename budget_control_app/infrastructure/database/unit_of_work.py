from infrastructure.database.repository.account_repository import (
    AccountRepository,
)
from infrastructure.database.repository.category_repository import (
    CategoryRepository,
)
from infrastructure.database.repository.check_repository import CheckRepository
from infrastructure.database.repository.product_repository import (
    ProductRepository,
)
from infrastructure.database.repository.recipient_repository import (
    RecipientRepository,
)
from infrastructure.database.repository.transaction_repository import (
    TransactionRepository,
)
from sqlalchemy.orm import Session


class UnitOfWork:
    """Unit of Work — управляет сессией БД и предоставляет доступ ко всем
    репозиториям. Гарантирует атомарность операций через commit/rollback.

    Использование:
        with UnitOfWork(Session) as uow:
            uow.transactions.add(...)
            uow.commit()
    """

    def __init__(self, session_factory):
        self.session_factory = session_factory
        self._session: Session | None = None
        # репозитории инициализируются лениво при первом обращении
        self._accounts = None
        self._categories = None
        self._recipients = None
        self._transactions = None
        self._checks = None
        self._products = None

    def __enter__(self) -> 'UnitOfWork':
        self._session = self.session_factory()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._session.commit()
        else:
            self._session.rollback()
        self._session.close()
        self._session = None

    @property
    def session(self) -> Session:
        if self._session is None:
            raise RuntimeError(
                'UnitOfWork не активен. '
                'Используйте контекстный менеджер (with).'
            )
        return self._session

    # ──────────────────────────────────────────
    # Репозитории (ленивая инициализация)
    # ──────────────────────────────────────────

    @property
    def accounts(self) -> AccountRepository:
        if self._accounts is None:
            self._accounts = AccountRepository(self.session)
        return self._accounts

    @property
    def categories(self) -> CategoryRepository:
        if self._categories is None:
            self._categories = CategoryRepository(self.session)
        return self._categories

    @property
    def recipients(self) -> RecipientRepository:
        if self._recipients is None:
            self._recipients = RecipientRepository(self.session)
        return self._recipients

    @property
    def transactions(self) -> TransactionRepository:
        if self._transactions is None:
            self._transactions = TransactionRepository(self.session)
        return self._transactions

    @property
    def checks(self) -> CheckRepository:
        if self._checks is None:
            self._checks = CheckRepository(self.session)
        return self._checks

    @property
    def products(self) -> ProductRepository:
        if self._products is None:
            self._products = ProductRepository(self.session)
        return self._products

    # ──────────────────────────────────────────
    # Управление транзакцией
    # ──────────────────────────────────────────

    def commit(self) -> None:
        """Зафиксировать изменения в БД."""
        self._session.commit()
        # сбрасываем кеш репозиториев после коммита
        self._accounts = None
        self._categories = None
        self._recipients = None
        self._transactions = None
        self._checks = None
        self._products = None

    def rollback(self) -> None:
        """Откатить все изменения текущей транзакции."""
        self._session.rollback()
