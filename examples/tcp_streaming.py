import cv2

cap = cv2.VideoCapture("tcp://192.168.20.74:11112")
print(cap)
while(True): 
    ret, frame = cap.read() 
    cv2.imshow('frame', frame) 
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
cap.release() 
cv2.destroyAllWindows() 
