from typing import Any
from typing import Dict

__contracts__ = ["generate_file"]

from idem_codegen.discovery.tool.utils import validate_json
from idem_codegen.idem_codegen.tool.utils import MyDumperNoBlankLines


def create(
    hub, module_name: str, module_output_directory_path: str, sls_data: Dict[str, Any]
):
    variables = {}
    for variable in hub.discovery.RUNS["STRING_PARAMETERS"]:
        variables[
            hub.discovery.RUNS["STRING_PARAMETERS"][variable]["VARIABLE_NAME"]
        ] = variable
    for variable in hub.discovery.RUNS["LIST_PARAMETERS"]:
        variables[
            hub.discovery.RUNS["LIST_PARAMETERS"][variable]["VARIABLE_NAME"]
        ] = validate_json(variable)
    hub.idem_codegen.tool.utils.dump_sls_data_to_file(
        f"{module_output_directory_path}/output/params/variables.sls",
        variables,
        dumper=MyDumperNoBlankLines,
    )
    hub.idem_codegen.generator.files.init.generate(
        module_output_directory_path, sls_data
    )
