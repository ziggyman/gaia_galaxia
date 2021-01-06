# Fetch command line arguments
myArgs <- commandArgs(trailingOnly = TRUE)

# Convert to numerics
nums = as.numeric(myArgs)

# Input data
# Specify either l,b or rlen. Set other to NA. rlen takes precedence.
w    <- nums[1] # parallax in mas (corrected for any zeropoint offset; +0.029mas in the catalogue)
wsd  <- nums[2] # parallax uncertainty in mas
glon <- nums[3] # Galactic longitude in degrees (0 to 360)
glat <- nums[4] # Galactic latitude (-90 to +90)
rlen <- nums[5] # length scale in pc
# Plotting parameters in pc
# rlo,rhi are range for computing normalization of posterior
# rplotlo, rplothi are plotting range (computed automatically if set to NA)
rlo <- nums[6]
rhi <- nums[7]
rplotlo <- nums[8]
rplothi <- nums[9]

# cat will write the result to the stdout stream
res <- source("distest_single.R")
print(res)
