
fuelbedsOfInterest = [1, 6, 14, 22, 28, 34, 56, 57, 66, 67, 69, 109, 110, 131, 135, 154, 190, 224, 237, 240, 282, 308, 312, 326, 358, 412, 414, 416, 423, 459, 460, 518, 519, 528, 529,1264]

fccs_loadings_path = '/Users/briandrye/Downloads/001SusanPCustom/fccs_loadings.csv'

# create a loadings file with just the fuelbeds of interest
# loop through the fccs_loadings.csv file, if the fuelbed_number is in the fuelbedsOfInterest list, write it to a new file called fccs_loadings_custom.csv
with open(fccs_loadings_path, 'r') as f:
    lines = f.readlines()
    header = lines[0]
    header2 = lines[1]
    with open('/Users/briandrye/Downloads/001SusanPCustom/fccs_loadings_custom.csv', 'w') as out:
        out.write(header)
        out.write(header2)
        for line in lines[2:]:
            fuelbed_number = int(line.split(',')[0])
            if fuelbed_number in fuelbedsOfInterest:
                out.write(line)


# create an input file with just the fuelbeds of interest, with these settings for all fuelbeds:
# fuelbeds,area,fm_duff,fm_1000hr,can_con_pct,shrub_black_pct,pile_black_pct,units,ecoregion,fm_litter,season,duff_pct_available,sound_cwd_pct_available,rotten_cwd_pct_available
# 52,1,40,15,0,50,90,tons,western,10,fall,55,55,70

with open('/Users/briandrye/Downloads/001SusanPCustom/input_file_default.csv', 'w') as out:
    out.write('fuelbeds,area,fm_duff,fm_1000hr,can_con_pct,shrub_black_pct,pile_black_pct,units,ecoregion,fm_litter,season,duff_pct_available,sound_cwd_pct_available,rotten_cwd_pct_available\n')
    for fuelbed_number in fuelbedsOfInterest:
        out.write(f"{fuelbed_number},1,40,15,0,50,90,tons,western,10,fall,55,55,70\n")

# also create a scenario file with just the fuelbeds of interest, with these settings for all fuelbeds:
#fuelbeds,area,fm_duff,fm_1000hr,can_con_pct,shrub_black_pct,pile_black_pct,units,ecoregion,fm_litter,season,duff_pct_available,sound_cwd_pct_available,rotten_cwd_pct_available
#52,1,20,10,75,100,90,tons,western,4,fall,70,70,70

with open('/Users/briandrye/Downloads/001SusanPCustom/input_file_custom.csv', 'w') as out:
    out.write('fuelbeds,area,fm_duff,fm_1000hr,can_con_pct,shrub_black_pct,pile_black_pct,units,ecoregion,fm_litter,season,duff_pct_available,sound_cwd_pct_available,rotten_cwd_pct_available\n')
    for fuelbed_number in fuelbedsOfInterest:
        out.write(f"{fuelbed_number},1,20,10,75,100,90,tons,western,4,fall,70,70,70\n")

# show example command to run consume against these new files to generate emissions estimates:
print('Example: (my310env) bdxfer@SEFS-A-DRYE consume813 % python consume_batch.py -f ~/Downloads/001SusanPCustom/fccs_loadings_custom.csv -o ~/Downloads/001SusanPCustom/consume_output_default.csv natural ~/Downloads/001SusanPCustom/input_file_default.csv')
print('Example: (my310env) bdxfer@SEFS-A-DRYE consume813 % python consume_batch.py -f ~/Downloads/001SusanPCustom/fccs_loadings_custom.csv -o ~/Downloads/001SusanPCustom/consume_output_custom.csv natural ~/Downloads/001SusanPCustom/input_file_custom.csv')



