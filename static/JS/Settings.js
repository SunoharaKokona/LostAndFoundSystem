function showImage(src) {
    var preview = document.getElementById('imagePreview');
    var img = preview.querySelector('img');
    img.src = src;
    preview.style.display = 'flex';
}

function hideImage() {
    var preview = document.getElementById('imagePreview');
    preview.style.display = 'none';
}

function deleteItem(button) {
    var row = button.parentNode.parentNode;
    var itemId = row.cells[0].innerText;  

    if (confirm('确定要删除此物品信息吗？')) {
        fetch('/delete_item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: 'item_id=' + encodeURIComponent(itemId),
        })
        .then(response => response.json())
        .then(data => {
            if (data.message === 'Item deleted successfully') {
                row.parentNode.removeChild(row);
                alert('成功移除物品信息');
            } else {
                alert('Failed to delete item');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}