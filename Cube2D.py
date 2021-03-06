from cube2d.cube2d import CubicalRipser2D, Filter2D

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import struct
import csv
import matplotlib.pyplot as plt
from matplotlib import gridspec
from mpl_toolkits.mplot3d import Axes3D
from sklearn.decomposition import PCA
import scipy.interpolate as interp
import ipywidgets as widgets
from IPython.display import display
import warnings
from multiprocessing import Pool, TimeoutError
import time
import os
warnings.filterwarnings('ignore')
plt.style.use("ggplot")

'''
    TDA package for Topological Data Analysis tools
'''

'''
    DIPHA Format file converter                             M. Tallon
    and converter to point cloud for CubicalRipser2D(small edits by N. Carrara)

'''


def convert_csv_to_dipha(input_file, output_file):
    df = pd.read_csv(input_file, header=None)

    array_size = df.shape[1]
    iterations = df.shape[0]

    with open(output_file, 'wb') as f:
        symbol = struct.pack("<Q", 8067171840)  # magic number
        f.write(symbol)
        symbol = struct.pack("<Q", 1)  # 1 = Image file
        f.write(symbol)
        symbol = struct.pack("<Q", array_size * iterations)  # image size
        f.write(symbol)
        symbol = struct.pack("<Q", 2)  # 2 dimensions
        f.write(symbol)
        symbol = struct.pack("<Q", array_size)  # image width
        f.write(symbol)
        symbol = struct.pack("<Q", iterations)  # image height
        f.write(symbol)

        # add data for all points
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                value = df.iloc[row, col]
                symbol = struct.pack("<d", value)
                f.write(symbol)
    print("Converted %s to DIPHA format file %s\n" % (input_file, output_file))


def save_array_to_dipha(input_array, output_file):
    df = pd.DataFrame(input_array)

    array_size = df.shape[1]
    iterations = df.shape[0]

    with open(output_file, 'wb') as f:
        symbol = struct.pack("<Q", 8067171840)  # magic number
        f.write(symbol)
        symbol = struct.pack("<Q", 1)  # 1 = Image file
        f.write(symbol)
        symbol = struct.pack("<Q", array_size * iterations)  # image size
        f.write(symbol)
        symbol = struct.pack("<Q", 2)  # 2 dimensions
        f.write(symbol)
        symbol = struct.pack("<Q", array_size)  # image width
        f.write(symbol)
        symbol = struct.pack("<Q", iterations)  # image height
        f.write(symbol)

        # add data for all points
        for row in range(df.shape[0]):
            for col in range(df.shape[1]):
                value = df.iloc[row, col]
                symbol = struct.pack("<d", value)
                f.write(symbol)
    print("Saved array to DIPHA format file %s\n" % output_file)


#   Converting Binary Cells to point cloud (M. Tallon)

def convert_binary_cells_to_point_cloud(input_file, output_file):
    df = pd.read_csv(input_file, header=None)
    df = np.where(df == 1)
    coords = np.asarray(list(zip(df[0], df[1])))
    dfOut = pd.DataFrame(coords)
    dfOut.to_csv(output_file, index=False, header=False)


def save_binary_cells_to_point_cloud(input_array, output_file):
    df = pd.DataFrame(input_array)
    df = np.where(df == 1)
    coords = np.asarray(list(zip(df[0], df[1])))
    dfOut = pd.DataFrame(coords)
    dfOut.to_csv(output_file, index=False, header=False)


'''
    Persistent Homology 

'''


#   Persistence and Barcode plotting (N. Carrara)

