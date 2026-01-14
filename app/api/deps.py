from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.security import require_api_key
from app.db.session import get_db


def auth_dep():
    return Depends(require_api_key)


def db_dep():
    return Depends(get_db)


def get_authed_db(db: Session = Depends(get_db), _: None = Depends(require_api_key)) -> Session:
    return db
