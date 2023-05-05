"""
Supporting functions for Sleep Detector project
"""

# Libraries
import numpy as np
from facenet_models import FacenetModel
import cv2

def find_eyes(image_data, box_threshold, *, prop_const=0.13):
    """
    Gets box coordinates around eyes in the image

    Parameters
    ----------
    image_data : numpy.ndarray, shape-(R, C, 3) (RGB is the last dimension)
        Pixel information for the image.
    box_threshold : float
        The confidence the model must have that a given section of the image is a face
    prop_const : float
        Sets the size of generated eye box proportional to the entire face

    Returns
    ----------
    leftBox : coordinates describing the box around the left eye
    rightBox : coordinates describing the box around the right eye
    image_data

    """
    i = 0
    leftBox = []
    rightBox = []
    model = FacenetModel()
    
    # The model doeesn't do well with rotated faces, so this checks for all possible rotations    
    while i < 4:
        boxes, probabilities, landmarks = model.detect(image_data)
        face_detected = True

        if boxes is None or probabilities[0]<box_threshold:
            i+=1
            image_data = cv2.rotate(image_data, cv2.ROTATE_90_CLOCKWISE)
            continue
        
        box = boxes[0]
        prob = probabilities[0]
        
        lefteye = landmarks[0][0]
        righteye = landmarks[0][1]

        # boxes in form [left,top,right,bottom]
        radius = ((box[3] - box[1]) + (box[2] - box[0]))/2 * prop_const

        leftBox = np.array([lefteye[0] - radius, 
                            lefteye[1] - radius, 
                            lefteye[0] + radius,
                            lefteye[1] + radius])
        rightBox = np.array([righteye[0] - radius, 
                            righteye[1] - radius, 
                            righteye[0] + radius,
                            righteye[1] + radius])

        leftBox = np.round(np.array(leftBox)).astype(int)
        rightBox = np.round(np.array(rightBox)).astype(int)
        
        break
    
    return leftBox, rightBox, image_data

def eye_img(pic, box_threshold=0.97):
    """
    Gets the image ready to be fed into the machine learning model

    Parameters
    ----------
    pic : numpy.ndarray, shape-(R, C, 3) (RGB is the last dimension)
        Pixel information for the image.

    Returns
    ----------
    lefteye : a 24x24 grayscale image of the left eye
    righteye : a 24x24 grayscale image of the right eye

    """

    # Makes sure image is rgb and not rgba
    if pic.shape[-1] == 4:
        pic = pic[..., :-1]

    left, right, pic = find_eyes(pic, box_threshold)

    if len(left)==0:
        return None

    # convert to grayscale
    gray = cv2.cvtColor(pic, cv2.COLOR_RGB2GRAY)
    
    # boxes in form [left,top,right,bottom]
    lefteye = gray[left[1]:left[3], left[0]:left[2]]
    righteye = gray[right[1]:right[3], right[0]:right[2]]
    
    # resize to fit model
    lefteye = cv2.resize(lefteye, (24,24), interpolation = cv2.INTER_LINEAR)
    righteye = cv2.resize(righteye, (24,24), interpolation = cv2.INTER_LINEAR)
    
    return lefteye, righteye
