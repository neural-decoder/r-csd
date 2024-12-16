


import os
import mne



def make_bem(subjects_dir, subject, bem_parameters):

    """
    Generate a BEM (Boundary Element Model) for a subject using watershed algorithm.

    This function leverages the MNE library to create a BEM structure using the
    watershed algorithm. It requires specific parameters provided in the
    `bem_parameters` dictionary to configure the BEM generation process. The optional
    `overwrite` parameter dictates whether existing BEM data should be replaced.

    :param subjects_dir: Path to the root directory where all MRI data is stored.
    :param subject: Name of the subject for whom the BEM is to be created.
    :param bem_parameters: Dictionary containing the necessary parameters for
        BEM generation, including 'preflood', 'brain_mask', 'volume', 'gcaatlas',
        'atlas', and 'T1'.
    :param overwrite: If True, overwrite any pre-existing BEM data. Defaults to False.
    :return: None
    """

    preflood = bem_parameters['preflood']
    brain_mask = bem_parameters['brain_mask']
    volume = bem_parameters['volume']
    gcaatlas = bem_parameters['gcaatlas']
    atlas = bem_parameters['atlas']
    T1 = bem_parameters['T1']
    show = bem_parameters['show']
    overwrite = bem_parameters['overwrite']


    mne.bem.make_watershed_bem(subject, subjects_dir=subjects_dir, overwrite=overwrite, volume=volume,
                               atlas=atlas, gcaatlas=gcaatlas, show=show, T1=T1, preflood=preflood,
                               brainmask=brain_mask, verbose=None)



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

    bem_dir_path = os.path.join(subjects_dir, subject, "bem")
    os.makedirs(bem_dir_path, exist_ok=True)

    bem_surfaces_path = os.path.join(bem_dir_path, f"{subject}-inner_skull-bem.fif")
    bem_model_path = os.path.join(bem_dir_path, f"{subject}-bem-sol.fif")

    # Create the BEM surfaces

    ico = head_parameters["ico"]
    conductivity = head_parameters["conductivity"]

    bem_surfaces = mne.make_bem_model(subject=subject, subjects_dir=subjects_dir, ico=ico,
                                      conductivity=conductivity)


    mne.write_bem_surfaces(bem_surfaces_path, bem_surfaces, overwrite=overwrite)

    # Create the BEM model

    bem_model = mne.make_bem_solution(bem_surfaces)

    mne.write_bem_solution(bem_model_path, bem_model, overwrite=overwrite)



def make_source(subjects_dir, subject, source_parameters, n_jobs=None):

    src_path = os.path.join(bem_dir_path, f"{subject}-src.fif")

    source_spacing = source_parameters['source_spacing']

    src = mne.setup_source_space(subject=subject, subjects_dir=subjects_dir, spacing=source_spacing, add_dist=False,
                                 n_jobs=n_jobs)

    mne.write_source_spaces(src_path, src, overwrite=overwrite)




def make_forward(subjects_dir, subject, measurement, overwrite=False, n_jobs=None):

    """
    Create and save a forward solution for MEG/EEG source analysis.

    The function constructs a forward solution using a provided subject’s anatomical,
    surface, and measurement data. It reads necessary BEM, source space, info, and
    transformation files, computes the forward solution, and saves it to the specified path.

    :param subjects_dir: Path to the subjects directory that contains all subject data.
    :type subjects_dir: str

    :param subject: Name of the subject whose data will be processed.
    :type subject: str

    :param measurement: Measurement folder that contains the required info data.
    :type measurement: str

    :param overwrite: Whether to overwrite an existing forward solution file. Default is False.
    :type overwrite: bool

    :param n_jobs: Number of parallel jobs to use for computation. Default is None.
    :type n_jobs: int, optional

    :return: None
    :raises CustomError: Raised at various points if required files or directories are not found.
    """

    bem_path = str(os.path.join(subjects_dir, subject, 'bem'))

    if not os.path.exists(bem_path):
        raise CustomError('There is no bem')
    else:
        bem = mne.read_bem_solution(os.path.join(bem_path, 'bem_model', 'bem_model.fif'))

    src_path = os.path.join(subjects_dir, subject, 'src')

    if not os.path.exists(src_path):
        raise CustomError('There is no source')
    else:
        src = mne.read_source_spaces(os.path.join(subjects_dir, subject, 'src', 'src.fif'))

    info_path = os.path.join(subjects_dir, subject, measurement_group, 'info', 'info.fif')

    if not os.path.exists(info_path):
        raise CustomError('There is no info')
    else:
        info = mne.read_info('info.fif')

    trans_path = os.path.join(subjects_dir, subject, 'trans', 'trans.fif')

    if not os.path.exists(trans_path):
        raise CustomError('There is no info')
    else:
        trans = mne.read_info('trans_path')

    forward_path = os.path.join(subjects_dir, subject, measurement_group, 'forward', 'forward.fif')

    fwd = mne.make_forward_solution(info=info, trans=trans, src=src, bem=bem, n_jobs=n_jobs)

    fwd.save(forward_path, overwrite=overwrite)



