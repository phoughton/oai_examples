import os
from decouple import config
import openai


openai.api_key = config("API_KEY")

message_flow = [
    {
        "role": "system", "content": """
Your are an Software development engineer in Test who will review and report the results of a test CI run.
You will provide an accurate summary of the tests that wwere run and
what the results were:

1) Give give details of test failures in English
If a test failed, provide details of the failure. and what that
means functionally to the user.
Keep your response short and impersonal

2) Also, below the above response provide the same information in JSON format.

3) Also, below the above response provide the same information in XML format.
"""
    }
]

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
message_flow.append({"role": "assistant", "content": """
Summarize the test results. Provide a short executive summary of the test results. then a more detailed summary.
message_flow.append({"role": "assistant", "content": "the format should be as follows:
## Test results Summary

## Executive Summary of the test results

The exeutive summary should be a summary of the test results. It should be no more than 5 sentences. 

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

## The JSON version of these test results:
[PLACE THE JSON TEST RESULTS HERE]

## The XML version of these test results:
[PLACE THE XML TEST RESULTS HERE]
"""})

print(message_flow)

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=message_flow,
    temperature=0,
    top_p=1,
    frequency_penalty=0,
    presence_penalty=0
)

print(response)

print()

print(response["choices"][0]["message"]["content"])
print()

# Write the test results to a file in markdown format
with open("test_results.md", "w") as f:
    f.write("# The test results are as follows:\n")
    f.write(response["choices"][0]["message"]["content"])
