from __future__ import annotations # NOTE: Forward referencing
from typing import Tuple

class ModelDataExtractor:

    @staticmethod
    def extract(model_data: "specklepy.objects.other.Collection") -> Tuple[list, list]:
        rooms = [element for element in model_data.elements if element.name == "Rooms"]
        areas = [element for element in model_data.elements if element.name == "Areas"]

        if not rooms or not areas:
            raise ValueError("No rooms or areas found")

        return rooms[0], areas[0]