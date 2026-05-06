

/* ================= SIDEBAR ================= */

const sidebar = document.getElementById("sidebar");
const toggleBtn = document.getElementById("toggleBtn");

/* ================= SIDEBAR TOGGLE ================= */

if(toggleBtn){

toggleBtn.addEventListener("click", function(e){

e.stopPropagation();

sidebar.classList.toggle("collapsed");

/* SAVE STATE */

localStorage.setItem(
"sidebarCollapsed",
sidebar.classList.contains("collapsed")
);

});

}

/* ================= LOAD SAVED STATE ================= */

if(localStorage.getItem("sidebarCollapsed") === "true"){

sidebar.classList.add("collapsed");

}

/* ================= PREVENT AUTO EXPAND ================= */

document.querySelectorAll(".sidebar-link").forEach(link => {

link.addEventListener("click", function(e){

/* Sidebar stays collapsed */
e.stopPropagation();

});

});

/* ================= THEME ================= */

function toggleTheme(){

document.body.classList.toggle("dark");

localStorage.setItem(
"theme",
document.body.classList.contains("dark")
);

}

/* LOAD SAVED THEME */

if(localStorage.getItem("theme") === "true"){

document.body.classList.add("dark");

}

/* ================= LOADER ================= */

function showLoader(){

document.getElementById("loader")
.style.display = "flex";

}

/* AUTO LOADER */

document.querySelectorAll("form").forEach(form => {

form.addEventListener("submit", () => {

showLoader();

});

});


/* ================= AUTO CLOSE FLASH ================= */

document.querySelectorAll(".flash-message").forEach(flash => {

const closeBtn = flash.querySelector(".flash-close");

/* AUTO REMOVE */

setTimeout(() => {

flash.classList.add("flash-hide");

setTimeout(() => {

flash.remove();

},300);

},5000);

/* MANUAL CLOSE */

closeBtn.addEventListener("click", () => {

flash.classList.add("flash-hide");

setTimeout(() => {

flash.remove();

},300);

});

});
