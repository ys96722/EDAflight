
# load library
library(biganalytics)
library(foreach)
library(ggplot2)
library(gplots)
library(treemap)
library(MASS)
library(reshape2)
library(readr)

# the following code is based on the following source:
# lecture code Chapter5.R, heatmaptreemapdensityplot.R
# circle_diagrams.R

# load data

# Creat big matrix object
x1 <- read.big.matrix("original_datasets/airlines98.csv", header = TRUE,
                      backingfile = "air98.bin",
                      descriptorfile = "air98.desc",
                      type = "integer")
x2 <- read.big.matrix("original_datasets/airlines06.csv", header = TRUE,
                      backingfile = "air06.bin",
                      descriptorfile = "air06.desc",
                      type = "integer")

# # once created, only attach needed
# x1 <- attach.big.matrix("air98.desc")
# x2 <- attach.big.matrix("air06.desc")

# load datasets created by hive
byState = read_csv("generated_datasets/byState.csv")
byCord = read_csv("generated_datasets/byCord.csv")
byCarr = read_csv("generated_datasets/byCarr.csv")
bymodel = read_csv("generated_datasets/bymodel.csv")
top5 = read.csv("generated_datasets/top5.csv", header = FALSE)

# creating plot for monthly/weekofday delay
# prepare data
# Monthly DepDelay
monthMean06dep <- foreach(i = 1:12, .combine=c) %do% {
  sum((x2[,"Month"] == i)*(x2[,"DepDelay"]), na.rm = T)/sum(x2[,"Month"] == i)
}
monthMean98dep <- foreach(i = 1:12, .combine=c) %do% {
  sum((x1[,"Month"] == i)*(x1[,"DepDelay"]), na.rm = T)/sum(x1[,"Month"] == i)
}

# Monthly ArrDelay
monthMean06arr <- foreach(i = 1:12, .combine=c) %do% {
  sum((x2[,"Month"] == i)*(x2[,"ArrDelay"]), na.rm = T)/sum(x2[,"Month"] == i)
}
monthMean98arr <- foreach(i = 1:12, .combine=c) %do% {
  sum((x1[,"Month"] == i)*(x1[,"ArrDelay"]), na.rm = T)/sum(x1[,"Month"] == i)
}

# Day of week DepDelay
weekMean06dep <- foreach(i = 1:7, .combine=c) %do% {
  sum((x2[,"DayOfWeek"] == i)*(x2[,"DepDelay"]), na.rm = T)/sum(x2[,"DayOfWeek"] == i)
}
weekMean98dep <- foreach(i = 1:7, .combine=c) %do% {
  sum((x1[,"DayOfWeek"] == i)*(x1[,"DepDelay"]), na.rm = T)/sum(x1[,"DayOfWeek"] == i)
}
# Day of week ArrDelay
weekMean06arr <- foreach(i = 1:7, .combine=c) %do% {
  sum((x2[,"DayOfWeek"] == i)*(x2[,"ArrDelay"]), na.rm = T)/sum(x2[,"DayOfWeek"] == i)
}
weekMean98arr <- foreach(i = 1:7, .combine=c) %do% {
  sum((x1[,"DayOfWeek"] == i)*(x1[,"ArrDelay"]), na.rm = T)/sum(x1[,"DayOfWeek"] == i)
}

Week = c(1:7)
Month = c(1:12)

# make the monthly plot
png(filename="plots/Monthly Average Delay.png", width=700, height=432)
plot(Month, monthMean06dep, col="#0072B2", type = "o", pch="o", lty=1, 
     ylim=c(0, 15), xlim=c(1,12), 
     ylab="mean(Delay)",
     xlab="Month",
     main="Monthly Average Delay")
points(Month, monthMean98dep, col="#D55E00",pch="o")
lines(Month, monthMean98dep, col="#D55E00", lty=1)

points(Month, monthMean06arr, col="#0072B2",pch="+")
lines(Month, monthMean06arr, col="#0072B2", lty=3)

points(Month, monthMean98arr, col="#D55E00",pch="+")
lines(Month, monthMean98arr, col="#D55E00", lty=3)

legend(x=1, y = 5,  
       legend=c("ArrDelay 2006", "ArrDelay 1998", "DepDelay 2006", "DepDelay 2006"),
       col=c("#0072B2", "#D55E00", "#0072B2","#D55E00"), 
       lty=c(3,3,1,1), pch=c("+","+","o","o"))
dev.off()

# make the week of day plot
png(filename="plots/Day of Week Average Delay.png", width=700, height=432)
plot(Week, weekMean06dep, col="#0072B2", type = "o", pch="o", lty=1, 
     ylim=c(0,15), xlim=c(1,7), 
     ylab="mean(Delay)",
     xlab="Day of Week",
     main="Day of Week Average Delay")
points(Week, weekMean98dep, col="#D55E00",pch="o")
lines(Week, weekMean98dep, col="#D55E00", lty=1)

points(Week, weekMean06arr, col="#0072B2",pch="+")
lines(Week, weekMean06arr, col="#0072B2", lty=3)

points(Week, weekMean98arr, col="#D55E00",pch="+")
lines(Week, weekMean98arr, col="#D55E00", lty=3)

legend(x=1, y = 5,  
       legend=c("ArrDelay 2006", "ArrDelay 1998", "DepDelay 2006", "DepDelay 2006"),
       col=c("#0072B2", "#D55E00", "#0072B2","#D55E00"), 
       lty=c(3,3,1,1), pch=c("+","+","o","o"))
