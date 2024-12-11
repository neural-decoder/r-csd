



import os
import mne


def make_head(subjects_dir, subject, head_parameters, source_parameters, overwrite=False, n_jobs=None):

    """
    Generates the necessary BEM (Boundary Element Method) model, surfaces, and source space files
    for a given subject. Ensures proper setup of the directory structure and writes the results to
    appropriate files.

    This function uses the subjects directory and subject ID to create and store BEM surfaces, BEM
    solutions, and source spaces essential for EEG/MEG data analysis pipelines.

    :param subjects_dir: Path to the FreeSurfer subjects directory containing anatomical data.
                         The directory must exist and contain the subject's folder.
    :type subjects_dir: str
    :param subject: Identifier for the subject. This should correspond to the folder name in
                    the subjects directory.
    :type subject: str
    :param head_parameters: Dictionary containing parameters for building the BEM model.
                            Keys include:
                            - "ico": Icosahedron subdivision level for the surface mesh.
                            - "conductivity": Conductivity values for the tissue layers.
    :type head_parameters: dict
    :param source_parameters: Dictionary containing parameters for setting up the source space.
                              Key:
                              - "source spacing": Defines the source spacing
    :type source_parameters: dict
    :param overwrite: Whether to overwrite existing files in the subject directory. Defaults to False.
    :type overwrite: bool, optional

    :param n_jobs: Number of parallel jobs to use for computations. If None, defaults to the number
                   of CPUs in the machine.
    :type n_jobs: int, optional

    :return: None
    """


    # Ensure the subjects_dir and subject are set correctly

    if not os.path.isdir(subjects_dir):
        raise ValueError(f'{subjects_dir} does not exist or is not a directory.')


    bem_dir_path = os.path.join(subjects_dir, subject, "bem")
    os.makedirs(bem_dir_path, exist_ok=True)

    bem_surfaces_path = os.path.join(bem_dir_path, f"{subject}-inner_skull-bem.fif")
    bem_model_path = os.path.join(bem_dir_path, f"{subject}-bem-sol.fif")
    src_path = os.path.join(bem_dir_path, f"{subject}-src.fif")

    # Create the BEM surfaces

    ico = head_parameters["ico"]
    conductivity = head_parameters["conductivity"]

    bem_surfaces = mne.make_bem_model(subject=subject, subjects_dir=subjects_dir, ico=ico, conductivity=conductivity)

    bem_surfaces_path = os.path.join(bem_surfaces_path, f'{subject}-inner_skull-bem.fif')

    mne.write_bem_surfaces(bem_surfaces_path, bem_surfaces, overwrite=overwrite)


    # Create the BEM model

    bem_model = mne.make_bem_solution(bem_surfaces)

    mne.write_bem_solution(bem_model_path, bem_model, overwrite=overwrite)


    # Create the source space

    source_spacing = source_parameters['source_spacing']

    src = mne.setup_source_space(subject=subject, subjects_dir=subjects_dir, spacing=source_spacing, add_dist=False,
                                 n_jobs=n_jobs)

    mne.write_source_spaces(src_path, src, overwrite=overwrite)
