# Fetch command line arguments
myArgs <- commandArgs(trailingOnly = TRUE)
source("functions.R")
source("./length_scale_model/sphharm_basis.R") # provides sphharm.basis
# First, set your working directory (see episode 'Analyzing Patient Data' for more
# info)
inputFileName <- myArgs[1]
outputFileName <- myArgs[2]
#inputFileName <- "/Volumes/discovery/azuri/data/gaia/dr2/xy/GaiaSource_0.008839-0.017678_0.008839-0.017678_xyz.csv"
#outputFileName <- "/Volumes/discovery/azuri/data/gaia/dr2_distances/xy/GaiaSource_0.008839-0.017678_0.008839-0.017678_xyz_dist.csv"
print(c("inputFileName = ",inputFileName,", outputFileName = ",outputFileName))

data <- read.csv(file=inputFileName)
print(c("data has ",nrow(data)," rows"))
data <- data[!is.na(data$parallax), ]
print(c("data has ",nrow(data)," rows"))
#print(head(data))
glons <- as.numeric(data$l)
glats <- as.numeric(data$b)
ws <- as.numeric(data$parallax)
wsds <- as.numeric(data$parallax_error)
rlen <-  NA # length scale in pc
# Plotting parameters in pc
# rlo,rhi are range for computing normalization of posterior
# rplotlo, rplothi are plotting range (computed automatically if set to NA)
rlo <- 0
rhi <- 1e5
rplotlo <- NA
rplothi <- NA

data$`rEst[pc]` <- numeric(nrow(data))
data$`rLo[pc]` <- numeric(nrow(data))
data$`rHi[pc]` <- numeric(nrow(data))
data$`rLen[pc]` <- numeric(nrow(data))
data$result_flag <- integer(nrow(data))
data$modality_flag <- integer(nrow(data))
#print(ws)
for (i in 1:length(ws)) {
  print(c("i = ",i,", ws[[i]] = ",ws[[i]]))
  if(!is.na(ws[[i]])) {
    w <- ws[[i]]+0.029
    wsd <- wsds[[i]]
    glon <- glons[[i]]
    glat <- glats[[i]]
    rlen <-  NA # length scale in pc
    # Plotting parameters in pc
    # rlo,rhi are range for computing normalization of posterior
    # rplotlo, rplothi are plotting range (computed automatically if set to NA)
    rlo <- 0
    rhi <- 1e5
    rplotlo <- NA
    rplothi <- NA
    res <- getDistFromGaia(w=w, wsd=wsd, glon=glon, glat=glat, calcIfBimod=FALSE)
#    print(c("res = ",res))
#    print(c("res$result_flag = ",res$result_flag))
    data$`rEst[pc]`[[i]] <- res[1]#$`rEst[pc]`
    data$`rLo[pc]`[[i]] <- res[2]#$`rLo[pc]`
    data$`rHi[pc]`[[i]] <- res[3]#$`rHi[pc]`
    data$`rLen[pc]`[[i]] <- res[4]#$`rLen[pc]`
    data$result_flag[[i]] <- res[5]#$result_flag
    data$modality_flag[[i]] <- res[6]#$modality_flag
  }
}
print(c("data has ",nrow(data)," rows"))
data <- data[!is.na(data$`rEst[pc]`), ]
print(c("data has ",nrow(data)," rows"))
write.csv(data,outputFileName, sep=",", row.names = FALSE, quote=FALSE)
