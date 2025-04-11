import json
import os
import pprint
import time
from typing import Dict, List, Optional
from google import genai
from google.genai import types
import pathlib
from pydantic import BaseModel
from dotenv import load_dotenv

load_dotenv()


class Data(BaseModel):
    fixtureType: str
    quantity: str
    unit: Optional[str]
    floor: str
    dimensions: Optional[str]
    mountingType: Optional[str]
    drawingName: str
    pageNumber: int


def get_context_from_document(prompt: str, file_path: str) -> Dict:
    path = pathlib.Path(file_path)
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    response = client.models.generate_content(
    model="gemini-2.0-flash",
    contents=[types.Part.from_bytes(data=path.read_bytes(), mime_type='application/pdf'), prompt],
    config={
        'response_mime_type': 'application/json',
        'response_schema': list[Data],
    },
    )
    return response.parsed

if __name__ == "__main__":
    # Example usage
    prompt = 'You are an OCR tool. Export all fixtures, their quantity (count), what unit they are part of, floor, dimensions (usually found to the left of the fitting name with null symbol), mounting type (whether wall-mounted, floor-mounted, etc.) if stated, along with the page number. Give result as an api response in JSON format with keys "fixtureType", "quantity", "unit", "floor", "dimensions", "mountingType", "drawingName", "pageNumber". Respond with an empty list if no data can be extracted'

    from file_utils import get_files_from_directory
    output_folder = "M&P mark-up against shop systems piping"
    # fetch all chunks from the output folder
    files = get_files_from_directory(output_folder)
    res = []
    for idx, file in enumerate(files):
        print(f"Parsing file {idx + 1} of {len(files)}")
        res_obj = get_context_from_document(prompt, file)
        for obj in res_obj:
            obj.pageNumber = idx + 1
            res.append(obj.model_dump())
        time.sleep(1)

    pprint.pprint(res)