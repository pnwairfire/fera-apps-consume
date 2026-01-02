
# open FB52_%Consumed.csv, create 7 fccs_loadings.csv rows based on columns L to R
import os
from pathlib import Path
import csv
import sys
fbConsumedPath = '/Users/briandrye/repos/uw/apps-consumeGIT/scripts/FB52_%Consumed.csv'
newFccsLoadingsPath = '/Users/briandrye/repos/uw/apps-consumeGIT/scripts/adjusted_fccs_loadings.csv'
inputFilePath = '/Users/briandrye/repos/uw/apps-consumeGIT/scripts/input_file_for_adjusted.csv'

# the columns in FB52_%Consumed.csv that we want to use to create new fccs_loadings rows
consumptionColumns = ['L', 'M', 'N', 'O', 'P', 'Q', 'R']

# write header to new fccs_loadings.csv
with open(newFccsLoadingsPath, 'w', newline='') as newLoadingsFile:
    writer = csv.writer(newLoadingsFile)
    # read FB52_%Consumed.csv again to create new rows
    with open(fbConsumedPath, 'r') as fbConsumedFile:
        # get fuelbed_number from column K, row 1, then create 7 rows based on columns L to R
        # make a new fuelbed number 52_1, 52_2, ..., 52_7
        reader = csv.reader(fbConsumedFile)
        all_rows = list(reader)
        fuelbed_number = all_rows[0][10] # column K

        # get the column names from J 10 - 42
        # create a list of column names from rows 10 to 42 in column J
        columnNames = []
        for row_index in range(10, 43):
            columnNames.append(all_rows[row_index][9])  # column J
            
        print(columnNames)
        # replace total_piles with pile_clean_loading
        for idx, name in enumerate(columnNames):
            if name == 'total piles':
                columnNames[idx] = 'pile_clean_loading'

        # add additional required columns (see below where hardcoded values are set)
        columnNames.extend(['shrubs_primary_perc_live', 'shrubs_secondary_perc_live',
                            'nw_primary_perc_live', 'nw_secondary_perc_live',
                            'litter_depth', 'lichen_depth', 'moss_depth',
                            'duff_lower_depth', 'duff_upper_depth',
                            'cover_type', 'ecoregion',
                            'pile_dirty_loading', 'pile_vdirty_loading',
                            'efg_natural', 'efg_activity'])


        # write header row for this fuelbed_number
        # 'GeneratorName=FCCS 4.0,GeneratorVersion=3.0.0,DateCreated=01/02/2026.'
        writer.writerow(['GeneratorName=FCCS 4.0', 'GeneratorVersion=3.0.0', 'DateCreated=01/02/2026.'])
        writer.writerow(['fuelbed_number'] + ['FCCSID'] + columnNames)

        # get the values from column L to R for rows 11 to 43
        for i in range(7):
            new_fuelbed_number = f"{fuelbed_number}_{i+1}"
            values = []
            for row_index in range(10, 43):
                values.append(all_rows[row_index][11 + i])  # columns L to R are 11 to 17

            # add placeholder values for the additional columns
            values.extend(['89', '95',  # shrubs_primary_perc_live, shrubs_secondary
                            '70', '80',  # nw_primary_perc_live, nw_secondary_perc_live
                            '0.7', '0.1', '.2',  # litter_depth, lichen_depth, moss_depth
                            '1.5', '1.1',  # duff_lower_depth, duff_upper_depth
                            '118', '240', # cover_type, ecoregion
                            '0', '0',   # pile_dirty_loading, pile_vdirty_loading
                            '8', '1'  # efg_natural, efg_activity
                            ])

            # write the values row for this fuelbed_number
            writer.writerow([fuelbed_number] +[new_fuelbed_number] + values)


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

with open(inputFilePath, 'w', newline='') as inputFile:
    writer = csv.writer(inputFile)
    # write header
    writer.writerow(['area','fm_duff','fm_1000hr','can_con_pct','shrub_black_pct','pile_black_pct','fuelbeds','units','ecoregion','fm_litter','season','rotten_cwd_pct_available','duff_pct_available','sound_cwd_pct_available'])
    # write 7 rows for each fuelbed_number
    for i in range(7):
        new_fuelbed_number = f"{fuelbed_number}000{i+1}"
        # example values, modify as needed
        writer.writerow([100,150,80,0,50,90,fuelbed_number,'tons','western',15,'spring',50,30,0])
        writer.writerow([100,150,80,0,50,90,fuelbed_number,'tons','western',15,'spring',20,10,0])
        writer.writerow([100,60,25,0,100,90,fuelbed_number,'tons','western',12,'fall',100,100,20])
        writer.writerow([100,60,35,0,100,90,fuelbed_number,'tons','western',12,'fall',50,50,0])
        writer.writerow([100,30,35,20,100,90,fuelbed_number,'tons','western',12,'summer',100,100,100])
        writer.writerow([100,30,25,50,100,90,fuelbed_number,'tons','western',9,'summer',100,100,100])
        writer.writerow([100,30,10,90,100,100,fuelbed_number,'tons','western',3,'summer',100,100,100])


print('Created adjusted loadings and input files based on consumption data.')

print('Run Consume against these new files to generate emissions estimates:')
print('Example: (my310env) bdxfer@SEFS-A-DRYE consume813 % python consume_batch.py -f adjusted_fccs_loadings.csv -o consume_output_2026_01_02.csv natural input_file_for_adjusted.csv')


