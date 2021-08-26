from skimage import io
import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.signal import convolve2d
from matplotlib import pyplot as plt

img = io.imread('PCB.jpg', as_gray = True)
img1 = io.imread('PCB.jpg') # placeholder to indicate the corners later

smoothened_img = gaussian_filter(img, 1)

# gradient along x-axis
sobel_x = np.array([[-1, 0, 1],
                    [-2, 0, 2],
                    [-1, 0, 1]])

# gradient along y-axis
sobel_y = np.array([[-1, -2, -1],
                    [0, 0 ,0],
                    [1, 2, 1]])

# Forming the structure tensor for the input image
grad_x = convolve2d(smoothened_img, sobel_x, mode = 'same', boundary = 'symm')
grad_y = convolve2d(smoothened_img, sobel_y, mode = 'same', boundary = 'symm')
grad_x_square = grad_x * grad_x
grad_y_square = grad_y * grad_y
grad_x_y = grad_x * grad_y

smoothened_grad_x_square = gaussian_filter(grad_x_square, 1)
smoothened_grad_y_square = gaussian_filter(grad_y_square, 1)
smoothened_grad_x_y = gaussian_filter(grad_x_y, 1)

ad = smoothened_grad_x_square * smoothened_grad_y_square
bc = smoothened_grad_x_y * smoothened_grad_x_y
trace_matrix = smoothened_grad_x_square + smoothened_grad_y_square
trace_matrix_square = trace_matrix * trace_matrix
det_J = ad-bc

# Computing the response by: det(J) - k Trace(M)^2, where k is an empirically chosen value
k = 0.1
corner_matrix = (-k * trace_matrix_square) + det_J

# Indicate corner pixels in red
img1[corner_matrix > k] = [255, 0, 0] 

fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.imshow(img, cmap = 'gray')
ax2.imshow(img1)