#Imports
import matplotlib.pyplot as plt
import matplotlib.image as mpatches
from PIL import Image
import SimpleITK as sitk
import sys
from skimage.measure import label, regionprops

#Ensuring the number of command prompt inputs is correct
if len(sys.argv) != 2:
	print("Usage: " + sys.argv[0] + " <InputFileName>")

#loading image for Canny Edge Detection
edg = sitk.ReadImage(sys.argv[1])
edg = sitk.Cast(edg, sitk.sitkFloat32)

#setting thresholds with different variance
edges1 = sitk.CannyEdgeDetection(edg, lowerThreshold=0, upperThreshold=.1, variance=[1, 1])
edges2 = sitk.CannyEdgeDetection(edg, lowerThreshold=0, upperThreshold=.1, variance=[3, 3])

#converting image to array
edg = sitk.GetArrayFromImage(edg)
edges1 = sitk.GetArrayFromImage(edges1)
edges2 = sitk.GetArrayFromImage(edges2)


#displaying original image and two images with varying edge detection
fig, (ax1, ax2, ax3) = plt.subplots(nrows=3, ncols=1, figsize=(100,100), sharex=True, sharey=True)
ax1.imshow(edg, cmap=plt.cm.gray)
ax1.margins(x=0, y=-0.25)
ax1.axis('off')
ax1.set_title('Input image', fontsize=20)

ax2.imshow(edges1, cmap=plt.cm.gray)
ax2.margins(x=0, y=-0.25)
ax2.axis('off')
ax2.set_title('Canny filter, $\sigma=1$', fontsize=20)

ax3.imshow(edges2, cmap=plt.cm.gray)
ax3.axis('off')
ax3.set_title('Canny filter, $\sigma=3$', fontsize=20)

fig.tight_layout()

plt.show()

#creating label map for edge detected image
label_image = label(edges2)

#Removing holes
#edges2 = scipy.ndimage.morphology.binary_closing(label_image, edges2)   
#Getting memory error

#edges2 = cv2. convertScaleAbs(edges2)
#(thresh, im_bw) = cv2.threshold(edges2, 127,255,0)

#edges2, contours, hierarchy = cv2.findContours(im_bw,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

fig, ax = plt.subplots(figsize=(101,222))

ax.set_axis_off()
omg = ax.imshow(label_image, cmap="gray")
plt.tight_layout()
plt.show()

#counting number of connected regions to get axon count
count = regionprops(label_image)
print("This sample has " +  str(len(count))  + " axons")