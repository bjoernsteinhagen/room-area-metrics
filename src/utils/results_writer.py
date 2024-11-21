import os
import tempfile
import json
from pathlib import Path
import pandas as pd
from typing import List


def export_dataframes_to_temp_file(
        dataframes: List[pd.DataFrame],
        headers: List[str]
) -> str:

    if len(dataframes) != len(headers):
        raise ValueError("Number of dataframes must match number of headers")

    try:
        os.makedirs(tempfile.gettempdir(), exist_ok=True)
        file_path = os.path.join(tempfile.gettempdir(), f"calculationExport.json")
        export_data = [
            {
                "header": header,
                "data": df.to_dict(orient='records')
            }
            for df, header in zip(dataframes, headers)
        ]

        Path(file_path).write_text(json.dumps(export_data, indent=2))

        return file_path

    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")
        raise