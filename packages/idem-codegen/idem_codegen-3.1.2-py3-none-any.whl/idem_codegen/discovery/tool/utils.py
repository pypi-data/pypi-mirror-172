import json
from typing import Dict


def decide_key_for_resource(hub, resource_attributes, default_value):
    name_tag_value = resource_attributes.get("resource_id", None)
    if "tags" in resource_attributes:
        tags = (
            resource_attributes.get("tags")
            if isinstance(resource_attributes.get("tags"), Dict)
            else hub.idem_codegen.tool.tag_utils.convert_tag_list_to_dict(
                resource_attributes.get("tags")
            )
        )
        if tags.get("name"):
            name_tag_value = tags.get("name")
        elif tags.get("Name"):
            name_tag_value = tags.get("Name")

    if not name_tag_value and resource_attributes.get(
        "name"
    ) != resource_attributes.get("resource_id"):
        name_tag_value = resource_attributes.get("name")
    return name_tag_value if name_tag_value else default_value


def validate_json(str_data):
    try:
        json_data = json.loads(str_data.replace("'", '"'))
    except ValueError:
        return str_data
    if isinstance(json_data, Dict):
        json_data = dict(sorted(json_data.items()))
    return json_data


def find_difference_between_two_lists(sub_list, parent_list):
    diff = []
    if len(sub_list) == len(parent_list):
        return diff
    for element in parent_list:
        if element not in sub_list:
            diff.append(element)
    return diff
