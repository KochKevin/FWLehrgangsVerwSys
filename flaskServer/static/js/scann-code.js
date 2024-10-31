//HTML element to display the video stream
var videoElement;
//The actual stream fronm the Camera
var videoStream;


/*
Nach dem der Button für den Zugriff auf die Kamera gedrückt wurde.
Sollte er verschwinden oder nicht nochmal drückbar sein, dass nicht mehrere Streams entstehen.


Wenn auf Code einlösen geklickt wird und ein Code vorhanden ist, soll
der code an den server geschickt werden.
Genauso wenn er über den QR Code scanner gefunden wurden ist oder wenn er über die URL mitgesendet wird

*/



var canvas;
var canvasElement;

var outputMessage;

var hasURLCode;

document.addEventListener('DOMContentLoaded', function() {



    document.getElementById("activateQRCodeScanner").addEventListener("click", activateQRCodeScannerButton)
    document.getElementById("codeInputButton").addEventListener("click", clickCodeInputButton)
    document.getElementById("scannerRetry").addEventListener("click", clickScannerRetryButton)

    let currentUrl = new URL(window.location);
    if(currentUrl.searchParams.has("c")){

        hasURLCode = true;
        console.log("URL has code");
        code = currentUrl.searchParams.get("c");
        sendCode(code);

    }

});



function askingForCameraAccesses(){

    //Setup
    videoElement = document.getElementById("videoElement");
    canvasElement = document.getElementById("canvas");
    outputMessage = document.getElementById("outputMessage");


    videoElement.setAttribute("playsinline", true); // required to tell iOS safari we don't want fullscreen
    videoElement.setAttribute("autoplay", "");
    videoElement.setAttribute("muted", "");
    

    var facingMode = "environment";
    var constraints = {
        audio: false,
        video: {
            facingMode: facingMode,

        }
    };

    
    navigator.mediaDevices.getUserMedia(constraints).then(function success(stream) {
        videoStream = stream;
        videoElement.srcObject = videoStream;


        videoElement.onloadedmetadata = function() { 

            // Setze die Canvas-Größe basierend auf der Video-Größe
            canvasElement.width = videoElement.videoWidth;  // Setze die Breite des Canvas
            canvasElement.height = videoElement.videoHeight; // Setze die Höhe des Canvas

            // Hole den Kontext nach dem Setzen der Größe
            canvas = canvasElement.getContext("2d");

            console.log("Canvas Element Width: " + canvasElement.width + " Height: " + canvasElement.height);

            requestAnimationFrame(scanQR);

        };

    })
    .catch(function (error) {
        console.log("ERROR: ", error);
    });
    
}





function getCodeFromQRCode(qrCode){
    console.log(qrCode)
    let codeAsUrl = new URL(qrCode.data);
    code = codeAsUrl.searchParams.get("c")
    return code;
}


function activateQRCodeScannerButton(){

    document.getElementById("activateQRCodeScanner").style.display = "none";
    askingForCameraAccesses();

}



function drawLine(begin, end, color) {
    canvas.beginPath();
    canvas.moveTo(begin.x, begin.y);
    canvas.lineTo(end.x, end.y);
    canvas.lineWidth = 4;
    canvas.strokeStyle = color;
    canvas.stroke();
}



function scanQR() {
    let codeFound = false;

    if (videoElement.readyState === videoElement.HAVE_ENOUGH_DATA) {

        // Display Stream on Canvas
        canvas.drawImage(videoElement, 0, 0, canvasElement.width, canvasElement.height);

        var imageData = canvas.getImageData(0, 0, canvasElement.width, canvasElement.height);
        //Scann Code
        var qrCode = jsQR(imageData.data, imageData.width, imageData.height, {
            inversionAttempts: "dontInvert"
        });

        if (qrCode) {

            foundQRCode(qrCode);
            codeFound = true;



            // Stoppe die Kamera
            /*
            let tracks = videoStream.getTracks();
            tracks.forEach(track => track.stop());
            */

            qrCode = getCodeFromQRCode(qrCode)
            outputMessage.innerText = "Found Code: " + qrCode;
            
            document.getElementById("scannerRetry").style.display = "block"
            sendCode(qrCode)
        }
    }

    if (!codeFound) {
        requestAnimationFrame(scanQR);
    }
}


function foundQRCode(qrCode){
    //Hide video stream but show Canvas
    //videoElement.style.display = "none";
    canvasElement.style.display = "block";

    // Markiere den Code
    drawLine(qrCode.location.topLeftCorner, qrCode.location.topRightCorner, "#FF3B58");
    drawLine(qrCode.location.topRightCorner, qrCode.location.bottomRightCorner, "#FF3B58");
    drawLine(qrCode.location.bottomRightCorner, qrCode.location.bottomLeftCorner, "#FF3B58");
    drawLine(qrCode.location.bottomLeftCorner, qrCode.location.topLeftCorner, "#FF3B58");



}


function getCodeFromQRCode(qrCode){
    console.log(qrCode)
    let codeAsUrl = new URL(qrCode.data);
    code = codeAsUrl.searchParams.get("c")
    return code;
}


function activateQRCodeScannerButton(){

    document.getElementById("activateQRCodeScanner").style.display = "none";
    askingForCameraAccesses();

}

function clickCodeInputButton(){

    console.log("Clicked reedeem code input button");

    inputFieldValue = document.getElementById("codeInput").value;

    //If code has not 4 digits end 
    if(inputFieldValue.length != 4){

        document.getElementById("errorMessage").innerHTML = "Code ist invalide"
        return;
    }

    sendCode(inputFieldValue)

}

function clickScannerRetryButton(){

    videoElement.style.display = "block";
    canvasElement.style.display = "none";
    requestAnimationFrame(scanQR);
}


function endVideoStream(){
    let tracks = videoStream.getTracks();
    tracks.forEach(track => track.stop());
}

function sendCode(code){

    console.log("Sending Code: " + code);

    const jsonData = JSON.stringify({
        qualification_code : code 
    })


    fetch("/api/v1/check-for-code", {
        method: "POST",
        headers: {
            "Content-Type" : "application/json"
        },
        body: jsonData
    })
    .then(response => {

        if(response.ok){
            return response.json();
        }else{
            throw new Error("Network-Error");
        }

    })
    .then(data => {

        message = data.message;

        alert(message);

        window.location.href = "https://192.168.178.71:5000/dashboard";
        

    })
    .catch(error => {
        console.error("Error: ", error);
    })





}



function onToDashboard(){
    window.location.href = "/dashboard";
}