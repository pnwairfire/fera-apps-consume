# open FB52_%Consumed.csv, create 7 fccs_loadings.csv rows based on columns L to R
import os
from pathlib import Path
import csv
import sys

fccsLoadingsPath = '/Users/briandrye/repos/uw/apps-consumeGIT/consume/input_data/fccs_loadings.csv'
consumeOutputPath = '/Users/briandrye/Downloads/consume813/consume_output2026_01_30.csv'

newFccsLoadingsPath = '/Users/briandrye/repos/uw/apps-consumeGIT/scripts/adjusted_fccs_loadings2026_01_30.csv'
inputFilePath = '/Users/briandrye/repos/uw/apps-consumeGIT/scripts/input_file_for_adjusted2026_01_30.csv'

#fuelbedsOfInterest = ['52', '208', '292']
fuelbedsOfInterest = ['1', '6', '8', '9', '10', '13', '20', '22', '28', '48', '52', '53', '56', '57', '59', '60', '70', '95', '208', '224', '235', '237', '292', '304', '305', '308', '310', '315', '321', '331', '358', '360', '361', '483', '493', '494', '496', '497', '498', '506', '514', '529', '530', '531', '532', '1223', '1232', '1262', '1264', '1273']

# scenarios:
# consume_output2026_01_29.csv has 7 scenarios per fuelbed (in row order)
# add a column Scenario1 to adjusted_fccs_loadings2026_01_29.csv after FCCSID to indicate initial scenario.
# also add a second column Scenario2 to indicate the scenario after consumption.
# SpringRx
# SpringRxRed
# FallRx
# FallRxRed
# WFLow
# WFMod
# WFHigh



# instead of using FB52_%Consumed.csv, use consume_output2026_01_29.csv to get the consumed values
# then subtract the consumed value from the original value in fccs_loadings.csv

# SpringRx overstory_loading (L) = original_loading
# (overstory_loading from fccs_loadings.csv) - c_overstory_crown (column CC where row is first for this fuelbed) (from consume output)

# SpringRx

fccsColumnMap = ['overstory_loading', 'midstory_loading', 'understory_loading',
               'snags_c1_foliage_loading', 'snags_c1wo_foliage_loading', 'snags_c1_wood_loading',
               'snags_c2_loading', 'snags_c3_loading', 'ladderfuels_loading',
               'shrubs_primary_loading', 'shrubs_secondary_loading',
               'nw_primary_loading', 'nw_secondary_loading',
               'pile_clean_loading',
               'w_sound_0_quarter_loading', 'w_sound_quarter_1_loading',
               'w_sound_1_3_loading', 'w_sound_3_9_loading',
               'w_sound_9_20_loading', 'w_sound_gt20_loading',
               'w_rotten_3_9_loading', 'w_rotten_9_20_loading',
               'w_rotten_gt20_loading',
               'w_stump_sound_loading', 'w_stump_rotten_loading', 'w_stump_lightered_loading',
               'litter_loading', 'lichen_loading', 'moss_loading',
               'duff_upper_loading', 'duff_lower_loading',
               'basal_accum_loading', 'squirrel_midden_loading']

# add additional required columns (see below where hardcoded values are set)
fccsColumnMap.extend(['shrubs_primary_perc_live', 'shrubs_secondary_perc_live',
                    'nw_primary_perc_live', 'nw_secondary_perc_live',
                    'litter_depth', 'lichen_depth', 'moss_depth',
                    'duff_lower_depth', 'duff_upper_depth',
                    'cover_type', 'ecoregion',
                    'pile_dirty_loading', 'pile_vdirty_loading',
                    'efg_natural', 'efg_activity'])

consumeColumnMap = ['c_overstory_crown', 'c_midstory_crown', 'c_understory_crown',
    'c_snagc1f_crown', 'c_snagc1f_wood', 'c_snagc1_wood', 'c_snagc2_wood', 'c_snagc3_wood',
    'c_ladder', 'c_shrub_1live', 'c_shrub_2live',
    'c_herb_1live', 'c_herb_2live', 'c_piles',
    'c_wood_1hr', 'c_wood_10hr', 'c_wood_100hr', 'c_wood_s1000hr', 'c_wood_r1000hr',
    'c_wood_s10khr', 'c_wood_r10khr', 'c_wood_s+10khr', 'c_wood_r+10khr',
    'c_stump_sound', 'c_stump_rotten', 'c_stump_lightered',
    'c_litter', 'c_lichen', 'c_moss',
    'c_upperduff', 'c_lowerduff',
    'c_basal', 'c_squirrel']


with open(fccsLoadingsPath, 'r') as fccsLoadingsFile:
    reader = csv.reader(fccsLoadingsFile)
    fccsLoadings = list(reader)
    fccsColumnNames = fccsLoadings[1]  # second row has column names


