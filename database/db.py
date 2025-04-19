from datetime import date

from sqlalchemy import create_engine, select, insert
from sqlalchemy.orm import sessionmaker

from database.models import Title


engine = create_engine('sqlite:///titles.db', echo=True)
Session = sessionmaker(engine)


def fetch_cmoa_results() -> list[tuple]:
    titles = []
    with Session.begin() as session:
        titles.extend(session.execute(select(Title)).all())
        session.expunge_all()

    return titles


def delete_title(id: str) -> bool:
    with Session.begin() as session:
        title = session.get(Title, id)
        if title:
            session.delete(title)
            return True
    return False


def add_title(data: dict):
    with Session.begin() as session:
        title = Title(
            id=data['id'],
            url=data['url'],
            img_url=data['img_url'],
            release_date=data['release_date']
        )
        exist = session.get(Title, data['id'])
        if not exist:
            session.add(title)
            return True
    return False