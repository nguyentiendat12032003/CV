import sys
import cv2
import numpy as np

# Load our images
img1 = cv2.imread("panorama_1.png")
img2 = cv2.imread("panorama_2.png")

img1_gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
img2_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

# Display grayscale images
cv2.imshow("Image 1 Gray", img1_gray)
cv2.imshow("Image 2 Gray", img2_gray)

# Create our ORB detector and detect keypoints and descriptors
orb = cv2.ORB_create(nfeatures=2000)

# Find the key points and descriptors with ORB
keypoints1, descriptors1 = orb.detectAndCompute(img1, None)
keypoints2, descriptors2 = orb.detectAndCompute(img2, None)

# Draw keypoints on the original images
img1_with_keypoints = cv2.drawKeypoints(img1, keypoints1, None, (255, 0, 255))
img2_with_keypoints = cv2.drawKeypoints(img2, keypoints2, None, (255, 0, 255))
cv2.imshow("Image 1 with Keypoints", img1_with_keypoints)
cv2.imshow("Image 2 with Keypoints", img2_with_keypoints)

# Create a BFMatcher object
bf = cv2.BFMatcher_create(cv2.NORM_HAMMING)

# Find matching points
matches = bf.knnMatch(descriptors1, descriptors2, k=2)

# Display the first descriptor and distance of the first match
print("Descriptor of the first keypoint: ", descriptors1[0])
print("Distance of the first match: ", matches[0][0].distance)

# Draw matches on both images
good_matches = []
for m, n in matches:
    if m.distance < 0.6 * n.distance:
        good_matches.append(m)

img_matches = cv2.drawMatches(img1, keypoints1, img2, keypoints2, good_matches, None)
cv2.imshow("Matches", img_matches)

# Set minimum match condition
MIN_MATCH_COUNT = 10

if len(good_matches) > MIN_MATCH_COUNT:
    # Convert keypoints to an argument for findHomography
    src_pts = np.float32([keypoints1[m.queryIdx].pt for m in good_matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([keypoints2[m.trainIdx].pt for m in good_matches]).reshape(-1, 1, 2)

    # Establish a homography
    M, _ = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)

    # Warp images
    result = cv2.warpPerspective(img2, M, (img1.shape[1] + img2.shape[1], img1.shape[0]))
    result[0:img1.shape[0], 0:img1.shape[1]] = img1
    cv2.imshow("Result", result)

cv2.waitKey(0)
cv2.destroyAllWindows()