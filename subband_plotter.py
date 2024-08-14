#Conor Sheridan - 14/08/2024
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d',   dest='dir',   type=str,   help='directory of data to plot. Default your current directory.',default='.')
parser.add_argument('-n',   dest='nsub',  type=int,   help='number of subbands to plot. Default = 1',default=1)
parser.add_argument('-f',   dest='file',  type=str,   help='naming convention of the file(s) with {0} where the number iteration is. eg: datafile{0}.txt')
args = parser.parse_args()
data_dir = args.dir
n = args.nsub
filename = args.file

x_sets={}
y_sets={}

#labels for graph - can change
freqsn=[107.71484375,118.65234375,129.58984375,140.52734375,151.46484375,162.40234375,173.33984375,184.27734375,193.65234375]

for i in range(n):
    x_sets['x_set{0}'.format(i)] = []
    y_sets['y_set{0}'.format(i)] = []

    with open(f'{data_dir}/{filename}'.format(i), 'r') as file:
        for line in file:
            if not line.startswith('#'):
                columns = line.split()
                x_sets["x_set{0}".format(i)].append(int(columns[2]))
                y_sets["y_set{0}".format(i)].append(float(columns[3]))
        
    plt.plot(np.array(x_sets["x_set{0}".format(i)])/128, np.array(y_sets["y_set{0}".format(i)])/max(y_sets["y_set{0}".format(i)]), label='{0:.2f} MHz'.format(freqsn[i]))

plt.xlabel('Phase')
plt.ylabel('Flux')
plt.xlim(0,1)
plt.title("2024/07/23 B0531+21 Flux vs Phase ")
plt.legend()
plt.show()