def plot_persistence_diagram(barcode, split=True, threshold=-1, save_fig=''):
    dims = [barcode[i][0] for i in range(len(barcode))]
    for d in range(len(barcode)):
        if barcode[d][2] == threshold+1:
            barcode[d][2] = -99999
    #  find max death value
    deaths = [barcode[i][2] for i in range(len(barcode))]
    births = [barcode[i][1] for i in range(len(barcode))]
    max_birth = max(births)
    max_death = max(deaths)
    if max(deaths) == None:
        max_death = max_birth + 1
    else:
        max_death += 1
    max_both = max(max_birth, max_death)
    y = np.linspace(0, max_both, 2)
    #  find unique dimensions    
    unique_dims = []
    for dim in dims:
        if dim not in unique_dims:
            unique_dims.append(dim)
    if len(unique_dims) == 1:
        fig, axs = plt.subplots(1)
        axs.plot(y, y, color='g', linestyle='--')
        for j in range(len(unique_dims)):
            birth_times = [barcode[i][1] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]
            death_times = [barcode[i][2] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]
        #   search for components which live forever
        for d in range(len(death_times)):
            if death_times[d] == -99999:
                death_times[d] = max_death
        axs.plot(y, y, color='g', linestyle='--')
        axs.scatter(birth_times, death_times)
        if max_death != threshold:
            axs.axhline(y = max_death, label="$\infty$", color='k')
        axs.set_xlabel('Birth Time')
        axs.set_ylabel('Death Time')
        axs.set_title('Persistence Diagram for degree $H_%s$' % 0)
        axs.grid(True)
        axs.legend()
        if save_fig:
            fig.savefig(save_fig)
    else:
        #   Plot persistence diagrams for each degree separately
        if split:
            fig, axs = plt.subplots(1, len(unique_dims), figsize=(15, 5))
            for j in range(len(unique_dims)):
                birth_times = [barcode[i][1] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]
                death_times = [barcode[i][2] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]
                #   search for components which live forever
                for d in range(len(death_times)):
                    if death_times[d] == -99999:
                        death_times[d] = max_death
                y = np.linspace(0, max_both, 2)
                axs[j].plot(y, y, color='g', linestyle='--')
                if max_death != threshold:
                    axs[j].axhline(y = max_death, label="$\infty$", color='k')
                axs[j].scatter(birth_times, death_times, color='b')
                axs[j].set_xlabel('Birth Time')
                axs[j].set_ylabel('Death Time')
                axs[j].set_title('Persistence Diagram for degree $H_%s$' % j)
                axs[j].grid(True)
                axs[j].legend()
            if save_fig:
                fig.savefig(save_fig)
        #   Or together
        else:
            fig, axs = plt.subplots(1, figsize=(15,10))
            for j in range(len(unique_dims)):
                birth_times = [barcode[i][1] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]
                death_times = [barcode[i][2] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]
                for d in range(len(death_times)):
                    if death_times[d] == -99999:
                        death_times[d] = max_death
                axs.scatter(birth_times, death_times, label='$H_%s$' % j)
            if max_death != threshold:
                    axs.axhline(y = max_death, label="$\infty$", color='k')
            y = np.linspace(0, max_both, 2)
            axs.plot(y, y, color='g', linestyle='--')
            axs.set_xlabel('Birth Time')
            axs.set_ylabel('Death Time')
            axs.legend()
            axs.set_title('Persistence Diagram')
            axs.grid(True)
            if save_fig:
                fig.savefig(save_fig)

    plt.show()


def plot_persistence_diagram_from_file(life_death_file, split=True):
    df = pd.read_csv(life_death_file, header=None)
    persist = [[df.values[i][0], df.values[i][1], df.values[i][2]] for i in range(len(df.values))]
    plot_persistence_diagram(persist, split=split)


