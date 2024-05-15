import pandas as pd
import plotly.graph_objects as go
from math import ceil
from plotly.subplots import make_subplots
from functools import reduce

### Objective: Expected turnout estimate. Divide this number by two and add one vote to get baseline win number. 

def calculateWinNumber(list_of_year_votes_input): #Calculates win number for a precinct

    #Step one is to find total number of votes
    list_of_year_votes = list_of_year_votes_input
    numYears = len(list_of_year_votes)
    print(numYears)

    totalVotes = []

    #Find the total number of votes for each precinct for a given year
    for yearVotes in list_of_year_votes:
        colToSum = ["demVotes", "repVotes", "otherVotes"]
        yearVotes[colToSum] = yearVotes[colToSum].apply(pd.to_numeric, errors='coerce')
        yearVotes["total"] = yearVotes[colToSum].sum(axis = 1, numeric_only = True) #The total number of votes is now
        #a new column in yearVotes

        totalVotes.append(yearVotes["total"].sum()) #find the total number of votes for a given year across all precincts

    numResults = len(totalVotes)
    if (numResults != numYears): #the number of values in totalVotes should be equal to the number of years
        print("ERROR")
        return -1
    
    sumVotes = sum(totalVotes)

    avgVotes = sumVotes/numYears

    winNumber = (avgVotes/2) + 1

    return winNumber

    




    


