import cv2
# pyrefly: ignore [missing-import]
import face_recognition

img = cv2.imread("images/messi.jpg")
rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img_encoding = face_recognition.face_encodings(rgb_img)[0]

img2 = cv2.imread("images/messi2.jpg")
rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]

'''
img2 = cv2.imread("images/elon.jpg")
rgb_img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
img_encoding2 = face_recognition.face_encodings(rgb_img2)[0]
'''
#Compare faces

result = face_recognition.compare_faces([img_encoding], img_encoding2)

if result == [True]:    
    print("Match")
else:
    print("Not Match")  

cv2.imshow("Messi", img)
cv2.imshow("Elon", img2)
cv2.waitKey(0) 