def plot_barcode_diagram(barcode):
    dims = [barcode[i][0] for i in range(len(barcode))]
    #  find unique dimensions
    unique_dims = []
    for dim in dims:
        if dim not in unique_dims:
            unique_dims.append(dim)
    fig, axs = plt.subplots(1, len(unique_dims), figsize=(15, 5))
    if len(unique_dims) == 1:
        for j in range(len(unique_dims)):
            birth_times = [barcode[i][1] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]
            death_times = [barcode[i][2] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]

            max_birth = np.max(birth_times)
            max_death = np.max(death_times)
            min_birth = np.min(birth_times)
            max_both = max(max_birth, max_death)
            scale = 1.0 / max_death
            for k in range(len(birth_times)):
                axs.plot([birth_times[k], death_times[k]], [(k + 1), (k + 1)], color='b', linewidth=10)
            axs.set_xlabel('Time')
            axs.set_ylabel('Component')
            axs.set_ylim(0, len(birth_times) + 1)
            axs.set_yticks([])
            axs.set_title('Barcode Diagram for degree $H_%s$' % 0)
            axs.grid(True)
    else:
        for j in range(len(unique_dims)):
            birth_times = [barcode[i][1] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]
            death_times = [barcode[i][2] for i in range(len(barcode)) if barcode[i][0] == unique_dims[j]]

            max_birth = np.max(birth_times)
            max_death = np.max(death_times)
            min_birth = np.min(birth_times)
            max_both = max(max_birth, max_death)
            scale = 1.0 / max_death
            for k in range(len(birth_times)):
                axs[j].plot([birth_times[k], death_times[k]], [(k + 1), (k + 1)], color='b', linewidth=10)
            axs[j].set_xlabel('Time')
            axs[j].set_ylabel('Component')
            axs[j].set_ylim(0, len(birth_times) + 1)
            axs[j].set_yticks([])
            axs[j].set_title('Barcode Diagram for degree $H_%s$' % j)
            axs[j].grid(True)

    plt.show()


def plot_barcode_diagram_from_file(life_death_file):
    df = pd.read_csv(life_death_file, header=None)
    persist = [[df.values[i][0], df.values[i][1], df.values[i][2]] for i in range(len(df.values))]
    plot_barcode_diagram(persist)


'''
    Persistent Homology Dimension                   (M. Tallon)
'''


def compute_2DPHD(barcode, show_plot=True, output_file=''):
    dfOut = pd.DataFrame([], columns=['PH Dim'])
    df = pd.DataFrame(barcode)
    df = df.dropna()
    #df.D.astype('float')
    df["X"] = (df.iloc[:, 2].values + df.iloc[:, 1].values) / 2
    df["Y"] = np.arccos(df.iloc[:, 1].values / df.iloc[:, 2].values)
    dfDim1 = df.loc[df.iloc[:, 0] == 1]
    dfDim0 = df.loc[df.iloc[:, 0] == 0]
    if dfDim1.shape[0] == 0:
        dfOut.append({'PH Dim': 'NA'}, ignore_index=True)
        return
    xSorted = np.sort(dfDim1.iloc[:, 3].values)
    logPH = np.empty((dfDim1.shape[0], 2))
    logPH[:, 0] = xSorted
    logPH[0, 1] = logPH.shape[0]
    eqCount = 1
    for row in range(1, logPH.shape[0]):
        if logPH[row, 0] > logPH[row - 1, 0]:
            logPH[row, 1] = logPH[row - 1, 1] - eqCount
            eqCount = 1
        else:
            logPH[row, 1] = logPH[row - 1, 1]
            eqCount += 1
    logPH = np.log10(logPH)
    slope = np.polyfit(logPH[:, 0], logPH[:, 1], 1)
    print(slope)
    dfOut = dfOut.append({'PH Dim': -slope[0]}, ignore_index=True)

    if output_file:
        dfOut.to_csv(output_file + ".csv", index=False)

    # Plots
    if show_plot:
        plt.figure()
        plt.tight_layout(pad=4.4, w_pad=4.5, h_pad=4.0)
        fitline = np.empty(logPH.shape)
        fitline[:, 0] = logPH[:, 0]
        fitline[:, 1] = fitline[:, 0] * slope[0] + slope[1]
        plt.plot(fitline[:, 0], fitline[:, 1])
        plt.scatter(logPH[:, 0], logPH[:, 1])
        plt.title("PH Dimension:  {}".format(str(round(-slope[0], 2))))
        plt.xlabel("Log(X)")
        plt.ylabel("Log(F(X))")
        plt.savefig((output_file + ".png"))
        plt.show()


def compute_2DPHD_from_file(input_file, show_plot=True, output_file=''):
    df = pd.read_csv(input_file, header=None)
    persist = [[df.values[i][0], df.values[i][1], df.values[i][2]] for i in range(len(df.values))]
    compute_2DPHD(persist, show_plot, output_file)


