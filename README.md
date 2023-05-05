# Sleep Detector
A flask web application that checks for closed eyes via the browser camera and image processing with machine learning in the Python server backend. The result is then updated live on the frontend webpage with colors and text.

Contains settings to adjust both the face detection threshold (e.g. if the app isn't detecting your face, you can turn it up) or sensitivity for closed eyes (i.e. how sensitive the app is to shut eyes, should be calibrated depending on the environment and lighting).

Run the main.py file to start the flask server locally.

## Credits
Thanks to [Sarcovora](https://github.com/Sarcovora), [amritapasu](https://github.com/amritapasu), [caasib](https://github.com/caasib), and [elainejiangg](https://github.com/elainejiangg), for collaborating on the machine learning component of this project at MIT BeaverWorks. The original project is [here](https://github.com/Sarcovora/CogWorks-2022-Gausslien-Final-Capstone).

## Server Side Python Dependencies
- numpy
- OpenCV
- Flask
- SocketIO
- Torchvision
- [facenet_models](https://github.com/CogWorksBWSI/facenet_models)

## Client Side
- Uses jQuery and SocketIO

## Examples
![Eyes Open](https://user-images.githubusercontent.com/47835799/236577098-b164964a-6f23-45f7-96b8-45d90695db1e.png)
![Eyes Closed](https://user-images.githubusercontent.com/47835799/236577099-842ea20a-1763-4592-bdb2-6ebfafc72338.png)
![No face detected](https://user-images.githubusercontent.com/47835799/236577095-466a1702-f4a3-419b-8678-0cba02cb7171.png)

