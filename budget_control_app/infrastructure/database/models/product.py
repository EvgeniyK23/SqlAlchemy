from infrastructure.database.base import Base  # noqa
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Product(Base):
    """Товар из справочника (накапливает историю покупок)."""

    __tablename__ = 'product'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    unit: Mapped[str] = mapped_column(String(20))  # шт / кг / л / упак

    # при удалении товара — удаляем все его позиции в чеках
    check_product_associations: Mapped[list['CheckProductAssociation']] = (  # noqa
        relationship(
            back_populates='product',
            cascade='all, delete-orphan',
        )
    )

    def __repr__(self) -> str:
        return f'Product(id={self.id}, name={self.name!r}, unit={self.unit!r})'
