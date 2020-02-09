import csv
import os
import pandas as pd
import configparser
from datetime import datetime
from collections import OrderedDict

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', -1)

class DataLoad(object):
    """
    Class to handle data load
    """
    def __init__(self):
        """
        Filepaths defined in config file
        initialize file paths
        """
        print("Initializing Data Load")
        config = configparser.ConfigParser()
        config.read('config.ini')
        self.folderpath = config['DEFAULT']['FOLDER_PATH']
        self.bankfile = config['DEFAULT']['BANK_FILE']
        self.covfile = config['DEFAULT']['COVENANTS_FILE']
        self.facfile = config['DEFAULT']['FACILITIES_FILE']
        print("Successfully Initialized Data Load Class")

    def loadBankData(self):
        """
        Read Bank Data from CSV File 
        return: Pandas dataframe with data
        """
        bankFilePath =''.join([self.folderpath,self.bankfile])
        bankDF = pd.read_csv(bankFilePath)
        print("Successfully Loaded Bank Data")
        return bankDF
    
    def loadCovenantData(self):
        """
        Read Covenant Data from CSV File 
        return: Pandas dataframe with data
        """
        covFilePath =''.join([self.folderpath,self.covfile])
        covDF = pd.read_csv(covFilePath)
        print("Successfully Loaded Covenant Data")
        return covDF

    def loadFacilitiesData(self):
        """
        Read Facilities Data from CSV File 
        return: Pandas dataframe with data
        """
        facFilePath =''.join([self.folderpath,self.facfile])
        facDF = pd.read_csv(facFilePath)
        print("Successfully Loaded Facilities Data")
        return facDF
