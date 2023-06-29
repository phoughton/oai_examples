from decouple import config
import openai
import subprocess
import json

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

message_flow.append({"role": "user", "content": f"Please create a matplotlib pie chart where X=10%, Y=50% and Z=40%, on a pink background."})


functions = [
    {
        "name": "run_python_code",
        "description": "Runs the code provided by chatGPT",
        "parameters": {
            "type": "object",
            "properties": {
                "the_code": {
                    "type": "string",
                    "description": "A description of a problem that needs some python code to solve.",
                }
            },
            "required": ["the_code"],
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
    code = json.loads(response_message["function_call"]["arguments"])["the_code"]
else:
    print("Bad things have occured, head for the hills.")
    exit(1)

print(f"Running the following code:\n{code}")
print()
results = subprocess.run(["python", "-c", code], capture_output=True)
print(results.stdout.decode("utf-8"))
print(results.stderr.decode("utf-8"))


