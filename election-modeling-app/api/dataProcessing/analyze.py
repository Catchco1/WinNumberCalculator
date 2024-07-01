import pandas as pd
import plotly.graph_objects as go
from math import ceil
from plotly.subplots import make_subplots
from helper import countVotes, intersect, intersectDistrictAndPrecinct, countVotesDistricts
from winNumber import calculateWinNumber

def tallyVotes(state, districtNum, office, year):

    # Construct current precinct/district/county dataframe
    currentDistricts = pd.read_csv("electionData/{}/results/{}_{}.csv".format(state, state, '2022'))
    currentDistricts = currentDistricts[currentDistricts['office'] == office]
    currentDistricts = currentDistricts[['precinct', 'county_name', 'district']]
    currentDistricts['precinct'] = currentDistricts['precinct'].str.split(' ').str.get(-1)

    # Read in old election data from MEDSL

    electionYear = pd.read_csv("electionData/{}/results/{}_{}.csv".format(state, state, year))

    # Select only the office you are interested in

    electionRace = electionYear[(electionYear['office'] == office) | (electionYear['office'] == 'STATE HOUSE')]

    # Select the district

    #electionDistrict = electionRace[electionRace['district'] == int(districtNum)]
    electionRace['precinct'] = electionRace['precinct'].str.split(' ').str.get(-1)

    # Find overlap between old precincts and current precincts

    findOverlap = intersect('electionData/{}/maps/{}_2024.shx'.format(state, state), 'electionData/{}/maps/{}_{}.shx'.format(state, state, year))

    # Merge the overlapped precincts with the election results

    merged = electionRace.merge(findOverlap, left_on=['precinct', 'county_name'], right_on=['oldPrecinct', 'County_Name'])

    merged = merged.merge(currentDistricts, left_on=['currentPrecinct', 'County_Name'], right_on=['precinct', 'county_name'], suffixes=['_old', '_current'])

    # Reduce merged data set down to just district of interest

    merged = merged[merged['district_current'] == districtNum]

    # Get county names 

    counties = sorted(merged['County_Name'].unique())

    # Put vote totals into a dataframe

    results = countVotes(counties, merged)
    
    return results

def makeGraphs(results):

    # Win number code

    win_number = calculateWinNumber(results)
    
    # Lists for easier graphing. Trying to make this work better with dataframes but work in progress

    years = ['2018', '2020', '2022']

    # Graphing. This should just open a browser tab with the graphs

    demResults = []
    repResults = []
    otherResults = []
    for result in results:
        demResults.append(result.demVotes[0])
        repResults.append(result.repVotes[0])
        otherResults.append(result.otherVotes[0])

    numRows = ceil(len(results[0].county)/5)

    fig = make_subplots(rows=numRows, cols=5, start_cell="bottom-left", subplot_titles=results[0].county + " " + results[0].precinct)

    fig.add_trace(
            go.Bar(name='Democrats', x=years, y=demResults, marker_color='blue', legendgroup='dem'), 
            row=1,
            col=1
    )
    fig.add_trace(
        go.Bar(name='Republicans', x=years, y=repResults, marker_color='red', legendgroup='rep'),
        row=1,
        col=1
    )
    fig.add_trace(
        go.Bar(name='Other', x=years, y=otherResults, marker_color='green', legendgroup='other'),
        row=1,
        col=1
    )

    fig.update_layout(title_text=f"Win Number: {win_number}", title_x=0.5)

    r = 1
    c = 2

    for idx, precinct in enumerate(results[0].county[1:]):
        demResults = []
        repResults = []
        otherResults = []
        for result in results:
            demResults.append(result.demVotes[idx+1])
            repResults.append(result.repVotes[idx+1])
            otherResults.append(result.otherVotes[idx+1])
        if (idx+1)%5 == 0:
            r += 1
        fig.add_trace(
            go.Bar(name='Democrats', x=years, y=demResults, marker_color='blue', legendgroup='dem', showlegend=False), 
            row=r,
            col=c
        )
        fig.add_trace(
            go.Bar(name='Republicans', x=years, y=repResults, marker_color='red', legendgroup='rep', showlegend=False),
            row=r,
            col=c
        )
        fig.add_trace(
            go.Bar(name='Other', x=years, y=otherResults, marker_color='green', legendgroup='other', showlegend=False),
            row=r,
            col=c
        )
        #fig.update_layout(title_text=f"Win Number: {win_number}", title_x=0.5, row = r, col = c)
        c = (c % 5) + 1

    # Uncomment to test just this function without the web server
    # fig.show()
    return fig.to_json()


# Test graphing multiple years
# results2022 = tallyVotes('WV', 88, 'HOUSE OF DELEGATES', '2022')
# results2020 = tallyVotes('WV', 88, 'HOUSE OF DELEGATES', '2020')
# results2018 = tallyVotes('WV', 88, 'HOUSE OF DELEGATES', '2018')

# makeGraphs([results2018, results2020, results2022])

def tallyVotesByDistrict(state, districtNum, office, year):
    # Construct current precinct/district/county dataframe
    currentDistricts = pd.read_csv("electionData/{}/results/{}_{}.csv".format(state, state, '2022'))
    currentDistricts = currentDistricts[currentDistricts['office'] == office]
    currentDistricts = currentDistricts[['precinct', 'county_name', 'district']]
    #currentDistricts['precinct'] = currentDistricts['precinct'].str.split(' ').str.get(-1)

    # Read in old election data from MEDSL

    electionYear = pd.read_csv("electionData/{}/results/{}_{}.csv".format(state, state, year))

    # Select only the office you are interested in

    electionRace = electionYear[(electionYear['office'] == office) | (electionYear['office'] == 'STATE HOUSE')]

    electionRace['district'] = electionRace['district'].str.lstrip('0')

    # Select the district

    electionDistrict = electionRace[electionRace['district'] == str(districtNum)]

    electionDistrict['precinct'] = electionDistrict['precinct'].astype(str)

    findOverlap = intersectDistrictAndPrecinct('electionData/{}/maps/stateHouseDistricts/{}_House_2022.shx'.format(state, state), 'electionData/{}/maps/precincts/{}_2010.shx'.format(state, state))

    merged = electionDistrict.merge(findOverlap, left_on=['precinct'], right_on=['PCT_CEB'])

    # Put vote totals into a dataframe

    results = countVotesDistricts(merged, districtNum)

    print(results)