dev.off()
# create delay reason plot
stack.data = x2[,c(25:29,2)]
month <- split(1:nrow(stack.data), stack.data[,6])
month.sum1<- foreach(monthInds = month, .combine = cbind) %do% {
  sum(stack.data[monthInds,1])
}
month.sum2<- foreach(monthInds = month, .combine = cbind) %do% {
  sum(stack.data[monthInds,2])
}
month.sum3<- foreach(monthInds = month, .combine = cbind) %do% {
  sum(stack.data[monthInds,3])
}
month.sum4<- foreach(monthInds = month, .combine = cbind) %do% {
  sum(stack.data[monthInds,4])
}
month.sum5<- foreach(monthInds = month, .combine = cbind) %do% {
  sum(stack.data[monthInds,5])
}

plot.data=rbind(month.sum1,month.sum2,month.sum3,month.sum4,month.sum5)
colnames(plot.data)=c("Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec")
# Get the stacked barplot
png(filename="plots/Delay Time for Each Reason in 2006.png", width=750, height=432)
barplot(plot.data, 
        xlim=c(0, ncol(plot.data) + 3),
        col=colors()[c(20,40,60,180,12)] , border="white", space=0.04, font.axis=2,
        xlab="Month",ylab="Minutes",
        main = "Delay Time for Each Reason in 2006",
        legend.text = c("CarrierDelay", "WeatherDelay","NASDelay","SecurityDelay","LateAircraftDelay"),
        args.legend=list(
          x=ncol(plot.data) + 4,
          y=max(colSums(plot.data)),
          bty = "n"
        ))
dev.off()
# creating percentile plot for June
probs = seq(0.50,0.99,0.01)
perc1 = quantile(x1[(x1[,"Month"]==6), "DepDelay"], probs, na.rm=TRUE)
perc2 = quantile(x2[(x2[,"Month"]==6), "DepDelay"], probs, na.rm=TRUE)

perc12 = cbind(perc1, perc2)
colnames(perc12) = c("1998", "2006")
dq = melt(perc12)
names(dq) = c("percentile", "Year", "DepDelay")
dq$Year = factor(dq$Year)

png(filename="plots/Percentile of Depature Delay in June.png", width=700, height=432)
qplot(as.numeric(percentile), DepDelay, data = dq, 
      color = Year, geom = "point", xlab = "Percentile", 
      main ="Percentile of Depature Delay in June")
dev.off()
# make the tree plots
# by State
cols = c("num_cancl", "r_cancl", "num_dely", "r_dely", "avg_dely")
titles = c("Number of Cancellation for Each State", "Cancellation Rate for Each State", 
           "Number of Delay for Each State", "Delay Rate for Each State", "Average Delay Time for Each State")
for(i in 1:5){
  png(filename=paste("plots/", titles[i], ".png", sep = ""), 
                 width=700, height=432)
  treemap(byState,
          index=c("year", "state"),
          vSize="num_flight",
          vColor=cols[i],
          type="value",
          title = titles[i])
  dev.off()
}


# by Carrier
cols = c("num_cancl", "r_cancl", "num_dely", "r_dely", "avg_dely")
titles = c("Number of Cancellation for Each Carrier", "Cancellation Rate for Each Carrier", 
           "Number of Delay for Each Carrier", "Delay Rate for Each Carrier", "Average Delay Time for Each Carrier")
for(i in 1:5){
  png(filename=paste("plots/", titles[i], ".png", sep = ""), 
      width=700, height=432)
  treemap(byCarr,
          index=c("year", "carrier"),
          vSize="num_flight",
          vColor=cols[i],
          type="value",
          title = titles[i])
  dev.off()
}

# by model
cols = c("r_cancl", "r_dely")
titles = c("Cancellation Rate for Each Model", "Delay Rate for Each Model")
for(i in 1:2){
  png(filename=paste("plots/", titles[i], ".png", sep = ""), 
      width=700, height=432)
  treemap(bymodel,
          index=c("year","manufacturer","model"),
          vSize="num_flight",
          vColor=cols[i],
          type="value",
          title=titles[i])
  dev.off()
}




# Chord Diagram
# flights between states
start = top5$V3
end = top5$V4

mat = matrix(0, nrow = length(unique(start)),
ncol = length(unique(end))
)

rownames(mat) = unique(start)
colnames(mat) = unique(end)

for(i in seq_along(start)) mat[start[i], end[i]] = 1+ mat[start[i], end[i]]

grid.col1 = c( "#E69F00", "#56B4E9", "#D55E00", "#009E73","#F0E442")

png(filename=paste("plots/", "Chord Diagram of Flights Between States" , ".png", sep = "")
chordDiagram(mat, grid.col = grid.col1)
dev.off()

# delayed flights between states
delay_top5 = top5[top5$V1==1,]
start = delay_top5$V3
end = delay_top5$V4

# Create Adjacency Matrix
mat1 = matrix(0, nrow = length(unique(start)),
ncol = length(unique(end))
)

rownames(mat1) = unique(start)
colnames(mat1) = unique(end)

for(i in seq_along(start)) mat1[start[i], end[i]] = 1 + mat1[start[i], end[i]]

png(filename=paste("plots/", "Chord Diagram of Delayed Flights Between States" , ".png", sep = "")
chordDiagram(mat1, grid.col = grid.col1, directional = TRUE)
dev.off()
