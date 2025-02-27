function retrieveItem(itemId) {
    window.location.href = `/RetrieveItem.html?item_id=${itemId}`;
}
        // 自动填写日期为本日日期
        document.getElementById('storageDate').value = new Date().toISOString().split('T')[0];

        // 图片放大查看功能
        var modal = document.getElementById("myModal");
        var modalImg = document.getElementById("img01");
        var span = document.getElementsByClassName("close")[0];

        function openModal(src) {
            modal.style.display = "block";
            modalImg.src = src;
        }

        span.onclick = function() { 
            modal.style.display = "none";
        }

        window.onclick = function(event) {
            if (event.target == modal) {
                modal.style.display = "none";
            }
        }