





import os
import mne



def make_inverse(subjects_dir, subject, measurement_parameters, overwrite=False, n_jobs=None):
    
    

    inverse_operator = mne.minimum_norm.make_inverse_operator(info=info_sim, forward=fwd, noise_cov=noise_cov,
                                                              fixed=fixed, depth=depth)

    # Read the averaged raw data

    measurement = measurement_parameters['measurement']
    measurement_group = measurement_parameters['measurement_group']

    raw_path = os.path.join(subjects_dir, subject, 'ave', measurement_group, measurement)
    info_path = os.path.join(subjects_dir, subject, measurement_group, 'info.fif')


    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Averaged raw data file not found: {raw_path}")

    raw = mne.io.read_raw_fif(raw_path, preload=True)
    info = mne.io.read_info(info_path)


    print(info)

    stc = mne.minimum_norm.apply_inverse_raw(raw=raw, inverse_operator=inverse_operator, lambda2=lambda2,
                                             method=inverse_method, pick_ori=None, n_jobs=n_jobs)
    
    # Save the stc file
    
    stc.save(os.path.join(subjects_dir, subject, 'stc_results', f"{measurement}-stc"), overwrite=overwrite)



