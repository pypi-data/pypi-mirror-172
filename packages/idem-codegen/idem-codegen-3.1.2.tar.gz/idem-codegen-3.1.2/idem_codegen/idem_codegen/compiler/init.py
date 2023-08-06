__func_alias__ = {"compile_": "compile"}


async def compile_(hub, run_name):
    """
    Compile the data defined in the given run name
    """
    hub.idem_codegen.RUNS["COMMON_VARIABLES"] = {}
    for compiler_stage in sorted(hub[run_name].compiler._loaded.keys()):
        await hub[run_name].compiler[compiler_stage].stage()
