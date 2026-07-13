import os

def write_file(working_directory: str, file_path: str, content: str) -> str:
    working_dir_abs = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(working_dir_abs,file_path))

    valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs

    if valid_target_dir == False:
     return f'Error: Cannot read "{file_path} as it is outside the permitted working directory'
    
    if os.path.isdir(target_dir):
       return f'Error: Cannot write to "{file_path}" as it is a directory'
   
    if not os.path.isfile(target_dir):
       parent_dir = os.path.dirname(target_dir)
       try:
         os.makedirs(parent_dir, exist_ok=True)
       except Exception as e:
            return f"Could not create parent dirs : {parent_dir} = {e}"
    try:
      with open(target_dir, "w") as f:
         f.write(content)
      return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
       return f'Failed to write to "{file_path}",{e}'



schema_write_file = {
    "type": "function",
    "function": {
        "name": "write_file",
        "description": "Open file, if it doesn't exist create one. Then overide its content with content",
        "parameters": {
            "type": "object",
            "properties": {
                "content": {
                    "type": "str",
                    "description": "String with content to write in the file",
                },
                "file_path":{
                   "type": "str",
                   "description": "Path to the file, relative to the working directory"
                }
            },
        },
    },
}
