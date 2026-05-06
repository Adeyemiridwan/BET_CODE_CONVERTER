/* ================= VERIFY_CODE PAGE INTRACTION ================= */

/* AUTO FOCUS */
document.getElementById("codeInput").focus();

/* BUTTON LOADING */
const form = document.getElementById("verifyForm");
const btn = document.getElementById("verifyBtn");

form.addEventListener("submit", function(){

btn.classList.add("loading");

});

/* TIMER SYSTEM */
let time = 30;

const timerText = document.getElementById("timerText");
const resendBtn = document.getElementById("resendBtn");

let interval = setInterval(updateTimer,1000);

function updateTimer(){

time--;

timerText.innerText = "Resend in " + time + "s";

if(time <= 0){

clearInterval(interval);

timerText.innerText = "You can resend now";

resendBtn.disabled = false;

}

}

/* START DISABLED */
resendBtn.disabled = true;

/* RESEND ACTION */
resendBtn.addEventListener("click", async function(){

resendBtn.disabled = true;

timerText.innerText = "Sending new code...";

try{

const res = await fetch("/auth/resend-code");
const data = await res.json();

if(data.success){

timerText.innerText = data.message;

}else{

timerText.innerText = "Failed to resend code";

}

setTimeout(()=>{

time = 30;

timerText.innerText = "Resend in 30s";

interval = setInterval(updateTimer,1000);

},1500);

}catch(err){

timerText.innerText = "Failed to resend code";

resendBtn.disabled = false;

}

});