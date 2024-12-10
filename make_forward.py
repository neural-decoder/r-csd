




import os
import mne


def make_forward(subjects_dir, subject, measurement, overwrite=False):


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

    fwd = mne.make_forward_solution(info, trans=trans, src=src, bem=bem)

    fwd.save(forward_path, overwrite=overwrite)