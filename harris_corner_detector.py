from skimage import io
import scipy

img = io.imread('PCB.jpg', as_gray = True)
img1 = io.imread('PCB.jpg')
smoothened_img = scipy.ndimage.gaussian_filter(img, 1)