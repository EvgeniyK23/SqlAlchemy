from datetime import datetime

from infrastructure.database.models.account import Account
from infrastructure.database.models.category import Category
from infrastructure.database.models.check import Check
from infrastructure.database.models.check_product_association import (
    CheckProductAssociation,
)
from infrastructure.database.models.product import Product
from infrastructure.database.models.recipient import Recipient
from infrastructure.database.models.transaction import Transaction
from infrastructure.database.models.transaction_check_association import (
    TransactionCheck,
)
from infrastructure.database.unit_of_work import UnitOfWork


class BudgetService:
    """Бизнес-логика для управления бюджетом.

    Работает исключительно через UnitOfWork и репозитории,
    не знает ничего про SQL напрямую.
    """

    def __init__(self, uow: UnitOfWork):
        self.uow = uow

    # ──────────────────────────────────────────
    # Счета
    # ──────────────────────────────────────────

    def create_account(
        self, name: str, account_type: str, balance: float = 0.0
    ) -> Account:
        """Создать новый счёт."""
        existing = self.uow.accounts.find_by_name(name)
        if existing:
            raise ValueError(f'Счёт с именем "{name}" уже существует.')
        account = Account(name=name, type=account_type, balance=balance)
        self.uow.accounts.add(account)
        return account

    # ──────────────────────────────────────────
    # Категории
    # ──────────────────────────────────────────

    def create_category(self, name: str, category_type: str) -> Category:
        """Создать категорию (income / expense)."""
        category = Category(name=name, type=category_type)
        self.uow.categories.add(category)
        return category

    # ──────────────────────────────────────────
    # Получатели
    # ──────────────────────────────────────────

    def create_recipient(
        self, name: str, phone: str = None, note: str = None
    ) -> Recipient:
        """Зарегистрировать получателя перевода."""
        recipient = Recipient(name=name, phone=phone, note=note)
        self.uow.recipients.add(recipient)
        return recipient

    # ──────────────────────────────────────────
    # Транзакции
    # ──────────────────────────────────────────

    def add_transaction(
        self,
        account_id: int,
        category_id: int,
        amount: float,
        txn_type: str,
        date: datetime = None,
        recipient_id: int = None,
        comment: str = None,
    ) -> Transaction:
        """Добавить транзакцию и обновить баланс счёта."""
        account = self.uow.accounts.get(account_id)
        if not account:
            raise ValueError(f'Счёт {account_id} не найден.')

        txn = Transaction(
            account_id=account_id,
            category_id=category_id,
            recipient_id=recipient_id,
            amount=amount,
            type=txn_type,
            date=date or datetime.now(),
            comment=comment,
        )
        self.uow.transactions.add(txn)

        # обновляем баланс
        if txn_type == 'income':
            account.balance += amount
        elif txn_type == 'expense':
            account.balance -= amount

        return txn

    # ──────────────────────────────────────────
    # Чеки и товары
    # ──────────────────────────────────────────

    def create_product(self, name: str, unit: str) -> Product:
        """Добавить товар в справочник."""
        product = Product(name=name, unit=unit)
        self.uow.products.add(product)
        return product

    def create_check(
        self,
        store_name: str,
        purchased_at: datetime,
        items: list[dict],  # [{'product': Product, 'qty': 1.0, 'price': 99.9}]
        transaction_ids: list[int] = None,
    ) -> Check:
        """Создать чек с позициями и привязать к транзакциям.

        Args:
            store_name: Название магазина.
            purchased_at: Дата и время покупки.
            items: Список позиций {'product': Product, 'qty': float,
            'price': float}.
            transaction_ids: ID транзакций, к которым привязан чек.
        """
        check = Check(store_name=store_name, purchased_at=purchased_at)
        self.uow.checks.add(check)

        for item in items:
            ri = CheckProductAssociation(
                check=check,
                product=item['product'],
                quantity=item['qty'],
                price=item['price'],
            )
            self.uow.session.add(ri)

        if transaction_ids:
            for txn_id in transaction_ids:
                link = TransactionCheck(check=check, transaction_id=txn_id)
                self.uow.session.add(link)

        return check

    # ──────────────────────────────────────────
    # Аналитика (делегируем репозиториям)
    # ──────────────────────────────────────────

    def get_spending_by_category(self) -> list[dict]:
        """Расходы и доходы по категориям (сводка)."""
        rows = self.uow.categories.get_spending_by_category()
        return [
            {
                'category': r.name,
                'type': r.type,
                'total': r.total,
                'count': r.txn_count,
            }
            for r in rows
        ]

    def get_top_recipients(self, limit: int = 5) -> list[dict]:
        """Топ получателей по сумме переводов."""
        rows = self.uow.recipients.get_top_recipients_by_amount(limit)
        return [
            {'recipient': r.name, 'count': r.txn_count, 'total': r.total}
            for r in rows
        ]

    def get_check_totals(self) -> list[dict]:
        """Все чеки с итоговыми суммами."""
        rows = self.uow.checks.get_all_with_totals()
        return [
            {
                'id': r.id,
                'store': r.store_name,
                'date': r.purchased_at,
                'items': r.items_count,
                'total': r.total,
            }
            for r in rows
        ]

    def get_top_products(self, limit: int = 5) -> list[dict]:
        """Самые покупаемые товары."""
        rows = self.uow.products.get_top_products(limit)
        return [
            {
                'name': r.name,
                'unit': r.unit,
                'times': r.times_bought,
                'total_qty': r.total_qty,
                'avg_price': r.avg_price,
            }
            for r in rows
        ]

    def update_account_balance(self, account_id: int, amount: float) -> None:
        """Обновить баланс счета."""
        account = self.uow.accounts.get(account_id)
        account.balance = amount
