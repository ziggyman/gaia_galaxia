# Fetch command line arguments
myArgs <- commandArgs(trailingOnly = TRUE)
inputFileName <- myArgs[1]
outputFileName <- myArgs[2]

# First, set your working directory (see episode 'Analyzing Patient Data' for more
# info)
#wd <- substr(inputFileName,1,)
#setwd("~/Desktop/r-novice-inflammation/")

data <- read.csv(file=inputFileName)
print(head(data))
glon <- as.numeric(data$l)
glat <- as.numeric(data$b)
w <- as.numeric(data$parallax)
wsd <- as.numeric(data$parallax_error)
print(w)
for (i in 1:length(w)) {
  print(w[[i]])
  if(!is.na(w[[i]])) {
    rlen <- NA
    rlo <- 0
    rhi <- 1e5
    rplotlo <- NA
    rplothi <- NA
    res <- source("distest_single.R")
    print(res)
  }
}

# Input data
# Specify either l,b or rlen. Set other to NA. rlen takes precedence.
#w    <- nums[1] # parallax in mas (corrected for any zeropoint offset; +0.029mas in the catalogue)
#wsd  <- nums[2] # parallax uncertainty in mas
#glon <- nums[3] # Galactic longitude in degrees (0 to 360)
#glat <- nums[4] # Galactic latitude (-90 to +90)
#rlen <- nums[5] # length scale in pc
# Plotting parameters in pc
# rlo,rhi are range for computing normalization of posterior
# rplotlo, rplothi are plotting range (computed automatically if set to NA)
#rlo <- nums[6]
#rhi <- nums[7]
#rplotlo <- nums[8]
#rplothi <- nums[9]

# cat will write the result to the stdout stream
#res <- source("distest_single.R")
#print(res)
