import cv2
import time
import boto3
import base64

sns = boto3.client('sns')
rekognition = boto3.client("rekognition")

cap = cv2.VideoCapture(0)
img_name = "Saved_Images/opencv_frame.jpeg"


def recognitionMethod(image):

    response = rekognition.detect_faces(
        Image={
            'Bytes':
                image
        })
    return response

def takeImage():

    ret, image = cap.read()
    success, encoded_image = cv2.imencode('.jpeg', image)
    # Save image to computer
    cv2.imwrite(img_name, image)
    return encoded_image.tobytes()


def sendImageToRek(image):

    response = recognitionMethod(image)
    return response

def checkImage(rekResponse):
    if len(rekResponse['FaceDetails']) > 0:
        msg = f"There is someone in your room! (amount: {len(rekResponse['FaceDetails'])})"
        print(msg)
        sendAlert(msg)
        return True
    else:
        print("All Clear")
        return False

def sendAlert(msg):

    sns.publish(
        TopicArn='arn:aws:sns:eu-west-1:269108739647:GetOut',
        Message= msg,
    )

while True:

    time.sleep(1)
    img = takeImage()
    rekResp = sendImageToRek(img)
    if checkImage(rekResp):
        break

cap.release()

'''
ToDo:
Detect Someone in the room: Done
Detect Who is in the room: X
Send message to sulprit: X
Send me link of image to show person in room via text (S3 Link): X 
'''