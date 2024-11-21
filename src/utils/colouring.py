from typing import Any, Dict, List
from specklepy.objects.other import RenderMaterial

def colorize_static_with_material(
        object_ids: List[str],
        room_dict: Dict[str, Any],
        color_type: str
) -> Dict[str, Dict[str, str]]:

    gradient_values: Dict[str, Dict[str, str]] = {}

    # Define RGBA colors for success, failed, and skipped
    color_mapping = {
        "success": (52, 211, 153, 1),  # rgba(52, 211, 153, 1) - Green for success
        "failed": (196, 89, 89, 1),  # rgba(196, 89, 89, 1) - Red for failed
        "skipped": (237, 237, 237, 1)  # rgba(237, 237, 237, 1) - Light gray for skipped
    }

    # Get the selected color based on color_type
    rgba_color = color_mapping.get(color_type)

    if rgba_color is None:
        raise ValueError("Invalid color type. Choose from 'success', 'failed', or 'skipped'.")

    alpha, red, green, blue = rgba_color
    argb_color = (alpha << 24) | (red << 16) | (green << 8) | blue

    for object_id in object_ids:
        obj = room_dict.get(object_id)

        if obj is not None:
            gradient_values[object_id] = {"color": f"rgba({red}, {green}, {blue}, {alpha})"}

            render_material = RenderMaterial()
            render_material.name = f"{color_type.capitalize()}Color"
            render_material.diffuse = argb_color
            render_material.opacity = 1
            render_material.metalness = 0
            render_material.roughness = 1
            render_material.emissive = -16777216  # black arbg

            obj.render_material = render_material

    return gradient_values