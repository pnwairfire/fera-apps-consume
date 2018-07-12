#
# Load this script in RStudio to compare disturbance timestep trends by fuelbed and column
#
# The output files are created using Consume version 4 (from FFT) and Consume version 5 (from bitbucket)
#
# The input files were created in Landfire (using FCCS build 284)
# 
# change directory to Consume v4  (paths below are from Brian Drye's dev machine)
#
# python3 consume_batch.py -f ~/repos/uw/landfiredisturbance/run_landfire/deliverables284/consume_loadings.csv 
# -o consumeV4OutputFromDeliverables284.csv natural ~/repos/uw/apps-consume/visualizer/deliverableInputFileWestern.csv

# python3 consume_batch.py -f ~/repos/uw/landfiredisturbance/run_landfire/baseline284/consume_loadings.csv 
# -o consumeV4OutputFromBaseline284.csv natural ~/repos/uw/apps-consume/test/regression_input_western.csv

#
# change directory to Consume v5  
#
# python3 consume_batch.py -f ../landfiredisturbance/run_landfire/deliverables284/consume_loadings.csv 
# -o consumeV5OutputFromDeliverables284.csv natural 
# ./visualizer/deliverableInputFileWestern.csv
#
# python3 consume_batch.py -f ../landfiredisturbance/run_landfire/baseline284/consume_loadings.csv 
# -o consumeV5OutputFromBaseline284.csv natural ./test/regression_input_western.csv


# (note: the input file deliverableInputFileWestern.csv is a custom input file made to match the number
#  of rows in the deliverables284/consume_loadings.csv)
#
#
# Copy the following files to the same directory as this script:
# consumeV4OutputFromBaseline284.csv
# consumeV4OutputFromDeliverables284.csv
# consumeV5OutputFromBaseline284.csv
# consumeV5OutputFromDeliverables284.csv
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

v5BaselineData = read.csv("consumeV5OutputFromBaseline284.csv", header=T)
dim(v5BaselineData)

v5DeliverableData = read.csv("consumeV5OutputFromDeliverables284.csv", header=T)
dim(v5DeliverableData)

v4BaselineData = read.csv("consumeV4OutputFromBaseline284.csv", header=T)
dim(v4BaselineData)

v4DeliverableData = read.csv("consumeV4OutputFromDeliverables284.csv", header=T)
dim(v4DeliverableData)


myPlot <- function(fb_number, disturbance, columnName){
  
  disturbance <- substring(disturbance, 1, 1)
  
  v4SelectedBaselineData <- v4BaselineData[v4BaselineData$fuelbeds == fb_number, c('fuelbeds', columnName, 'filename')]
  v5SelectedBaselineData <- v5BaselineData[v5BaselineData$fuelbeds == fb_number, c('fuelbeds', columnName, 'filename')]
  
  bdtest <- paste(fb_number, disturbance, sep="_")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- sort(bdtest)
  
  v4SelectedDeliverableData <- v4DeliverableData[v4DeliverableData$fuelbeds %in% bdtest, c('fuelbeds', columnName, 'filename')]
  prefixV4 <- substr(v4SelectedDeliverableData$fuelbeds, 0, nchar(fb_number) + 3)
  timeStepV4 <- substr(v4SelectedDeliverableData$fuelbeds, nchar(fb_number) + 4, nchar(fb_number) + 4)
  
  v5SelectedDeliverableData <- v5DeliverableData[v5DeliverableData$fuelbeds %in% bdtest, c('fuelbeds', columnName, 'filename')]
  prefixV5 <- substr(v5SelectedDeliverableData$fuelbeds, 0, nchar(fb_number) + 3)
  timeStepV5 <- substr(v5SelectedDeliverableData$fuelbeds, nchar(fb_number) + 4, nchar(fb_number) + 4)
  
  v4SelectedDeliverableData$Prefix <- prefixV4
  v4SelectedDeliverableData$TimeStep <- as.numeric(timeStepV4)
  
  v5SelectedDeliverableData$Prefix <- prefixV5
  v5SelectedDeliverableData$TimeStep <- as.numeric(timeStepV5)
  
  v4BaselineDataExpanded <- v4SelectedBaselineData[rep(row.names(v4SelectedBaselineData), length(unique(v4SelectedDeliverableData$Prefix))), 1:3]
  v4BaselineDataExpanded$Prefix <- unique(v4SelectedDeliverableData$Prefix)
  v4BaselineDataExpanded$TimeStep <- rep(0, length(unique(v4SelectedDeliverableData$Prefix)))
  
  v5BaselineDataExpanded <- v5SelectedBaselineData[rep(row.names(v5SelectedBaselineData), length(unique(v5SelectedDeliverableData$Prefix))), 1:3]
  v5BaselineDataExpanded$Prefix <- unique(v5SelectedDeliverableData$Prefix)
  v5BaselineDataExpanded$TimeStep <- rep(0, length(unique(v5SelectedDeliverableData$Prefix)))
  
  v4CombinedData <- rbind(v4SelectedDeliverableData, v4BaselineDataExpanded)
  v5CombinedData <- rbind(v5SelectedDeliverableData, v5BaselineDataExpanded)
  
  graphV4 <- ggplot(data = v4CombinedData, aes_string(x="TimeStep", y=columnName)) + geom_line(aes(colour=Prefix))
  graphV4 <- graphV4 + guides(colour=guide_legend(title="Disturbance"))
  graphV4 <- graphV4 + ggtitle(paste(v4CombinedData$filename[1], "Consume V4", sep=" ")) + xlim(0,3)
  graphV4 <- graphV4 + scale_color_manual(values = c("green4", "orange", "red"))
  
  graphV5 <- ggplot(data = v5CombinedData, aes_string(x="TimeStep", y=columnName)) + geom_line(aes(colour=Prefix))
  graphV5 <- graphV5 + guides(colour=guide_legend(title="Disturbance"))
  graphV5 <- graphV5 + ggtitle(paste(v5CombinedData$filename[1], "Consume V5", sep=" ")) + xlim(0,3)
  graphV5 <- graphV5 + scale_color_manual(values = c("green4", "orange", "red"))
  
  grid.arrange(graphV4, graphV5, nrow=2)
  
}
manipulate(myPlot(fb_number, disturbance, columnName), fb_number = picker(lapply(v5BaselineData$fuelbeds, as.character)), 
           disturbance = picker("1 Fire", "2 Mechanical Add", "3 Mechanical Remove", "4 Wind", "5 Insect & Disease"), 
           columnName = picker(lapply(colnames(v5BaselineData), as.character)))

