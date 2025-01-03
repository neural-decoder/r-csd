







import r_csd
import joblib

import mne
import pyvista


"""
GENERAL PARAMETERS

njobs : None
The number of jobs to run in parallel.
If -1, it is set to the number of CPU cores. 
Requires the joblib package.
None (default) is a marker for ‘unset’ that will be interpreted as n_jobs=1 (sequential execution) 
unless the call is performed under a joblib.parallel_config context manager that sets another value for n_jobs.
# """


subjects_dir = '/media/white/EXT_4T1/DATA/LAB/resting'
subject = 'sub-K2C68132'

n_jobs = None


eeg_recording = 'task-rest_eeg'


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
bem_parameters['overwrite'] = False


r_csd.make_bem(subjects_dir, subject, bem_parameters)



"""
STAGE 2 : MAKE HEAD MODEL

ico : None / int
The surface mesh is subdivided into icohedrons.
The surface ico downsampling to use, e.g. 5=20484, 4=5120, 3=1280. 
If None, no subsampling is applied.

conductivity : float / array of floats
default : [0.3, 0.006, 0.3]
The conductivity values for the tissue layers.
The conductivities to use for each shell.

3 Layers model
Scalp Layer:
The outermost layer, representing the scalp,
typically has a conductivity value around 0.3 Sm
Skull Layer:
The middle layer, which represents the skull, 
has a significantly lower conductivity.
This low conductivity is essential as it models 
the attenuating effect of the skull on electrical signals.
Brain Layer:
The innermost layer corresponds to the brain tissue, with a higher conductivity value around 0.3 Sm
0.33S m, similar to that of the scalp.

Should be a single element for a one-layer model, or three elements for a three-layer model.
Defaults to [0.3, 0.006, 0.3]. The MNE-C default for a single-layer model is [0.3]


"""

head_parameters = {}
head_parameters['ico'] = 4
head_parameters['conductivity'] = [0.3, 0.006, 0.3]
head_parameters['overwrite'] = False


r_csd.make_head(subjects_dir, subject, head_parameters, n_jobs=n_jobs)


"""
STAGE 3 : MAKE SOURCE SPACE

spacing : str
The spacing to use. Can be 
'ico#' for a recursively subdivided icosahedron,
'oct#' for a recursively subdivided octahedron, 
'all' for all points, or an integer to use approximate distance-based spacing (in mm).


"""

source_parameters = {}
source_parameters['source_spacing'] = 'oct6'
source_parameters['overwrite'] = False


r_csd.make_source(subjects_dir, subject, source_parameters, n_jobs=n_jobs)



"""
STAGE 4 : MAKE INFO

"""

montage_fname = '/media/white/EXT_4T1/DATA/LAB/resting/sub-K2C68132/_eeg/montage/coords/sub-K2C68132_captrak.bvct'

eeg_fname = f'{subject}_{eeg_recording}'

r_csd.make_info(subjects_dir, subject, eeg_fname, montage_fname, overwrite=True)



"""
STAGE 4 : MAKE FORWARD SOLUTION

"""

r_csd.make_forward(subjects_dir, subject, overwrite=False, n_jobs=n_jobs)











