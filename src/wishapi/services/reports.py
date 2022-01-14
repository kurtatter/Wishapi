import csv
from io import StringIO

from fastapi import Depends
from typing import Any

from .wishes import WishService
from ..models.wishes import Wish, WishCreate


class ReportsService:
    def __init__(self, wishes_service: WishService = Depends()):
        self.wishes_service = wishes_service

    def import_csv(self, user_id: int, file: Any):
        reader = csv.DictReader(
            (line.decode() for line in file),
            fieldnames=[
                'date',
                'title',
                'url',
                'price',
                'description',
            ]
        )

        wishes = []

        next(reader)
        for row in reader:
            wish_data = WishCreate.parse_obj(row)
            if wish_data.description == '':
                wish_data.description = None
            wishes.append(wish_data)

        self.wishes_service.create_many(
            user_id=user_id,
            wishes_data=wishes,
        )

    def export_csv(self, use_id: int) -> Any:
        output = StringIO()
        writer = csv.DictWriter(
            output,
            fieldnames=[
                'date',
                'title',
                'url',
                'price',
                'description',
            ],
            extrasaction='ignore',
        )

        wishes = self.wishes_service.get_list(user_id=use_id)
        writer.writeheader()
        for wish in wishes:
            wish_data = Wish.from_orm(wish)
            writer.writerow(wish_data.dict())

        output.seek(0)
        return output
