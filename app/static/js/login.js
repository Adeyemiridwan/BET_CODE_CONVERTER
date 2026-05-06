/* ================= LOGIN PAGE INTRACTION ================= */

/* TOGGLE PASSWORD */
function togglePassword(id, btn){

const input = document.getElementById(id);
const icon = btn.querySelector("i");

if(input.type === "password"){
input.type = "text";
icon.classList.replace("fa-eye","fa-eye-slash");
}else{
input.type = "password";
icon.classList.replace("fa-eye-slash","fa-eye");
}

}

/* BUTTON LOADING */
const form = document.querySelector("form");
const btn = document.getElementById("loginBtn");

form.addEventListener("submit", function(){
btn.classList.add("btn-loading");
});