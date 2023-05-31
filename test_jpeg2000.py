import tifffile
import numpy as np
import time


embryo = "/media/tema/big_storage/work/goethe/fiji/test_dataset/DS0016_MEME6/(P0)-ZStacks-Raw/CH0001/DR0001/MGolden2022A-DS0016TP0001DR0001CH0001PL(ZS).tif"
z1_cells = "/media/tema/big_storage/work/goethe/fiji/test_dataset/Z1/20211228_huLO_CCA14_p115+4_expansion_1,5umSpacing_TL3_one_part.tif"
pyArray = tifffile.imread(z1_cells)



start_time = time.time()

tif = tifffile.imwrite('jpeg2000_lossy_65_z1_cells.tif', pyArray, compression=('JPEG_2000_LOSSY', 65),
# tif = tifffile.imwrite('jpeg2000_zlib_embryo.tif', pyArray, compression='ZLIB', 
                       maxworkers=11)

end_time = time.time()
execution_time = end_time - start_time

# Print the execution time
print(f'Execution time: {execution_time} seconds')
