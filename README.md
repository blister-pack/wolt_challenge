# wolt_coding_challenge

--- INSTRUCTIONS FOR INSTALLATION ---

Thank you for taking the time to review my code.
The instructions for the installation of and running of the program are as follows:

1. Navigate to the project directory:
    `cd <project_directory>`

2. Create a Virtual Environment:
    `python -m venv .venv`

3. Activate Virtual Environment:
    `source .venv/bin/activate`

4. Install required dependencies:
    `pip install -r requirements.txt`


--- INSTRUCTIONS FOR RUNNING THE APP ---

1. Navigate to source folder:
    `cd source/`

2. Start the FastAPI development server:
    `uvicorn dopc:app --reload`

3. Open browser and navigate to:
    `http://127.0.0.1:8000/docs` (default)
    Here you should be able to explore and test the API


--- INSTRUCTIONS TO RUN TESTS ---

1. Run tests:
    `pytest tests/`