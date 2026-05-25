"""
Система учёта бюджета — демонстрация работы с БД.

Запуск:  python main.py
"""

from datetime import datetime

from infrastructure.database.base import Base

# импорт всех моделей, чтобы Base знала о них при create_all
from infrastructure.database.models.account import Account  # noqa
from infrastructure.database.models.category import Category  # noqa
from infrastructure.database.models.check import Check  # noqa
from infrastructure.database.models.product import Product  # noqa
from infrastructure.database.models.recipient import Recipient  # noqa
from infrastructure.database.models.transaction import Transaction  # noqa
from infrastructure.database.unit_of_work import UnitOfWork
from service.budget_service import BudgetService
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite+pysqlite:///budget.db', echo=False)
Session = sessionmaker(bind=engine)


# ──────────────────────────────────────────
# Вспомогательные функции вывода
# ──────────────────────────────────────────
def header(title: str, icon: str = '📌') -> None:
    line = '─' * 60
    print(f'\n{line}')
    print(f'  {icon}  {title}')
    print(line)


def row(label: str, value) -> None:
    print(f'  {label:<30} {value}')


# ──────────────────────────────────────────
# Заполнение тестовыми данными
# ──────────────────────────────────────────
def seed(service: BudgetService, uow: UnitOfWork) -> None:
    """Создаём все тестовые данные одной транзакцией."""

    # — Счета —
    cash = service.create_account('Наличные', 'cash',
                                  balance=5_000)
    card = service.create_account('Карта Сбербанк', 'card',
                                  balance=45_000)
    savings = service.create_account(
        'Накопительный', 'deposit', balance=100_000
    )

    # — Категории расходов —
    cat_food = service.create_category('Еда',
                                       'expense')
    cat_trans = service.create_category('Транспорт',
                                        'expense')
    cat_ent = service.create_category('Развлечения',
                                      'expense')
    cat_util = service.create_category('ЖКХ', 'expense')
    cat_health = service.create_category('Здоровье',
                                         'expense')

    # — Категории доходов —
    cat_salary = service.create_category('Зарплата',
                                         'income')
    cat_freelance = service.create_category('Фриланс',
                                            'income')

    # — Получатели —
    rec_pyat = service.create_recipient(
        'Пятёрочка', note='Продуктовый магазин'
    )
    rec_lenta = service.create_recipient('Лента', note='Гипермаркет')
    rec_ivan = service.create_recipient(
        'Иванов Петр', phone='+7-900-123-45-67', note='Друг'
    )
    rec_rent = service.create_recipient(
        'Аренда жилья', note='Ежемесячно 1-го числа'
    )
    rec_yandex = service.create_recipient('Яндекс Go', note='Такси')

    uow.commit()  # сохраняем справочники, чтобы получить ID

    # — Транзакции —
    # Доходы
    t_sal1 = service.add_transaction(  # noqa
        card.id,
        cat_salary.id,
        85_000,
        'income',
        datetime(2024, 4, 5),
        comment='Зарплата за март',
    )
    t_frl = service.add_transaction(  # noqa
        card.id,
        cat_freelance.id,
        15_000,
        'income',
        datetime(2024, 4, 12),
        comment='Проект по Python',
    )

    # Расходы с карты
    t_food1 = service.add_transaction(
        card.id,
        cat_food.id,
        3_200,
        'expense',
        datetime(2024, 4, 8),
        recipient_id=rec_pyat.id,
        comment='Недельная закупка',
    )
    t_food2 = service.add_transaction(
        card.id,
        cat_food.id,
        5_800,
        'expense',
        datetime(2024, 4, 15),
        recipient_id=rec_lenta.id,
        comment='Большой закуп на месяц',
    )
    t_util = service.add_transaction(  # noqa
        card.id,
        cat_util.id,
        6_500,
        'expense',
        datetime(2024, 4, 2),
        comment='ЖКХ апрель',
    )
    t_health = service.add_transaction(  # noqa
        card.id,
        cat_health.id,
        2_100,
        'expense',
        datetime(2024, 4, 20),
        comment='Аптека',
    )

    # Расходы наличными
    t_taxi = service.add_transaction(  # noqa
        cash.id,
        cat_trans.id,
        450,
        'expense',
        datetime(2024, 4, 9),
        recipient_id=rec_yandex.id,
        comment='Поездка в аэропорт',
    )
    t_ent = service.add_transaction(  # noqa
        cash.id,
        cat_ent.id,
        1_800,
        'expense',
        datetime(2024, 4, 14),
        comment='Кино + кафе',
    )

    # Пополнение накопительного счёта
    service.add_transaction(
        savings.id,
        cat_salary.id,
        20_000,
        'income',
        datetime(2024, 4, 5),
        comment='Откладываем на депозит',
    )
    service.add_transaction(
        savings.id,
        cat_freelance.id,
        5_000,
        'income',
        datetime(2024, 4, 12),
        comment='Бонус на накопления',
    )

    # Переводы
    t_rent = service.add_transaction(  # noqa
        card.id,
        cat_util.id,
        25_000,
        'transfer',
        datetime(2024, 4, 1),
        recipient_id=rec_rent.id,
        comment='Аренда за апрель',
    )
    t_gift = service.add_transaction(  # noqa
        card.id,
        cat_ent.id,
        3_000,
        'transfer',
        datetime(2024, 4, 22),
        recipient_id=rec_ivan.id,
        comment='Подарок на день рождения',
    )

    uow.commit()

    # — Товары —
    p_milk = service.create_product('Молоко', 'л')
    p_bread = service.create_product('Хлеб', 'шт')
    p_eggs = service.create_product('Яйца', 'шт')
    p_chicken = service.create_product('Курица', 'кг')
    p_rice = service.create_product('Рис', 'кг')
    p_oil = service.create_product('Масло подсолн.', 'л')
    p_coffee = service.create_product('Кофе молотый', 'кг')
    p_cheese = service.create_product('Сыр', 'кг')

    uow.commit()

    # — Чеки —
    # Чек 1: покупка в Пятёрочке → привязан к транзакции t_food1
    service.create_check(
        store_name='Пятёрочка',
        purchased_at=datetime(2024, 4, 8, 19, 30),
        items=[
            {'product': p_milk, 'qty': 2, 'price': 89.9},
            {'product': p_bread, 'qty': 1, 'price': 55.0},
            {'product': p_eggs, 'qty': 10, 'price': 9.5},
            {'product': p_coffee, 'qty': 0.25, 'price': 1_200},
        ],
        transaction_ids=[t_food1.id],
    )

    # Чек 2: основная закупка в Ленте → привязан к t_food2
    service.create_check(
        store_name='Лента',
        purchased_at=datetime(2024, 4, 15, 13, 0),
        items=[
            {'product': p_chicken, 'qty': 1.5, 'price': 289.0},
            {'product': p_rice, 'qty': 2, 'price': 99.9},
            {'product': p_oil, 'qty': 1, 'price': 159.0},
            {'product': p_milk, 'qty': 3, 'price': 87.0},
            {'product': p_cheese, 'qty': 0.4, 'price': 890.0},
        ],
        transaction_ids=[t_food2.id],
    )

    # Чек 3: ещё одна покупка в Пятёрочке — сплит-оплата (карта + наличные)
    # один чек, две транзакции
    t_food3a = service.add_transaction(
        card.id,
        cat_food.id,
        1_000,
        'expense',
        datetime(2024, 4, 25),
        recipient_id=rec_pyat.id,
        comment='Сплит: карта',
    )
    t_food3b = service.add_transaction(
        cash.id,
        cat_food.id,
        500,
        'expense',
        datetime(2024, 4, 25),
        recipient_id=rec_pyat.id,
        comment='Сплит: наличные',
    )
    uow.commit()

    service.create_check(
        store_name='Пятёрочка',
        purchased_at=datetime(2024, 4, 25, 10, 15),
        items=[
            {'product': p_eggs, 'qty': 10, 'price': 9.8},
            {'product': p_bread, 'qty': 2, 'price': 58.0},
            {'product': p_milk, 'qty': 4, 'price': 91.0},
        ],
        transaction_ids=[t_food3a.id, t_food3b.id],  # ← 1 чек, 2 транзакции
    )

    uow.commit()
    print('  ✅  Тестовые данные успешно загружены.')


