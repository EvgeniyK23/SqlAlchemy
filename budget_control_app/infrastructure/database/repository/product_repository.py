from infrastructure.database.models.check_product_association import (
    CheckProductAssociation,
)
from infrastructure.database.models.product import Product
from infrastructure.database.repository.base_repository import BaseRepository
from sqlalchemy import func, select
from sqlalchemy.orm import Session


class ProductRepository(BaseRepository[Product]):
    """Репозиторий для работы с товарами."""

    def __init__(self, session: Session):
        super().__init__(session, Product)

    def find_by_name(self, name: str) -> Product | None:
        """WHERE — найти товар по названию."""
        return self.session.execute(
            select(Product).where(Product.name.ilike(f'%{name}%'))
        ).scalar_one_or_none()

    def get_top_products(self, limit: int = 5) -> list[tuple]:
        """GROUP BY + ORDER BY + JOIN — топ товаров по частоте покупок.

        Возвращает: (название, единица, кол-во покупок, суммарное кол-во,
        средняя цена).
        """
        return self.session.execute(
            select(
                Product.name,
                Product.unit,
                func.count(CheckProductAssociation.check_id).label(
                    'times_bought'
                ),
                func.sum(CheckProductAssociation.quantity).label('total_qty'),
                func.avg(CheckProductAssociation.price).label('avg_price'),
            )
            .join(
                CheckProductAssociation,
                CheckProductAssociation.product_id == Product.id,
            )
            .group_by(Product.id, Product.name, Product.unit)
            .order_by(func.count(CheckProductAssociation.check_id).desc())
            .limit(limit)
        ).all()

    def get_products_with_checks(self) -> list[Product]:
        """EXISTS / any() — товары, которые хотя бы раз покупали."""
        return (
            self.session
            .execute(
                select(Product).where(Product.check_product_associations.any())
            )
            .scalars()
            .all()
        )

    def get_expensive_products(self, min_price: float) -> list[tuple]:
        """WHERE + GROUP BY + ORDER BY — товары, средняя цена которых
        выше порога."""
        return self.session.execute(
            select(
                Product.name,
                Product.unit,
                func.avg(CheckProductAssociation.price).label('avg_price'),
            )
            .join(
                CheckProductAssociation,
                CheckProductAssociation.product_id == Product.id,
            )
            .group_by(Product.id, Product.name, Product.unit)
            .having(func.avg(CheckProductAssociation.price) > min_price)
            .order_by(func.avg(CheckProductAssociation.price).desc())
        ).all()
