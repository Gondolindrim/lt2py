import numpy as np

# MatplotLib and PyPlot for plotting
import matplotlib.pyplot as pyplot
import matplotlib as mplot
from matplotlib import rc

import easygui as eg

import matplotlib.cm as cm

# Adds the option to specify the target file in the form of a argument, like in
# python lt2py --plotfile <file destination>
import argparse
parser = argparse.ArgumentParser(
	prog = 'LT2PY API',
	description = 'A Python API for LTSpiceXVII plots.',
	)

parser.add_argument(	'--plotfile',
			type = str,
			metavar = 'PLOTFILE',
			default = '',
			help='Target LTSpice-exported *.txt file containing plot data')

args = parser.parse_args()
file_path = args.plotfile
# If the plotfile argument was null (no --plotfile argument was passed) execute a GUI to select it
if file_path == '':
	# File prompt to ask for the file path
	file_path = eg.fileopenbox(msg='Select simulation data *.txt file', title='LT2PY file selection', default='', filetypes=["*.txt"], multiple=False)

with open(file_path, 'r', encoding='ISO-8859-1') as f:

	# Reading the first time which contains the curve names
	line = f.readline().split('\t')

	# For some reason the last element of 'line' comes with a '\n' last element. Removing this '\n' character:
	line[-1] = line[-1][:-1]

	# Storing the names of the curves in the signal_names variable
	signal_names = line

	# If the second line contains the "Step information" string, this means that the file contains a stepped dataset.
	line = f.readline()
	if 'Step Information' in line:
		stepped_dataset = True
		f.seek(0)
		f.readline()
		# step_data storess the raw data, including time values, as a list of two-dimensional series_data. In the case of a stepped dataset, it is comprised of a three-dimensional array where the first dimension is the step run, the second dimension is the number of the datasample, and the third index is the step run.
		temp_series_data = []
		step_data = []
		step_info = []

		for line in f:
			if 'Step Information' in line:
				# if the line contains "Step Information" then a step timeseries has ended. The temp time series is stored and the temp_series_data variable is cleared
				step_info.append(line.replace('Step Information: ', '').replace('\n',''))
				if temp_series_data != []: step_data.append(temp_series_data)
				temp_series_data = []

			else:
				line_temp = [float(x) for x in line.split('\t')]
				temp_series_data.append(line_temp)


	else: #If the second line does not contain "Step information" then the dataset is not stepped.
		stepped_dataset = False
		f.seek(0)
		f.readline()
		
		# series_data storess the raw data, including time values. In the case of a non-stepped dataset, it is comprised of a two-dimensional array where the vertical dimension is the number of the datasample and the horizontal direction is the curves index.
		series_data = []
		for line in f:
			line_temp = [float(x) for x in line.split('\t')]
			series_data.append(line_temp)

		series_data = np.array(series_data)

if stepped_dataset:

	# Selecting target curves
	step_choice = eg.multchoicebox('What steps do you want to plot?' , 'LT2PY step selecion', step_info)
	if step_choice == None:
		print('No plot steps selected!')
		raise SystemExit(0)

	# Once the choices are chosen, step_choice_index stores the indexes of the curves chosen relative to the curve data stored either in step_data or series_data
	step_choice_index = []
	for x in step_choice:
		for k in range(len(step_info)):
			if x == step_info[k]:
				step_choice_index.append('{}'.format(k))

	step_choice_index = [int(x) for x in step_choice_index]

	# Same drill now for choosing target steps
	curve_choice = eg.multchoicebox('What curves do you want to plot?' , 'LT2PY curve plot selecion', signal_names[1:])
	if curve_choice == None:
		print('No plot curves selected!')
		raise SystemExit(0)

	curve_choice_index = []
	for x in curve_choice:
		for k in range(len(signal_names)):
			if x == signal_names[k]:
				curve_choice_index.append('{}'.format(k))

	curve_choice_index = [int(x) for x in curve_choice_index]

	# What happens in stepped data is that each step has a different time series with different time stamps. So for every step the timestap vector needs to be stored
	timestamps = []
	for step in step_data:
		timestamps.append(np.array([x[0] for x in step]))

	if eg.ynbox('Do you want to plot steps in individual figures?','Please confirm'):     # show a Continue/Cancel dialog
		fig_list = []
		ax_list = []
		for choice in step_choice: 
			temp_fig = pyplot.figure()
			temp_ax = temp_fig.add_axes([0.1,0.1,0.8,0.8]);
			fig_list.append(temp_fig)
			ax_list.append(temp_ax)

		for step_choice_number, ax_choice in zip(step_choice_index, ax_list):
			for curve_choice_number in curve_choice_index:
				ax_choice.plot(timestamps[step_choice_number], [x[curve_choice_number] for x in step_data[step_choice_number]],label=signal_names[curve_choice_number],linewidth=1)
		
		for step_choice_number, ax in zip(step_choice_index, ax_list):
			ax.legend(loc='best')
			ax.grid(which='major')
			ax.grid(which='minor',dashes=(5,2))
			ax.set_xlim([min([min(x) for x in timestamps]),max([max(x) for x in timestamps])])
			ax.set_title(step_info[step_choice_number])

	else:
		fig1 = pyplot.figure()
		ax1 = fig1.add_axes([0.1,0.1,0.8,0.8]);

		# If the data set is stepped but the user has only
		if len(curve_choice) == 1:
			colors = [cm.rainbow(x) for x in np.linspace(0, 1, len(step_choice))]
			for step_choice_number, color_index in zip(step_choice_index, colors):
				ax1.plot(timestamps[step_choice_number], [x[1] for x in step_data[step_choice_number]],linewidth=1, label=step_info[step_choice_number])
		else:
			colors = [cm.rainbow(x) for x in np.linspace(0, 1, len(curve_choice))]
			temp_signal_names = signal_names
			for step_choice_number in step_choice_index:
				for curve_choice_number, color_index in zip(curve_choice_index, range(len(curve_choice_index))):
					ax1.plot(timestamps[step_choice_number], [x[curve_choice_number] for x in step_data[step_choice_number]],label=temp_signal_names[curve_choice_number],linewidth=1, color=colors[color_index])
					temp_signal_names[curve_choice_number] = '_nolegend_'

		ax1.legend(loc='best')
		ax1.grid(which='major')
		ax1.grid(which='minor',dashes=(5,2))
		ax1.set_xlim([min([min(x) for x in timestamps]),max([max(x) for x in timestamps])])


else:
	choice = eg.multchoicebox('What curves do you want to plot?' , 'LT2PY plot selecion', signal_names[1:])
	if choice == None:
		print('No plot curves selected!')
		raise SystemExit(0)

	choice_index = []
	for x in choice:
		for k in range(len(signal_names)):
			if x == signal_names[k]:
				choice_index.append('{}'.format(k))

	choice_index = [int(x) for x in choice_index]

	time_values = [x[0] for x in series_data]

	fig1 = pyplot.figure();
	ax1 = fig1.add_axes([0.1,0.1,0.8,0.8]);

	for choice_number in choice_index:
		ax1.plot(time_values, [x[choice_number] for x in series_data],label=signal_names[choice_number],linewidth=1)

	ax1.legend(loc='best')

	ax1.grid(which='major')
	ax1.grid(which='minor',dashes=(5,2))
	ax1.set_xlim([min(time_values),max(time_values)])

pyplot.show()
