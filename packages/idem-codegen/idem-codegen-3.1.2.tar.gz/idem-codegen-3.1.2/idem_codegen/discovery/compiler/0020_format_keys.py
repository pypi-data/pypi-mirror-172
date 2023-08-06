from collections import ChainMap

"""
    This stage takes sls data and constructs unique keys for each entity.
"""

__contracts__ = ["compile"]


def set_resource_key(name_tag_value, updated_sls_data, resource):
    if name_tag_value in updated_sls_data:
        resource_index = name_tag_value.split("-")[-1]
        if resource_index.isnumeric():
            resource_index = int(resource_index) + 1
            name_tag_arr = name_tag_value.split("-")
            name_tag_arr.pop()
            name_tag_value = "-".join(name_tag_arr)
        else:
            resource_index = 0

        return set_resource_key(
            name_tag_value + "-" + str(resource_index), updated_sls_data, resource
        )

    updated_sls_data[name_tag_value] = resource
    return updated_sls_data


async def stage(hub):
    sls_data = hub.discovery.RUNS["SLS_DATA"]
    updated_sls_data = {}
    for item in sls_data:
        resource_attributes = list(sls_data[item].values())[0]
        resource_map = dict(ChainMap(*resource_attributes))
        resource_type = (
            list(sls_data[item].keys())[0].replace(".present", "").replace(".", "_")
        )
        name_tag_value = hub.discovery.tool.utils.decide_key_for_resource(
            resource_map, item
        )
        updated_sls_data = set_resource_key(
            resource_type + "." + name_tag_value, updated_sls_data, sls_data[item]
        )
    hub.discovery.RUNS["SLS_DATA_WITH_KEYS"] = updated_sls_data
    hub.discovery.RUNS["SLS_DATA_WITH_KEYS_ORIGINAL"] = updated_sls_data
    return updated_sls_data