def make_inverse(subjects_dir, subject, measurement_parameters, inverse_parameters, overwrite=False, n_jobs=None):

    """
    Generate and apply the inverse operator to M/EEG data for a given subject.

    This function generates an inverse operator using provided MNE environment data, and
    applies it to the averaged raw M/EEG data of a given subject. The resulting source-level
    data (stc) is subsequently saved into a specified directory. The function requires proper
    measurement configurations and may leverage parallel processing via n_jobs.

    :param subjects_dir: Path to the directory containing subject subdirectories.
    :type subjects_dir: str

    :param subject: The subject identifier corresponding to the directory in `subjects_dir`.
    :type subject: str

    :param measurement_parameters: A dictionary containing keys such as 'measurement'
        and 'measurement_group', which define the measurement type and its associated
        group, respectively.
    :type measurement_parameters: dict

    :param overwrite: Flag indicating whether to overwrite existing files when saving
        the resulting source-level data.
    :type overwrite: bool, optional

    :param n_jobs: Number of parallel jobs to use in processing. If None, all available
        CPUs are used.
    :type n_jobs: int, optional

    :return: None
    """

    fixed = inverse_parameters['fixed']
    depth = inverse_parameters['depth']
    lambda2 = inverse_parameters['lambda2']
    pick_ori = inverse_parameters['pick_ori']


    # Read the averaged raw data

    measurement = measurement_parameters['measurement']
    measurement_group = measurement_parameters['measurement_group']

    raw_path = os.path.join(subjects_dir, subject, measurement_group, measurement)
    info_path = os.path.join(subjects_dir, subject, measurement_group, 'info.fif')

    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw data file not found: {raw_path}")

    raw = mne.io.read_raw_fif(raw_path, preload=True)
    info = mne.io.read_info(info_path)

    print(info)


    # Read the forward solution from file
    forward_path = os.path.join(subjects_dir, subject, measurement_group, 'forward', 'forward.fif')

    if not os.path.exists(forward_path):
        raise FileNotFoundError(f"Forward solution file not found: {forward_path}")

    fwd = mne.read_forward_solution(forward_path)


    # Read the noise covariance matrix from file

    noise_cov_path = os.path.join(subjects_dir, subject, measurement_group, 'cov', 'noise-cov.fif')

    if not os.path.exists(noise_cov_path):
        raise FileNotFoundError(f"Noise covariance file not found: {noise_cov_path}")

    noise_cov = mne.read_cov(noise_cov_path)


    inverse_operator = mne.minimum_norm.make_inverse_operator(info=info, forward=fwd, noise_cov=noise_cov,
                                                              fixed=fixed, depth=depth)

    stc = mne.minimum_norm.apply_inverse_raw(raw=raw, inverse_operator=inverse_operator, lambda2=lambda2,
                                             method=inverse_method, pick_ori=pick_ori, n_jobs=n_jobs)


    # Save the inverse operator to a file
    inverse_operator_path = os.path.join(subjects_dir, subject, 'inverse_operators',
                                         f"{measurement}-inverse-operator.fif")

    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(inverse_operator_path), exist_ok=True)

    mne.minimum_norm.write_inverse_operator(inverse_operator_path, inverse_operator, overwrite=overwrite)


    # Save the stc file

    stc.save(os.path.join(subjects_dir, subject, 'stc_results', f"{measurement}-stc"), overwrite=overwrite)