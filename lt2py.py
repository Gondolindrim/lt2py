import numpy as np

# MatplotLib and PyPlot for plotting
import matplotlib.pyplot as pyplot
import matplotlib as mplot
from matplotlib import rc

import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()

# File prompt to ask for the file path
file_path = filedialog.askopenfilename()

with open(file_path, 'r', encoding='ISO-8859-1') as f:

	line = f.readline().split('\t')

	# For some reason the last element of 'line' comes with a '\n' last element. Removing this '\n' character:
	line[-1] = line[-1][:-1]

	# This first line contains the names of the signals. signal_names stores their values.
	signal_names = line
	
	# series_data storess the raw data, including time values
	series_data = []
	for line in f:
		line_temp = [float(x) for x in line.split('\t')]
		series_data.append(line_temp)

	series_data = np.array(series_data)	

# point_number stores the number of time series datapoints
# curve_number stores the number of time data curves in the data set
point_number = len(series_data)
curve_number = len(series_data[0]) - 1

time_values = [x[0] for x in series_data]

fig1 = pyplot.figure();
ax1 = fig1.add_axes([0.1,0.1,0.8,0.8]);

for k in range(curve_number):
	ax1.plot(time_values, [x[k+1] for x in series_data],label=signal_names[k+1],linewidth=1)

ax1.legend(loc='best')

ax1.grid(which='major')
ax1.grid(which='minor',dashes=(5,2))
ax1.set_xlim([min(time_values),max(time_values)])

pyplot.show()
