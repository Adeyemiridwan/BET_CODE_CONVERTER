/* ================= SIGNUP PAGE INTRACTION ================= */

/* ================= TOGGLE PASSWORD ================= */

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

/* ================= PASSWORD STRENGTH ================= */

const password = document.getElementById("password");

const strengthText =
document.getElementById("passwordStrength");

const strengthFill =
document.getElementById("strengthFill");

password.addEventListener("input", function(){

let value = password.value;

if(value.length < 4){

strengthText.innerText = "Weak password";
strengthText.style.color = "#ef4444";

strengthFill.style.width = "30%";
strengthFill.style.background = "#ef4444";

}
else if(value.length < 8){

strengthText.innerText = "Medium password";
strengthText.style.color = "#f59e0b";

strengthFill.style.width = "65%";
strengthFill.style.background = "#f59e0b";

}
else{

strengthText.innerText = "Strong password";
strengthText.style.color = "#22c55e";

strengthFill.style.width = "100%";
strengthFill.style.background = "#22c55e";

}

});

/* ================= CONFIRM PASSWORD ================= */

const confirmPassword =
document.getElementById("confirm_password");

const matchMessage =
document.getElementById("matchMessage");

function validatePassword(){

if(confirmPassword.value === ""){
matchMessage.innerText = "";
return;
}

if(password.value !== confirmPassword.value){

matchMessage.innerText = "Passwords do not match";
matchMessage.style.color = "#ef4444";

confirmPassword.style.borderColor = "#ef4444";

}else{

matchMessage.innerText = "Passwords matched";
matchMessage.style.color = "#22c55e";

confirmPassword.style.borderColor = "#22c55e";

}

}

password.addEventListener("input", validatePassword);
confirmPassword.addEventListener("input", validatePassword);