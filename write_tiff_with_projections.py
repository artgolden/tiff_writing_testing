import tifffile
import numpy as np
import time
from skimage.transform import resize


def convert(img, target_type_min, target_type_max, target_type):
    imin = img.min()
    imax = img.max()

    a = (target_type_max - target_type_min) / (imax - imin)
    b = target_type_max - a * imax
    new_img = (a * img + b).astype(target_type)
    return new_img



embryo = "/media/tema/big_storage/work/goethe/fiji/test_dataset/DS0016_MEME6/(P0)-ZStacks-Raw/CH0001/DR0001/MGolden2022A-DS0016TP0001DR0001CH0001PL(ZS).tif"

pyArray = tifffile.imread(embryo)
anisotropy_factor = 4

omexml = tifffile.OmeXml()
omexml.addimage(
    dtype=pyArray.dtype,
    shape=pyArray.shape,
    storedshape=(pyArray.shape[0], 1, 1, pyArray.shape[1], pyArray.shape[2], 1),
    axes='ZYX',  # or DimensionOrder='XYZCT'
)
omexml = omexml.tostring()

start_time = time.time()

tif = tifffile.TiffWriter('embryo.ome.tif', ome=False, bigtiff=True)
x_projection = np.empty((pyArray.shape[0], pyArray.shape[2]), dtype=pyArray.dtype)
y_projection = np.empty((pyArray.shape[0], pyArray.shape[1]), dtype=pyArray.dtype)

for i, plane in enumerate(pyArray):
    tif.write(plane, description=omexml, contiguous=True)
    x_projection[i] = plane.max(axis=0)
    y_projection[i] = plane.max(axis=1)
    omexml = None

y_projection = resize(y_projection, (pyArray.shape[0] * anisotropy_factor, y_projection.shape[1]))
x_projection = resize(x_projection, (pyArray.shape[0] * anisotropy_factor, x_projection.shape[1]))

tifffile.imwrite('Y_projection_embryo.ome.tif', convert(
    y_projection, 0, np.iinfo('uint16').max, np.uint16), imagej=True)
tifffile.imwrite('X_projection_embryo.ome.tif', convert(
    x_projection, 0, np.iinfo('uint16').max, np.uint16), imagej=True)

end_time = time.time()
execution_time = end_time - start_time

# Print the execution time
print(f'Execution time: {execution_time} seconds')

tif.close()



