import pandas
import os

class Loan(object):
    def __init__(self, loanId, loanAmount, loanIR, loanDefaultL, state):
        self.loanId = loanId
        self.loanAmount = loanAmount
        self.loanInterestRate = loanIR
        self.loanDefaultL = loanDefaultL
        self.state = state
        self.assignedFacility = None
        self.expectedYield = None

class Facility(object):
    
    def __init__(self, facilityId, bankId, interestRate, amount):
        self.facilityId = facilityId
        self.bankId = bankId
        self.interestRate = interestRate
        self.amount = amount
        self.maxDefault = None
        self.bannedStates = set()
        
    def addCovnentInfo(self, maxDefault, bannedStates):
        """
        bannedStates: set of banndedStates
        """
        self.maxDefault = maxDefault
        self.bannedStates = bannedStates
        
        return self
    
    def updateAvailableAmount(self, loanRequest):
        self.amount -= loanRequest
        
        return self


class FacilityList(object):
    def __init__(self):
        self.facilities = {}
    
    def createList(self, facilityDF, covenantDF):
        
        for idx, row in facilityDF.iterrows():
            f_id = row['id']
            
            fObj = Facility(f_id, row['bank_id'], row['interest_rate'], row['amount'])
            
            covList = covenantDF.loc[covenantDF['facility_id'] == f_id]
            
            #if covenant list exists for facility
            if covList.shape[0] > 0:
                bState = set()
                maxDef = None
                for idxC, rowC in covList.iterrows():
                    if rowC['max_default_likelihood'] is not None:
                        maxDef = rowC['max_default_likelihood']
                    if rowC['banned_state'] is not None:
                        bState.add(rowC['banned_state'])
                fObj.addCovnentInfo(maxDef, bState)
                
                #print(fObj.facilityId, fObj.bankId, fObj.maxDefault)
            self.facilities[f_id] = fObj
        
        return self.facilities
    
                
        
        
    
    
    