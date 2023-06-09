# Simple OpenAI GPT4 examples for analysing test code and results

Two problems frequently arise in software development and testing:
 - interpreting and communicating test results
 - Underatanding what tests are actually doing
 - Augmenting the analytical abilities of LLMs

The canned examples below show how this can be improved with ChatGPT4 and function calling.

How to use...

1. Install the libraries
    ```bash
    pip install -r requirements.txt
    ```

2. Add the API key to the .env file
    ```
    API_KEY="sk-YOUR_API_KEY
    ORG_ID="org-YOUR ORG_ID"
    ```

3. Run hermes if you want to find out what the test results mean and translate that into JSON or XML
    ```
    python hermes.py
    ```

4. Run de_scytale.py if you want to decipher what the test code is actually doing.
    ```
    python de_scytale.py
    ```

4. Run crib_func.py to score a scribbage hand with the help of OpenAI Functions.
    ```
    python crib_func.py
    ```

5. Run run_genned_python.py to execute code generated by GPT4 locally via a GPT4 Function call.
    (This is insecure and you should take steps to run this is a safe manner, or not at all)
    ```
    python run_genned_python.py
    ```

**Some of the above examples** read in data from the `input` folder and place outputs, yes you guessed it, in the `output` folder.
