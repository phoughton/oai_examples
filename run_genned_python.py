from decouple import config
import openai
import requests
from file_chooser import choose_a_file


openai.api_key = config("API_KEY")

message_flow = [
    {
        "role": "system", "content": """
You are an coder who provides working python code.
When presented with a coding request, You should provide working code as an argument to the function.
"""}
]

print()
# message_flow.append({"role": "user", "content": f"Please score my cribbage hand: ```{hand_desc}```\n"})

message_flow.append({"role": "user", "content": f"Please create the first 10 fibonacci numbers."})


functions = [
    {
        "name": "run_python_code",
        "description": "Runs the code provided by chatGPT",
        "parameters": {
            "type": "object",
            "properties": {
                "code_question": {
                    "type": "string",
                    "description": "A description of a problem that needs some python code to solve.",
                }
            },
            "required": ["code_question"],
        }
    }
]

print(message_flow)
print("\nCalculating the results...\n")

response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=message_flow,
    functions=functions,
    function_call={"name": "run_python_code"},
    temperature=0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
response_message = response["choices"][0]["message"]
results = ""
print(response_message)
if response_message["function_call"]["name"] == "run_python_code":
    code = response_message["function_call"]["arguments"]
    exec(code)
else:
    print("Bad things have occured, head for the hills.")
    exit(1)

