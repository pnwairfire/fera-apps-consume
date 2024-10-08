# consume file generator
# create a loadings file and corresponding input file for fuelbeds in fuelbedList
# note: this only creates disturbances in 111 - 333 range. 411 -533 not included.

# Command to run afterwards: 
# (my310env) briandrye@Brians-MacBook-Pro consume813 % python consume_batch.py -f new_fccs_loadings.csv -o consume_output.csv natural input_file.csv


fccsLoadingsPath = '/Users/briandrye/Downloads/consume (1)/consume/input_data/fccs_loadings.csv'
newFccsLoadingsPath = '/Users/briandrye/Downloads/consume (1)/consume/input_data/new_fccs_loadings.csv'
inputFilePath = '/Users/briandrye/Downloads/consume (1)/consume/input_data/input_file.csv'
scenarioPath =  '/Users/briandrye/Downloads/EmissonsTradeoffs_ConsumeScenarios.csv'

fuelbedList = [1,4,8,9,13,21,22,24,28,41,52,53,56,57,59,60,61,63,208,238,308,319,329,530,1262,1264]
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

        with open(inputFilePath, 'a') as newInputFile:
            newInputFile.write(inputHeader + '\n')

            # split the file into lines
            lines = loadingsData.split('\n')

            with open(newFccsLoadingsPath, 'a') as newLoadingsFile:
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
                            for i in range(1,8):
                                newLoadingsFile.write(line + '\n')
                                # in scenarioLines[i], replace "populate rows for each FBID" with fb_num
                                tempScenarioLines[i] = tempScenarioLines[i].replace('populate rows for each FBID', str(fb_num))
                                # remove first 3 strings in tempScenarioLines[i] separated by commas
                                tempScenarioLines[i] = tempScenarioLines[i].split(',', 3)[3]  # split on first 3 commas
                                newInputFile.write(tempScenarioLines[i] + '\n')
                    if not found:
                        print('not found: ' + fb_num)





