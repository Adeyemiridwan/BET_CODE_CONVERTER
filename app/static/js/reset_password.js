/* ================= RESET_PASSWORD PAGE INTRACTION ================= */

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

/* PASSWORD STRENGTH */
const password = document.getElementById("password");
const strengthText = document.getElementById("strengthText");

const bars = [
document.getElementById("bar1"),
document.getElementById("bar2"),
document.getElementById("bar3"),
document.getElementById("bar4")
];

password.addEventListener("input", function(){

const val = password.value;

bars.forEach(bar => {
bar.style.background = "#e5e7eb";
});

if(val.length < 4){

bars[0].style.background = "#ef4444";
strengthText.innerText = "Weak password";
strengthText.style.color = "#ef4444";

}
else if(val.length < 8){

bars[0].style.background = "#f59e0b";
bars[1].style.background = "#f59e0b";

strengthText.innerText = "Medium password";
strengthText.style.color = "#f59e0b";

}
else if(val.length < 12){

bars[0].style.background = "#3b82f6";
bars[1].style.background = "#3b82f6";
bars[2].style.background = "#3b82f6";

strengthText.innerText = "Strong password";
strengthText.style.color = "#3b82f6";

}
else{

bars.forEach(bar => {
bar.style.background = "#22c55e";
});

strengthText.innerText = "Very strong password";
strengthText.style.color = "#22c55e";

}

});

/* MATCH CHECK */
const confirmPassword = document.getElementById("confirm_password");
const matchText = document.getElementById("matchText");
const confirmWrapper = document.getElementById("confirmWrapper");

function checkMatch(){

if(confirmPassword.value === ""){
matchText.innerText = "Password confirmation required";
matchText.style.color = "var(--muted)";
confirmWrapper.style.borderColor = "var(--border)";
return;
}

if(password.value !== confirmPassword.value){

matchText.innerText = "Passwords do not match";
matchText.style.color = "#ef4444";
confirmWrapper.style.borderColor = "#ef4444";

}else{

matchText.innerText = "Passwords match successfully";
matchText.style.color = "#22c55e";
confirmWrapper.style.borderColor = "#22c55e";

}

}

password.addEventListener("input", checkMatch);
confirmPassword.addEventListener("input", checkMatch);

/* BUTTON LOADING */
const form = document.querySelector("form");
const btn = document.getElementById("updateBtn");

form.addEventListener("submit", function(){

btn.classList.add("btn-loading");

});