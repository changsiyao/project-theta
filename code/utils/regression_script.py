import nibabel as nib
import numpy as np
from behavtask_tr import events2neural_extend, merge_cond
from regression_functions import hrf, getGainLoss, calcBeta, calcMRSS, deleteOutliers
import os
from scipy.stats import gamma
import math
import numpy.linalg as npl
import json

n_vols=240
TR=2
tr_times = np.arange(0, 30, TR)
hrf_at_trs = hrf(tr_times)

os.chdir("../../data")

dvars_out = json.load(open("dvarsOutliers.txt"))
fd_out = json.load(open("fdOutliers.txt"))

for i in range(1,10):
    # first three dimension for data shape is 64, 64, 34.
    # create array to store the combined dataset of three runs
    data_full = np.empty([64, 64, 34, 0])
    gain_full = np.empty([0,])
    loss_full = np.empty([0,])
    for j in range(1,4):
        direct='ds005/sub00'+`i`+'/BOLD/task001_run00'+`j`+'/'
        boldname = direct+'bold.nii.gz'
        img=nib.load(boldname)
        data=img.get_data()
        run = j
        behav_cond = 'ds005/sub00'+`i`+'/behav/task001_run00'+`j`+'/behavdata.txt'
        task_cond1 = 'ds005/sub00'+`i`+'/model/model001/onsets/task001_run00'+`j`+'/cond001.txt'
        task_cond2 = 'ds005/sub00'+`i`+'/model/model001/onsets/task001_run00'+`j`+'/cond002.txt'
        task_cond3 = 'ds005/sub00'+`i`+'/model/model001/onsets/task001_run00'+`j`+'/cond003.txt'
        task_cond4 = 'ds005/sub00'+`i`+'/model/model001/onsets/task001_run00'+`j`+'/cond004.txt'
        parameters = merge_cond(behav_cond, task_cond1, task_cond2, task_cond3, task_cond4)
        neural_prediction = events2neural_extend(parameters,TR, n_vols)
        gain, loss = getGainLoss(TR, n_vols, hrf_at_trs, neural_prediction)
        data, gain, loss = deleteOutliers(data, gain, loss, i, run, dvars_out, fd_out)
        data_full = np.concatenate((data_full,data),axis=3)
        gain_full = np.concatenate((gain_full,gain),axis=0)
        loss_full = np.concatenate((loss_full,loss),axis=0)
    mea=calcMRSS(data_full, gain_full, loss_full)
    X, Y, beta=calcBeta(data_full, gain_full, loss_full)
    write='ds005/sub00'+`i`+'/model/model001/onsets/sub'+`i`+'_beta.txt'
    np.savetxt(write, beta)

for i in range(10,17):
    # first three dimension for data shape is 64, 64, 34.
    # create array to store the combined dataset of three runs
    data_full = np.empty([64, 64, 34, 0])
    gain_full = np.empty([0,])
    loss_full = np.empty([0,])
    for j in range(1,4):
        direct='ds005/sub0'+`i`+'/BOLD/task001_run00'+`j`+'/'
        boldname = direct+'bold.nii.gz'
        img=nib.load(boldname)
        data=img.get_data()
        run = j
        behav_cond = 'ds005/sub0'+`i`+'/behav/task001_run00'+`j`+'/behavdata.txt'
        task_cond1 = 'ds005/sub0'+`i`+'/model/model001/onsets/task001_run00'+`j`+'/cond001.txt'
        task_cond2 = 'ds005/sub0'+`i`+'/model/model001/onsets/task001_run00'+`j`+'/cond002.txt'
        task_cond3 = 'ds005/sub0'+`i`+'/model/model001/onsets/task001_run00'+`j`+'/cond003.txt'
        task_cond4 = 'ds005/sub0'+`i`+'/model/model001/onsets/task001_run00'+`j`+'/cond004.txt'
        parameters = merge_cond(behav_cond, task_cond1, task_cond2, task_cond3, task_cond4)
        neural_prediction = events2neural_extend(parameters,TR, n_vols)
        gain, loss = getGainLoss(TR, n_vols, hrt_at_trs, neural_prediction)
        data, gain, loss = deleteOutliers(data, gain, loss, i, j, dvars_out, fd_out)
        data_full = np.concatenate((data_full,data),axis=3)
        gain_full = np.concatenate((gain_full,gain),axis=0)
        loss_full = np.concatenate((loss_full,loss),axis=0)
    mea=calcMRSS(data_full, gain_full, loss_full)
    X, Y, beta=calcBeta(data_full, gain_full, loss_full)
    write='ds005/sub0'+`i`+'/model/model001/onsets/sub'+`i`+'_beta.txt'
    np.savetxt(write, beta)
