import tifffile
import numpy as np
import time
pyArray = np.random.randint(0, 255, (1, 4000, 3000), 'uint8')# This allows you to access the true numpy array under the C# wrapper



omexml = tifffile.OmeXml()
omexml.addimage(
    dtype=pyArray.dtype,
    shape=(500, 4000, 3000),
    storedshape=(500, 1, 1, 4000, 3000, 1),
    axes='ZYX',  # or DimensionOrder='XYZCT'
)
omexml = omexml.tostring()
tif = tifffile.TiffWriter('output.ome.tif', ome=False, bigtiff=True)

start_time = time.time()
for i in range(500):
    tif.write(pyArray, description=omexml, contiguous=True)
    omexml = None


end_time = time.time()
execution_time = end_time - start_time

# Print the execution time
print(f'Execution time: {execution_time} seconds')

tif.close()