import datetime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String, Date
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


class Title(Base):
    __tablename__ = 'title'

    id: Mapped[str] = mapped_column(primary_key=True, autoincrement=False)
    url: Mapped[str] = mapped_column(String)
    img_url: Mapped[str] = mapped_column(String)
    release_date: Mapped[datetime.date] = mapped_column(Date)

    def __repr__(self) -> str:
        return f'Title(id={self.id!r}, url={self.url!r}, img_url={self.img_url!r}, release_date={self.release_date!r})'