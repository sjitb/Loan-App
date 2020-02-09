import csv
import os
import pandas as pd
import configparser
from datetime import datetime
from collections import OrderedDict

#IMPORT CUSTOM LIBRARIES
from data_loader import DataLoad
from data_models import Facility, FacilityList, Loan

class LoanApp(object):
    def __init__(self):
        """
        Filepaths defined in config file
        initialize file paths
        """
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.folderpath = config['DEFAULT']['FOLDER_PATH']
        self.loanfile = config['DEFAULT']['LOANS_FILE']
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        self.afile = "assignments" + timestamp + ".csv"
        self.yfile = "yields" + timestamp + ".csv"
        self.processedLoans = []
    
    def processLoans(self):
        """
        Driver Function to process loans in loans.csv
        """

        loandf = self.loadLoansData()

        dataLoadObj = DataLoad()
        
        bd = dataLoadObj.loadBankData()
        cd = dataLoadObj.loadCovenantData()
        fd = dataLoadObj.loadFacilitiesData()
        
        flObj = FacilityList()
        facilityList = flObj.createList(fd,cd)
                

        for index, row in loandf.iterrows():

            loanId = row['id']
            loanAmount = row['amount']
            loanIR = row['interest_rate']
            loanDefaultL = row['default_likelihood']
            loanState = row['state']
            
            print("Processing Loan Id:" + str(loanId))
            
            loanObj = Loan(loanId, loanAmount, loanIR, loanDefaultL, loanState)

            #pick facility
            facilityId = self.findFacility(facilityList, loanObj) 

            # When no Facility found, drop loan request and skip
            if facilityId == -1:
                print("Cannot Assign Loan Id:" + str(loanId))
                continue

            loanObj.assignedFacility = facilityId

            facilityList = self.updateFacilityBalance(facilityList, facilityId, loanObj.loanAmount)

            yieldAmount = self.calculateYield(facilityList[facilityId], loanObj) 

            loanObj.expectedYield = yieldAmount
            
            self.processedLoans.append(loanObj)

            self.writeAssignments(loanId, facilityId)            
            self.writeYields(facilityId, yieldAmount)

        return True
    
    
    def findFacility(self, facilityList, loanObj): # loanAmount, defaultProb, stateId):
        """
        findFacility to assign to loan
        """
        facId = -1
        availableList = []
        for key, val in facilityList.items():
            validFac = 0
            if val.amount and val.amount > loanObj.loanAmount:
                validFac += 1
            else:
                continue
            if not val.maxDefault or (val.maxDefault and val.maxDefault > loanObj.loanDefaultL):
                validFac += 1
            else:
                continue
            if not val.bannedStates or (val.bannedStates and loanObj.state not in val.bannedStates):
                validFac += 1
            else:
                continue
            #When all 3 conditions are met 
            if validFac == 3:
                availableList.append((key, val.interestRate))
        if len(availableList) > 0:
            minVal = min(availableList, key = lambda t: t[1])
            facId = int(minVal[0])
            
        return facId
    
    def updateFacilityBalance(self, facilityList, facilityId, loanAmount):
        facObj = facilityList[facilityId]
        facObj.amount -= loanAmount
        facilityList[facilityId] = facObj
        
        return facilityList


    def calculateYield(self, fObj, loanObj): # loanAmount, loanIR):
        f_ir = fObj.interestRate
        l_df = loanObj.loanDefaultL
        l_ir = loanObj.loanInterestRate
        l_a = loanObj.loanAmount
        yeildAmount = ((1 - l_df) * l_ir * l_a) - (l_df * l_a) - (f_ir * l_a)         

        return yeildAmount

    def loadLoansData(self):
        loanFilePath = self.folderpath + self.loanfile

        loanDF = pd.read_csv(loanFilePath)

        return loanDF


    def writeAssignments(self,loanId,facilityId):
        """
        Function to Create/Update CSV file to track 
        Assignments of Loan 
        """
        aFilePath =''.join([self.folderpath,self.afile])
        header = ['loan_id', 'facility_id']
        datarow = [loanId, facilityId]

        enterFile = self.writeFile(aFilePath,header,datarow)

        return enterFile

    def writeYields(self,facilityId,expectedYield):
        """
        Function to Create/Update CSV file to track 
        Yields from Loan 
        """
        yFilePath = ''.join([self.folderpath,self.yfile])
        header = ['facility_id', 'expected_yield']

        datarow = [facilityId, expectedYield]
        enterFile = self.writeFile(yFilePath,header,datarow)

        return enterFile

    def writeFile(self, dataFilePath, headerRow, dataRow):
        """
        Function to Create/Update CSV files 
        """
        fileExists = os.path.isfile(dataFilePath)
        if not fileExists:
            with open(dataFilePath, "w", newline='') as f:
                writer = csv.writer(f, delimiter=',')
                writer.writerow(headerRow) # write the header
        with open(dataFilePath, "a", newline='') as f:
            writer = csv.writer(f, delimiter=',')
            # write the actual content
            writer.writerow(dataRow)
        return True


def main():

    print("Launching App")
    
    loanAppObj = LoanApp()
    
    res = loanAppObj.processLoans()
    
    print(res)

if __name__ == "__main__":
    main()

