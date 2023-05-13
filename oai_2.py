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
    {
        "role": "system", "content": "Your are an Software development engineer in Test who will review and report the results of a test CI run.\n" +
        "You will provide an accurate summary of the tests that wwere run and what the results were.\n" +
        "Give give details of test failures\n" +
        "If a test failed, provide details of the failure. and what that means functionally to the user.\n" +
        "Keep your response short and impersonal\n"
    }
]

message_flow.append({"role": "user", "content": f"I will now give you the code used to run the tests. there will be {len(test_code)} files containing tests.\n"})

for url in test_code.keys():
    message_flow.append({"role": "assistant", "content": test_code[url]})


print(message_flow)

test_results = ""
last_line = ""
print()
print("Enter the test results from pytest, line by line. When you are done, enter 2 blank lines.")
while True:
    line = input()
    if line == "" and last_line == "":
        break
    test_results += line + "\n"
    last_line = line

# add the test results to the message flow
message_flow.append({"role": "user", "content": f"The pytest results for the above tests are delimited here with 3 backticks. ```{test_results}```\n"})

message_flow.append({"role": "assistant", "content": "Summarize the test results. Provide a short executive summary of the test results. then a more detailed summary.\n"})
message_flow.append({"role": "assistant", "content": "the format should be as follows:\n"})
message_flow.append({"role": "assistant", "content": """
# Test results Summary

## Executive Summary of the test results

The exeutive summary should be a short summary of the test results. It should be no more than 3 sentences. 

## Detailed Test Results for all tests executed

1. Description of the test
   - One sentence description of the test
   - Number tests passed / failed

2. Description of the test
   - One sentence description of the test
   - Number tests passed / failed

3. Description of the test
   - One sentence description of the test
   - Number tests passed / failed
   - The details of the tests that failed in plain English
"""})

print(message_flow)

openai.api_key = config("API_KEY")


response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=message_flow,
    temperature=0
)

print(response)

print()

print(response["choices"][0]["message"]["content"])
print()
