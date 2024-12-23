





import mne


subjects_dir = '/media/white/EXT_4T1/DATA/LAB/resting'
subject = 'sub-K2C68132'


mne.gui.coregistration(subjects_dir=subjects_dir, subject=subject)