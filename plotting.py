import numpy as np
from numpy import sqrt, log, exp, mean, cumsum, sum, zeros, ones, argsort, argmin, argmax, array, maximum, concatenate
from numpy.random import randn, rand
np.set_printoptions(precision = 4)

import os
import matplotlib
matplotlib.use('Agg')
import matplotlib as mpl
import seaborn as sns
mpl.rcParams['mathtext.fontset'] = 'cm'
mpl.rcParams['font.family'] = 'STIXGeneral'
mpl.rcParams['font.size'] = 24
mpl.rcParams['axes.labelsize'] = 36
mpl.rcParams['xtick.labelsize']= 28
mpl.rcParams['ytick.labelsize']= 28

import matplotlib.pyplot as plt
plt.switch_backend('agg')
pgf_with_rc_fonts = {"pgf.texsystem": "pdflatex"}
matplotlib.rcParams.update(pgf_with_rc_fonts)


## Plotting settings

plot_style = ['-', '--','-.',':','--']
both_plot_style = ['-', '--']
plot_col = ['green', 'darkorange', 'royalblue','mediumslateblue','firebrick']
plot_mark = [ 'x', 'o', '^', 'v', '+']
plots_ind = 1


def saveplot(direc, filename, lgd, ext = 'pdf',  close = True, verbose = True):
    filename = "%s.%s" % (filename, ext)
    if not os.path.exists(direc):
        os.makedirs(direc)
    savepath = os.path.join(direc, filename)
    plt.savefig(savepath, bbox_extra_artists=(lgd,), bbox_inches='tight')
    if verbose:
        print("Saving figure to %s" % savepath)
    if close:
        plt.close()


def heatmapplot(xlabel, ylabel, mat, dirname, filename, xparalist, yparalist, vmin, vmax, value = "power", extra = "_r"):
    sns.set(font_scale = 1)

    if len(yparalist)<=10:
        ax = sns.heatmap(mat, vmin = vmin, vmax = vmax, cmap = "YlGnBu"+extra,  xticklabels = xparalist, yticklabels = yparalist, cbar_kws={'label': value})
        cbar_axes = ax.figure.axes[-1]
        ax.figure.axes[-1].yaxis.label.set_size(20)
        ax.set_xlabel(xlabel, fontsize=20)
        ax.set_ylabel(ylabel, fontsize=20)
    else:
        num_ticks = 10
        # the index of the position of yticks
        yticks = np.linspace(0, len(yparalist) - 1, num_ticks, dtype=np.int)
        # the content of labels of these yticks
        yticklabels = [yparalist[idx] for idx in yticks]
        change = 0
        if len(xparalist)>10:
            xticks = np.linspace(0, len(xparalist) - 1, num_ticks, dtype=np.int)
            xticklabels = [xparalist[idx] for idx in xticks]  
            xparalist = xticklabels 
            change = 1         
        ax = sns.heatmap(mat, vmin = vmin, vmax = vmax, cmap = "YlGnBu"+extra,  xticklabels = xparalist, yticklabels = yticklabels, cbar_kws={'label': value})
        cbar_axes = ax.figure.axes[-1]
        ax.figure.axes[-1].yaxis.label.set_size(20)
        ax.set_xlabel(xlabel, fontsize=20)
        ax.set_ylabel(ylabel, fontsize=20)
        if change == 1:  
            ax.set_xticks(xticks) 
        ax.set_yticks(yticks) 
    saveplot(dirname, filename, ax)



def plot_errors_mat_both(xs, matrix_av_pow, matrix_av_fdr, matrix_err_pow, matrix_err_fdr, labels, dirname, filename, xlabel, ylabel):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    no_lines = len(matrix_av_pow)

    for i in range(no_lines):
            ys = np.array(matrix_av_pow[i])
            zs = np.array(matrix_err_pow[i])
            ax.errorbar(xs, ys, yerr = zs, color = plot_col[i % len(plot_col)], marker = plot_mark[i % len(plot_mark)], linestyle = plot_style[i%len(plot_style)], lw= 2, markersize =8, label=labels[i])

    lgd = ax.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, handletextpad=0.3,
                       ncol=min(no_lines,2), mode="expand", borderaxespad=0., prop={'size': 15})
    for j in range(no_lines):
            ys = np.array(matrix_av_fdr[j])
            zs = np.array(matrix_err_fdr[j])
            ax.errorbar(xs, ys, yerr = zs, color = plot_col[j % len(plot_col)], marker = plot_mark[j % len(plot_mark)], linestyle = plot_style[1], lw= 2, markersize = 8, label = None)
    ax.hlines(y=0.05, xmin=min(xs), xmax = max(xs), color='k')
    ax.set_xlabel(xlabel, labelpad=15)
    ax.set_ylabel(ylabel, labelpad=15)
    ax.set_xlim((min(xs), max(xs)))
    ax.set_ylim((0, 1))
    yt = ax.get_yticks() 
    yt[0]=0.05
    ytl=yt.tolist()
    ytl[0]="0.05"
    ax.set_yticks(yt)
    ax.set_yticklabels(ytl)
    ax.grid(True)
    saveplot(dirname, filename, lgd)




    
