#!/usr/bin/python
import matplotlib
#matplotlib.rcParams['font.family'] = 'serif'
#matplotlib.rcParams['legend.fontsize']=12
from pylab import *
import numpy
from analysedata import *

fdirect="/Users/Suzie/Physics/KURRIFFAG/DATA/2015/2015_06_25/"

fname1 = "sakamoto_mon_23.csv"
fname2= "sakamoto_mon_38.csv"
bunchmonf="sakamoto_mon_ref.csv"

#get raw signals from file
tdat, data1=read_scope(fdirect, fname1)
tdat2, data2=read_scope(fdirect, fname2)

#this is a bunch monitor signal for reference/comparison
rtdat, rvdat=read_scope(fdirect, bunchmonf)

#choose index range over which to analyse data (the initial stuff is probably rubbish!)
starti = 300000
endi=300100
plot(rtdat[starti:endi], rvdat[starti:endi], 'r-')
plot(tdat[starti:endi], abs(numpy.array(data1[starti:endi])), 'b-')
plot(tdat2[starti:endi], abs(numpy.array(data2[starti:endi])), 'g-')
show()

filter=True
if filter==True:
	#parameters for filter
	cut_off_freq = 0.5e6
	dt = tdat[1] - tdat[0]
	RC = 1/(2*np.pi*cut_off_freq)

	#apply high pass filter
	filter_chf1 = highpass(data1,dt,RC)
	filter_chf2 = highpass(data2,dt,RC)
	#plot(tdat[starti:endi], filter_chf1[starti:endi], 'r-')
	#plot(tdat2[starti:endi], filter_chf2[starti:endi], 'b-')
	

	data1=filter_chf1
	data2=filter_chf2
#find peaks in the data
interval=90
Lpeakdat = find_peaks(tdat[starti:endi], data1[starti:endi], interval, 0)
Rpeakdat = find_peaks(tdat2[starti:endi], data2[starti:endi], interval, 0)

#plot(tdat[starti:endi], data1[starti:endi], 'b-')
plot(tdat[starti:endi], abs(numpy.array(data1[starti:endi])), 'r-')
plot(tdat2[starti:endi], abs(numpy.array(data2[starti:endi])), 'b-')
#plot(Lpeakdat[1], Lpeakdat[2], 'r.-')
#plot(Rpeakdat[1], Rpeakdat[2], 'b.-')
show()
#sys.exit()

#take sum and difference
sumdat=[]
diffdat=[]
tdata=[]

#find where peak indices correspond in the data (ie. L and R had same peak time, so beam actually went past at same time)
#then do sum/difference of those peaks
print len(Lpeakdat[0])
print len(Rpeakdat[0])

for pkindex in Lpeakdat[0]:
	if Lpeakdat[1][pkindex] in Rpeakdat[1]:
		print Lpeakdat[1][pkindex], Rpeakdat[1][pkindex]
		tdata.append(Lpeakdat[1][pkindex])
		sumdat.append(Lpeakdat[2][pkindex]+Rpeakdat[2][pkindex])
		diffdat.append(Lpeakdat[2][pkindex]-Rpeakdat[2][pkindex])

#normalise to find position
divdat=numpy.array(diffdat)/numpy.array(sumdat)
print len(sumdat), len(diffdat)
print len(divdat)
print Rpeakdat[1][:10]
print Lpeakdat[1][:10]
print tdat[:10]
print tdata[:10]
sys.exit()
#plot position vs time
plot(tdata, sumdat, 'c-')
plot(tdata, diffdat, 'm-')
show()

plot(tdata, divdat, 'k-')
show()

