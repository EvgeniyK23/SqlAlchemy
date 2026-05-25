from sqlalchemy import func, select
from sqlalchemy.orm import Session, selectinload

from infrastructure.database.models.check import Check
from infrastructure.database.models.check_product_association import CheckProductAssociation
from infrastructure.database.models.product import Product
from infrastructure.database.repository.base_repository import BaseRepository


class CheckRepository(BaseRepository[Check]):
    """Репозиторий для работы с чеками."""

    def __init__(self, session: Session):
        super().__init__(session, Check)

    def get_with_items(self, check_id: int) -> Check | None:
        """JOIN (selectinload) — чек со всеми позициями и товарами."""
        return self.session.execute(
            select(Check)
            .where(Check.id == check_id)
            .options(
                selectinload(Check.items).selectinload(CheckProductAssociation.product)
            )
        ).scalar_one_or_none()

    def get_all_with_totals(self) -> list[tuple]:
        """GROUP BY + ORDER BY + JOIN — все чеки с суммой и кол-вом позиций.

        Возвращает: (магазин, дата, кол-во позиций, итоговая сумма).
        """
        return self.session.execute(
            select(
                Check.id,
                Check.store_name,
                Check.purchased_at,
                func.count(CheckProductAssociation.product_id).label('items_count'),
                func.sum(CheckProductAssociation.quantity * CheckProductAssociation.price).label('total'),
            )
            .join(CheckProductAssociation, CheckProductAssociation.check_id == Check.id)
            .group_by(Check.id, Check.store_name, Check.purchased_at)
            .order_by(func.sum(CheckProductAssociation.quantity * CheckProductAssociation.price).desc())
        ).all()

    def find_by_store(self, store_name: str) -> list[Check]:
        """WHERE — найти чеки по названию магазина."""
        return (
            self.session.execute(
                select(Check)
                .where(Check.store_name.ilike(f'%{store_name}%'))
                .order_by(Check.purchased_at.desc())
            )
            .scalars()
            .all()
        )

    def get_checks_with_product(self, product_name: str) -> list[tuple]:
        """JOIN + WHERE — чеки, в которых есть конкретный товар."""
        return self.session.execute(
            select(
                Check.store_name,
                Check.purchased_at,
                Product.name.label('product'),
                CheckProductAssociation.quantity,
                CheckProductAssociation.price,
            )
            .join(CheckProductAssociation, CheckProductAssociation.check_id == Check.id)
            .join(Product, Product.id == CheckProductAssociation.product_id)
            .where(Product.name.ilike(f'%{product_name}%'))
            .order_by(Check.purchased_at.desc())
        ).all()