# at this point we have fccsLoadings, fccsColumnNames, consumeOutput,
# in consumeOutput up to the next 196 rows after consumeOutputRowIndex:
    # plain number (1) + variations: 28 total
    # 111,112,113,121,122,123,131,132,133, (9)
    # 211,212,213,221,222,223,231,232,233, (9)
    # 311,312,313,321,322,323,331,332,333, (9)
    # total 1 + 9 + 9 + 9 = 28 variations
    # then 7 scenarios per variation = 196 rows

# write header to new adjusted_fccs_loadings<date>.csv
with open(newFccsLoadingsPath, 'w', newline='') as newLoadingsFile:
    writer = csv.writer(newLoadingsFile)
    writer.writerow(['GeneratorName=FCCS 4.0', 'GeneratorVersion=3.0.0', 'DateCreated=01/02/2026.'])
    writer.writerow(['fuelbed_number'] + ['FCCSID']  + fccsColumnMap)

with open(inputFilePath, 'w', newline='') as inputFile:
    writer = csv.writer(inputFile)
    writer.writerow(
        ['area', 'fm_duff', 'fm_1000hr', 'can_con_pct', 'shrub_black_pct', 'pile_black_pct', 'fuelbeds', 'units',
         'ecoregion', 'fm_litter', 'season', 'rotten_cwd_pct_available', 'duff_pct_available',
         'sound_cwd_pct_available'])

for fb in fuelbedsOfInterest:
    for variation in ['', '111', '112', '113', '121', '122', '123', '131', '132', '133',
                      '211', '212', '213', '221', '222', '223', '231', '232', '233',
                      '311', '312', '313', '321', '322', '323', '331', '332', '333']:

        # find the row in fccsLoadings for the fuelbed_number of interest
        fccsRowIndex = None

        if variation == '':
            fb_variation = fb + '0000'
        else:
            fb_variation = fb + '0'+ variation
        print(fb_variation)
        for idx, row in enumerate(fccsLoadings):
            # print(row[0])
            if row[0] == fb_variation:
                fccsRowIndex = idx
                print('fccsRowIndex:' + str(fccsRowIndex))
                break
        if fccsRowIndex is None:
            print("Could not find " + fb_variation + " in fccs loadings", file=sys.stderr)
            # skip to next variation
            continue

        # find the index of fuelbed_number in consume output
        scenario1Index = 0
        consumeOutputRowIndex = None
        with open(consumeOutputPath, 'r') as consumeOutputFile:
            reader2 = csv.reader(consumeOutputFile)
            consumeOutput = list(reader2)

            # find row index where row[0] starts with fb_variation  520111
            for idx, row in enumerate(consumeOutput):
                if row[0].startswith(fb_variation):
                    consumeOutputRowIndex = idx
                    print('ConsumeOutputRowIndex: ' + str(consumeOutputRowIndex))
                    break

        if consumeOutputRowIndex is None:
            print("Could not find " + fb_variation + " consume output", file=sys.stderr)
            sys.exit(1)

        # for each of the 7 scenarios
        # make array of values to write
