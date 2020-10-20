# ProcessingData


## ReadVicarDEM

Reads .ht heightmaps and saves a pickle file containing the elevation data and a pickle file contatining relevant spatial information.


## CreatingSpatialData

Uses the pickle files containing the elevation data and spatial information (i.e. the files which are generated after running ReadVicarDEM) to generate GeoTiff files with spatial reference data, allowing the resulting GeoTiff file to be analyzed using gdal, ArcGIS, etc. 



## CreatingTiles

Creates smaller tiles of a large tiff image.
These tiles can then be used for analysis (such as running the geomorphon algorithm).

Installing matlab engine API for python (requires Matlab to be installed): Go into matlabroot directory, `$ cd extern/engines/python/`, `$ python setup.py build --build-base=$(mktemp -d) install` 

