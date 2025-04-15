from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///titles.db', echo=True)
Session = sessionmaker(engine)
