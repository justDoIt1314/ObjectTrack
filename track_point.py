import cv2
import time
import sys
import os
import argparse
import threading

parser = argparse.ArgumentParser(description='getsubImage')
parser.add_argument('--imagePath', default="D:\\MyWork\\VRAuto\\VRAuto\\VRAuto\\VRAuto\\bin\\x64\\Debug\\SaveImage4\\", type=str, help='imagePath')
parser.add_argument('--x', default=1000, type=int, help='x')
parser.add_argument('--y', default=1000, type=int, help='y')

minor_ver = 4
if __name__ == '__main__' :
    

    # Set up tracker.
    # Instead of MIL, you can also use
 
    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'GOTURN', 'MOSSE']
    tracker_type = tracker_types[1]
    
    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()
        if tracker_type == 'GOTURN':
            tracker = cv2.TrackerGOTURN_create()
        if tracker_type == 'MOSSE':
            tracker = cv2.TrackerMOSSE_create()
    
    # Read frame
    # path = "D:\\MyWork\\VRAuto\\VRAuto\\VRAuto\\VRAuto\\bin\\x64\\Debug\\SaveImage4\\"
    args = parser.parse_args()
    path = args.imagePath
    names = os.listdir(path)

    
    
    
    # Read first frame.
    frame = cv2.imread(path+names[-1])
    # x,y = (1062,1246)
    x,y = (args.x,args.y)
    add = 8
    bbox = (x-add,y-add,2*add,2*add) #saveIamge4 
    # Define an initial bounding box
    # bbox = (960, 1367, 16, 15) #saveImage1
    # bbox = (1282, 1272, 14, 13)  #saveImage2
    # bbox = (899, 1260, 16, 16)  #saveImage3
    # Uncomment the line below to select a different bounding box
    # bbox = cv2.selectROI(frame, False)
 
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
 
    while True:
        # Read a new frame
        names = os.listdir(path)
        frame = cv2.imread(path+names[-1])

        # Update tracker
        ok, bbox = tracker.update(frame)
 
       
        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            center = (int(bbox[0] + bbox[2]//2), int(bbox[1] + bbox[3]//2))
            print("{0}".format(center))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
 
        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2)
     
        picName = "{0},{1},{2}".format("picfile/",str(time.time()),".jpg")
        cv2.imwrite(picName,frame)
        time.sleep(10)
        # Display result
        # cv2.imshow("Tracking", frame)
        # cv2.waitKey()