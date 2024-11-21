from typing import Any, Dict, List, Tuple

def colorize_static_with_material(
        all_object_ids: Dict[str, List],
) -> Tuple[Dict[str, Dict[str, str]], List[str]]:
    gradient_values: Dict[str, Dict[str, str]] = {}

    color_mapping = {
        "success": 0,
        "failed": 1,
        "skipped": 2
    }

    # Create a flat list of all ids
    all_ids = []

    # Loop through each list in the dictionary
    for key, ids in all_object_ids.items():
        # Ensure lists are non-empty before processing
        if ids:
            for object_id in ids:
                # Here we can assign the corresponding color based on the key (success, failed, or skipped)
                color_type = key  # success, failed, or skipped
                gradient_values[object_id] = {"gradientValue": color_mapping[color_type]}
                all_ids.append(object_id)

    return gradient_values, all_ids
