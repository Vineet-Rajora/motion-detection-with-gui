from tkinter import *
import tkinter as tk 
from tkinter import Message, Text
from imutils.video import VideoStream
import argparse
import datetime
import imutils
import time
import cv2

def detecting_motion():
      images=(txt.get())
      if images:
            ap = argparse.ArgumentParser()
            ap.add_argument("-v", "--video",type=str,default=txt.get(),
                            help="path to the video file")
            ap.add_argument("-a", "--min-area", type=int, default=600, help="minimum area size")
            args = vars(ap.parse_args())
            
            vs = cv2.VideoCapture(args["video"])

            # initialize the first frame in the video stream
            firstFrame = None

            # loop over the frames of the video
            while True:
                    # grab the current frame and initialize the occupied/unoccupied
                    # text
                    frame = vs.read()
                    frame = frame if args.get("video", None) is None else frame[1]
                    text = "Unoccupied"

                    # if the frame could not be grabbed, then we have reached the end
                    # of the video
                    if frame is None:
                            break

                    # resize the frame, convert it to grayscale, and blur it
                    frame = imutils.resize(frame, width=500)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray = cv2.GaussianBlur(gray, (21, 21), 0)

                    # if the first frame is None, initialize it
                    if firstFrame is None:
                            firstFrame = gray
                            continue

                    # compute the absolute difference between the current frame and
                    # first frame
                    frameDelta = cv2.absdiff(firstFrame, gray)
                    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

                    # dilate the thresholded image to fill in holes, then find contours
                    # on thresholded image
                    thresh = cv2.dilate(thresh, None, iterations=2)
                    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)

                    # loop over the contours
                    for c in cnts:
                            # if the contour is too small, ignore it
                            if cv2.contourArea(c) < args["min_area"]:
                                    continue

                            # compute the bounding box for the contour, draw it on the frame,
                            # and update the text
                            (x, y, w, h) = cv2.boundingRect(c)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
                            text = "Occupied"

                    # draw the text and timestamp on the frame
                    cv2.putText(frame, "Room Status: {}".format(text), (30,20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

                    # show the frame and record if the user presses a key
                    cv2.imshow("Security Feed", frame)
                    cv2.imshow("Thresh", thresh)
                    cv2.imshow("Frame Delta", frameDelta)
                    key = cv2.waitKey(1) & 0xFF

                    # if the `x` key is pressed, break from the lop
                    if key == ord("x"):
                            break

            # cleanup the camera and close any open windows
            vs.stop() if args.get("video", None) is None else vs.release()
            cv2.destroyAllWindows()
      else:
            print("You didn't provide any input Video file.")
            print("[INFO]Starting the Camera......")
            ap = argparse.ArgumentParser()
            ap.add_argument("-v", "--video",help="path to the video file")
            ap.add_argument("-a", "--min-area", type=int, default=500, help="minimum area size")
            args = vars(ap.parse_args())
            
            vs = VideoStream(src=0).start()
            time.sleep(2.0)

            # initialize the first frame in the video stream
            firstFrame = None

            # loop over the frames of the video
            while True:
                    # grab the current frame and initialize the occupied/unoccupied
                    # text
                    frame = vs.read()
                    frame = frame if args.get("video", None) is None else frame[1]
                    text = "Unoccupied"

                    # if the frame could not be grabbed, then we have reached the end
                    # of the video
                    if frame is None:
                            break

                    # resize the frame, convert it to grayscale, and blur it
                    frame = imutils.resize(frame, width=500)
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    gray = cv2.GaussianBlur(gray, (21, 21), 0)

                    # if the first frame is None, initialize it
                    if firstFrame is None:
                            firstFrame = gray
                            continue

                    # compute the absolute difference between the current frame and
                    # first frame
                    frameDelta = cv2.absdiff(firstFrame, gray)
                    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]

                    # dilate the thresholded image to fill in holes, then find contours
                    # on thresholded image
                    thresh = cv2.dilate(thresh, None, iterations=2)
                    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
                            cv2.CHAIN_APPROX_SIMPLE)
                    cnts = imutils.grab_contours(cnts)

                    # loop over the contours
                    for c in cnts:
                            # if the contour is too small, ignore it
                            if cv2.contourArea(c) < args["min_area"]:
                                    continue

                            # compute the bounding box for the contour, draw it on the frame,
                            # and update the text
                            (x, y, w, h) = cv2.boundingRect(c)
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 255), 2)
                            text = "Occupied"

                    # draw the text and timestamp on the frame
                    cv2.putText(frame, "Room Status: {}".format(text), (30,20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
                    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
                            (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 255, 0), 1)

                    # show the frame and record if the user presses a key
                    cv2.imshow("Security Feed", frame)
                    cv2.imshow("Thresh", thresh)
                    cv2.imshow("Frame Delta", frameDelta)
                    key = cv2.waitKey(1) & 0xFF

                    # if the `x` key is pressed, break from the lop
                    if key == ord("x"):
                            break

            # cleanup the camera and close any open windows
            vs.stop() if args.get("video", None) is None else vs.release()
            cv2.destroyAllWindows()

def VCR_TECHDOT():
        print("IF YOU LIKE THE CONTENT THEN LIKE THE VIDEO")
        print("IF YOU'RE NOT SUBSCRIBED MY CHANNEL THEN WHY ARE YOU WAITING FOR?? \n JUST HIT THAT SUBSCRIBE BUTTON")
        print("IF YOU THINK THIS IS GOING TO BE HELPFUL TO ANYONE THEN SHARE WITH THEM.\n\n")

window = tk.Tk()
photo=PhotoImage(file="vcr_techdot.png")
canvas = tk.Canvas(window, height=500, width=700,bg='black')
canvas.pack()

window.title("Motion Detection Project Window") 
window.configure(background ='black') 
window.grid_rowconfigure(1, weight = 1) 
window.grid_columnconfigure(1, weight = 1)

message = tk.Label( window, text ="MOTION-DETECTION\n(Using OpenCV & Python)",
                    bg ="black", fg = "red", width = 20,  height = 1, font = ('arial', 30, 'bold'))        
message.place(relx = 0.5, rely = 0,relwidth=.9,relheight=.3, anchor='n')

frame = tk.Frame(window, bg='yellow', bd=10)
frame.place(relx=0.5, rely=0.32, relwidth=0.85, relheight=0.1, anchor='n')

message2 = tk.Label( frame, text ="Created by VCR TECHDOT",
                    bg='black', fg = "yellow", font = ('arial', 20, 'bold'))        
message2.place(relx = 0.5, rely = 0,relwidth=1,relheight=1, anchor='n')

lbl = tk.Label(window, text = "Input Video File",  
width = 20, height = 2, fg ="blue",  
bg = "yellow", font = ('Arial', 15, ' bold ') )  
lbl.place(relx=.15, rely = .5) 
  
txt = tk.Entry(window,  
width = 20, bg ="blue",  
fg ="red", font = ('Arial', 15, ' bold ')) 
txt.place(relx=.57, rely=.52)

testImg = tk.Button(window, text ="DETECT\nMOTION",  
command = detecting_motion, fg ="Red", bg ="violet",  
width = 15, height = 4, activebackground = "Red",  
font =('fixedsys', 14, ' bold ')) 
testImg.place(relx=.25, rely=.7)

TECHDOT = tk.Button(window,  command = VCR_TECHDOT, bg ="blue",  
image=photo,width=60,height=70, activebackground = "Red",) 
TECHDOT.place(relx=.88, rely=.83)

quitWindow = tk.Button(window, text ="QUIT",  
command = window.destroy, fg ="red", bg ="blue",  
width = 15, height = 4, activebackground = "Red",  
font =('fixedsys', 16, ' bold ')) 
quitWindow.place(relx=.6, rely=.7)
