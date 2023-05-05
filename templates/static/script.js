// Connect to server socket
var socket = io.connect(window.location.protocol + '//' + document.domain + ':' + location.port);

// Set up video/canvas elements with selectors
var canvas = document.getElementById('canvas');
var context = canvas.getContext('2d');
const video = document.querySelector("#videoElement");

// Sensitivity sliders
var eyeSlider = document.getElementById('eyeRange');
var faceSlider = document.getElementById('faceRange');

eyeSlider.oninput = function() {
    v = this.value/50;
    socket.emit('eyeSenseUpdate', v);
    $("#sensitivitylabel1").text(v)
}
faceSlider.oninput = function() {
    v = 90 + this.value/10;
    socket.emit('faceSenseUpdate', v);
    $("#sensitivitylabel2").text(v);
}

video.width = 400;
video.height = 300;

// Wait for user permission to use camera
if (navigator.mediaDevices.getUserMedia) {

    // Promise video stream object
    navigator.mediaDevices.getUserMedia({
        video: true
    })
        .then(function (stream) {
            video.srcObject = stream;
            video.play();
        })
        .catch(function (oops) {

        });
}

// Draw image onto canvas and send image data to python backend at defined fps
const fps = 0.5;
let data = canvas.toDataURL('image/jpeg', 0.5)
setInterval(() => {
    width = video.width;
    height = video.height;
    context.drawImage(video, 0, 0, width, height);
    data = canvas.toDataURL('image/jpeg', 0.5);
    context.clearRect(0, 0, width, height);
    socket.emit('frame', data);
}, 1000 / fps);

// Handle the response from the python backend
socket.on('update', function (status) {
    if(status===-1) {
        $("#container").css("background-color","yellow");
        $("#textupdate").text("FACE NOT FOUND");
    } else if(status===1) {
        $("#container").css("background-color","red");
        $("#textupdate").text("EYES CLOSED")
    } else {
        $("#container").css("background-color","lightblue");
        $("#textupdate").text("EYES OPEN");
    }
    
})