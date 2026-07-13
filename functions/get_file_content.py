import os

MAX_CHARS = 10000

def get_file_content(working_directory: str, file_path: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs,file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if valid_target_dir == False:
     return f'Error: Cannot read "{file_path} as it is outside the permitted working directory'
    
    if os.path.isfile(target_dir) == False:
       return f'Error: File not found or is not a regular file: "{file_path}"'

    contents = open(target_dir)
    string = contents.read(MAX_CHARS)

    if(contents.read(1)):
       string += f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'

    return string

schema_get_file_content = {
    "type": "function",
    "function": {
        "name": "get_file_content",
        "description": "Open file, then return as string its content. Limit is 100000 characters.",
        "parameters": {
            "type": "object",
            "properties": {
                "file_path":{
                   "type": "str",
                   "description": "Path to the file, relative to the working directory"
                }
            },
        },
    },
}