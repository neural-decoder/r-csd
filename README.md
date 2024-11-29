




# r-csd


scripts for csd reconstruction in mne-python


Stages of CSD reconstruction:

1. make_head (you need MRI scans or you can use fsaverage model)
   1.1. bem surface
   1.2  bem model
   1.3  source model

2. make_info
   1.1. read measurement files and create info

4. make_raw


5. make_forward (you need info file - information about montage - position of electrodes)
   3.1  read / construct INFO
   3.2  make forward solution 

6. calcuate and apply inverse operator


we need 3 general functions: 

everything in a script r_csd_pipeline


data orgazization
------------------------------------
we will follow BIDS standards


generate_head >> bem + src (in files) 

generate_forward >> info + forward (in files)

generate_inverse >> inverse_operator + stc (in files)


visualize - class of functions for vizualization



