from infrastructure.database.base import Base  # noqa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class CheckProductAssociation(Base):
    """Позиция в чеке: Чек ↔ Товар (many-to-many с доп. данными).

    Хранит количество и цену на момент покупки — они могут
    меняться от чека к чеку для одного и того же товара.
    """

    __tablename__ = 'check_product_association'

    check_id: Mapped[int] = mapped_column(
        ForeignKey('check.id', ondelete='CASCADE'), primary_key=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE'), primary_key=True
    )
    quantity: Mapped[float]
    price: Mapped[float]  # цена за единицу

    check: Mapped['Check'] = relationship(back_populates='items')  # noqa
    product: Mapped['Product'] = relationship(  # noqa
        back_populates='check_product_associations'
    )

    @property
    def subtotal(self) -> float:
        return self.quantity * self.price

    def __repr__(self) -> str:
        return (
            f'CheckProductAssociation(check={self.check_id}, '
            f'product={self.product_id}, qty={self.quantity}, '
            f'price={self.price:.2f})'
        )
