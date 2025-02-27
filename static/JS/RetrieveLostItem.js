function handleRetrieveSuccess() {
    alert('取回失物成功！');
    window.location.href = 'Index.html';
}

function handleRetrieveFailure(error) {
    alert('取回失物失败：' + error);
}

function submitForm(event) {
    event.preventDefault();
    const form = event.target;
    const formData = new FormData(form);

    fetch('/retrieve_item', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.message === 'Item retrieved successfully') {
            handleRetrieveSuccess();
        } else {
            handleRetrieveFailure(data.message);
        }
    })
    .catch(error => handleRetrieveFailure(error.message));
}