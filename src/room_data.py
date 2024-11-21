import pandas as pd

class RoomData:

    @staticmethod
    def create_dataframe(rooms: "specklepy.objects.other.Collection") -> tuple[pd.DataFrame, dict]:

        room_dict = {room.id: room for room in rooms.elements}

        df = pd.DataFrame([
            {
                'id': room.id,
                'area': room.area,
                'name': room.name,
                'level_name': room.level.name,
                'level_elevation': room.level.elevation
            } for room in rooms.elements
        ])

        return df, room_dict