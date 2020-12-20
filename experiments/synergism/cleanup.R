## This script is used to clean up the combination data

setwd("~/Dev/HerbicideDev/Synergism_Analysis")
combination.data <- read.csv("data/combinations.csv", sep = ";")[-c(6,8,4)]
rownames(combination.data) <- combination.data[, 1]
combination.data <- combination.data[-1]
combination.data <- transform(combination.data, appl=as.numeric(appl), day7=as.numeric(day7))
combination.data$effect <- apply(combination.data, 1, function(x){1-as.numeric(x[4])/as.numeric(x[3])})
combination.data.aggregated <- aggregate(effect~combination+concs, combination.data, mean)

combname2values <- function(row){
  
}