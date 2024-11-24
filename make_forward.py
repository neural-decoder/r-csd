




import os

import mne
import matplotlib.pyplot as plt


''' PATHS
subjects
34375
mrtlne88_0101
'''

subjects_dir = '/home/white/DATA/LAB/MRI/'
subject = '106'


''' CREATE BEM SURFACE
if volume='T1' in mne.bem.make_watershed_bem then T1.mgz from subject/mri folder is taken to make bem surfaces
'''

if not os.path.exists('/home/white/DATA/LAB/MRI/' + subject + '/bem'):

    mne.bem.make_watershed_bem(subject, subjects_dir=subjects_dir, overwrite=False,
                               atlas=False, gcaatlas=False, show=False,
                               copy=True, T1=None, preflood=2, brainmask='ws.mgz', verbose=None)



plot_bem_kwargs = dict(subject=subject, subjects_dir=subjects_dir,
                       brain_surfaces='white', orientation='coronal',
                       slices=[50, 100, 150, 200])
#
mne.viz.plot_bem(**plot_bem_kwargs)
#
#
''' CREATE BEM MODEL
'''


conductivity = (0.3, 0.006, 0.3)

model = mne.make_bem_model(subject=subject, subjects_dir=subjects_dir, ico=4, conductivity=conductivity)

bem = mne.make_bem_solution(model)



if not os.path.exists(subjects_dir + subject + '/bem/model/'):

    os.makedirs(subjects_dir + subject + '/bem/model/')


mne.write_bem_solution('/home/white/DATA/LAB/MRI/' + subject + '/bem/model/bem_model.fif',
                       bem, overwrite=True, verbose=None)


print(model)

print(bem)

'''  CREATE SOURCE SPACE
'''


spacing = 'oct6'

src = mne.setup_source_space(subject, subjects_dir=subjects_dir, spacing=spacing, add_dist='patch')

mne.viz.plot_bem(src=src, **plot_bem_kwargs)

print(src)

plt.show()

if not os.path.exists(subjects_dir + subject + '/-src.fif'):

    os.makedirs(subjects_dir + subject + '/_src/')


src.save(subjects_dir + subject + '/_src/-src.fif', overwrite=True, verbose=None)