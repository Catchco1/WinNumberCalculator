from analyze import makeGraphs, tallyVotes
import geopandas as gpd

results = tallyVotes('VT', 'ADD-1', 'STATE HOUSE', '2020')

makeGraphs(results)