# consume file generator
# create a loadings file and corresponding input file for fuelbeds in fuelbedList
# note: this only creates disturbances in 111 - 333 range. 411 -533 not included.

# Command to run afterwards: 
# (my310env) briandrye@Brians-MacBook-Pro consume813 % python consume_batch.py -f new_fccs_loadings.csv -o consume_output.csv natural input_file.csv


# this is old fccs_loadings with overstory 1.8 for FB52 (don't use
#fccsLoadingsPath = '/Users/briandrye/Downloads/consume813/consume/input_data/fccs_loadings.csv'

# use latest fccs_loadings where overstory for FB52 is
fccsLoadingsPath = '/Users/briandrye/repos/uw/apps-consumeGIT/consume/input_data/fccs_loadings.csv'
newFccsLoadingsPath = '/Users/briandrye/Downloads/consume813/consume/input_data/new_fccs_loadings2026_01_30.csv'
inputFilePath = '/Users/briandrye/Downloads/consume813/consume/input_data/input_file2026_01_30.csv'
scenarioPath =  '/Users/briandrye/Downloads/consume813/EmissonsTradeoffs_ConsumeScenarios.csv'

#fuelbedList = [1,4,8,9,13,21,22,24,28,41,52,53,56,57,59,60,61,63,208,238,308,319,329,530,1262,1264]
#fuelbedList = [0,1,4,21,22,24,28,52,57,59,61,63,208,224,235,237,238,302,308,319,1226,1229,1230,1232,1262,1264,1271]
#fuelbedList = [0,1,4,21,22,24,28,52,57,59,61,63,208,224,235,237,238,302,308,319,1226,1229,1232,1262,1271]
#fuelbedList = [0,1,4,21,22,24,28,52,57,59,61,63,208,224,235,237,238,302,308,319,1271]
# don't include zero. It will cause trouble when running consume because "000001" will become 1 and not match
# False, "Error: Invalid fuelbed specified"
fuelbedList =  [1, 6, 8, 9, 10, 13, 20, 22, 28, 48, 52, 53, 56, 57, 59, 60, 70, 95, 208, 224, 235, 237, 292, 304, 305, 308, 310, 315, 321, 331, 358, 360, 361, 483, 493, 494, 496, 497, 498, 506, 514, 529, 530, 531, 532, 1223, 1232, 1262, 1264, 1273]
 # 1/30/2026
fbListWithVariations = []
print(len(fuelbedList))

# create a list of fuelbed_numbers 1, 10111, 10112, etc.
# adjust the first range to get 400 and/or 500: "for i in range(1,6)"" would do 111 through 533
for fb_num in fuelbedList:
    print(fb_num)
    fbListWithVariations.append(str(fb_num))
    for i in range(1,4):
        for j in range(1,4):
            for k in range(1,4):
                print(str(fb_num) + '0'+ str(i) + str(j) + str(k))
                fbListWithVariations.append(str(fb_num) + '0'+ str(i) + str(j) + str(k))

print('number of fuelbed variations: ', len(fbListWithVariations))
print('wait... not done yet')
# 728

# get all the lines from the fccs_loadings.csv file that have a fuelbed_number in the fbListWithVariations list
# create a new csv with these lines: new_fccs_loadings.csv
# also create a new input_file.csv based on EmissonsTradeoffs_ConsumeScenarios.csv 
with open(fccsLoadingsPath, 'r') as file:
    loadingsData = file.read()

    # open the scenario file and get the header
    with open(scenarioPath, 'r') as scenarioFile:
        scenarioData = scenarioFile.read()
        scenarioLines = scenarioData.split('\n')
        inputHeader = scenarioLines[0]
        # remove first 3 (unneeded) columns named "Abbrev. Scen.", "Scenario"
        inputHeader = inputHeader.replace(',Scenario,', '')
        inputHeader = inputHeader.replace('Abbrev. Scen.,', '')

        with open(inputFilePath, 'w') as newInputFile:
            newInputFile.write(inputHeader + '\n')

            # split the file into lines
            lines = loadingsData.split('\n')

            with open(newFccsLoadingsPath, 'w') as newLoadingsFile:
                newLoadingsFile.write(lines[0] + '\n')
                newLoadingsFile.write(lines[1] + '\n')

                # find corresponding lines in the fccs_loadings.csv file, slow but comes out in desired order
                for fb_num in fbListWithVariations:
                    found = False
                    # make a copy of scenarioLines to modify
                    tempScenarioLines = scenarioLines.copy()

                    for line in lines:
                        columns = line.split(',')
                        if columns[0] == fb_num:
                            found = True
#                            scenarios = ['SpringRx', 'SpringRxRed', 'FallRx', 'FallRxRed', 'WFLow', 'WFMod', 'WFHigh']
                            for i in range(1,8):
                                # set (don't replace) fuelbed_number in line with fb_num + "_" + scenarios[i-1], only in first column
                                # remove whatever is in first column
                                tempCols = line.split(',')
                                # then add new fuelbed number
                                newFuelbedString = fb_num + "0" + str(i)
                                if int(fb_num) <= 1297:
                                    newFuelbedString = fb_num + "00000" + str(i)

                                tempCols[0] = newFuelbedString
                                line = ','.join(tempCols)

#                                line = line.replace(columns[0], str(fb_num) + "_" + scenarios[i-1], 1)
                                newLoadingsFile.write(line + '\n')
                                # in scenarioLines[i], replace "populate rows for each FBID" with fb_num
                                tempScenarioLines[i] = tempScenarioLines[i].replace('populate rows for each FBID', newFuelbedString)
                                # remove first 3 strings in tempScenarioLines[i] separated by commas
                                tempScenarioLines[i] = tempScenarioLines[i].split(',', 3)[3]  # split on first 3 commas
                                newInputFile.write(tempScenarioLines[i] + '\n')
                    if not found:
                        print('not found: ' + fb_num)





