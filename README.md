




# r-csd


scripts for csd reconstruction in mne-python


Stages of CSD reconstruction:

1. head model (you need MRI scans or you can use fsaverage model)
   1.1. bem surface
   1.2  bem model
   1.3  source model

2. make forward solution (you need info file - information about montage - position of electrodes)
   2.1  read / construct INFO
   2.2  make forward solution 

3. calcuate and apply inverse operator


we need 3 general functions: 

everythin in a script run_r_csd

generate_head >> bem + src (in files) 

generate_forward >> info + forward (in files)

generate_inverse >> inverse_operator + stc





