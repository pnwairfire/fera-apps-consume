Readme
created 04/06/2026

/Users/briandrye/Downloads/2026_04_06Scratch/ 

copy fccs_loadings.csv from consume repo: 
https://github.com/pnwairfire/fera-apps-consume/commits/master/consume/input_data/fccs_loadings.csv
(last changed 1/30/2026)

copy EmissonsTradeoffs_ConsumeScenarios.csv to folder from SusanP email

open /Users/briandrye/Downloads/2026_04_06Scratch/createSelectedDisturbanceLoadAndInputFiles.py in PyCharm

set file paths like so: 

fccsLoadingsPath = '/Users/briandrye/Downloads/2026_04_06Scratch/fccs_loadings.csv'
newFccsLoadingsPath = '/Users/briandrye/Downloads/2026_04_06Scratch/loadings_for_run_1.csv'
inputFilePath = '/Users/briandrye/Downloads/2026_04_06Scratch/input_file_for_run_1.csv'
scenarioPath =  '/Users/briandrye/Downloads/2026_04_06Scratch/EmissonsTradeoffs_ConsumeScenarios.csv'

run the script.
this script will create two files: 
loadings_for_run_1.csv
input_file_for_run_1.csv

run consume against these two files... example terminal input/output below

(my310env) bdxfer@SEFS-A-DRYE consume813 % python consume_batch.py -f ~/Downloads/2026_04_06Scratch/loadings_for_run_1.csv -o ~/Downloads/2026_04_06Scratch/consume_output_run_1.csv natural ~/Downloads/2026_04_06Scratch/input_file_for_run_1.csv

Success!!! Description of units used "/Users/briandrye/Downloads/2026_04_06Scratch/consume_output_run_1_units.csv"

Success!!! Results are in "/Users/briandrye/Downloads/2026_04_06Scratch/consume_output_run_1.csv"
(my310env) bdxfer@SEFS-A-DRYE consume813 %

This creates consume_output_run_1.csv

open /Users/briandrye/Downloads/2026_04_06Scratch/createAdjustedLoadingsFromFccsLoadingsAndConsumeOutput.py in PyCharm

set file paths like so: 

# input files
fccsLoadingsPath = '/Users/briandrye/Downloads/2026_04_06Scratch/fccs_loadings.csv'
consumeOutputPath = '/Users/briandrye/Downloads/2026_04_06Scratch/consume_output_run_1.csv'

# output files
newFccsLoadingsPath = '/Users/briandrye/Downloads/2026_04_06Scratch/loadings_for_run_2.csv'
inputFilePath = '/Users/briandrye/Downloads/2026_04_06Scratch/input_file_for_run_2.csv'

# file for comparison
referencePath = '/Users/briandrye/Downloads/2026_04_06Scratch/SPAdjustedFCCSLoadingsFormatted3.csv'
inputReferencePath = '/Users/briandrye/Downloads/2026_04_06Scratch/input_file_reference.csv'

# log of differences between our generated file and the reference file
diffLogPath = '/Users/briandrye/Downloads/2026_04_06Scratch/diff_log.txt'
diffInputLogPath = '/Users/briandrye/Downloads/2026_04_06Scratch/diff_input_log.txt'

run the script. 
this script will create two files: 
loadings_for_run_2.csv
input_file_for_run_2.csv

note: the script will also create two log files diff_log.txt will have a bunch of differences related to zero vs. blank fields. This is ok. We want zeros instead of blanks. If the pile settings are blank, the emissions columns in the next step will come out blank (wrong). 

run consume against the run_2 files... example terminal input/output below

(my310env) bdxfer@SEFS-A-DRYE consume813 %
(my310env) bdxfer@SEFS-A-DRYE consume813 % python consume_batch.py -f ~/Downloads/2026_04_06Scratch/loadings_for_run_2.csv -o ~/Downloads/2026_04_06Scratch/consume_output_after_second_run.csv natural ~/Downloads/2026_04_06Scratch/input_file_for_run_2.csv

Success!!! Description of units used "/Users/briandrye/Downloads/2026_04_06Scratch/consume_output_after_second_run_units.csv"

Success!!! Results are in "/Users/briandrye/Downloads/2026_04_06Scratch/consume_output_after_second_run.csv"
(my310env) bdxfer@SEFS-A-DRYE consume813 % ;

This creates consume_output_after_second_run.csv. This file contains the consumption/emission info of each fuelbed after (7x7) 49 possible scenario combinations. 

