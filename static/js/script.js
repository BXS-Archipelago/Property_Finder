document.addEventListener("click", function (e){
    if(e.target.classList.contains("gallery-item")){

        const src = e.target.getAttribute("src");
        document.querySelectorAll("modal-img").src = src;
        var myModal = new bootstrap.Modal(document.getElementById("gallery-modal"));
        myModal.show();
    }
})
   
