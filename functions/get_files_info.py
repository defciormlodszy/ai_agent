import os

def get_files_info(working_directory: str, directory: str = ".") -> str:
    #First get full dir to working_directory, then join with inside directory, and normalise
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs,directory))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs 

    if target_dir == working_dir_abs:
        name_directory = "current"
    else:
        name_directory = directory

    final_response = f'Result for "{name_directory}" directory:\n'

    if(valid_target_dir is False):
        return f'{final_response}   Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    if not os.path.isdir(target_dir):
        return f'{final_response}   Error: "{directory}" is not a directory'
    
    #Loop listing info abou contents of directory
    contents = os.listdir(target_dir)
    for content in contents:
        content_path = os.path.join(target_dir, content)
        file_size = os.path.getsize(content_path)
        is_dir = os.path.isdir(content_path)
        final_response += f"- {content}: file_size={file_size}, is_dir={is_dir}\n"
    


    
    return f'{final_response}'

schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
