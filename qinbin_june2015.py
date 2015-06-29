from __future__ import division
import numpy as np
import sys
import analysedata as adata
import matplotlib
from pylab import *

#Find last signal signal recorded during Qin Bin scan. 
#Set 'dirname' to directory containing files to be analysed.
#Set 'indices_select' to choose files by index (indices_select=[] selects all files)
#'channel_id' can be used to select particular channels 
#
#'cut_off_freq' determines the cut off point in the high pass filter
#Set 'method' to 'fixed' or 'noise' to determine the signal threshold in two ways. In the 'fixed' case
#         a fixed voltage threshold is used (threshold_volts in signal_loss_time) while in the 'noise' case
#         the signal is assumed to be some multiple of the rms of the noise calculated at the end of the data 

#dirname ="../data/SortByDate/2014/3/24/dmag/"	 
#dirname ="../data/SortByDate/2014/3/25/D0_1012_D1_140_F7/" 
#dirname = "../data/SortByDate/2014/3/27/Corr_700A/"
dirname = "/Users/Suzie/Physics/KURRIFFAG/DATA/2015/2015_06_24/COD_accel/900A/"
#dirname = "../data/SortByDate/2014/3/31/QinBin/F7/"

#
indices_select = [] #select particular indices from each channel, empty list means process all files
#channel_id = ["CH1","CH2","CH3"] #string to identify each channel
#channel_id = ["F1","F5","F7"] #identifier for channels to be analysed
channel_id = ["F12"]

#select channel files
ch_files_sel = adata.select_filenames(dirname, indices_select, channel_id)

print "ch_files_sel ",ch_files_sel

#set parameters for high pass filter
cut_off_freq = 0.5e6 #0.5 MHz
nstd = 10 #set threshold above noise to determine final loss point

method = 'noise' #choose "fixed" or "noise"

#calculate loss time
trigger_offset = 0
#trigger_offset = -0.00203983999
#trigger_offset=-0.00203983999+0.000919839994
loss_time_all = []
for chf in ch_files_sel:	
	loss_time_ch  =[]
	if chf != []:
		for chf1 in chf:
			#read scope data
			tdat_chf, data_chf = adata.read_scope(dirname, chf1)
			loss_time = adata.signal_loss_time(tdat_chf, data_chf, method)
			loss_time_ch.append(loss_time)
			#plot(tdat_chf, data_chf, 'r-')
			#axvline(loss_time[0],color='k',ls='dashed')
			#show()
	loss_time_all.append(loss_time_ch)

print "loss time all ",loss_time_all, "len ",len(loss_time_all)
	

#-------------------------Rest specific to file format used at particular time-----------------
#31/3/14 - map each index to probe position			
F01_pos = np.arange(340, 840, 20)
F02_pos = np.arange(360,920, 20)
F03_pos = np.arange(320, 800, 20)
F05_pos = np.arange(360, 920, 20)
F12_pos = np.arange(320, 800, 20)
#F5_pos = [890, 870, 850, 830, 800, 750, 700, 650, 600, 550, 500, 450, 425, 400, 380, 360, 340]
#F1_pos = [870, 850, 800, 750, 700, 650, 600, 550, 500, 450, 425, 400, 380, 360, 340]
#F7_pos = [870, 850, 800, 750, 700, 650, 600, 550, 500, 450, 425, 400, 380, 360, 340, 320, 300]


loss_time_flatten = np.array(loss_time_all[0])

if "F01" in channel_id:
	fout = 'QinBin_F01.txt'
	fpos = list(F01_pos)
elif "F02" in channel_id:
	fout = 'QinBin_F02.txt'
	fpos = list(F02_pos)
elif "F03" in channel_id:
	fout = 'QinBin_F03.txt'
	fpos = list(F03_pos)
elif "F05" in channel_id:
	fout = 'QinBin_F05.txt'
	fpos = list(F05_pos)
elif "F12" in channel_id:
	fout = 'QinBin_F12.txt'
	fpos = list(F12_pos)
	
ff = open(fout,"w")
print >>ff, "probe position (mm) loss time (us)"
for pos, losst in zip(fpos, loss_time_flatten): 
	print >>ff, pos, 1e6*(losst[0]-trigger_offset)
ff.close()
