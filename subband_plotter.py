#Conor Sheridan - 14/08/2024
import numpy as np
import matplotlib.pyplot as plt
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-d',   dest='dir',   type=str,   help='directory of data to plot. Default your current directory.',default='.')
parser.add_argument('-l',   dest='lbl',   type=str,   help='Optional. Location of csv file containing subband frequency labels.',default='')
parser.add_argument('-s',   dest='nsub',  type=int,   help='number of subbands to plot. Default = 1',default=1)
parser.add_argument('-b',   dest='nbins', type=int,   help='Phase normalization (should be number of bins). Default = 128',default=128)
parser.add_argument('-f',   dest='file',  type=str,   help='naming convention of the file(s) with %i where the number iteration is. eg: datafile%i.txt')
args = parser.parse_args()
data_dir = args.dir
n = args.nsub
filename = args.file
nbins = args.nbins
lblfile = args.lbl

x_sets = {}
y_sets = {}

#takes a csv file, converts string -> list -> np string array -> np float array
if lblfile != '':
    with open(f'{lblfile}') as file:
        lbl_list = np.array(file.readline().split(',')).astype(np.float16)
    file.close()
else:
    lbl_list = np.linspace(0,n,n+1).astype(int)

for i in range(n+1):
    x_sets['x_set%i' % i] = []
    y_sets['y_set%i' % i] = []

    with open(f"{data_dir}/{filename}" % i, 'r') as file:
        for line in file:
            if not(line.startswith('#') or line.startswith(' ')):
                columns = line.split()
                x_sets["x_set%i" % i].append(int(columns[2]))
                y_sets["y_set%i" % i].append(float(columns[3]))
    file.close()

    #adjusting x-axis for peak centering
    # x_sets["x_set%i" % i]=np.array(x_sets["x_set%i" % i])
    # x_sets["x_set%i" % i]+=centerval[i]


    #if no labels given, just names subbands 0 to n
    if lblfile == '':
        plt.plot(np.array(x_sets["x_set%i" % i])/nbins, np.array(y_sets["y_set%i" % i])/max(y_sets["y_set%i" % i]), label='{0}'.format(lbl_list[i]))
    
    #otherwise formats them to MHz
    else:
        plt.plot(np.array(x_sets["x_set%i" % i])/nbins, np.array(y_sets["y_set%i" % i])/max(y_sets["y_set%i" % i]), label='{0:.2f} MHz'.format(lbl_list[i]))

plt.xlabel('Phase')
plt.ylabel('Flux')
plt.xlim(0,1)
plt.title("2024/07/23 B0531+21 Flux vs Phase ")
plt.legend()
plt.grid()
plt.show()