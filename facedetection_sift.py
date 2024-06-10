import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Load images
img1 = cv.imread('face_detection.jpg', cv.IMREAD_GRAYSCALE)  # queryImage
img2 = cv.imread('face.jpg', cv.IMREAD_GRAYSCALE)  # trainImage

# Initiate SIFT detector
sift = cv.SIFT_create()

# Set SIFT parameters
sift.setContrastThreshold(0.03)
sift.setEdgeThreshold(5)

# Find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
search_params = dict(checks=50)  # or pass empty dictionary

flann = cv.FlannBasedMatcher(index_params, search_params)

# Match keypoints
matches = flann.knnMatch(des1, des2, k=2)

# Ratio test as per Lowe's paper
good_matches = []
for m, n in matches:
    if m.distance < 0.1 * n.distance:
        good_matches.append(m)

# Extract coordinates of matched keypoints
src_pts = np.float32([kp1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
dst_pts = np.float32([kp2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

# Calculate bounding box coordinates for image 1 (face_detection.jpg)
x_min, y_min = np.min(src_pts, axis=0)[0]
x_max, y_max = np.max(src_pts, axis=0)[0]

# Draw bounding box on the first image (face_detection.jpg)
img1_with_bb = cv.cvtColor(img1, cv.COLOR_GRAY2BGR)
cv.rectangle(img1_with_bb, (int(x_min), int(y_min)), (int(x_max), int(y_max)), (0, 255, 0), 2)

# Draw keypoints on both images with specified parameters
img1_with_keypoints = cv.drawKeypoints(img1_with_bb, kp1, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
img2_with_keypoints = cv.drawKeypoints(img2, kp2, None, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)

# Display the images with bounding box and keypoints
plt.subplot(121)
plt.imshow(img1_with_keypoints)
plt.title('Image 1 with bounding box and keypoints')

plt.subplot(122)
plt.imshow(img2_with_keypoints, cmap='gray')
plt.title('Image 2 with keypoints')

plt.show()