#        scenarios = ['SpringRx', 'SpringRxRed', 'FallRx', 'FallRxRed', 'WFLow', 'WFMod', 'WFHigh']
        for i in range(7):
            # for each of the original columns, get the value from consume output
            # and subtract the consumed value from the original value in fccs_loadings.csv
            columnValues = []
            for idx, col_name in enumerate(fccsColumnMap[:-15]):  # exclude the last 16 additional columns
                # find the index of col_name in fccsColumnNames
                fccsColumnIndex = fccsColumnNames.index(col_name)
                # get consume output column name that corresponds to this fccs column
                consumeColumnName = consumeColumnMap[idx]
                # find the index of col_name in consumeOutputColumnNames
                consumeColumnIndex = consumeOutput[0].index(consumeColumnName)

                # get the original value from fccs_loadings.csv
                original_value = fccsLoadings[fccsRowIndex][fccsColumnIndex]

                # get the consumed value from consume output
                consumed_value = consumeOutput[consumeOutputRowIndex][consumeColumnIndex]
                # calculate the adjusted value
                adjusted_value = float(original_value) - float(consumed_value)
                if adjusted_value < 0:
                    adjusted_value = 0.0  # ensure no negative values
                columnValues.append(str(adjusted_value))

                # print("FCCS column: " + col_name)
                # print("fccsRowIndex: " + str(fccsRowIndex))
                # print("fccsColumnIndex: " + str(fccsColumnIndex))
                # print("Consume column: " + consumeColumnName)
                # print("consumeOutputRowIndex: " + str(consumeOutputRowIndex))
                # print("consumeColumnIndex: " + str(consumeColumnIndex))
                # print("Original value: " + str(original_value))
                # print("Consumed value: " + str(consumed_value))
                # print("Adjusted value: " + str(adjusted_value))
                # print("-----")

            # add placeholder values for the additional columns
            columnValues.extend(['89', '95',  # shrubs_primary_perc_live, shrubs_secondary
                           '70', '80',  # nw_primary_perc_live, nw_secondary_perc_live
                           '0.7', '0.1', '.2',  # litter_depth, lichen_depth, moss_depth
                           '1.5', '1.1',  # duff_lower_depth, duff_upper_depth
                           '118', '240',  # cover_type, ecoregion
                           '0', '0',  # pile_dirty_loading, pile_vdirty_loading
                           '8', '1'  # efg_natural, efg_activity
                           ])

            # write the values row for this fuelbed_number 7 times
            with open(newFccsLoadingsPath, 'a', newline='') as newLoadingsFile:
                writer = csv.writer(newLoadingsFile)
                for jj in range(7):
                    values = []
                    values.append(str(fb_variation) + "0" + str(i+1) + "0" + str(jj+1))  # fuelbed_number
                    values.append(str(fb_variation))  # FCCSID
                    # values.append(scenarios[i])  # Scenario1
                    # values.append(scenarios[jj])  # Scenario2
                    values.extend(columnValues)
                    writer.writerow(values)

            consumeOutputRowIndex = consumeOutputRowIndex + 1
        scenario1Index = scenario1Index + 1

        with open(inputFilePath, 'a', newline='') as inputFile:
            writer = csv.writer(inputFile)
            # write 7 rows for each fuelbed_number
            for j in range(7):
                writer.writerow([100, 150, 80, 0, 50, 90, fb_variation + "0" + str(j+1) + "01", 'tons', 'western', 15, 'spring', 50, 30, 0])
                writer.writerow([100, 150, 80, 0, 50, 90, fb_variation + "0" + str(j+1) + "02", 'tons', 'western', 15, 'spring', 20, 10, 0])
                writer.writerow([100, 60, 25, 0, 100, 90, fb_variation + "0" + str(j+1) + "03", 'tons', 'western', 12, 'fall', 100, 100, 20])
                writer.writerow([100, 60, 35, 0, 100, 90, fb_variation + "0" + str(j+1) + "04", 'tons', 'western', 12, 'fall', 50, 50, 0])
                writer.writerow([100, 30, 35, 20, 100, 90, fb_variation + "0" + str(j+1) + "05", 'tons', 'western', 12, 'summer', 100, 100, 100])
                writer.writerow([100, 30, 25, 50, 100, 90, fb_variation + "0" + str(j+1) + "06", 'tons', 'western', 9, 'summer', 100, 100, 100])
                writer.writerow([100, 30, 10, 90, 100, 100, fb_variation + "0" + str(j+1) + "07", 'tons', 'western', 3, 'summer', 100, 100, 100])


print('Created adjusted loadings and input files based on consumption data.')

print('Run Consume against these new files to generate emissions estimates:')
print(
    'Example: (my310env) bdxfer@SEFS-A-DRYE consume813 % python consume_batch.py -f adjusted_fccs_loadings.csv -o consume_output_2026_01_02.csv natural input_file_for_adjusted.csv')


# create input_file_for_adjusted.csv with header and 7 rows per fuelbed_number
# area,fm_duff,fm_1000hr,can_con_pct,shrub_black_pct,pile_black_pct,fuelbeds,units,ecoregion,fm_litter,season,rotten_cwd_pct_available,duff_pct_available,sound_cwd_pct_available
# 100,150,80,0,50,90,52_1,tons,western,15,spring,50,30,0
# 100,150,80,0,50,90,52_1,tons,western,15,spring,20,10,0
# 100,60,25,0,100,90,52_1,tons,western,12,fall,100,100,20
# 100,60,35,0,100,90,52_1,tons,western,12,fall,50,50,0
# 100,30,35,20,100,90,52_1,tons,western,12,summer,100,100,100
# 100,30,25,50,100,90,52_1,tons,western,9,summer,100,100,100
# 100,30,10,90,100,100,52_1,tons,western,3,summer,100,100,100
# 100,150,80,0,50,90,52_2,tons,western,15,spring,50,30,0
# 100,150,80,0,50,90,52_2,tons,western,15,spring,20,10,0
# 100,60,25,0,100,90,52_2,tons,western,12,fall,100,100,20
# 100,60,35,0,100,90,52_2,tons,western,12,fall,50,50,0
# 100,30,35,20,100,90,52_2,tons,western,12,summer,100,100,100
# 100,30,25,50,100,90,52_2,tons,western,9,summer,100,100,100
# 100,30,10,90,100,100,52_2,tons,western,3,summer,100,100,100
# ...
