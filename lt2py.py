import easygui as eg

import libraries.time_series as ts

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

	if line[0] == 'time':
		f.seek(0)
		ts.time_series(f)
