#
# Load this script in RStudio to look at changes to consume output based on varying one variable at a time in FB 52
#
# The output files are created using Consume version 5 (from bitbucket)
#
# The input files were created manually, similar to what Landfire creates. 
# 
############## steps to create v5 output files using Western input files #######################
#
# change directory to Consume v5  
#
# python3 consume_batch.py -f ../landfiredisturbance/run_landfire/baseline284/consume_loadingsSensitivityTest.csv 
# -o consumeV5SensitivityOutputWestern.csv natural ./test/sensitivity_input_western.csv
###############################################################################################################
#
# Copy the following files to the same directory as this script:
# consumeV5SensitivityOutput.csv
#
# set the working directory to the source file location
# From RStudio menu: Session->Set Working Directory->To Source File Location
#
# To run: click the "Source" button (you should see two empty graphs)
# click the gear icon in the top left of the graph to select fuelbed, disturbance, and column
#

library(ggplot2) 
library(manipulate)
library(gridExtra)

# Western
# v5BaselineData = read.csv("consumeV5SensitivityOutputWestern.csv", header=T)

# Southern
v5BaselineData = read.csv("consumeV5SensitivityOutputSouthern.csv", header=T)

v5BaselineData[is.na(v5BaselineData)] <- 0

tempDataframe <- data.frame(do.call('rbind', strsplit(as.character(v5BaselineData$fuelbeds),'_',fixed=TRUE)))
colnames(tempDataframe) <- c("root", "increment")

v5BaselineData <- cbind(v5BaselineData, tempDataframe)
v5BaselineData

myPlot <- function(fb, columnName){
 
  v5SelectedBaselineData <- v5BaselineData[v5BaselineData$root == fb, c('root', columnName, 'filename', 'increment', 'c_stump_sound')]
  
  ggplot(v5SelectedBaselineData, aes_string("increment", columnName, colour = "increment")) + 
    geom_point()
  
}
manipulate(myPlot(fb,columnName), 
           fb = picker(lapply(unique(v5BaselineData$root), as.character)),
           columnName = picker(lapply(colnames(v5BaselineData), as.character))
)
