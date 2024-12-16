







import r_csd
import joblib

"""
GENERAL PARAMETERS

njobs : None
The number of jobs to run in parallel.
If -1, it is set to the number of CPU cores. 
Requires the joblib package.
None (default) is a marker for ‘unset’ that will be interpreted as n_jobs=1 (sequential execution) 
unless the call is performed under a joblib.parallel_config context manager that sets another value for n_jobs.
# """


subjects_dir = '/media/white/EXT_4T/DATA/LAB/resting'
subject = 'sub-B9T21173'

n_jobs = None




"""
STAGE 1 : MAKE BEM

preflood : None
The watershed algorithm is used during the skull stripping step to find a boundary between the brain and skull. 
The mri_watershed program uses a default preflooding height of 25 percent.
If we want the algorithm to be more conservative (i.e. if part of the brain has been removed), 
you will want to make that number larger than 25.
If you want the algorithm to be more aggressive (i.e. part of the skull has been left behind), 
you will want to make the height less than 25. 
There aren't any hard and fast rules about how to select your height value.


"""

bem_parameters = {}
bem_parameters['preflood'] = None
bem_parameters['brain_mask'] = "ws.mgz"
bem_parameters['volume'] = 'T1'
bem_parameters['gcaatlas'] = False
bem_parameters['atlas'] = False
bem_parameters['T1'] = None
bem_parameters['show'] = True
bem_parameters['overwrite'] = True


r_csd.make_bem(subjects_dir, subject, bem_parameters)



# """
# STAGE 2 : MAKE HEAD MODEL
#
# """
#
# r_csd.make_head(subjects_dir, subject, head_parameters, source_parameters, n_jobs=n_jobs)
#
#
# """
# STAGE 3 : MAKE SOURCE SPACE
#
# """
#
#
# r_csd.make_source(subjects_dir, subject, source_parameters, n_jobs=n_jobs)
#
#
#
# """
# STAGE 4 : MAKE FORWARD SOLUTION
#
# """
#
#
# """
# STAGE 5 : MAKE INVERSE SOLUTION
# """







