import pandas as pd
import geopandas as gpd
import numpy as np

def countVotes(counties, electionData):
    precinctTotals = pd.DataFrame(columns=['county', 'precinct', 'demVotes', 'repVotes', 'otherVotes'])
    electionData['proportionVotes'] = electionData['votes'].multiply(electionData['overlapping'], axis='index')
    electionData['proportionVotes'] = electionData['proportionVotes'].apply(np.ceil)
    for county in counties:
        countyData = electionData[electionData['County_Name'] == county]
        precincts = sorted(countyData['currentPrecinct'].unique())
        for precinct in precincts:
            demVotes = electionData.loc[(electionData['County_Name'] == county) & (electionData['currentPrecinct'] == precinct) & (electionData['party_simplified'] == 'DEMOCRAT'), 'proportionVotes'].sum()
            repVotes = electionData.loc[(electionData['County_Name'] == county) & (electionData['currentPrecinct'] == precinct) & (electionData['party_simplified'] == 'REPUBLICAN'), 'proportionVotes'].sum()
            otherVotes = electionData.loc[(electionData['County_Name'] == county) & (electionData['currentPrecinct'] == precinct) & (electionData['party_simplified'] != 'REPUBLICAN') & (electionData['party_simplified'] != 'DEMOCRAT'), 'proportionVotes'].sum()
            precinctTotals = pd.concat([precinctTotals, pd.DataFrame({'county': [county], 'precinct': precinct, 'demVotes': [demVotes], 'repVotes': [repVotes], 'otherVotes': [otherVotes]})], ignore_index=True)
    return precinctTotals

def intersect(path_to_current_precinct_shapefile, path_to_old_precinct_shapefile):
    # setup district and precinct dataframes
    currentPrecincts = gpd.read_file(path_to_current_precinct_shapefile)
    oldPrecincts = gpd.read_file(path_to_old_precinct_shapefile)
    if currentPrecincts.crs != oldPrecincts.crs:
        oldPrecincts = oldPrecincts.to_crs(crs=currentPrecincts.crs)

    # calculate area of each precinct
    oldPrecincts['precinct_area'] = oldPrecincts.area

    # create merged dataframe including the intersection shapes between currentPrecincts and precincts. This includes precinct/district combos where the precinct just borders the district
    merged = gpd.overlay(oldPrecincts, currentPrecincts, how='intersection')

    # calculate intersection area and divide by total precinct area to find which shapes are actually the full precinct in a district
    merged['area_joined'] = merged.area
    merged['overlapping'] = merged['area_joined'] / merged['precinct_area']

    # the values are not perfect, so anyting with greater than half the area reporting should work. May be worth checking to see that the number of rows in merged after this slicing matches the number of rows in precincts
    merged = merged[merged['overlapping'] > 0.1]
    
    countyColumn = ''
    precinctColumn = ''
    for col in merged.columns:
        if 'County_Nam' in col:
            countyColumn = col
        if 'NAMELSAD' in col or 'SHORTNAME_1' in col:
            precinctColumn = col

    merged = merged[[precinctColumn, 'LONGNAME', countyColumn, 'overlapping']].rename(columns={precinctColumn: 'oldPrecinct', 'LONGNAME': 'currentPrecinct', countyColumn: 'County_Name'})

    # remove text from precinct columns for later merging 
    merged['oldPrecinct'] = merged['oldPrecinct'].str.split(' ').str.get(-1)
    merged['currentPrecinct'] = merged['currentPrecinct'].str.split(' ').str.get(-1)
    merged['County_Name'] = merged['County_Name'].str.upper()
    return merged
