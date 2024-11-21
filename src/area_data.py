from typing import List
import pandas as pd

class AreaData:

    @staticmethod
    def create_dataframe(areas: "specklepy.objects.other.Collection") -> pd.DataFrame:
        return pd.DataFrame([
            {
                'area': area.area,
                'name': area.name,
                'level_name': area.level.name,
                'level_elevation': area.level.elevation
            } for area in areas.elements
        ])

    @staticmethod
    def get_gross_areas(area_df: pd.DataFrame) -> pd.DataFrame:

        gross_areas = area_df[area_df['name'].str.contains('Gross')].sort_values('level_elevation')
        gross_areas_summed = gross_areas.groupby('level_name')['area'].sum().reset_index()

        return gross_areas_summed

    @staticmethod
    def filter_areas(area_df: pd.DataFrame, rooms_to_exclude: List[str]) -> pd.DataFrame:

        # Areas with names that don't contain the word Gross
        areas_grouped = area_df[~area_df['name'].str.contains('Gross')].groupby(['level_name', 'name'])[
            'area'].sum().reset_index()

        # Get the minimum elevation for each level name
        elevation_map = area_df.groupby('level_name')['level_elevation'].min().reset_index()

        # Merge the area data with elevation information
        areas_grouped = areas_grouped.merge(elevation_map, on='level_name').sort_values('level_elevation')

        # Area calculation doesn't include "rooms_to_exclude"
        filtered_areas_grouped = areas_grouped[~areas_grouped['name'].str.contains('|'.join(rooms_to_exclude))]

        return filtered_areas_grouped

    @staticmethod
    def sum_filtered_areas(filtered_areas_grouped: pd.DataFrame) -> pd.DataFrame:

        areas_per_level = filtered_areas_grouped.groupby('level_name')['area'].sum().reset_index()

        return areas_per_level