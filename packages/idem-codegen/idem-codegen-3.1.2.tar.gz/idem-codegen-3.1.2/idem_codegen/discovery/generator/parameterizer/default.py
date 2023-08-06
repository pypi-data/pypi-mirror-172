from collections import ChainMap
from typing import Any
from typing import Dict

__contracts__ = ["parameterize"]

from idem_codegen.discovery.tool.utils import (
    find_difference_between_two_lists,
    validate_json,
)


def parameterize(hub, sls_data: Dict[str, Any]):
    """
    This function takes sls_data as input loop through all the attribute values and
    check if they can be parameterized to {{params.get("test_variable")}} in sls.

    :param hub:
    :param sls_data:
    :return:
    """
    for resource in sls_data:
        resource_attributes = list(sls_data[resource].values())[0]
        resource_attributes = dict(ChainMap(*resource_attributes))
        resource_attributes["resource_id"] = f'{{{{ params.get("{resource}") }}}}'

        if (
            resource not in hub.discovery.RUNS["STRING_PATHS_FOR_PARAMS"]
            and resource not in hub.discovery.RUNS["LIST_PATHS_FOR_PARAMS"]
        ):
            sls_data[resource][list(sls_data[resource].keys())[0]] = [
                {ne_key: ne_value} for ne_key, ne_value in resource_attributes.items()
            ]
            continue
        if resource in hub.discovery.RUNS["LIST_PATHS_FOR_PARAMS"]:
            for path in hub.discovery.RUNS["LIST_PATHS_FOR_PARAMS"][resource]:
                try:
                    if len(path) == 1 and path[0] in resource_attributes:
                        reference = hub.discovery.RUNS["LIST_PATHS_FOR_PARAMS"][
                            resource
                        ][path][0]
                        diff = find_difference_between_two_lists(
                            validate_json(reference), resource_attributes[path[0]]
                        )
                        param_name = f'{{{{params["{hub.discovery.RUNS["LIST_PARAMETERS"][reference]["VARIABLE_NAME"]}"]}}}}'
                        if len(diff) == 0:
                            resource_attributes[path[0]] = param_name
                        else:
                            resource_attributes[path[0]] = (
                                param_name + " + " + str(diff)
                            )
                    elif len(path) == 2 and path[0] in resource_attributes:
                        reference = hub.discovery.RUNS["LIST_PATHS_FOR_PARAMS"][
                            resource
                        ][path][0]
                        diff = find_difference_between_two_lists(
                            validate_json(reference),
                            resource_attributes[path[0]][path[1]],
                        )
                        param_name = f'{{{{params["{hub.discovery.RUNS["LIST_PARAMETERS"][reference]["VARIABLE_NAME"]}"]}}}}'
                        if len(diff) == 0:
                            resource_attributes[path[0]][path[1]] = param_name
                        else:
                            resource_attributes[path[0]][path[1]] = (
                                param_name + " + " + str(diff)
                            )
                    elif len(path) == 3 and path[0] in resource_attributes:
                        reference = hub.discovery.RUNS["LIST_PATHS_FOR_PARAMS"][
                            resource
                        ][path][0]
                        diff = find_difference_between_two_lists(
                            validate_json(reference),
                            resource_attributes[path[0]][path[1]][path[2]],
                        )
                        param_name = f'{{{{params["{hub.discovery.RUNS["LIST_PARAMETERS"][reference]["VARIABLE_NAME"]}"]}}}}'
                        if len(diff) == 0:
                            resource_attributes[path[0]][path[1]][path[2]] = param_name
                        else:
                            resource_attributes[path[0]][path[1]][path[2]] = (
                                param_name + " + " + str(diff)
                            )
                except TypeError:
                    continue

        if resource in hub.discovery.RUNS["STRING_PATHS_FOR_PARAMS"]:
            for path in hub.discovery.RUNS["STRING_PATHS_FOR_PARAMS"][resource]:
                try:
                    if len(path) == 1 and path[0] in resource_attributes:
                        reference = resource_attributes[path[0]]
                        if (
                            hub.discovery.RUNS["STRING_PATHS_FOR_PARAMS"][resource][
                                path
                            ][0]
                            != reference
                        ):
                            continue
                        resource_attributes[
                            path[0]
                        ] = f'{{{{params["{hub.discovery.RUNS["STRING_PARAMETERS"][reference]["VARIABLE_NAME"]}"]}}}}'
                    elif len(path) == 2 and path[0] in resource_attributes:
                        reference = resource_attributes[path[0]][path[1]]
                        if (
                            hub.discovery.RUNS["STRING_PATHS_FOR_PARAMS"][resource][
                                path
                            ][0]
                            != reference
                        ):
                            continue
                        resource_attributes[path[0]][
                            path[1]
                        ] = f'{{{{params["{hub.discovery.RUNS["STRING_PARAMETERS"][reference]["VARIABLE_NAME"]}"]}}}}'
                    elif len(path) == 3 and path[0] in resource_attributes:
                        reference = resource_attributes[path[0]][path[1]][path[2]]
                        if (
                            hub.discovery.RUNS["STRING_PATHS_FOR_PARAMS"][resource][
                                path
                            ][0]
                            != reference
                        ):
                            continue
                        resource_attributes[path[0]][path[1]][
                            path[2]
                        ] = f'{{{{params["{hub.discovery.RUNS["STRING_PARAMETERS"][reference]["VARIABLE_NAME"]}"]}}}}'
                except TypeError:
                    continue

        sls_data[resource][list(sls_data[resource].keys())[0]] = [
            {ne_key: ne_value} for ne_key, ne_value in resource_attributes.items()
        ]

    return sls_data
