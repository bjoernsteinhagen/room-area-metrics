from __future__ import annotations # NOTE: Forward referencing
from typing import Tuple

class ModelDataExtractor:

    @staticmethod
    def extract(model_data: "specklepy.objects.other.Collection", automate_context) -> Tuple[list, list]:
        rooms = [element for element in model_data.elements if element.name == "Rooms"]
        areas = [element for element in model_data.elements if element.name == "Areas"]

        if not areas:
            automate_context.mark_run_exception(f"No collection of type Objects.BuiltElements.Area found. Please send complete model.")
        if not rooms:
            automate_context.mark_run_exception(f"No collection of type Objects.BuiltElements.Room found. Please send complete model.")

        return rooms[0], areas[0]