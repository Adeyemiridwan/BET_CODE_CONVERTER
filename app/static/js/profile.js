
const imageInputTop = document.getElementById("imageInput");
const imageInputBottom = document.getElementById("imageInputBottom");

const fileName = document.getElementById("fileName");

const profilePreview = document.getElementById("profilePreview");

function previewImage(file){

    if(file){

        const reader = new FileReader();

        reader.onload = function(e){

            profilePreview.src = e.target.result;

        }

        reader.readAsDataURL(file);

        fileName.innerText = file.name;

    }

}

imageInputTop.addEventListener("change", function(){

    previewImage(this.files[0]);

});

imageInputBottom.addEventListener("change", function(){

    previewImage(this.files[0]);

});