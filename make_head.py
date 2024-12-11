



import os
import mne


def make_head(subjects_dir, subject, head_parameters, source_parameters, overwrite=False, n_jobs=None):

    # Ensure the subjects_dir and subject are set correctly

    if not os.path.isdir(subjects_dir):
        raise ValueError(f'{subjects_dir} does not exist or is not a directory.')


    # Create the BEM surfaces

    ico = head_parameters["ico"]
    conductivity = head_parameters["conductivity"]

    bem_surfaces = mne.make_bem_model(subject=subject, subjects_dir=subjects_dir, ico=ico, conductivity=conductivity)

    bem_surfaces_path = os.path.join(subjects_dir, subject, 'bem', f'{subject}-inner_skull-bem.fif')

    mne.write_bem_surfaces(bem_surfaces_path, bem_surfaces, overwrite=overwrite)


    # Create the BEM model

    bem_model = mne.make_bem_solution(bem_surfaces)

    bem_model_path = os.path.join(subjects_dir, subject, 'bem', f'{subject}-bem-sol.fif')

    mne.write_bem_solution(bem_model_path, bem_model, overwrite=overwrite)


    # Create the source space

    source_spacing = source_parameters['oct6']

    src = mne.setup_source_space(subject=subject, subjects_dir=subjects_dir, spacing=source_spacing, add_dist=False,
                                 n_jobs=n_jobs)

    src_path = os.path.join(subjects_dir, subject, "bem", f"{subject}-src.fif")


    mne.write_source_spaces(src_path, src, overwrite=overwrite)
