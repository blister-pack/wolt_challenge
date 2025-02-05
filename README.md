# wolt_coding_challenge

--- INSTRUCTIONS FOR INSTALLATION ---

Thank you for taking the time to review my code.
The instructions for the installation of and running of the program are as follows:

1. Navigate to the project directory:
    `cd <project_directory>`

2. Create a Virtual Environment:
    `python -m venv .venv` 
    if it doesn't work:
    `python3 -m venv .venv` 

3. Activate Virtual Environment:
    `source .venv/bin/activate`

4. Install required dependencies:
    `pip install -r requirements.txt`


--- INSTRUCTIONS FOR RUNNING THE APP ---

1. Start the FastAPI development server:
    `uvicorn source.dopc:app --reload`

2. Open browser and navigate to:
    `http://127.0.0.1:8000/docs` (default)
    Here you should be able to explore and test the API


--- INSTRUCTIONS TO RUN TESTS ---

1. Run tests:
    `pytest tests/`
    `pytest -s tests/` allows print statements!

used coordinates for testing:

lat: 24.93913512 lon: 60.18112143 venue: home-assignment-venue-helsinki

Note on Endpoint Testing
Due to time constraints, I was unable to develop dedicated tests for the endpoint. However, here's what I would have implemented:

Test Framework: Use pytest along with httpx for FastAPI's TestClient.
Mocking Dependencies: Use Python's unittest.mock to mock functions like get_venue_data, get_distance, and get_delivery_fee to isolate the endpoint logic from external dependencies.
Simulated Scenarios:
Valid inputs returning expected results.
Edge cases such as missing or invalid parameters.
Dependency failures, raising appropriate exceptions.
This testing strategy would ensure the endpoint behaves as expected under different conditions.


--- HOW TO RUN COVERAGE ---

Coverage is cool because it tests how much of the code is actually ran with your tests.

how to use coverage:
1. Run your tests with coverage
`coverage run -m pytest tests/`

2. Check coverage:
`coverage report`