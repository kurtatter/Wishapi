from sqlalchemy.orm import Session

from fastapi import Depends, HTTPException, status
from typing import List, Optional

from .. import tables
from ..database import get_session
from ..models.wishes import Wish, WishCreate, WishUpdate


class WishService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, user_id: int, wish_id: int) -> tables.Wish:
        wish = (
            self.session
                .query(tables.Wish)
                .filter_by(id=wish_id, user_id=user_id)
                .first()
        )

        if not wish:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return wish

    def get_list(self, user_id: int) -> List[Wish]:
        wishes = (
            self.session
            .query(tables.Wish)
            .filter_by(user_id=user_id)
            .all()
        )
        if not wishes:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return wishes

    def get(self, user_id: int, wish_id: int) -> tables.Wish:
        return self._get(user_id=user_id,
                         wish_id=wish_id)

    def create(self, user_id: int, wish_data: WishCreate) -> tables.Wish:
        wish = tables.Wish(
            **wish_data.dict(),
            user_id=user_id
        )
        self.session.add(wish)
        self.session.commit()
        return wish

    def create_many(self, user_id: int,
                    wishes_data: List[WishCreate]) -> List[tables.Wish]:
        wishes = [
            tables.Wish(**wish_data.dict(), user_id=user_id) for wish_data in wishes_data
        ]
        self.session.add_all(wishes)
        self.session.commit()
        return wishes

    def update(self, user_id: int, wish_id: int, wish_data: WishUpdate) -> tables.Wish:
        wish = self._get(user_id, wish_id)
        for field, value in wish_data:
            setattr(wish, field, value)
        self.session.commit()
        return wish

    def delete(self, user_id: int, wish_id: int):
        wish = self._get(user_id, wish_id)
        self.session.delete(wish)
        self.session.commit()
