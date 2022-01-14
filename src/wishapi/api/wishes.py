from fastapi import APIRouter, Depends, Response, status
from typing import List

from ..services.wishes import WishService
from ..services.auth import get_current_user
from ..models.wishes import Wish, WishCreate, WishUpdate
from ..models.auth import User

router = APIRouter(
    prefix='/wish',
    tags=['wishes'],
)


@router.get('/', response_model=List[Wish])
def get_wishes(service: WishService = Depends(),
               user: User = Depends(get_current_user)):
    return service.get_list(user_id=user.id)


@router.get('/{wish_id}', response_model=Wish)
def get_wish(wish_id: int,
             service: WishService = Depends(),
             user: User = Depends(get_current_user)):
    return service.get(wish_id=wish_id, user_id=user.id)


@router.post('/', response_model=Wish)
def create_wish(wish_data: WishCreate,
                service: WishService = Depends(),
                user: User = Depends(get_current_user)):
    return service.create(wish_data=wish_data, user_id=user.id)


@router.put('/{wish_id}', response_model=Wish)
def update_wish(wish_id: int,
                wish_data: WishUpdate,
                service: WishService = Depends(),
                user: User = Depends(get_current_user)):
    return service.update(wish_id=wish_id,
                          wish_data=wish_data,
                          user_id=user.id)


@router.delete('/{wish_id}')
def delete_wish(wish_id: int,
                service: WishService = Depends(),
                user: User = Depends(get_current_user)):
    service.delete(wish_id=wish_id, user_id=user.id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
