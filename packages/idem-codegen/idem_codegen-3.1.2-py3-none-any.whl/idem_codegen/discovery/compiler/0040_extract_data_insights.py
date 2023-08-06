import re

from idem_codegen.discovery.tool.utils import validate_json


async def stage(hub):
    # Get sls data
    sls_data = (await hub.idem_data_insights.compiler.compile())["low"]
    # get high sls data
    data = hub.idem_data_insights.build.build(sls_data)[0]

    string_variation_frequency_map = {}
    list_variation_frequency_map = {}
    for path in data.get("PATH_VARIATIONS"):
        if "require" in path or data.get("PATH_VARIATIONS")[path].get("UNIQUE") > 50:
            continue
        for variation in data.get("PATH_VARIATIONS")[path].get("VARIATIONS"):
            resource_indexes = data.get("PATH_VARIATIONS")[path].get("VARIATIONS")[
                variation
            ]
            if (
                variation.startswith("str-")
                and len(data.get("PATH_VARIATIONS")[path].get("VARIATIONS")[variation])
                > 5
            ):
                tokenize_string(
                    variation[4:],
                    string_variation_frequency_map,
                    resource_indexes,
                    path,
                )
            elif variation.startswith("list-"):
                tokenize_list(
                    variation[5:], list_variation_frequency_map, resource_indexes, path
                )
                # Process dict and lists as well
    process_string_variation_frequency_map(string_variation_frequency_map)
    list_variation_frequency_map = process_list_variation_frequency_map(
        list_variation_frequency_map
    )
    string_parameterization_possibilities = reverse_normalize_frequency_map(
        hub, string_variation_frequency_map, data
    )
    list_parameterization_possibilities = reverse_normalize_frequency_map(
        hub, list_variation_frequency_map, data
    )
    hub.discovery.RUNS["LIST_PARAMETERS"] = list_variation_frequency_map
    hub.discovery.RUNS["LIST_PATHS_FOR_PARAMS"] = list_parameterization_possibilities
    hub.discovery.RUNS["STRING_PARAMETERS"] = string_variation_frequency_map
    hub.discovery.RUNS[
        "STRING_PATHS_FOR_PARAMS"
    ] = string_parameterization_possibilities


def tokenize_list(variation, variation_frequency_map, resource_indexes, path):
    list_variation = validate_json(variation)
    if len(list_variation) == 0:
        return
    frequency = len(resource_indexes)
    for item in list_variation:
        item_as_string = str(item)
        if item_as_string in variation_frequency_map:
            variation_frequency_map[item_as_string]["COUNT"] += frequency
        else:
            variation_frequency_map[item_as_string] = {}
            variation_frequency_map[item_as_string]["VARIATIONS"] = {}
            variation_frequency_map[item_as_string]["COUNT"] = frequency
        if variation in variation_frequency_map[item_as_string]["VARIATIONS"]:
            variation_frequency_map[item_as_string]["VARIATIONS"][variation].update(
                {path: resource_indexes}
            )
        else:
            variation_frequency_map[item_as_string]["VARIATIONS"][variation] = {
                path: resource_indexes
            }


def process_list_variation_frequency_map(variation_frequency_map):
    clusters = {}
    for curr_variation in list(variation_frequency_map):
        if variation_frequency_map[curr_variation]["COUNT"] < 5:
            del variation_frequency_map[curr_variation]
            continue
        for variation in variation_frequency_map[curr_variation]["VARIATIONS"]:
            for path in variation_frequency_map[curr_variation]["VARIATIONS"][
                variation
            ]:
                for resource_index in variation_frequency_map[curr_variation][
                    "VARIATIONS"
                ][variation][path]:
                    cluster_key = (
                        str(resource_index) + "_" + "_".join([str(x) for x in path])
                    )
                    if cluster_key in clusters:
                        clusters[cluster_key]["DATA"].append(
                            validate_json(curr_variation)
                        )
                    else:
                        clusters[cluster_key] = {}
                        clusters[cluster_key]["DATA"] = [validate_json(curr_variation)]
                        clusters[cluster_key]["VARIATIONS"] = {}
                        clusters[cluster_key]["VARIATIONS"][variation] = {}
                    if path in clusters[cluster_key]["VARIATIONS"][variation]:
                        clusters[cluster_key]["VARIATIONS"][variation][path].add(
                            resource_index
                        )
                    else:
                        clusters[cluster_key]["VARIATIONS"][variation][path] = {
                            resource_index
                        }
    cluster_insight = {}
    for i, v in clusters.items():
        cluster_insight[str(v["DATA"])] = (
            [i]
            if str(v["DATA"]) not in cluster_insight.keys()
            else cluster_insight[str(v["DATA"])] + [i]
        )

    for insight in list(cluster_insight):
        for parent_insight in list(cluster_insight):
            if parent_insight == insight:
                continue
            if insight in parent_insight:
                del cluster_insight[insight]
                break

    variation_frequency_map = {}
    count = 1
    for insight in list(cluster_insight):
        if len(cluster_insight[insight]) < 5:
            del cluster_insight[insight]
            continue
        variation_frequency_map[insight] = {}
        variation_frequency_map[insight]["VARIATIONS"] = {}
        variation_frequency_map[insight]["VARIABLE_NAME"] = "var_list_" + str(count)
        count = count + 1
        for item in cluster_insight[insight]:
            for variation in clusters[item]["VARIATIONS"]:
                if variation in variation_frequency_map[insight]["VARIATIONS"]:
                    for path in clusters[item]["VARIATIONS"][variation]:
                        if (
                            path
                            in variation_frequency_map[insight]["VARIATIONS"][variation]
                        ):
                            variation_frequency_map[insight]["VARIATIONS"][variation][
                                path
                            ].update(clusters[item]["VARIATIONS"][variation][path])
                        else:
                            variation_frequency_map[insight]["VARIATIONS"][variation][
                                path
                            ] = clusters[item]["VARIATIONS"][variation][path]
                else:
                    variation_frequency_map[insight]["VARIATIONS"][variation] = {}
                    for path in clusters[item]["VARIATIONS"][variation]:
                        variation_frequency_map[insight]["VARIATIONS"][variation][
                            path
                        ] = clusters[item]["VARIATIONS"][variation][path]
    return variation_frequency_map


