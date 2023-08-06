# stnpy
Python Library for Search Trajectory Networks

### Purpose

For the purposes of my Honours projecrt I have been using the following R library: [STNs](https://github.com/gabro8a/STNs)

However, it's not suited to my needs. For one, it's in R, which is horrible. Two, it assumes much that is not related to my work. For this reason I wish to port the R library to Python, which will allow me to both call it natively during my processing pipeline as well as cater it specifically to my needs.

#### Port Details

My port follows the same file conventions as the original, however, my port assumes there is only one run per file. I have also only ported the `create.py` and `metrics.py` files from the original for my purpose.