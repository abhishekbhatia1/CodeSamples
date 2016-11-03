# -*- coding: utf-8 -*-
"""
Created on Tue Nov 24 00:30:33 2015

@author: apark
"""


from os.path import join
import numpy as np
import pylab as pl
from utils import datasets, masking, signal
import nibabel


adhd_mask = join('utils', 'adhd_mask.nii.gz')
dataset = datasets.fetch_adhd(n_subjects=1)
X = masking.apply_mask(dataset.func[0], adhd_mask)
X = signal.clean(X, standardize=True, detrend=False)
X_smoothed = masking.apply_mask(dataset.func[0], adhd_mask,
        smoothing_fwhm=6.)
X_smoothed = signal.clean(X_smoothed, standardize=True, detrend=False)
mask = nibabel.load(adhd_mask).get_data().astype(np.bool)