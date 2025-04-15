from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///titles.db')
Session = sessionmaker(engine)

# with Session().begin() as session: