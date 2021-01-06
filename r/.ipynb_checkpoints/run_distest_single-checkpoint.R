# Input data
# Specify either l,b or rlen. Set other to NA. rlen takes precedence.
w    <- 1 # parallax in mas (corrected for any zeropoint offset; +0.029mas in the catalogue)
wsd  <- abs(0.2*w) # parallax uncertainty in mas
glon <- 340 # Galactic longitude in degrees (0 to 360)
glat <-  45 # Galactic latitude (-90 to +90)
rlen <-  NA # length scale in pc
# Plotting parameters in pc
# rlo,rhi are range for computing normalization of posterior
# rplotlo, rplothi are plotting range (computed automatically if set to NA)
rlo <- 0
rhi <- 1e5
rplotlo <- NA
rplothi <- NA

source("Gaia-DR2-distances/distest_single.R")