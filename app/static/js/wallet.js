/* ===================================================== */
/* ================= TAB SWITCH ======================== */
/* ===================================================== */

function switchWalletTab(tab){

const forms = document.querySelectorAll(".wallet-form");

forms.forEach(form => {
form.classList.remove("active");
});

document
.getElementById(tab + "Form")
.classList.add("active");


const buttons = document.querySelectorAll(".action-btn");

buttons.forEach(btn => {
btn.classList.remove("active");
});

document
.getElementById("btn-" + tab)
.classList.add("active");

}


/* ===================================================== */
/* ================= QUICK AMOUNTS ===================== */
/* ===================================================== */

function setAmount(value){

const input = document.getElementById("depositAmount");

input.value = value;

updateSummary();

}


/* ===================================================== */
/* ================= SUMMARY =========================== */
/* ===================================================== */

function updateSummary(){

const input =
document.getElementById("depositAmount");

const amount =
parseFloat(input.value) || 0;

document.getElementById("summaryAmount").innerText =
"$" + amount.toFixed(2);

document.getElementById("summaryTotal").innerText =
"$" + amount.toFixed(2);

}


/* ===================================================== */
/* ================= INPUT LISTENER ==================== */
/* ===================================================== */

document.addEventListener("input", function(e){

if(e.target.id === "depositAmount"){
updateSummary();
}

});