# ──────────────────────────────────────────
# Демонстрация запросов
# ──────────────────────────────────────────
def demo(uow: UnitOfWork) -> None:
    service = BudgetService(uow)

    # ── Запрос 1: WHERE ──────────────────────────────────────────────────
    header('ЗАПРОС 1 — WHERE: расходы за период (01.04–30.04.2024)',
           '📅')
    print("  SQL: SELECT ... FROM transaction WHERE type='expense'")
    print(
        "       AND date BETWEEN '2024-04-01' AND '2024-04-30' ORDER BY "
        'date DESC\n'
    )

    txns = uow.transactions.find_by_date_range(
        start=datetime(2024, 4, 1),
        end=datetime(2024, 4, 30, 23, 59),
    )
    expense_txns = [t for t in txns if t.type == 'expense']
    print(f'  {"ID":<5} {"Сумма":>10}  {"Дата":<12}  {"Комментарий"}')
    print(f'  {"─" * 5} {"─" * 10}  {"─" * 12}  {"─" * 30}')
    for t in expense_txns:
        print(
            f'  {t.id:<5} {t.amount:>9.2f}₽  {str(t.date.date()):<12}  '
            f'{t.comment or "—"}'
        )

    # ── Запрос 2: GROUP BY + ORDER BY ────────────────────────────────────
    header('ЗАПРОС 2 — GROUP BY + ORDER BY: сводка по категориям',
           '📊')
    print('  SQL: SELECT category.name, SUM(amount), COUNT(id)')
    print(
        '       FROM transaction JOIN category ... GROUP BY category.id '
        'ORDER BY total DESC\n'
    )

    rows_cat = service.get_spending_by_category()
    print(f'  {"Категория":<20} {"Тип":<10} {"Сумма":>12}  {"Операций":>9}')
    print(f'  {"─" * 20} {"─" * 10} {"─" * 12}  {"─" * 9}')
    for r in rows_cat:
        icon = '🟢' if r['type'] == 'income' else '🔴'
        print(
            f'  {icon} {r["category"]:<18} {r["type"]:<10} '
            f'{r["total"]:>10.2f}₽  {r["count"]:>9}'
        )

    # ── Запрос 3: JOIN ───────────────────────────────────────────────────
    header(
        'ЗАПРОС 3 — JOIN: транзакции со счётом, категорией и получателем',
        '🔗'
    )
    print('  SQL: SELECT t.*, a.name, c.name, r.name FROM transaction t')
    print(
        '       JOIN account a ON ... JOIN category c ON ... LEFT JOIN '
        'recipient r ON ...\n'
    )

    details = uow.transactions.get_all_with_details()
    print(
        f'  {"ID":<4} {"Сумма":>10}  {"Тип":<10}  {"Счёт":<18}  '
        f'{"Категория":<15}  {"Получатель"}'
    )
    print(
        f'  {"─" * 4} {"─" * 10}  {"─" * 10}  {"─" * 18}  {"─" * 15}  '
        f'{"─" * 20}'
    )
    for d in details:
        print(
            f'  {d.id:<4} {d.amount:>9.2f}₽  {d.type:<10}  {d.account:<18}  '
            f'{d.category:<15}  {d.recipient or "—"}'
        )

    # ── Запрос 4: EXISTS / any() ─────────────────────────────────────────
    header(
        'ЗАПРОС 4 — EXISTS (any): категории с хотя бы одной транзакцией',
        '✅'
    )
    print('  SQL: SELECT * FROM category WHERE EXISTS')
    print(
        '       (SELECT 1 FROM transaction WHERE '
        'transaction.category_id = category.id)\n'
    )

    active_cats = uow.categories.get_categories_with_transactions()
    all_cats = uow.categories.get_all()
    print(
        f'  Всего категорий: {len(all_cats)}, активных (есть транзакции): '
        f'{len(active_cats)}\n'
    )
    for c in active_cats:
        print(f'  ✔  {c.name} ({c.type})')

    # ── Запрос 5: GROUP BY + JOIN (топ получателей) ───────────────────────
    header('ЗАПРОС 5 — GROUP BY + JOIN: топ получателей по сумме',
           '👥')
    print('  SQL: SELECT r.name, COUNT(t.id), SUM(t.amount) FROM recipient r')
    print(
        '       JOIN transaction t ON ... GROUP BY r.id '
        'ORDER BY total DESC LIMIT 5\n'
    )

    top_rec = service.get_top_recipients()
    print(f'  {"#":<3} {"Получатель":<20} {"Операций":>9}  {"Итого":>12}')
    print(f'  {"─" * 3} {"─" * 20} {"─" * 9}  {"─" * 12}')
    for i, r in enumerate(top_rec, 1):
        print(
            f'  {i:<3} {r["recipient"]:<20} {r["count"]:>9}  '
            f'{r["total"]:>10.2f}₽'
        )

    # ── Запрос 6: GROUP BY + JOIN (чеки с суммами) ────────────────────────
    header('ЗАПРОС 6 — GROUP BY + JOIN: чеки с итоговыми суммами',
           '🧾')
    print(
        '  SQL: SELECT r.store_name, COUNT(ri.product_id), '
        'SUM(ri.quantity * ri.price)'
    )
    print(
        '       FROM check r JOIN check_product_association ri ON ... '
        'GROUP BY r.id ORDER BY total DESC\n'
    )

    checks = service.get_check_totals()
    print(
        f'  {"ID":<4} {"Магазин":<15}  {"Дата":<12}  {"Позиций":>7}  '
        f'{"Итого":>12}'
    )
    print(f'  {"─" * 4} {"─" * 15}  {"─" * 12}  {"─" * 7}  {"─" * 12}')
    for r in checks:
        print(
            f'  {r["id"]:<4} {r["store"]:<15}  {str(r["date"].date()):<12}  '
            f'{r["items"]:>7}  {r["total"]:>10.2f}₽'
        )

    # ── Запрос 7: GROUP BY + ORDER BY (топ товаров) ───────────────────────
    header('ЗАПРОС 7 — GROUP BY + ORDER BY: топ покупаемых товаров',
           '🛒')
    print(
        '  SQL: SELECT p.name, COUNT(ri.check_id), SUM(ri.quantity), '
        'AVG(ri.price)'
    )
    print(
        '       FROM product p JOIN check_product_association ri '
        'ON ... GROUP BY p.id ORDER BY times DESC\n'
    )

    top_prod = service.get_top_products(limit=5)
    print(
        f'  {"#":<3} {"Товар":<22} {"Ед.":<6} {"Покупок":>7}  '
        f'{"Кол-во":>8}  {"Ср. цена":>10}'
    )
    print(f'  {"─" * 3} {"─" * 22} {"─" * 6} {"─" * 7}  {"─" * 8}  {"─" * 10}')
    for i, p in enumerate(top_prod, 1):
        print(
            f'  {i:<3} {p["name"]:<22} {p["unit"]:<6} {p["times"]:>7}  '
            f'{p["total_qty"]:>8.2f}  {p["avg_price"]:>8.2f}₽'
        )

    # ── Запрос 8: EXISTS (has) ────────────────────────────────────────────
    header('ЗАПРОС 8 — EXISTS (has): транзакции с расходной категорией',
           '🔍')
    print('  SQL: SELECT * FROM transaction WHERE EXISTS')
    print(
        '       (SELECT 1 FROM category WHERE '
        'category.id = transaction.category_id'
    )
    print("        AND category.type = 'expense')\n")

    exp_txns = uow.transactions.find_transactions_with_expense_category()
    print(f'  Найдено транзакций с категорией-расходом: {len(exp_txns)}')
    for t in exp_txns[:5]:
        print(f'  → id={t.id}  {t.amount:.2f}₽  {t.comment or "—"}')
    if len(exp_txns) > 5:
        print(f'  ... и ещё {len(exp_txns) - 5} транзакций')

    # ── Запрос 9: WHERE + HAVING ──────────────────────────────────────────
    header(
        'ЗАПРОС 9 — WHERE + HAVING: категории расходов суммой > 3000₽',
        '💸'
    )
    print(
        '  SQL: SELECT c.name, SUM(t.amount) FROM category c '
        'JOIN transaction t ON ...'
    )
    print(
        "       WHERE t.type='expense' GROUP BY c.id "
        'HAVING SUM(t.amount) > 3000\n'
    )

    heavy = uow.categories.get_expense_categories_above(3_000)
    for name, total in heavy:
        print(f'  🔺  {name:<20}  {total:>10.2f}₽')

    # ── Запрос 10: Каскадное удаление ─────────────────────────────────────
    header('ЗАПРОС 10 — DEMO: каскадное удаление счёта', '🗑️')
    print(
        '  Удаляем счёт "Накопительный" → его транзакции '
        'удалятся автоматически\n'
    )
    savings = uow.accounts.find_by_name('Накопительный')
    before = uow.transactions.count()
    uow.accounts.delete(savings)
    uow.commit()
    after = uow.transactions.count()
    print(f'  Транзакций до удаления:   {before}')
    print(f'  Транзакций после удаления: {after}')
    print(f'  Каскадно удалено: {before - after} транзакций')

    print('\n' + '─' * 60)
    print('  🎉  Все запросы выполнены успешно!')
    print('─' * 60 + '\n')


# ──────────────────────────────────────────
# Точка входа
# ──────────────────────────────────────────
def main() -> None:
    # Создаём все таблицы (если не существуют)
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    print('\n' + '═' * 60)
    print('        💰  СИСТЕМА УЧЁТА БЮДЖЕТА  💰')
    print('═' * 60)

    # Заполняем данными
    header('Загрузка тестовых данных', '📦')
    with UnitOfWork(Session) as uow:
        service = BudgetService(uow)
        seed(service, uow)

    # Демонстрируем запросы
    with UnitOfWork(Session) as uow:
        demo(uow)


if __name__ == '__main__':
    main()