def tokenize_string(variation, variation_frequency_map, resource_indexes, path):
    frequency = len(resource_indexes)
    indexes = [-1, len(variation)]
    indexes.extend([m.start() for m in re.finditer(r"-|_", variation)])
    indexes = sorted(indexes)
    for i in range(len(indexes)):
        for j in range(i + 1, len(indexes)):
            curr_substring = variation[indexes[i] + 1 : indexes[j]]
            if curr_substring in variation_frequency_map:
                variation_frequency_map[curr_substring]["COUNT"] += frequency
            else:
                variation_frequency_map[curr_substring] = {}
                variation_frequency_map[curr_substring]["VARIABLE_NAME"] = (
                    "var_" + curr_substring
                )
                variation_frequency_map[curr_substring]["VARIATIONS"] = {}
                variation_frequency_map[curr_substring]["COUNT"] = frequency
            if variation in variation_frequency_map[curr_substring]["VARIATIONS"]:
                variation_frequency_map[curr_substring]["VARIATIONS"][variation].update(
                    {path: resource_indexes}
                )
            else:
                variation_frequency_map[curr_substring]["VARIATIONS"][variation] = {
                    path: resource_indexes
                }


def process_string_variation_frequency_map(frequency_map):
    regex = re.compile(r"[@_!#$%^&*()<>?/\|}{~:]")
    for string_variation in list(frequency_map):
        if len(string_variation) == 0 or len(string_variation.split(" ")) > 4:
            del frequency_map[string_variation]
            continue
        if len(string_variation) == 1 and regex.search(string_variation):
            del frequency_map[string_variation]
            continue
        if string_variation == "true" or string_variation == "false":
            del frequency_map[string_variation]
            continue
        if len(string_variation) < 3 and string_variation.isnumeric():
            del frequency_map[string_variation]
            continue
        if (
            string_variation.startswith("-")
            and len(string_variation) < 4
            and string_variation[1:].isnumeric()
        ):
            del frequency_map[string_variation]
            continue
        for variation in list(frequency_map[string_variation]["VARIATIONS"]):
            if variation in frequency_map and variation != string_variation:
                for resource_indices in frequency_map[string_variation]["VARIATIONS"][
                    variation
                ].values():
                    frequency_map[string_variation]["COUNT"] -= len(resource_indices)
                del frequency_map[string_variation]["VARIATIONS"][variation]
            else:
                for path in list(
                    frequency_map[string_variation]["VARIATIONS"][variation]
                ):
                    if "Key" in path:
                        frequency_map[string_variation]["COUNT"] -= len(
                            frequency_map[string_variation]["VARIATIONS"][variation][
                                path
                            ]
                        )
                        del frequency_map[string_variation]["VARIATIONS"][variation][
                            path
                        ]
        if frequency_map[string_variation]["COUNT"] == 0:
            del frequency_map[string_variation]


def reverse_normalize_frequency_map(hub, frequency_map, data):
    parameterization_possibilities = {}
    index_to_resource_key_map = {}
    for parameter in frequency_map:
        for variation in frequency_map[parameter]["VARIATIONS"]:
            for path in frequency_map[parameter]["VARIATIONS"][variation]:
                for index in frequency_map[parameter]["VARIATIONS"][variation][path]:
                    if index in index_to_resource_key_map:
                        resource_key = index_to_resource_key_map[index]
                    else:
                        resource_attributes = data.get("STATES")[index]
                        name_tag_value = (
                            hub.discovery.tool.utils.decide_key_for_resource(
                                resource_attributes, None
                            )
                        )
                        resource_key = construct_resource_key(
                            resource_attributes["state"].replace(".", "_")
                            + "."
                            + name_tag_value,
                            parameterization_possibilities,
                        )
                        index_to_resource_key_map[index] = resource_key
                    if resource_key in parameterization_possibilities:
                        if path in parameterization_possibilities[resource_key]:
                            parameterization_possibilities[resource_key][path].append(
                                parameter
                            )
                        else:
                            parameterization_possibilities[resource_key][path] = [
                                parameter
                            ]
                    else:
                        parameterization_possibilities[resource_key] = {
                            path: [parameter]
                        }
    return parameterization_possibilities


def construct_resource_key(name_tag_value, parameterization_possibilities):
    if name_tag_value in parameterization_possibilities:
        resource_index = name_tag_value.split("-")[-1]
        if resource_index.isnumeric():
            resource_index = int(resource_index) + 1
            name_tag_arr = name_tag_value.split("-")
            name_tag_arr.pop()
            name_tag_value = "-".join(name_tag_arr)
        else:
            resource_index = 0

        return construct_resource_key(
            name_tag_value + "-" + str(resource_index), parameterization_possibilities
        )
    return name_tag_value
