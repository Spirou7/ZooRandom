import cv2

chunklist_url = "https://zssd-penguin.hls.camzonecdn.com/CamzoneStreams/zssd-penguin/chunklist.m3u8"

cap = cv2.VideoCapture(rtmp_url)

ret, frame = cap.read()
if ret:
    cv2.imwrite("frame.jpg", frame)
    print("Frame saved")
cap.release()
