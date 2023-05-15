import os
from decouple import config
import openai
import requests
import yaml


openai.api_key = config("API_KEY")

# Choose a yaml file to read
# Ask the user to choose one of the yaml files in the current directory

# list the yaml files in the current directory, numbered
yaml_files = []
for file in os.listdir():
    if file.endswith(".yaml"):
        yaml_files.append(file)

# print the numbered list of yaml files
print("The following yaml files are available:")
for i in range(len(yaml_files)):
    print(f"{i}. {yaml_files[i]}")

# ask the user to choose one of the yaml files from a numbered list:
yaml_file = ""
while True:
    try:
        yaml_file = input("Enter the number of the yaml file you want to use: ")
        if yaml_file == "":
            print("Exiting...")
            exit(0)
        yaml_file = int(yaml_file)
        break
    except:
        print("Please enter a number")

yaml_file_name = yaml_files[yaml_file]

print(f"You chose {yaml_file_name}")

with open(yaml_file_name, 'r') as file:
    data = yaml.safe_load(file)

test_code = {}
for url in data["test_code_urls"]:
    test_code[url] = None

print("The following urls will be used to download the test code:")
for url in test_code.keys():
    print(url)


# download the source code for each url key in test_code
for url in test_code.keys():
    # get the content of the url
    response = requests.get(url)
    # if the response is valid
    if response.status_code == 200:
        # add the content to the dictionary
        test_code[url] = response.text


code_and_instructions = [{"role": "system", "content" : f"""
You are senior software develeopment engineer in test.
You should analyse a the following triple backticked code and provide a summary of the tests that were run and what the results were.
Provide a verbose description sentence description of each test.
Do not comment on test results.
Use markdown format.
```
{test_code}
```
"""}]


response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=code_and_instructions,
    temperature=0
)


test_summary = response["choices"][0]["message"]["content"]


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
"""})

print(message_flow)

response = openai.ChatCompletion.create(
    model="gpt-4",
    messages=message_flow,
    temperature=0
)

print(response)

print()

print("# An analysis of what the tests do is as follows:\n")
print(test_summary)
print()

print(response["choices"][0]["message"]["content"])
print()

# Write the test results to a file in markdown format
with open("test_results.md", "w") as f:
    f.write("# An analysis of what the tests do is as follows:\n")
    f.write(test_summary)
    f.write("\n")
    f.write("# The test results are as follows:\n")
    f.write(response["choices"][0]["message"]["content"])
