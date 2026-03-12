// ============================================================
//  script.js — Device Fingerprint Access Control
//    ضع بصمة جهازك في ALLOWED_FINGERPRINT
// ============================================================

const ALLOWED_FINGERPRINT = "96159b5bdf00721e1e6f779d0651598a";

// ── UI ──────────────────────────────────────────────────────

function showDenied(fp) {
  document.getElementById("loading-screen").classList.add("hidden");
  document.getElementById("denied-screen").classList.remove("hidden");
  document.getElementById("visitor-fp").textContent = "ID: " + fp;
}

function showContent(fp) {
  document.getElementById("loading-screen").classList.add("hidden");
  document.getElementById("main-content").classList.remove("hidden");
  document.getElementById("allowed-fp").textContent = "ID: " + fp;
}

// ── Check ────────────────────────────────────────────────────

async function initCheck() {
  try {
    const fp     = await FingerprintJS.load();
    const result = await fp.get();
    const visitorId = result.visitorId;

    console.log("Fingerprint:", visitorId);

    visitorId === ALLOWED_FINGERPRINT
      ? showContent(visitorId)
      : showDenied(visitorId);

  } catch (err) {
    console.error(err);
    showDenied("تعذّر التحقق");
  }
}
