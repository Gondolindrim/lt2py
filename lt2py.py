import numpy as np

# MatplotLib and PyPlot for plotting
import matplotlib.pyplot as pyplot
import matplotlib as mplot
from matplotlib import rc

with open('cmrr.txt', 'r', encoding='ISO-8859-1') as f:

	# Counting number of rows in file
	for k, i in enumerate(f):
		pass

	# Number of rows in the file, which is given by number of data points
	lineLen = k
	f.seek(0)

	pointer1 = 4
	line = f.readline()

	# Counter for the number of traces in the file
	dataTraces = 0
	i = 0
	labels = [];
	while 1:

		pointer1 += 1

		while line[pointer1]!='\t':
			pointer1 += 1

		pointer2 = pointer1 + 1

		while line[pointer2]!='\t' and line[pointer2]!='\n':
			pointer2 += 1

		labels.append(str(line[pointer1+1:pointer2]))

		dataTraces += 1
		i += 1

		if line[pointer2] == '\n':
			break

	
	# Initializing data
	gain = 0*np.ones((lineLen,dataTraces))
	phase = 0*np.ones((lineLen,dataTraces))
	freq = 0*np.ones((lineLen,1))

	for i in range(lineLen):
		
		line = f.readline()
		freq[i,0] = float(line[0:22])

		#print('\n{0:8.5f}'.format(freq[i,0]))

		pointer = 22
		pointer2 = 0
		
		for k in range(dataTraces):
			
			while line[pointer2]!=',':
				pointer2 += 1

			gain[i,k] = float(line[pointer+1:pointer2-2])
			#print(gain[i,k])

			pointer = pointer2

			while line[pointer2]!=')':
				pointer2 += 1

			phase[i,k] = float(line[pointer+1:pointer2-1])
			#print(phase[i,k])

			if k < dataTraces - 1:
				while line[pointer]!='(':
					pointer += 1

fig1 = pyplot.figure();
ax1 = fig1.add_axes([0.1,0.1,0.8,0.8]);

fig2 = pyplot.figure();
ax2 = fig2.add_axes([0.1,0.1,0.8,0.8]);

for k in range(dataTraces):
	ax1.semilogx(freq[:,0],gain[:,k],label=labels[k],linewidth=1)
	ax2.semilogx(freq[:,0],phase[:,k],label=labels[k],linewidth=1)

ax1.legend(loc='bottom left')
ax2.legend(loc='upper left')

ax1.grid(which='major')
ax1.grid(which='minor',dashes=(5,2))
ax1.set_xlim([min(freq),max(freq)])

ax2.grid(which='major')
ax2.grid(which='minor',dashes=(5,2))
ax2.set_xlim([min(freq),max(freq)])

pyplot.show()
