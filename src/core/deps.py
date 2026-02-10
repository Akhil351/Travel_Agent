from typing import Annotated
from fastapi import Depends
from sqlalchemy.orm import Session

from src.database import get_db_session


# DB Dependency
def get_db():
    db = get_db_session()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]
