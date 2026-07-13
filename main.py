import json
import os
from dotenv import load_dotenv
from openai import OpenAI
import argparse
from config import system_prompt

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.run_python_file import schema_run_python_file
from functions.write_file import schema_write_file
from functions.call_function import call_function

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )
    
    #Main prompt
    parser = argparse.ArgumentParser(description = "Chatbot")
    parser.add_argument("user_prompt", type = str, help = "User prompt")
    #Verbose flag. Enables more info
    parser.add_argument("--verbose", action="store_true", help = "Enable verbose output")

    args = parser.parse_args()
    
    messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": args.user_prompt},
    ]

    available_functions = [
    schema_get_files_info,
    schema_get_file_content,
    schema_write_file,
    schema_run_python_file
]
    for i in range(20):
        response = client.chat.completions.create(model = "openrouter/free", messages=messages,
                                                tools=available_functions,)

        if response.usage is None:
            print("response is none")
            return

        if args.verbose is True:
            print("User prompt:", args.user_prompt)
            print("Prompt tokens:", response.usage.prompt_tokens)
            print("Response tokens:", response.usage.completion_tokens) 

        message = response.choices[0].message
        messages.append(message)


        if message.tool_calls:
            for tool_call in message.tool_calls:
                function_args = json.loads(tool_call.function.arguments or "{}")
                result_mesage = call_function(tool_call, args.verbose)
                messages.append(result_mesage)
        else:
            print(message.content)
            return
        
        try:
            if args.verbose:
                print(f"-> {result_mesage['content']}")
        except Exception as e:
            return(f"-> result_mesage has no content")

    return 1

main()