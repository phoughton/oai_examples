import os
from decouple import config
import openai
import requests
import yaml


openai.api_key = config("API_KEY")

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


code_and_instructions = [{"role": "system", "content": f"""
You are senior software develeopment engineer in test.
You should analyse a the following triple backticked code and provide a
summary of the tests that were run and what the results were.
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

print(test_summary)
