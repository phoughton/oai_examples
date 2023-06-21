from decouple import config
import openai
import requests
from file_chooser import choose_a_file


openai.api_key = config("API_KEY")
THE_SCORER_URL = config("SCORING_URL")

message_flow = [
    {
        "role": "system", "content": """
You are an expert at scoring games.
You should calculate the score for the game of cribbage.
"""}
]

# Ask the user to choose the test results file and then read the contents of that file into a variable called test_results
hand_desc = choose_a_file("input_crib_hands", ".txt", "Please choose the hand of cards by number:")
print()
message_flow.append({"role": "user", "content": f"Please score my cribbage hand: ```{hand_desc}```\n"})
functions = [
    {
        "name": "get_cribbage_hand_score",
        "description": "Get the current weather in a given location",
        "parameters": {
            "type": "object",
            "properties": {
                "starter": {
                    "type": "string",
                    "description": "The starter card, e.g. '5H' for 5 of hearts",
                },
                "hand": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "A card in the hand, e.g. and array with cards like '5H' for 5 of hearts"
                    }
                },
                "isCrib": {
                    "type": "boolean", 
                    "description": "Whether the hand is a crib"
                }
            },
            "required": ["starter", "hand", "isCrib"],
        }
    }
]

print(message_flow)
print("\nCalculating the results...\n")

response = openai.ChatCompletion.create(
    model="gpt-4-0613",
    messages=message_flow,
    functions=functions,
    function_call="auto",
    temperature=0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)
response_message = response["choices"][0]["message"]

results = ""
if response_message["function_call"]["name"] == "get_cribbage_hand_score":
    print(response_message)
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    results = requests.post(url=THE_SCORER_URL, data=response_message["function_call"]["arguments"], headers=headers).json()


print(results)
print()
