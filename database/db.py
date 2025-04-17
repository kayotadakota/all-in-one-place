from sqlalchemy import create_engine, select
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