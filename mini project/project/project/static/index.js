// Access the webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then(function (stream) {
        var video = document.getElementById('video');
        video.srcObject = stream;
        video.play();
    })
    .catch(function (error) {
        console.error('Error accessing webcam:', error);
        alert('Camera access is denied or not working!');
    });

// Change clothes overlay
function changeClothes(clothesImage) {
    var clothesOverlay = document.getElementById('clothes-overlay');
    clothesOverlay.src = `/static/${clothesImage}`;
}
