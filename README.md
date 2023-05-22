# Simple OpenAI GPT4 examples for analysing test code and results

Two problems frequently arise in software test automation:
 - interpreting and communicating test results
 - Underatanding what tests are actually doing

The canned examples below show how this can be improved with ChatGPT4.

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

4. Run de_scytale.py if you want to decopher what your tests are actually doing.
    ```
    python de_scytale.py
    ```


The above examples read in data from the `input` folder and place outputs, yes you guessed it, in the `output` folder.
