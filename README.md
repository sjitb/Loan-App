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

## Questions and Improvement Scope:
**1. How long did you spend working on the problem? What did you find to be the most difficult part?**
<br>About 5 hours. Design aspect of the solution. The main decision was how to maintain state of available facilities.
<br>**2. How would you modify your data model or code to account for an eventual introduction of new, as-of-yet unknown types of covenants, beyond just maximum default likelihood and state restrictions?**
<br>I have made use of classes as often as possible. So, when new rules are added, only the function for selecting facility needs to be modified, without changing parameter lists
<br>**3. How would you architect your solution as a production service wherein new facilities can be introduced at arbitrary points in time.** 
**Assume these facilities become available by the finance team emailing your team and describing the addition with a new set of CSVs.**
<br>Making use of a database to store the facility information could be useful in that regard. That way, we are not using data models for data persistance.
We can query the database for each loan request to find the candidate facility. 
Otherwise on new dataload we regenarate the data model, in my code `FacilityList` object with current state and the new set of facilities
<br>**4. Your solution most likely simulates the streaming process by directly calling a method in your code to process the loans inside of a for loop.**
**What would a REST API look like for this same service? Stakeholders using the API will need, at a minimum, to be able to**
**request a loan be assigned to a facility, and read the funding status of a loan, as well as query the capacities remaining in facilities.**
<br>The REST API could be setup as follows:<br>
**POST** `app/loanrequest/{json_payload_loan_object}` : Returns facility_id of facility assigned to loan <br>
**GET** `app/getfacilitylist/` : Returns the list of facilities and their state, including capacities remaining <br>
**GET** `app/getloanbyid/loan_id`: Returns loan object as JSON, which would also contain assigned facility id and expected yield when available <br>
**GET** `app/getfacilitybyid/facility_id`: Return specific facility information <br>

<br>**5. How might you improve your assignment algorithm if you were permitted to assign loans**
**in batch rather than streaming? We are not looking for code here, but pseudo code or description of a revised algorithm appreciated.**
<br>We could find the set of loans and the corresponding set of facilities that meets the covenants.
Then we create a priority queue of facilities with the facilities with some sort of metric (maybe remaining capacity), so as to optimize assignments 
<br>**6. Discuss your solution’s runtime complexity.**
<br>Most of the processing is done in sequentially with a linear run time of O(N)
Only when creating the `FacilityList` object in `FacilityList.createList` we iterate over the covenants associated with a facility
with a time complexity of  O(MxN) M-> Number of Covenants for N Facilities 