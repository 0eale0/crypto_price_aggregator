from local_configs import Configuration
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine(Configuration.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
