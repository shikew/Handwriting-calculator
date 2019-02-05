var wrapper = document.getElementById("signature-pad");
var clearButton = wrapper.querySelector("[data-action=clear]");
var changeColorButton = wrapper.querySelector("[data-action=change-color]");
var undoButton = wrapper.querySelector("[data-action=undo]");
var recognizeButton = wrapper.querySelector("[data-action=recognize]");
var savePNGButton = wrapper.querySelector("[data-action=save-png]");
var saveJPGButton = wrapper.querySelector("[data-action=save-jpg]");
var saveSVGButton = wrapper.querySelector("[data-action=save-svg]");
var canvas = wrapper.querySelector("canvas");
var numPreview = document.querySelector("#num-preview");
var signaturePad = new SignaturePad(canvas, {
    // It's Necessary to use an opaque color when saving image as JPEG;
    // this option can be omitted if only saving as PNG or SVG
    backgroundColor: 'rgb(255, 255, 255)'
});

// Adjust canvas coordinate space taking into account pixel ratio,
// to make it look crisp on mobile devices.
// This also causes canvas to be cleared.
function resizeCanvas() {
    // When zoomed out to less than 100%, for some very strange reason,
    // some browsers report devicePixelRatio as less than 1
    // and only part of the canvas is cleared then.
    var ratio = Math.max(window.devicePixelRatio || 1, 1);

    // This part causes the canvas to be cleared
    canvas.width = canvas.offsetWidth * ratio;
    canvas.height = canvas.offsetHeight * ratio;
    canvas.getContext("2d").scale(ratio, ratio);

    // This library does not listen for canvas changes, so after the canvas is automatically
    // cleared by the browser, SignaturePad#isEmpty might still return false, even though the
    // canvas looks empty, because the internal data of this library wasn't cleared. To make sure
    // that the state of this library is consistent with visual state of the canvas, you
    // have to clear it manually.
    signaturePad.clear();
}

// On mobile devices it might make more sense to listen to orientation change,
// rather than window resize events.
window.onresize = resizeCanvas;
resizeCanvas();

function download(dataURL, filename) {
    if (navigator.userAgent.indexOf("Safari") > -1 && navigator.userAgent.indexOf("Chrome") === -1) {
        window.open(dataURL);
    } else {
        var blob = dataURLToBlob(dataURL);
        var url = window.URL.createObjectURL(blob);

        var a = document.createElement("a");
        a.style = "display: none";
        a.href = url;
        a.download = filename;

        document.body.appendChild(a);
        a.click();

        window.URL.revokeObjectURL(url);
    }
}

// One could simply use Canvas#toBlob method instead, but it's just to show
// that it can be done using result of SignaturePad#toDataURL.
function dataURLToBlob(dataURL) {
    // Code taken from https://github.com/ebidel/filer.js
    var parts = dataURL.split(';base64,');
    var contentType = parts[0].split(":")[1];
    var raw = window.atob(parts[1]);
    var rawLength = raw.length;
    var uInt8Array = new Uint8Array(rawLength);

    for (var i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }

    return new Blob([uInt8Array], {type: contentType});
}

function img2text(b64img) {

    var formData = new FormData();
    //var blob = dataURItoBlob(b64img);

    formData.append("predictImg", dataURLToBlob(b64img));

    var request = new XMLHttpRequest();


    request.onreadystatechange = function () {
        if (request.readyState == 4) {
            if ((request.status >= 200 && request.status < 300) || request.status == 304) {
                console.log(request.response)
                document.querySelector('#mnist-pad-result').innerHTML = request.response;
            }
            ;
        }
    };

    request.open("POST", "./recognize");
    request.send(formData);
};

clearButton.addEventListener("click", function (event) {
    signaturePad.clear();
}, false);

undoButton.addEventListener("click", function (event) {
    var data = signaturePad.toData();

    if (data) {
        data.pop(); // remove the last dot or line
        signaturePad.fromData(data);
    }
});

changeColorButton.addEventListener("click", function (event) {
    var r = Math.round(Math.random() * 255);
    var g = Math.round(Math.random() * 255);
    var b = Math.round(Math.random() * 255);
    var color = "rgb(" + r + "," + g + "," + b + ")";

    signaturePad.penColor = color;
});

savePNGButton.addEventListener("click", function (event) {
    if (signaturePad.isEmpty()) {
        alert("Please provide a signature first.");
    } else {
        var dataURL = signaturePad.toDataURL();
        download(dataURL, "signature.png");
    }
});

saveJPGButton.addEventListener("click", function (event) {
    if (signaturePad.isEmpty()) {
        alert("Please provide a signature first.");
    } else {
        var dataURL = signaturePad.toDataURL("image/jpeg");
        //img2text(dataURL);
        download(dataURL, "signature.jpg");
    }
});

saveSVGButton.addEventListener("click", function (event) {
    if (signaturePad.isEmpty()) {
        alert("Please provide a signature first.");
    } else {
        var dataURL = signaturePad.toDataURL('image/svg+xml');
        download(dataURL, "signature.svg");
    }
});

recognizeButton.addEventListener("click", function (event) {
    if (signaturePad.isEmpty()) {
        alert("Please provide a signature first.");
    } else {
        let box = document.getElementById("box")
        let context2d = box.getContext("2d");
        let imgData = context2d.getImageData(0, 0, canvas.width, canvas.height).data;


        let numPreviewContext2d = numPreview.getContext("2d");
        numPreviewContext2d.fillStyle = "#ffffff";
        numPreviewContext2d.fillRect(0, 0, 20, 20);
        numPreviewContext2d.drawImage(canvas, 0, 0, 20, 20);

        let photoData = numPreviewContext2d.getImageData(0, 0, 20, 20);
        let photoDataArray = [];
        for (let i = 0; i < photoData.data.length; i += 4) {
            let r = photoData.data[i];
            let g = photoData.data[i + 1];
            let b = photoData.data[i + 2];
            let color = Math.round((r + g + b) / 3);
            photoDataArray.push(color);
        }

       // $.post("/recognize", {photo_data: JSON.stringify(photoDataArray)}).done(result => {
         //   $("#result").html(`识别结果：${result}`);
       // });

        $.post("/result", {"img_data": imgData.toLocaleString()}, function (result) {
            $("#result").html(result);
        });

    }


});