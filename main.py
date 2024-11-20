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


def automate_function(
    automate_context: AutomationContext,
    function_inputs: FunctionInputs,
) -> None:

    # Variables
    rooms_to_exclude = [room.strip() for room in function_inputs.rooms_to_exclude.split(",")]
    threshold = function_inputs.threshold

    # Receiving the trigger version
    version_root_object = automate_context.receive_version()

    # Extracting only rooms and areas from the elements
    rooms, areas = ModelDataExtractor.extract(version_root_object)

    # Preparing DataFrames
    print(rooms)
    print(dir(rooms))
    room_df = RoomData.create_dataframe(rooms)
    area_df = AreaData.create_dataframe(areas)

    # Processing area_df
    gross_areas_summed = AreaData.get_gross_areas(area_df)
    areas_per_level = AreaData.get_areas(area_df, rooms_to_exclude)

    # Computations
    area_percentages = Computation.percentages(gross_areas_summed, areas_per_level)

    # TODO: Avoid things like this after POC
    ### <------- HACKY SECTION BELOW

    # Filter out unwanted levels
    area_percentages = area_percentages[~area_percentages['level_name'].str.contains('R2|Green Roof')]
    room_df = room_df[~room_df['level_name'].str.contains('R2|Green Roof Hardscape')]

    def map_level_name(level_name):
        if 'L1 - Block' in level_name:
            return 'L1 - Block 35'
        return level_name

    # Map level names in room_df
    room_df['level_name'] = room_df['level_name'].apply(map_level_name)

    ### END OF HACKY SECTION ------->

    # Summary String
    base_string = "The automation was run successfully. See details below for KPI results."
    summary_strings = []
    for _, row in area_percentages.iterrows():
        summary_string = (
            f"{row['level_name']} with a net internal area of {int(round(row['area']))} "
            f"and a gross area of {int(round(row['area_gross']))} "
            f"had a KPI of {int(round(row['percentage']*100))}%. "
        )
        summary_strings.append(summary_string)

    full_report = base_string + "\n\n" + "\n".join(summary_strings) + "\n"

    # We want viewable results, for that we use the Room meshes (a different type)
    Computation.build_relations_to_viewable_rooms(room_df, area_percentages, rooms_to_exclude, threshold)

    # Post-processing for results
    skipped_ids = room_df[room_df['result'] == 'skipped']['id'].tolist()
    failed_ids = room_df[room_df['result'] == 'failed']['id'].tolist()
    passed_ids = room_df[room_df['result'] == 'passed']['id'].tolist()

    if passed_ids:
        automate_context.attach_info_to_objects(
            category="Levels Passed",
            object_ids=passed_ids,
            message="Rooms included in the calculation of the net internal area on this level did had a KPI >= threshold value.",
            visual_overrides={"color":"#00ff00"},
        )
    if failed_ids:
        automate_context.attach_error_to_objects(
            category="Levels Failed",
            object_ids=failed_ids,
            message="Rooms included in the calculation of the net internal area on this level did had a KPI < threshold value.",
            visual_overrides={"color":"#ff0000"},
        )
    if skipped_ids:
        automate_context.attach_info_to_objects(
            category="Areas Skipped",
            object_ids=skipped_ids,
            message="Rooms not included in the calculation of the net internal area. See function inputs.",
            visual_overrides={"color":"#DFDFDF"},
        )
    automate_context.mark_run_success(full_report)
    automate_context.set_context_view()

if __name__ == "__main__":

    execute_automate_function(automate_function, FunctionInputs)

