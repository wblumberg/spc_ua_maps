import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# CODE FROM:
# https://jakevdp.github.io/blog/2014/10/16/how-bad-is-your-colormap/
# The function will tranform any colormap into a grayscale version of it.

def grayify_cmap(cmap):
    """Return a grayscale version of the colormap"""
    cmap = plt.cm.get_cmap(cmap)
    colors_i = np.linspace(0, 1., 100)
    colors=cmap(colors_i)

    # convert RGBA to perceived greyscale luminance
    # cf. http://alienryderflex.com/hsp.html
    RGB_weight = [0.299, 0.587, 0.114]
    luminance = np.sqrt(np.dot(colors[:, :3] ** 2, RGB_weight))
    N=100
    rgb=np.zeros((3,N,3))
    for n in range(3):
        rgb[n,:,0]=np.linspace(0,1,N)
        rgb[n,:,1]=luminance
        rgb[n,:,2]=luminance
    k=['red', 'green', 'blue']
    data=dict(zip(k,rgb)) 
    my_cmap = mpl.colors.LinearSegmentedColormap("grayify",data)
    return my_cmap
