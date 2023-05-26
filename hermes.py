from decouple import config
import openai
from file_chooser import choose_a_file


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
Do not calculate any totals or percentages.

2) Also, below the above response provide the same information in JSON format.

3) Also, below the above response provide the same information in XML format.
"""
    }
]

# Ask the user to choose the test results file and then read the contents of that file into a variable called test_results
test_results = choose_a_file("input", ".txt", "Please choose the test results file you want to review by number:")
print()
message_flow.append({"role": "user", "content": f"The pytest results for the above tests are delimited here with 3 backticks. ```{test_results}```\n"})

message_flow.append({"role": "assistant", "content": """
Summarize the test results. Provide a short executive summary of the test results. then a more detailed summary.

the format should be as follows:

## Test results Summary

A description of the test results. Including: 
 - The number of tests executed - exactly, 
  - the number of tests passed and the number of tests failed - based on the data provided by the user only.

## Executive Summary of the test results

The executive summary should be a summary of the test results.

## Detailed Test Results for all tests executed

Repeat this for each test file in the user provided results file:

- [TEST FILE NAME] Description of the test
    - One or two sentence explanation of the test in plain English
    - [NUMBER OF TESTS FAILED]


## The details of the tests that failed in plain English


## The JSON version of these test passes and failures:
[PLACE THE JSON TEST RESULTS HERE]


## The XML version of these test passes and failures:
[PLACE THE XML TEST RESULTS HERE]
"""})

print(message_flow)
print("\nCalculating the test results...\n")

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

# Write the test results to a file in markdown format
with open("output/test_results.md", "w") as f:
    f.write("# The test results are as follows:\n")
    f.write(response["choices"][0]["message"]["content"])

print("The test results have been written to output/test_results.md")

