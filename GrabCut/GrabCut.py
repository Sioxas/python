import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('php.png')
mask = np.zeros(img.shape[:2],np.uint8)

bgdModel = np.zeros((1,65),np.float64)
fgdModel = np.zeros((1,65),np.float64)

rect = (0,0,img.shape[1]-1,img.shape[0]-1)
cv2.grabCut(img,mask,rect,bgdModel,fgdModel,5,cv2.GC_INIT_WITH_RECT)

mask2 = np.where((mask==2)|(mask==0),0,1).astype('uint8')
img = img*mask2[:,:,np.newaxis]
img = cv2.merge((img, 255*mask2))
cv2.imwrite('phpa.png',img)
# plt.imshow(img),plt.colorbar(),plt.show()