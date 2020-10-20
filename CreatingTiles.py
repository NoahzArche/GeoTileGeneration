# change source_path to point to the original DTM file and tiles_folder to the directory where the tiles should be saved

import os
import gdal
import matlab.engine

# %% Reading DTM file

source_path = '/Users/noahzr/Desktop/TerrainCharacterization/OrbitalData/Jezeroorbitalproducts20200316113258/JEZ_hirise_soc_004_DTM_IAUSphericalDatum_DeltaRadius_1m_Ortho_blend40.tif'
tiles_folder = '/Users/noahzr/Desktop/TerrainCharacterization/OrbitalData/Jezeroorbitalproducts20200316113258/DTMTiles2000kPGM/'

dtm = gdal.Open(source_path)
band = dtm.GetRasterBand(1)

# Pixel size in m
pixel_size_x = dtm.GetGeoTransform()[1]
pixel_size_y = dtm.GetGeoTransform()[5]


# %% Creating tiles (2000 x 2000) and saving them in tiles_folder in png format

tile_size_x = tile_size_y = 2000
window_size = 451

tile_prefix = "tile"
tile_x = tile_y = 0
 
# Orthomosaic band size
xsize = band.XSize - 1
ysize = band.YSize - 1
k = 100;
 
min_height, max_height = band.ComputeRasterMinMax()

for i in range(0, xsize, tile_size_x - 1 + window_size):
    for j in range(0, ysize, tile_size_y - 1 + window_size):
        
        format = "-of PGM -ot UInt16 -scale " + str(min_height) +  " " + str(max_height) + " 0 65535"
        cutting_frame = "-srcwin " + str(i) + " " + str(j) + " " + str(tile_size_x + window_size) + " " + str(tile_size_y + window_size)
        #output_path = tiles_folder + tile_prefix + "_x" + str(tile_x) + "_y" + str(tile_y) + ".png"
        output_path = tiles_folder + tile_prefix + str(k) + ".pgm"
        full_command = "gdal_translate " + format + " " + cutting_frame + " " + source_path + " " + output_path
        os.system(full_command)
        
        k = k + 1
        
        tile_y = tile_y + 1
 
        i = i - window_size # added
        j = j - window_size # added
        
    tile_x = tile_x + 1
    tile_y = 0


# %% Running Geomorphon Classification algorithm

os.chdir('/Users/noahzr/Desktop/TerrainCharacterization/')

eng = matlab.engine.start_matlab()


(max_height - min_height)/65536

# importing variables into matlab workspace
window_size = 451
tdegree = 1
skip = 20
eng.workspace['scaling'] = 0.0155
res = 1


for filename in os.listdir(tiles_folder):
    if filename.endswith((".png")):
        print(filename)
        eng.cd(r'/Users/noahzr/Desktop/TerrainCharacterization/', nargout=0) # where matlab function is saved   
        input_file = tiles_folder + filename
        case_matrix = eng.CSV_Geomorphon_classification_orbital_tile(input_file, 0.0155)
        print('done with geomorphon classification')
    else:
        print('had to continue' + filename)
        continue
        


# %% Merging the tiles back together


tiles = [f for f in os.listdir(tiles_folder) if f.endswith('.png')]
tiles = sorted(tiles)
tiles_string = " ".join(tiles)
os.chdir(tiles_folder)

# sort list of tile files (maybe add a number to them when they are formed) for the command to work 

full_command_merge = "gdal_merge.py -v " + tiles_string + " -o output_merge.tif"

os.system(full_command_merge)





