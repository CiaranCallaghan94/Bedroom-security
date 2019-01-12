import cv2
import time
import boto3
import base64

sns = boto3.client('sns')
rekognition = boto3.client("rekognition")

cap = cv2.VideoCapture(0)
img_name = "Saved_Images/opencv_frame.jpeg"

know_faces = {
    ""
}

def takeImage():

    ret, image = cap.read()
    success, encoded_image = cv2.imencode('.jpeg', image)
    # Save image to computer
    cv2.imwrite(img_name, image)
    return encoded_image.tobytes()


def recognitionMethodDetectFaces(image):

    response = rekognition.detect_faces(
        Image={
            'Bytes':
                image
        })
    print(response)
    faces_detected = len(response['FaceDetails'])
    return faces_detected

def recognitionFaceInCollection(image):

    person_found = None

    response = rekognition.search_faces_by_image(
        CollectionId='GetOutOfMyRoom',
        Image={
            'Bytes': image
        }
    )

    if  len(response['FaceMatches']):
        person_found = response['FaceMatches'][0]['Face']['ExternalImageId']
    return person_found

'''
Method: Takes in how many people are detected in image and if the person is recognised.
        Sends Ciaran an alert message depending on passed values.
'''
def alertCiaran(detected_faces, person_detected):
    if detected_faces > 0:
        if detected_faces == 1:
            msg = "There is someone in your room!"
        else:
            msg = f"There are {detected_faces} people in your room!"

        if person_detected != None:

            if person_detected == "ciaran":
                msg = msg + f" Looks like you!"
            else:
                msg = msg + f" Looks like {person_detected.capitalize()}!"

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

def detectPeopleInRoom(image):
    '''
    pass an image to detect faces....
    If face detected, check to see if face is in collection.
    Send message to subscribers.
    '''
    person_detected = None
    faces_detected = recognitionMethodDetectFaces(image)
    if faces_detected > 0: person_detected = recognitionFaceInCollection(image)

    alertCiaran(faces_detected,person_detected)


while True:

    time.sleep(1)
    img = takeImage()
    detectPeopleInRoom(img)
    break

cap.release()

'''
ToDo:
Detect Someone in the room: Done
Detect Who is in the room: X
Send message to sulprit: X
Send me link of image to show person in room via text (S3 Link): X 
'''