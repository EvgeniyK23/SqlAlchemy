from infrastructure.database.base import Base  # noqa
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Category(Base):
    """Категория транзакции (Еда, Транспорт, Зарплата и т.д.)."""

    __tablename__ = 'category'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    type: Mapped[str] = mapped_column(String(10))  # income / expense

    # при удалении категории — удаляем все связанные транзакции
    transactions: Mapped[list['Transaction']] = relationship(  # noqa
        back_populates='category',
        cascade='all, delete-orphan',
    )

    def __repr__(self) -> str:
        return (
            f'Category(id={self.id}, name={self.name!r}, type={self.type!r})'
        )
