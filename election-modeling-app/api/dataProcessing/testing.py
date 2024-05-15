from analyze import makeGraphs
import geopandas as gpd

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
    merged = merged[['NAMELSAD', 'LONGNAME', 'County_Nam', 'overlapping']].rename(columns={'NAMELSAD': 'oldPrecinct', 'LONGNAME': 'currentPrecinct', 'County_Nam': 'County_Name'})
    print('merged precincts')
    print(merged)

    # remove text from current precinct for later merging 

    #merged['currentPrecinct'] = merged['currentPrecinct'].str.extract('(^\\D*)', expand=False)
    return merged
makeGraphs(88, 'HOUSE OF DELEGATES')