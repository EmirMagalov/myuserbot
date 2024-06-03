from sqlalchemy import String,Text
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column

class Base(DeclarativeBase):
    pass


class Like(Base):
    __tablename__ = "like"

    id: Mapped[int] = mapped_column(primary_key=True,autoincrement=True)
    username:Mapped[str]=mapped_column(String(150))
    value:Mapped[int]