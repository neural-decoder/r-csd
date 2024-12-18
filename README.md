




# r-csd


scripts for csd reconstruction in mne-python


Stages of CSD reconstruction:


1. make_bem

2. make_head (you need MRI scans or you can use fsaverage model)
   1.2  bem model
   1.3  source model

3. make_source

4. make_forward (you need info file - information about montage - position of electrodes)
   4.1  read / construct INFO
   4.2  make forward solution 

5. make_inverse (calcuate and apply inverse operator)



everything in a script r_csd_pipeline


data organization
------------------------------------
we will follow BIDS standards


generate_head >> bem + src (in files) 

generate_forward >> info + forward (in files)

generate_inverse >> inverse_operator + stc (in files)


visualize - class of functions for vizualization



