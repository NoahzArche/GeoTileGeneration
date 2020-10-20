
from ImageData import VicarData
import matplotlib.pyplot as plt
from matplotlib import cm
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import os


# change filename and mod_file 
sol_directory = "/home/sesto/navcam_meshes/01601/"
filename = "NLB_539621449RASLF0603162NCAM00260M1.ht"
mod_file = "N_L1601_RASLF_060_3162_AUTOGENM3.mod"

dem = VicarData.read_vicarfile(sol_directory + "wedge/" + filename)

height = dem.get_height()
width = dem.get_width()

X = np.arange(dem.get_width())  
Y = np.arange(dem.get_height()) 
N, M = len(X), len(Y)
Z = np.zeros((N, M))
   
for coord, j in np.ndenumerate(Z):
    val = dem.get_pixel_double(coord[0], coord[1],0)
    Z[coord[0], coord[1]] = val 


X, Y = np.meshgrid(X,Y)
# Plot DEM
#fig = plt.figure()
#ax = Axes3D(fig)
#ax.scatter3D( X, Y, Z.T, cmap = cm.coolwarm, linewidth = 0, antialiased = False)    
#plt.show()   
  
os.chdir('/home/noahzr/data/')
# saving DEM to .npy file
np.save(filename, Z)




# %% Reading spatial values 

file = open(sol_directory + mod_file)
lines = file.readlines()

for line in lines:
    if filename in line:
        #print(line)
        transform_values = lines[lines.index(line)+1]
        transform_values = transform_values.split(' ')
        transform_values = [i for i in transform_values if i]
        transform_values = [i for i in transform_values if '\n' not in i]
        #print(transform_values)
        
# saving values from .mod file        
xaxis_min = transform_values[0]
yaxis_min = transform_values[1]
xmap_scale = transform_values[2]
ymap_scale = transform_values[5]


spatial_values = [height, width, xaxis_min, yaxis_min, xmap_scale, ymap_scale]

os.chdir('/home/noahzr/data/')
np.save(filename + '_transform', spatial_values)


