#
# Load this script in RStudio to compare disturbance timestep trends by fuelbed and column
#
# The output files that are compared are created using commands like: 
# python3 consume_batch.py -f ../landfiredisturbance/run_landfire/deliverables284/consume_loadings.csv 
# -o consumeOutputFromDeliverables284.csv natural 
# ./visualizer/deliverableInputFileWestern.csv
#
# (note: the input file deliverableInputFileWestern.csv is a custom input file made to match the number
#  of rows in the deliverables284/consume_loadings.csv)
#
#
# Copy the following files to the same directory as this script:
# consumeOutputFromBaseline276.csv
# consumeOutputFromDeliverables276.csv
# consumeOutputFromBaseline284.csv
# consumeOutputFromDeliverables284.csv
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

fccsBaselineData284 = read.csv("consumeOutputFromBaseline284.csv", header=T)
dim(fccsBaselineData284)

fccsData284 = read.csv("consumeOutputFromDeliverables284.csv", header=T)
dim(fccsData284)

fccsBaselineData276 = read.csv("consumeOutputFromBaseline276.csv", header=T)
dim(fccsBaselineData276)

fccsData276 = read.csv("consumeOutputFromDeliverables276.csv", header=T)
dim(fccsData276)


myPlot <- function(fb_number, disturbance, columnName){
  
  disturbance <- substring(disturbance, 1, 1)
  
  baselineData276 <- fccsBaselineData276[fccsBaselineData276$fuelbeds == fb_number, c('fuelbeds', columnName, 'filename')]
  baselineData284 <- fccsBaselineData284[fccsBaselineData284$fuelbeds == fb_number, c('fuelbeds', columnName, 'filename')]
  
  bdtest <- paste(fb_number, disturbance, sep="_")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- apply(expand.grid(bdtest, c(1,2,3)), 1, paste, collapse="")
  bdtest <- sort(bdtest)
  
  fb_data276 <- fccsData276[fccsData276$fuelbeds %in% bdtest, c('fuelbeds', columnName, 'filename')]
  prefix276 <- substr(fb_data276$fuelbeds, 0, nchar(fb_number) + 3)
  timeStep276 <- substr(fb_data276$fuelbeds, nchar(fb_number) + 4, nchar(fb_number) + 4)
  
  fb_data284 <- fccsData284[fccsData284$fuelbeds %in% bdtest, c('fuelbeds', columnName, 'filename')]
  prefix284 <- substr(fb_data284$fuelbeds, 0, nchar(fb_number) + 3)
  timeStep284 <- substr(fb_data284$fuelbeds, nchar(fb_number) + 4, nchar(fb_number) + 4)
  
  fb_data276$Prefix <- prefix276
  fb_data276$TimeStep <- as.numeric(timeStep276)
  
  fb_data284$Prefix <- prefix284
  fb_data284$TimeStep <- as.numeric(timeStep284)
  
  baselineDataExpanded276 <- baselineData276[rep(row.names(baselineData276), length(unique(fb_data276$Prefix))), 1:3]
  baselineDataExpanded276$Prefix <- unique(fb_data276$Prefix)
  baselineDataExpanded276$TimeStep <- rep(0, length(unique(fb_data276$Prefix)))
  
  baselineDataExpanded284 <- baselineData284[rep(row.names(baselineData284), length(unique(fb_data284$Prefix))), 1:3]
  baselineDataExpanded284$Prefix <- unique(fb_data284$Prefix)
  baselineDataExpanded284$TimeStep <- rep(0, length(unique(fb_data284$Prefix)))
  
  combinedData276 <- rbind(fb_data276, baselineDataExpanded276)
  combinedData284 <- rbind(fb_data284, baselineDataExpanded284)
  
  mygraph276 <- ggplot(data = combinedData276, aes_string(x="TimeStep", y=columnName)) + geom_line(aes(colour=Prefix))
  mygraph276 <- mygraph276 + guides(colour=guide_legend(title="Disturbance"))
  mygraph276 <- mygraph276 + ggtitle(paste(combinedData276$filename[1], "Original Calculations (FCCS build 276)", sep=" ")) + xlim(0,3)
  mygraph276 <- mygraph276 + scale_color_manual(values = c("green4", "orange", "red"))
  
  mygraph284 <- ggplot(data = combinedData284, aes_string(x="TimeStep", y=columnName)) + geom_line(aes(colour=Prefix))
  mygraph284 <- mygraph284 + guides(colour=guide_legend(title="Disturbance"))
  mygraph284 <- mygraph284 + ggtitle(paste(combinedData284$filename[1], "New Calculations (FCCS build 284)", sep=" ")) + xlim(0,3)
  mygraph284 <- mygraph284 + scale_color_manual(values = c("green4", "orange", "red"))
  
  grid.arrange(mygraph276, mygraph284, nrow=2)
  
}
manipulate(myPlot(fb_number, disturbance, columnName), fb_number = picker(lapply(fccsBaselineData284$fuelbeds, as.character)), 
           disturbance = picker("1 Fire", "2 Mechanical Add", "3 Mechanical Remove", "4 Wind", "5 Insect & Disease"), 
           columnName = picker(lapply(colnames(fccsBaselineData284), as.character)))

