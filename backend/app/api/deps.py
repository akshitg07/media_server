from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.db.session import get_db
from app.models.models import User


def get_current_user(db: Session = Depends(get_db)) -> User:
    """
    Authentication disabled mode:
    always returns a persistent local guest user.
    """
    guest = db.scalar(select(User).where(User.username == "guest"))
    if guest:
        return guest

    guest = User(username="guest", password_hash="disabled", is_admin=True)
    db.add(guest)
    db.commit()
    db.refresh(guest)
    return guest
