// ============================================================
//  script.js — IP Access Control
//  الجهاز المصرّح به: 37.236.1.125
// ============================================================

const ALLOWED_IP = "37.236.1.125";

// ── UI ──────────────────────────────────────────────────────

function showDenied(ip) {
  document.getElementById("loading-screen").classList.add("hidden");
  document.getElementById("denied-screen").classList.remove("hidden");
  document.getElementById("visitor-ip").textContent = "IP: " + ip;
}

function showContent(ip) {
  document.getElementById("loading-screen").classList.add("hidden");
  document.getElementById("main-content").classList.remove("hidden");
  document.getElementById("allowed-ip").textContent = "IP: " + ip;
}

// ── Check ────────────────────────────────────────────────────

async function checkAccess() {
  try {
    const res  = await fetch("https://api.ipify.org?format=json");
    const data = await res.json();
    const ip   = data.ip;

    console.log("IP الزائر:", ip);
    ip === ALLOWED_IP ? showContent(ip) : showDenied(ip);

  } catch (err) {
    console.error(err);
    showDenied("تعذّر التحقق");
  }
}

document.addEventListener("DOMContentLoaded", checkAccess);
