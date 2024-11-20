import pandas as pd

class RoomData:

    @staticmethod
    def create_dataframe(rooms: "specklepy.objects.other.Collection") -> pd.DataFrame:
        return pd.DataFrame([
            {
                'id': room.id,
                'area': room.area,
                'name': room.name,
                'level_name': room.level.name,
                'level_elevation': room.level.elevation
            } for room in rooms.elements
        ])