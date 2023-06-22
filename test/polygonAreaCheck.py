import cv2
import numpy as np

# Define your points
pts = np.array([[10,10],[20,10],[10,20],[20,20]], np.int32)

# Create a black image and a white mask
image = np.zeros((30,30), dtype=np.uint8)
mask = np.ones((30,30), dtype=np.uint8)*255

# Draw the polyline on the mask
pts = pts.reshape((-1, 1, 2))
cv2.polylines(mask, [pts], isClosed=True, color=(0,0,0), thickness=2)

# Now we have a mask where the polyline area is black and outside is white
# Let's use the mask to get the inside and outside areas
inside = cv2.bitwise_and(image, image, mask=mask)
outside = cv2.bitwise_and(image, image, mask=cv2.bitwise_not(mask))

# Save the images
cv2.imwrite('inside.png', inside)
cv2.imwrite('outside.png', outside)