def slinding_window_conv(time_grid, filter_size, dim, Tau, dT):
    num_x = len(time_grid) - filter_size + 1
    num_y = len(time_grid[0]) - filter_size + 1

    convolutions = []
    iteration = 0
    for y in num_y:
        for x in num_x:
            convolution = [[time_grid[i][j][k] for j, k in range(len(time_grid[0])) 
                                if x <= j <= x + filter_size - 1 and y <= k <= j + filter_size - 1] for i in range(len(time_grid))]
            convolutions.append(["conv_%s" % iteration, convolution])
            iteration += 1
    
    
    pool = Pool(processes=50)              # start 4 worker processes

        # print "[0, 1, 4,..., 81]"

    print(pool.map(sliding_window, convolutions))


def sliding_window(X):
    dim = 30
    Tau = 1
    dT = 1
    XS = getSlidingWindowVideo(X[1], dim, Tau, dT)

    #Mean-center and normalize sliding window
    XS = XS - np.mean(XS, 1)[:, None]
    XS = XS/np.sqrt(np.sum(XS**2, 1))[:, None]

    #Get persistence diagrams
    dgms = ripser(XS)['dgms']

    #Do PCA for visualization
    pca = PCA(n_components = 3)
    Y = pca.fit_transform(XS)


    fig = plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plot_dgms(barcode)
    plt.title("1D Persistence Diagram %s" % X[0])

    c = plt.get_cmap('nipy_spectral')
    C = c(np.array(np.round(np.linspace(0, 255, Y.shape[0])), dtype=np.int32))
    C = C[:, 0:3]
    ax2 = fig.add_subplot(122, projection = '3d')
    ax2.set_title("PCA of Sliding Window Embedding")
    ax2.scatter(Y[:, 0], Y[:, 1], Y[:, 2], c=C)
    ax2.set_aspect('equal', 'datalim')
    plt.savefig(X[0] + ".png")
    plt.show()



#   Chris Tralie's Sliding Window
def getSlidingWindowVideo(I, dim, Tau, dT):
    N = I.shape[0] #Number of frames
    P = I.shape[1] #Number of pixels (possibly after PCA)
    pix = np.arange(P)
    NWindows = int(np.floor((N-dim*Tau)/dT))
    X = np.zeros((NWindows, dim*P))
    idx = np.arange(N)
    for i in range(NWindows):
        idxx = dT*i + Tau*np.arange(dim)
        start = int(np.floor(idxx[0]))
        end = int(np.ceil(idxx[-1]))+2
        if end >= I.shape[0]:
            X = X[0:i, :]
            break
        f = scipy.interpolate.interp2d(pix, idx[start:end+1], I[idx[start:end+1], :], kind='linear')
        X[i, :] = f(pix, idxx).flatten()
    return X



if __name__ == "__main__":
    grid = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,1,0,0]]
    with open("square.csv", 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',')
        writer.writerows(grid)
    #   try 2D von neumann filter
    filt = Filter2D()
    filt.loadBinaryFromFile("square.csv")
    filt.filterBinaryL2(10)
    filt.saveBinaryFiltration("square2.csv")
    cube2D = CubicalRipser2D()
    convert_csv_to_dipha("square2.csv", "square_dipha.csv")
    cube2D.ComputeBarcode("square_dipha.csv", "test.csv", "DIPHA", 10, True)
    barcode = cube2D.getBarcode()
    plot_persistence_diagram(barcode)

    grid = [[0,0,1,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,0,0,0],[0,0,1,0,0]]
    filt = Filter2D(grid)
    filt.filterBinaryL2(10)
    cube2D = CubicalRipser2D(filt.getBinaryFiltration(), 10)
    cube2D.ComputeBarcode()
    barcode = cube2D.getBarcode()
    plot_persistence_diagram(barcode)

    grid = [[2,2,2],[2,3,2],[2,2,2]]
    cube2D_2 = CubicalRipser2D(grid, 4);
    cube2D_2.ComputeBarcode()
    barcode = cube2D_2.getBarcode()
    print(barcode)
    plot_persistence_diagram(barcode)

