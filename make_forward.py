




import os
import mne


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


    info_path = os.path.join(subjects_dir, subject, measurement, 'info', 'info.fif')

    if not os.path.exists(info_path):
        raise CustomError('There is no info')
    else:
        info = mne.read_info('info.fif')


    trans_path = os.path.join(subjects_dir, subject, 'trans', 'trans.fif')

    if not os.path.exists(trans_path):
        raise CustomError('There is no info')
    else:
        trans = mne.read_info('trans_path')


    forward_path = os.path.join(subjects_dir, subject, measurement, 'forward', 'forward.fif')

    fwd = mne.make_forward_solution(info=info, trans=trans, src=src, bem=bem, n_jobs=n_jobs)

    fwd.save(forward_path, overwrite=overwrite)