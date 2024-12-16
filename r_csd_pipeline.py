







import r_csd


# GENERAL PARAMETERS

subjects_dir = '/media/white/EXT_4T/DATA/LAB/resting'
subject = 'sub-B9T21173'




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

