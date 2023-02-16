import csv
from typing import Dict, Union
import ujson


def json_to_csv(
    json: Union[str, Dict],
    destination_path: str,
    template_csv_path: str,
):
    json_dict = json
    if isinstance(json, str):
        json_dict = ujson.loads(json)

    rows = []
    with open(template_csv_path) as csv_template_file:
        reader = csv.DictReader(csv_template_file, delimiter=';')
        head = next(reader)
        headers = {header: description for header, description in head.items()}

    with open(destination_path, 'w') as destination_file:
        writer = csv.DictWriter(destination_file, delimiter=';', fieldnames=head.keys())


    return rows
