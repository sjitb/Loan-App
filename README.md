# Loan Processing App
This application will process a stream of loan requests and assign it to facilities, based on meeting of certain covenants

## Environment Set-up:
1. Create Virtual Environment:<br>
`python -m venv env`
2. Launch Python Virtual Environment by executing:<br>
`.\env\Scripts\activate`
3. Install pandas if required: <br>
`pip install pandas`
4. Use config.ini to update files to be processed

## Execution and Results:
1. Run the app by executing: <br>
`python loan_app.py`
2. Result Files for Assignments and Expected Yields are saved in the folder set up in the config file. The result filenames have timestamp of execution associated with them

## Components:
1. `loan_app.py`: driver function <br>
2. `data_loader.py`: library for loading data from csv files to dataframe <br>
3. `data_models.py`: contains data models for loan, facility and facility list <br> 
