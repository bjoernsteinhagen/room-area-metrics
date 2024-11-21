from pydantic import Field
from speckle_automate import (
    AutomateBase,
    AutomationContext,
    execute_automate_function,
)

from src.model_data_extractor import ModelDataExtractor
from src.room_data import RoomData
from src.area_data import AreaData
from src.computation import Computation
from src.utils.results_writer import export_dataframes_to_temp_file
from src.utils.colouring import colorize_static_with_material


class FunctionInputs(AutomateBase):

    threshold: float = Field(
        default=0.8,
        title="Threshold Value",
        description="Represents the minimum KPI (Net Internal Area / Gross Floor Area). Value must be between 0 and 1.",
    )

    rooms_to_exclude: str = Field(
        default="Corridor, Elevator, Stair, Storage",
        title="Rooms to Exclude",
        description="Represents the list of rooms to exclude from the computation of net internal area. Input is a comma-separated list of rooms to exclude.",
    )

    levels_to_exclude: str = Field(
        default="L1 - Block 37, L1 - Block 43, Green Roof Hardscape, R2",
        title="Levels to Exclude",
        description="List of levels to exclude from the computations. Input is a comma-separated list of levels to exclude.",
    )


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:

    # Variables
    levels_to_exclude = [level.strip() for level in function_inputs.levels_to_exclude.split(",")]
    rooms_to_exclude = [room.strip() for room in function_inputs.rooms_to_exclude.split(",")]
    threshold = function_inputs.threshold

    # Receiving the trigger version
    version_root_object = automate_context.receive_version()

    # Extracting only rooms and areas from the elements
    rooms, areas = ModelDataExtractor.extract(version_root_object)

    # Preparing DataFrames
    room_df, room_dict = RoomData.create_dataframe(rooms)
    area_df = AreaData.create_dataframe(areas)

    # Processing area_df
    gross_areas_summed = AreaData.get_gross_areas(area_df)
    areas_per_level = AreaData.filter_areas(area_df, rooms_to_exclude)
    areas_summed = AreaData.sum_filtered_areas(areas_per_level)

    # Computations
    area_percentages = Computation.percentages(gross_areas_summed, areas_summed)

    # Filter out rows in area_percentages and room_df that have level_names in levels_to_exclude
    area_percentages = area_percentages[~area_percentages['level_name'].isin(levels_to_exclude)]
    excluded_room_ids_based_on_levels = room_df[room_df['level_name'].isin(levels_to_exclude)]['id'].tolist()
    room_df = room_df[~room_df['level_name'].isin(levels_to_exclude)]


    # We want viewable results, for that we use the Room meshes (a different type)
    Computation.build_relations_to_viewable_rooms(room_df, area_percentages, rooms_to_exclude, threshold)

    # Post-processing for results
    skipped_ids = room_df[room_df['result'] == 'skipped']['id'].tolist()
    failed_ids = room_df[room_df['result'] == 'failed']['id'].tolist()
    passed_ids = room_df[room_df['result'] == 'passed']['id'].tolist()

    gradient_values = colorize_static_with_material(passed_ids, room_dict, color_type="success")
    if passed_ids:
        automate_context.attach_info_to_objects(
            category="Levels Passed",
            object_ids=passed_ids,
            message="Rooms included in the calculation of the net internal area on this level did had a KPI >= threshold value.",
        )

    gradient_values = colorize_static_with_material(failed_ids, room_dict, color_type="failed")
    if failed_ids:
        automate_context.attach_error_to_objects(
            category="Levels Failed",
            object_ids=failed_ids,
            message="Rooms included in the calculation of the net internal area on this level did had a KPI < threshold value.",
        )

    gradient_values = colorize_static_with_material(skipped_ids, room_dict, color_type="skipped")
    if skipped_ids:
        automate_context.attach_info_to_objects(
            category="Areas Skipped",
            object_ids=skipped_ids,
            message="Rooms not included in the calculation of the net internal area. See function inputs.",
        )

    if excluded_room_ids_based_on_levels:
        automate_context.attach_info_to_objects(
            category="Levels Skipped",
            object_ids=excluded_room_ids_based_on_levels,
            message="Levels not included in the calculation (see calculationExport.json) or for this visualization. Rendered rooms do not directly affect the calculation, but are as a result of mapping Area data to Room data.",
        )

    file_path = export_dataframes_to_temp_file([areas_per_level, areas_summed, gross_areas_summed, area_percentages], ["Areas Grouped per Level per Usage", "Net Internal Areas Summed per Level", "Gross Areas Summed per Level", "KPIs Calculated per Level"])
    automate_context.store_file_result(file_path)

    automate_context.mark_run_success("The automation was run successfully. See details below for KPI results.")
    automate_context.set_context_view()


if __name__ == "__main__":

    execute_automate_function(automate_function, FunctionInputs)

