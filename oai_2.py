import os
from decouple import config
import openai
import requests


test_code = {
    "https://raw.githubusercontent.com/phoughton/cribbage_scorer/master/tests/play/play_scorer_exceptions_test.py": None,
    "https://raw.githubusercontent.com/phoughton/cribbage_scorer/master/tests/play/play_scorer_test.py": None,
    "https://raw.githubusercontent.com/phoughton/cribbage_scorer/master/tests/show/show_scorer__impossible_score_test.py": None,
    "https://raw.githubusercontent.com/phoughton/cribbage_scorer/master/tests/show/show_scorer_exceptions_test.py": None,
    "https://raw.githubusercontent.com/phoughton/cribbage_scorer/master/tests/show/show_scorer_test.py": None
}

# download the source code for each url key in test_code
for url in test_code.keys():
    # get the content of the url
    response = requests.get(url)
    # if the response is valid
    if response.status_code == 200:
        # add the content to the dictionary
        test_code[url] = response.text


message_flow = [
    {"role": "system", "content": "Your are an analyst who will review the results of a test run. You will summary what tests were run in the test run and what the results were." +
     "The tests are for a python package that scores cribbage hands. The package is called cribbage_scorer. The tests are written in python and use the pytest framework." +
     "cribbage is a card game. The tests are for a package that scores hands in the game."}
]

message_flow.append({"role": "user", "content": f"I will now give you the code used to run the tests. there will be {len(test_code)} files containing tests."})

for url in test_code.keys():
    message_flow.append({"role": "assistant", "content": test_code[url]})


print(message_flow)

# On the command line prompt the user to enter the test results from pytest, line by line
test_results = ""
last_line = ""
print("Enter the test results from pytest, line by line. When you are done, enter 2 blank lines.")
while True:
    line = input()
    if line == "" and last_line == "":
        break
    test_results += line + "\n"
    last_line = line

# add the test results to the message flow
message_flow.append({"role": "user", "content": f"The pytest results the above tests are delimited here with 3 backticks. ```{test_results}```"})

print(message_flow)

# openai.api_key = config("API_KEY")


# response = openai.ChatCompletion.create(
#     model="gpt-4",
#     messages=message_flow,  
#     temperature=0
# )

# print(response)
