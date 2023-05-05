"""
Flask Web Application for Sleep Detector project
"""

# Turn off request logging
import logging
log = logging.getLogger('werkzeug')
log.disabled = True

# Built in
import base64
import os

# Libraries
import cv2
import numpy as np
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import torch

# My modules
from eye_img import eye_img

__author__ = 'Alan Wang'
__version__ = '1.0.0'
__email__ = 'alan.wang1618@gmail.com'

# Set up global variables
app = Flask(__name__, static_folder="./templates/static")
app.config["SECRET_KEY"] = os.urandom(12)
socketio = SocketIO(app)
model = torch.load("model.pb", map_location=torch.device('cpu'))

# Sensitivity variables
face_sensitivity = 0.97
eye_sensitivity = 0

def base64_to_image(base64_string):
    """
    Converts base64 encoded strings to image data

    Parameters
    ----------
    base64_string : string
        The base64 string to be decoded

    Returns
    -------
    Image array
    
    """

    base64_data = base64_string.split(",")[1]
    image_bytes = base64.b64decode(base64_data)
    image_array = np.frombuffer(image_bytes, dtype=np.uint8)
    image = cv2.imdecode(image_array, cv2.IMREAD_COLOR)
    return image



@socketio.on("eyeSenseUpdate")
def update_eye_senstivity(value):
    eye_sensitivity = int(value)
@socketio.on("faceSenseUpdate")
def update_face_sensitivity(value):
    face_sensitivity = int(value)

@socketio.on("frame")
def receive_image(image):
    """
    Processes the image whenever one is received from client

    Parameters
    ----------
    image : str
        Base64 image data

    Returns
    -------
    Image array
    
    """

    # Decode the base64-encoded image data
    image = base64_to_image(image)

    lr = eye_img(image, face_sensitivity)
    if lr:
        left, right = lr
    else:
        emit("update", -1)
        return

    # Standardize the images so that they can be fed into the model
    left = torch.tensor(left).reshape(1,1,24,24).float()/255
    right = torch.tensor(right).reshape(1,1,24,24).float()/255

    leftscore = model(left)[0][0].item() - model(left)[0][1].item()
    rightscore = model(right)[0][0].item() - model(right)[0][1].item()

    # 0 (eyes open) or 1 (eyes closed) integer value
    eyes_closed = int(leftscore>eye_sensitivity and rightscore>eye_sensitivity)

    emit("update", eyes_closed)

    return


@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, debug=True, port=5000, host='0.0.0.0')