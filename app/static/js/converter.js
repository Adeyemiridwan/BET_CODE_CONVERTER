
// =====================================================
// ================= FORM CONTROL ======================
// =====================================================

const form = document.getElementById("convertForm");

const btn = document.getElementById("convertBtn");

if(form){

form.addEventListener("submit", function(e){

e.preventDefault();

document.getElementById("loadingOverlay").style.display = "flex";

btn.style.opacity = "0.7";

setTimeout(() => {
form.submit();
}, 1500);

});

}


// =====================================================
// ================= COPY RESULT =======================
// =====================================================

document.addEventListener("click", function(e){

const resultBox =
document.getElementById("convertedCode");

if(
resultBox &&
(
e.target.id === "convertedCode" ||
resultBox.contains(e.target)
)
){

navigator.clipboard.writeText(
resultBox.innerText.trim()
);

let toast = new bootstrap.Toast(
document.getElementById("liveToast")
);

toast.show();

}

});


// =====================================================
// ================= SWITCH ROTATE =====================
// =====================================================

const switchBtn =
document.getElementById("switchBtn");

if(switchBtn){

switchBtn.addEventListener("click", function(){

this.classList.toggle("rotated");

});

}