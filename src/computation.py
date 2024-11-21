from typing import List
import pandas as pd

class Computation:

    @staticmethod
    def percentages(gross_areas: pd.DataFrame, room_areas: pd.DataFrame) -> pd.DataFrame:

        # Merge the two DataFrames on level_name
        area_percentages = pd.merge(room_areas, gross_areas, on='level_name', suffixes=('', '_gross'))
        area_percentages['percentage'] = area_percentages['area'] / area_percentages['area_gross']

        return area_percentages

    @staticmethod
    def build_relations_to_viewable_rooms(room_df: pd.DataFrame,
                                          area_percentages: pd.DataFrame,
                                          rooms_to_exclude: List[str],
                                          threshold: float) -> None:

        # Mark rooms to be excluded based on their name
        room_df['result'] = room_df['name'].apply(
            lambda x: "skipped" if any(substring in x for substring in rooms_to_exclude) else None
        )

        for index, row in room_df.iterrows():
            if room_df.loc[index, 'result'] is None:
                # Try to get the corresponding percentage for the level
                level_percentage = area_percentages.loc[
                    area_percentages['level_name'] == row['level_name'],
                    'percentage'
                ].values

                # If no matching percentage is found, handle the exception
                if len(level_percentage) == 0:
                    raise KeyError(f"Level name '{row['level_name']}' not found in area_percentages.")
                else:
                    # If a match is found, compare with the threshold
                    level_percentage_value = level_percentage[0]
                    room_df.loc[index, 'result'] = (
                        "passed" if level_percentage_value >= threshold else "failed"
                    )