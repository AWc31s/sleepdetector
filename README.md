# Sleep Detector
A flask web application that checks for closed eyes via the browser camera. Contains settings to both adjust the face detection threshold (e.g. if the app isn't detecting your face, you can turn it up) or sensitivity for closed eyes (how sensitive the app is to shut eyes, should be calibrated depending on the environment and lighting).

## Credits
Thanks to [Sarcovora](https://github.com/Sarcovora), [amritapasu](https://github.com/amritapasu), [caasib](https://github.com/caasib), and [elainejiangg](https://github.com/elainejiangg), for collaborating on the machine learning component of this project at MIT BeaverWorks.

## Server Side Python Dependencies
- numpy
- OpenCV
- Flask
- SocketIO
- Torchvision
- [facenet_models](https://github.com/CogWorksBWSI/facenet_models)

## Examples
![Eyes Open](https://user-images.githubusercontent.com/47835799/236577098-b164964a-6f23-45f7-96b8-45d90695db1e.png)
![Eyes Closed](https://user-images.githubusercontent.com/47835799/236577099-842ea20a-1763-4592-bdb2-6ebfafc72338.png)
![No face detected](https://user-images.githubusercontent.com/47835799/236577095-466a1702-f4a3-419b-8678-0cba02cb7171.png)

