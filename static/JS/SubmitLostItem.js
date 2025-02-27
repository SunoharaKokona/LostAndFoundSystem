document.getElementById('captureButton').addEventListener('click', function() {
    const video = document.getElementById('video');
    const canvas = document.getElementById('canvas');
    const context = canvas.getContext('2d');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const dataURL = canvas.toDataURL('image/png');
    document.getElementById('previewImage').src = dataURL;
    const itemPhotoInput = document.getElementById('itemPhoto');
    const blob = dataURLToBlob(dataURL);
    const file = new File([blob], 'captured_image.png', { type: 'image/png' });
    const container = new DataTransfer();
    container.items.add(file);
    itemPhotoInput.files = container.files;
});

function dataURLToBlob(dataURL) {
    const parts = dataURL.split(';base64,');
    const contentType = parts[0].split(':')[1];
    const raw = window.atob(parts[1]);
    const rawLength = raw.length;
    const uInt8Array = new Uint8Array(rawLength);
    for (let i = 0; i < rawLength; ++i) {
        uInt8Array[i] = raw.charCodeAt(i);
    }
    return new Blob([uInt8Array], { type: contentType });
}

document.getElementById('lostItemForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    fetch('/submit_lost_item', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        alert('失物信息已提交');
        console.log(data);
        window.location.href = 'Index.html'; 
    })
    .catch(error => {
        console.error('Error:', error);
    });
});