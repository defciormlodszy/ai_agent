import os
import subprocess

def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs,file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if valid_target_dir == False:
     return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    
    if os.path.isfile(target_dir) == False:
       return f'Error: "{file_path}" does not exist or is not a regular file'
    
    if file_path.endswith("py") == False:
       return f'Error: "{file_path}" is not a Python file'
    
    command = ["python", target_dir]

    if args is not None :
       command.extend(args)
    
    try:
        output = subprocess.run(command, cwd= working_dir_abs, timeout=30, text=True)
        final_string =  f"""
STDOUT: {output.stdout}
STDERR: {output.stderr}
    """
        if output.stdout == "" and output.stderr == "":
            final_string = "Not output produced.\n"       
        if output.returncode != 0:
            final_string += f'Proccess exited with code {output.returncode}'
        return final_string
      
    except Exception as e:
        return f'Error: executing Python file: {e}'
    

schema_run_python_file = {
    "type": "function",
    "function": {
        "name": "run_python_file",
        "description": "Execute Python file with optional arguments, return file output, STUDOUT and STDERR. ",
        "parameters": {
            "type": "object",
            "properties": {
                "args": {
                    "type": "array",
                    "items": "string",
                    "description": "Lists arguments for the programme",
                },
                "file_path":{
                   "type": "str",
                   "description": "Path to the python file, relative to the working directory"
                }
            },
        },
    },
}