// ============================================================
//  script.js — Device Fingerprint Access Control
// ============================================================

const ALLOWED_FINGERPRINTS = [
  "96159b5bdf00721e1e6f779d0651598a",  // الجهاز الأول
  "56df8ab1b1825ff4c0d563395951de85",  // الجهاز الثاني
];

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
    const fp      = await FingerprintJS.load();
    const result  = await fp.get();
    const visitorId = result.visitorId;

    console.log("Fingerprint:", visitorId);

    ALLOWED_FINGERPRINTS.includes(visitorId)
      ? showContent(visitorId)
      : showDenied(visitorId);

  } catch (err) {
    console.error(err);
    showDenied("تعذّر التحقق");
  }
}
