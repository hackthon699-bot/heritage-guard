/**
 * Heritage-Guard v4.2 | Render Cloud Edition: spotlight_shield.js (v4.2)
 * - Runs TensorFlow.js COCO-SSD phone detection + privacy-shutter liveness directly in Chrome
 * - Zero camera frames ever leave the user's device (keeps Render RAM under ~140 MB)
 * - Homepage camera starts OFF until clicked (zero unwanted popups)
 * - Weaver Studio PIN Unlock bar protects /api/protect while Verifier & Audit stay public
 * - Muted pakda_gaya_meme.mp4 plays smoothly on lockout with automatic emoji fallback
 */

const STATUTORY_PLAIN_TEXT =
  "⚠️ STATUTORY LEGAL WARNING: Unauthorised copying or commercial reproduction of textile designs may constitute Intellectual Property Theft, punishable under Sections 51 and 63 of the Copyright Act, 1957, Section 22 of the Designs Act, 2000, and Section 39 of the GI Act, 1999. Legal action may result in imprisonment, fines and damages.";

const I18N_DICT = {
  en: {
    title: 'Heritage Guard <span class="gold-version">v4.2</span>',
    catalogHeading: "B2B BUYER INSPECTION GATE — Interactive Spotlight & Optical Shield",
    catalogHelp:
      "Hover inside the protected viewport to inspect intricate Zari and Ikat weave geometry through the 95px Spotlight Aperture. Right-clicking, copying, dragging, capturing the screen, or raising a phone triggers an instant 0ms PAKDA GAYA! statutory lockout.",
    uploadHeading: "🛡️ ARTISAN COOPERATIVE STUDIO — Zero-Retention RAM Cloak",
    verifyHeading: "🔎 FORENSIC 3-ZONE LSB & SQL GI VERIFIER",
    auditHeading: "📋 SQL SECURITY BREACH & AUDIT VAULT",
    honeypotTitle: "PAKDA GAYA! UNAUTHORISED COPYING / OPTICAL THEFT BLOCKED",
    legalWarningHtml:
      '⚖️ <strong>STATUTORY LEGAL NOTICE:</strong> Unauthorised copying or commercial reproduction of textile designs may constitute <strong>Intellectual Property Theft</strong>, punishable under <strong>Sections 51 and 63 of the Copyright Act, 1957</strong>, <strong>Section 22 of the Designs Act, 2000</strong>, and <strong>Section 39 of the GI Act, 1999</strong>. Legal action may result in imprisonment, fines and damages.',
    toastHeading: "STATUTORY IP THEFT WARNING — COPY ATTEMPT LOGGED",
    btnProtect: "✨ Generate 8×8 Zari-Work Cloak & Buyer Share Links in RAM",
    btnVerify: "🧬 Verify Ownership",
    dlZari: "✨ Download 8×8 Zari-Work PNG",
    dlMeme: "🕵️ Download Meme-Embedded PNG",
    waMaster: "💬 Send Complete Buyer Access Package on WhatsApp",
  },
  te: {
    title: 'హెరిటేజ్-గార్డ్ <span class="gold-version">v4.2</span>',
    catalogHeading: "B2B కొనుగోలుదారు స్పాట్‌లైట్ వ్యూపోర్ట్ & కెమెరా రక్షణ కవచం",
    catalogHelp:
      "95px స్పాట్‌లైట్ ద్వారా చేనేత జరి మరియు ఇకత్ డిజైన్‌ను పరిశీలించండి. చిత్రాన్ని కాపీ చేయడం, రైట్-క్లిక్ చేయడం లేదా ఫోన్/కెమెరా పైకి ఎత్తితే 0ms లో చట్టపరమైన హెచ్చరికతో స్క్రీన్ లాక్ అవుతుంది.",
    uploadHeading: "🛡️ చేనేత సహకార స్టూడియో — జీరో-రిటెన్షన్ RAM క్లోక్",
    verifyHeading: "🔎 3-జోన్ LSB & GI యాజమాన్య నిర్ధారణ",
    auditHeading: "📋 భద్రతా ఆడిట్ లాగ్స్ (SQL వాల్ట్)",
    honeypotTitle: "పట్టుబడ్డారు! అనధికార కాపీ / ఫోటో చోరీ నిరోధించబడింది",
    legalWarningHtml:
      '⚖️ <strong>చట్టపరమైన హెచ్చరిక:</strong> చేనేత డిజైన్లను అనధికారికంగా కాపీ చేయడం లేదా వాణిజ్యపరంగా పునరుత్పత్తి చేయడం <strong>మేధో సంపత్తి చోరీ (IP Theft)</strong> కిందకు వస్తుంది. ఇది <strong>కాపీరైట్ చట్టం, 1957 (సెక్షన్లు 51 &amp; 63)</strong>, <strong>డిజైన్స్ చట్టం, 2000 (సెక్షన్ 22)</strong> మరియు <strong>GI చట్టం, 1999 (సెక్షన్ 39)</strong> ప్రకారం జైలు శిక్ష మరియు జరిమానాకు గురిచేస్తుంది.',
    toastHeading: "చట్టపరమైన IP చోరీ హెచ్చరిక — కాపీ ప్రయత్నం నమోదు చేయబడింది",
    btnProtect: "✨ 8×8 జరి క్లోక్ & కొనుగోలుదారు లింక్‌లను రూపొందించండి",
    btnVerify: "🧬 యాజమాన్యాన్ని నిర్ధారించండి",
    dlZari: "✨ 8×8 జరి-వర్క్ PNG డౌన్‌లోడ్",
    dlMeme: "🕵️ మీమ్-ఎంబెడెడ్ PNG డౌన్‌లోడ్",
    waMaster: "💬 వాట్సాప్‌లో కొనుగోలుదారు లింక్‌లను పంపండి",
  },
  hi: {
    title: 'हेरिटेज-गार्ड <span class="gold-version">v4.2</span>',
    catalogHeading: "B2B खरीदार स्पॉटलाइट निरीक्षण गेट और ऑप्टिकल सुरक्षा कवच",
    catalogHelp:
      "95px स्पॉटलाइट अपर्चर के माध्यम से ज़री और इकत बुनाई का निरीक्षण करें। छवि को कॉपी करना, राइट-क्लिक करना या फ़ोन/कैमरा उठाना 0ms में कानूनी चेतावनी के साथ स्क्रीन लॉक कर देता है।",
    uploadHeading: "🛡️ बुनकर सहकारी स्टूडियो — जीरो-रिटेंशन RAM क्लोक",
    verifyHeading: "🔎 फॉरेंसिक 3-ज़ोन LSB और SQL GI सत्यापन",
    auditHeading: "📋 SQL सुरक्षा उल्लंघन और ऑडिट वॉल्ट",
    honeypotTitle: "पकड़ा गया! अनधिकृत कॉपी / ऑप्टिकल चोरी ब्लॉक की गई",
    legalWarningHtml:
      '⚖️ <strong>वैधानिक कानूनी चेतावनी:</strong> कपड़ा डिजाइनों की अनधिकृत नकल या व्यावसायिक पुनरुत्पादन <strong>बौद्धिक संपदा चोरी (Intellectual Property Theft)</strong> है, जो <strong>कॉपीराइट अधिनियम, 1957 की धारा 51 और 63</strong>, <strong>डिजाइन अधिनियम, 2000 की धारा 22</strong> और <strong>GI अधिनियम, 1999 की धारा 39</strong> के तहत दंडनीय है। कानूनी कार्रवाई के परिणामस्वरूप कारावास, जुर्माना और हर्जाना हो सकता है।',
    toastHeading: "वैधानिक IP चोरी चेतावनी — कॉपी प्रयास लॉग किया गया",
    btnProtect: "✨ RAM में 8×8 ज़री क्लोक और खरीदार लिंक बनाएं",
    btnVerify: "🧬 स्वामित्व सत्यापित करें",
    dlZari: "✨ 8×8 ज़री-वर्क PNG डाउनलोड",
    dlMeme: "🕵️ मीम-एम्बेडेड PNG डाउनलोड",
    waMaster: "💬 व्हाट्सएप पर दोनों खरीदार लिंक भेजें",
  },
};

(function () {
  const SPOTLIGHT_RADIUS_PX = 95;

  let shieldLocked = false;
  let memeOverlayVisible = false;
  let manualHoldUntil = 0;
  let lastAiLogTs = 0;
  let toastTimeoutId = null;
  let flickerPhase = 0;
  let heatmapMode = false;
  let judgePipEnabled = false;
  let allowProgrammaticCopy = false;
  let cameraHardwareEnabled = false;
  let blockExternalHdmi = false;

  let studioStream = null;
  let studioVideoEl = null;
  let liveCanvasEl = null;
  let scanTimer = null;
  let scanInFlight = false;
  let cocoModel = null;
  let prevGray = null;
  let frozenStreak = 0;
  let memeVideo = null;
  let weaverPin = "";

  try { weaverPin = sessionStorage.getItem("hg_weaver_pin") || ""; } catch (_) {}

  let currentAssetId = "ikat";
  let currentAssetLabel = "Pochampally Ikat GI #4";
  let currentNormalImgSrc = "/api/demo_weave?style=ikat";
  let currentHeatmapImgSrc = "/api/demo_weave?style=ikat&heatmap=1";

  const viewport = document.getElementById("weave-viewport");
  const blurredLayer = document.getElementById("weave-blurred-layer");
  const clearLayer = document.getElementById("weave-clear-layer");
  const emojiOverlay = document.getElementById("emoji-shield-overlay");
  const statusBadge = document.getElementById("guard-status-badge");
  const cameraPowerBtn = document.getElementById("camera-power-btn");
  const reasonText = document.getElementById("shield-reason-text");
  const valDetector = document.getElementById("val-detector");
  const valLatency = document.getElementById("val-latency");
  const valCamDiag = document.getElementById("val-cam-diag");
  const valMonitors = document.getElementById("val-monitors");
  const antiShutterCanvas = document.getElementById("anti-shutter-canvas");
  const copyWarningToast = document.getElementById("copy-warning-toast");

  function loadScript(src) {
    return new Promise((resolve, reject) => {
      const s = document.createElement("script");
      s.src = src;
      s.async = true;
      s.onload = resolve;
      s.onerror = reject;
      document.head.appendChild(s);
    });
  }

  async function ensureBrowserAI() {
    if (cocoModel) return cocoModel;
    try {
      if (!window.tf) {
        await loadScript("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js");
      }
      if (!window.cocoSsd) {
        await loadScript("https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd@2.2.3/dist/coco-ssd.min.js");
      }
      cocoModel = await window.cocoSsd.load({ base: "lite_mobilenet_v2" });
      return cocoModel;
    } catch (_) {
      return null;
    }
  }

  function checkStudioLiveness() {
    const ctx = liveCanvasEl.getContext("2d", { willReadFrequently: true });
    ctx.drawImage(studioVideoEl, 0, 0, 96, 72);
    const data = ctx.getImageData(0, 0, 96, 72).data;
    const n = 96 * 72;
    const gray = new Uint8Array(n);
    let sum = 0;
    let sumSq = 0;

    for (let i = 0, p = 0; i < n; i++, p += 4) {
      const y = (data[p] * 77 + data[p + 1] * 150 + data[p + 2] * 29) >> 8;
      gray[i] = y;
      sum += y;
      sumSq += y * y;
    }

    const mean = sum / n;
    const std = Math.sqrt(Math.max(0, (sumSq / n) - (mean * mean)));
    if (mean < 15.0 || std < 7.0) {
      prevGray = gray;
      return { threat: true, reason: "PRIVACY_SHUTTER_OR_COVERED_CAMERA" };
    }

    if (prevGray) {
      let diffSum = 0;
      for (let i = 0; i < n; i++) diffSum += Math.abs(gray[i] - prevGray[i]);
      if (diffSum / n < 0.32) frozenStreak++;
      else frozenStreak = 0;
    }
    prevGray = gray;

    if (frozenStreak >= 4) {
      return { threat: true, reason: "PRIVACY_SHUTTER_OR_FROZEN_CAMERA" };
    }
    return { threat: false, reason: "SAFE" };
  }

  // 1. Inject compact styling + muted pakda_gaya_meme.mp4
  (function setupHoneypotMemeVideo() {
    if (!document.getElementById("hg-meme-video-styles")) {
      const styleEl = document.createElement("style");
      styleEl.id = "hg-meme-video-styles";
      styleEl.textContent = `
        .hidden { display: none !important; }
        .emoji-shield-overlay { padding: 12px 14px !important; overflow-y: auto; }
        .honeypot-meme-video {
          width: 100%;
          max-width: 245px;
          max-height: 146px;
          border-radius: 10px;
          border: 2px solid #f87171;
          background: #000;
          object-fit: cover;
          display: block;
          margin: 0 auto 6px;
          box-shadow: 0 8px 22px rgba(0, 0, 0, 0.75);
          pointer-events: none;
        }
        .meme-honeypot h2 { font-size: 1.0rem !important; margin: 2px 0 !important; line-height: 1.25; }
        .reason-pill { padding: 3px 10px !important; font-size: 0.74rem !important; margin: 4px 0 !important; }
        .emoji-shield-overlay .legal-warning-box { padding: 6px 10px !important; margin: 5px auto !important; }
        .emoji-shield-overlay .legal-warning-box p { font-size: 0.69rem !important; line-height: 1.36 !important; }
        .honeypot-sub { font-size: 0.7rem !important; margin: 4px auto 0 !important; }
      `;
      document.head.appendChild(styleEl);
    }

    const honeypot = document.getElementById("meme-honeypot");
    if (!honeypot) return;

    const emojiBox = honeypot.querySelector(".emoji-huge");
    memeVideo = document.getElementById("honeypot-meme-video");

    if (!memeVideo) {
      memeVideo = document.createElement("video");
      memeVideo.id = "honeypot-meme-video";
      memeVideo.className = "honeypot-meme-video";
      memeVideo.src = "/static/pakda_gaya_meme.mp4";
      memeVideo.loop = true;
      memeVideo.playsInline = true;
      memeVideo.preload = "auto";
      memeVideo.setAttribute("muted", "");
      memeVideo.setAttribute("playsinline", "");
      honeypot.insertBefore(memeVideo, honeypot.firstChild);
    }

    memeVideo.muted = true;
    memeVideo.defaultMuted = true;
    memeVideo.volume = 0;
    memeVideo.disablePictureInPicture = true;

    if (emojiBox) emojiBox.classList.add("hidden");
    memeVideo.addEventListener("error", () => {
      memeVideo.classList.add("hidden");
      if (emojiBox) emojiBox.classList.remove("hidden");
    });
  })();

  function startMemeVideo() {
    if (!memeVideo || memeVideo.classList.contains("hidden")) return;
    try {
      memeVideo.muted = true;
      memeVideo.volume = 0;
      memeVideo.currentTime = 0;
      const p = memeVideo.play();
      if (p && p.catch) p.catch(() => {});
    } catch (_) {}
  }

  function stopMemeVideo() {
    if (!memeVideo) return;
    try { memeVideo.pause(); memeVideo.currentTime = 0; } catch (_) {}
  }

  // 2. Permanent Cloud HTTPS Banner
  (function injectCloudHttpsBar() {
    const waHub = document.getElementById("whatsapp-section");
    const tierGrid = waHub ? waHub.querySelector(".tier-grid") : null;
    if (!waHub || !tierGrid || document.getElementById("cloud-https-bar")) return;

    const bar = document.createElement("div");
    bar.id = "cloud-https-bar";
    bar.style.cssText =
      "margin-bottom:12px; padding:10px 12px; background:rgba(16,185,129,0.12); " +
      "border:1px solid rgba(52,211,153,0.45); border-radius:8px; font-size:0.78rem; color:#34d399; word-break:break-all;";
    bar.innerHTML =
      `✅ <strong>Permanent Cloud HTTPS Active:</strong> <code>${window.location.origin}</code> — ` +
      `WhatsApp Buyer-Only links stay live 24/7 with On-Device Browser AI even when your laptop is OFF.`;
    waHub.insertBefore(bar, tierGrid);
  })();

  // 3. Weaver Studio PIN Unlock Bar
  (function injectWeaverPinBar() {
    const studio = document.getElementById("studio-section");
    const form = document.getElementById("protect-form");
    if (!studio || !form || document.getElementById("weaver-pin-bar")) return;

    const bar = document.createElement("div");
    bar.id = "weaver-pin-bar";
    bar.style.cssText =
      "display:flex; flex-wrap:wrap; gap:8px; align-items:center; margin-bottom:12px; padding:10px; " +
      "background:rgba(13,22,51,0.9); border:1px solid rgba(77,136,255,0.45); border-radius:8px;";
    bar.innerHTML = `
      <span style="font-size:0.75rem; font-weight:700; color:#7dd3fc;">🔐 Weaver Studio PIN:</span>
      <input
        type="password"
        id="weaver-pin-input"
        placeholder="Enter Weaver PIN"
        autocomplete="off"
        style="flex:1; min-width:130px; background:#060a19; color:#fff; border:1px solid rgba(96,165,250,0.4); padding:6px 10px; border-radius:6px; font-size:0.78rem;"
      />
      <button type="button" id="btn-unlock-studio" class="btn-copy">🔓 Unlock Studio</button>
      <span id="weaver-pin-status" style="width:100%; font-size:0.72rem; color:${weaverPin ? "#34d399" : "#fbbf24"};">
        ${weaverPin ? "✅ Weaver Studio unlocked for this browser tab." : "🔒 Upload Studio is PIN-locked for public visitors — enter Weaver PIN to cloak new sarees."}
      </span>
    `;
    studio.insertBefore(bar, form);

    const pinInput = document.getElementById("weaver-pin-input");
    if (pinInput && weaverPin) pinInput.value = weaverPin;

    async function unlockStudio() {
      const val = (pinInput ? pinInput.value : "").trim();
      const status = document.getElementById("weaver-pin-status");
      if (!val) {
        if (status) { status.style.color = "#fbbf24"; status.textContent = "⚠️ Please enter the Weaver PIN first."; }
        return;
      }
      try {
        const res = await fetch("/api/weaver_unlock", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ weaver_pin: val }),
        });
        if (res.ok) {
          weaverPin = val;
          try { sessionStorage.setItem("hg_weaver_pin", val); } catch (_) {}
          if (status) { status.style.color = "#34d399"; status.textContent = "✅ Weaver Studio unlocked! You can now upload & cloak sarees."; }
        } else {
          weaverPin = "";
          try { sessionStorage.removeItem("hg_weaver_pin"); } catch (_) {}
          if (status) { status.style.color = "#f87171"; status.textContent = "❌ Incorrect Weaver PIN. Try again."; }
        }
      } catch (_) {
        if (status) { status.style.color = "#f87171"; status.textContent = "⚠️ Could not reach server to verify PIN."; }
      }
    }

    document.getElementById("btn-unlock-studio").addEventListener("click", unlockStudio);
    if (pinInput) {
      pinInput.addEventListener("keydown", (e) => {
        if (e.key === "Enter") { e.preventDefault(); unlockStudio(); }
      });
    }
  })();

  function updateCameraButtonUI() {
    if (!cameraPowerBtn) return;
    cameraPowerBtn.textContent = cameraHardwareEnabled
      ? "📷 Browser AI Cam: ON"
      : "📷 Browser AI Cam: OFF";
  }
  updateCameraButtonUI();

  async function stopBrowserCamera() {
    cameraHardwareEnabled = false;
    updateCameraButtonUI();
    if (scanTimer) { clearTimeout(scanTimer); scanTimer = null; }
    if (studioStream) {
      try { studioStream.getTracks().forEach((t) => t.stop()); } catch (_) {}
      studioStream = null;
    }
    if (studioVideoEl) {
      studioVideoEl.srcObject = null;
      studioVideoEl.classList.add("hidden");
    }
    prevGray = null;
    frozenStreak = 0;
    if (Date.now() >= manualHoldUntil) setEmojiShield(false, "CAMERA_PAUSED");
  }

  async function startBrowserCamera() {
    if (!window.isSecureContext || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      alert("Browser camera requires a secure https:// link.");
      return;
    }
    try {
      if (valCamDiag) { valCamDiag.textContent = "⏳ STARTING CAM & AI..."; valCamDiag.style.color = "#7dd3fc"; }
      studioStream = await navigator.mediaDevices.getUserMedia({
        video: { facingMode: "user", width: { ideal: 320 }, height: { ideal: 240 } },
        audio: false,
      });
      cameraHardwareEnabled = true;
      updateCameraButtonUI();

      if (!studioVideoEl && viewport) {
        studioVideoEl = document.createElement("video");
        studioVideoEl.id = "cloud-cam-pip";
        studioVideoEl.className = "live-cam-pip hidden";
        studioVideoEl.autoplay = true;
        studioVideoEl.playsInline = true;
        studioVideoEl.muted = true;
        viewport.appendChild(studioVideoEl);
      }
      if (!liveCanvasEl) {
        liveCanvasEl = document.createElement("canvas");
        liveCanvasEl.width = 96;
        liveCanvasEl.height = 72;
      }

      if (studioVideoEl) {
        studioVideoEl.srcObject = studioStream;
        studioVideoEl.classList.toggle("hidden", !judgePipEnabled);
        await studioVideoEl.play();
      }

      const track = studioStream.getVideoTracks()[0];
      if (track) track.onended = () => stopBrowserCamera();

      await ensureBrowserAI();
      runBrowserVisionLoop();
    } catch (_) {
      cameraHardwareEnabled = false;
      updateCameraButtonUI();
      alert("Camera permission denied or no webcam found. 95px Spotlight + 8×8 Cloak remain active.");
    }
  }

  async function runBrowserVisionLoop() {
    if (!cameraHardwareEnabled || !studioStream || !studioVideoEl) return;

    if (!scanInFlight && studioVideoEl.readyState >= 2 && studioVideoEl.videoWidth > 0) {
      scanInFlight = true;
      const t0 = performance.now();
      try {
        const liveCheck = checkStudioLiveness();
        let threatReason = liveCheck.threat ? liveCheck.reason : "";

        if (!threatReason && cocoModel) {
          const preds = await cocoModel.detect(studioVideoEl, 8, 0.24);
          const personPresent = preds.some((p) => p.class === "person" && p.score >= 0.35);
          for (const p of preds) {
            if (p.class === "cell phone" && p.score >= 0.25) {
              threatReason = "CELL_PHONE_DETECTED_BROWSER_AI";
              break;
            }
            if (personPresent && (p.class === "remote" || p.class === "book") && p.score >= 0.45) {
              threatReason = "HANDHELD_OPTICAL_DEVICE_DETECTED";
              break;
            }
          }
        }

        const ms = Math.round(performance.now() - t0);
        if (valLatency) valLatency.textContent = ms + " ms";
        if (valDetector) valDetector.textContent = cocoModel ? "Browser TF.js COCO-SSD" : "Browser Liveness Guard";

        if (cameraHardwareEnabled) {
          setEmojiShield(Boolean(threatReason), threatReason || "SAFE_VIEWER_VERIFIED");
          if (threatReason && Date.now() - lastAiLogTs > 4000) {
            lastAiLogTs = Date.now();
            fetch("/api/log-breach", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ reason: threatReason }),
            }).then(() => window.refreshAuditLogs()).catch(() => {});
          }
        }
      } catch (_) {
      } finally {
        scanInFlight = false;
      }
    }

    if (cameraHardwareEnabled) {
      scanTimer = setTimeout(runBrowserVisionLoop, 280);
    }
  }

  window.addEventListener("pagehide", () => { stopBrowserCamera(); stopMemeVideo(); });

  window.toggleCameraPower = async function () {
    if (cameraHardwareEnabled) await stopBrowserCamera();
    else await startBrowserCamera();
  };

  window.toggleJudgeCamPreview = function () {
    judgePipEnabled = !judgePipEnabled;
    const btn = document.getElementById("btn-pip-toggle");
    if (btn) btn.textContent = judgePipEnabled ? "👁️ Judge Cam: ON" : "👁️ Judge Cam: OFF";
    if (studioVideoEl) {
      studioVideoEl.classList.toggle("hidden", !(judgePipEnabled && cameraHardwareEnabled));
    }
    if (judgePipEnabled && !cameraHardwareEnabled) startBrowserCamera();
  };

  function updateTierLinksAndWhatsApp(assetLabel, assetId) {
    currentAssetLabel = assetLabel;
    currentAssetId = assetId;

    const shareOrigin = window.location.origin;
    const strictUrl = `${shareOrigin}/b/strict/${assetId}`;
    const standardUrl = `${shareOrigin}/b/standard/${assetId}`;

    const highInput = document.getElementById("high-priority-url");
    const lowInput = document.getElementById("low-priority-url");
    if (highInput) highInput.value = strictUrl;
    if (lowInput) lowInput.value = standardUrl;

    const openHigh = document.getElementById("open-high-link");
    const openLow = document.getElementById("open-low-link");
    const navBuyerBtn = document.getElementById("nav-buyer-mode-btn");
    if (openHigh) openHigh.href = `/b/strict/${assetId}`;
    if (openLow) openLow.href = `/b/standard/${assetId}`;
    if (navBuyerBtn) navBuyerBtn.href = `/b/strict/${assetId}`;

    const msgStrict =
      `🪷 *Heritage-Guard | Tier-1 Biometric Buyer Link*\n` +
      `GI Saree: *${assetLabel}*\n` +
      `🔒 *Locked Buyer-Only View (Live Camera Unlock Required):*\n\n` +
      `${strictUrl}\n\n` +
      `⚖️ _Protected under Sec 51 & 63 Copyright Act 1957 & Sec 22 Designs Act 2000._`;

    const msgStandard =
      `🪷 *Heritage-Guard | Tier-2 Catalog Preview Link*\n` +
      `GI Saree: *${assetLabel}*\n` +
      `🛡️ *Locked Buyer-Only Preview (95px Spotlight + 8x8 Zari Cloak):*\n\n` +
      `${standardUrl}\n\n` +
      `⚖️ _Protected under Sec 51 & 63 Copyright Act 1957 & Sec 22 Designs Act 2000._`;

    const msgPackage =
      `🪷 *Heritage-Guard GI Handloom B2B Buyer Dispatch*\n` +
      `GI Saree: *${assetLabel}*\n\n` +
      `🔒 *1. Tier-1 Biometric Vault Link (Camera Unlock Required):*\n` +
      `${strictUrl}\n\n` +
      `🛡️ *2. Tier-2 Catalog Preview Link (Quick View):*\n` +
      `${standardUrl}`;

    const setHref = (id, msg) => {
      const el = document.getElementById(id);
      if (el) el.href = `https://wa.me/?text=${encodeURIComponent(msg)}`;
    };
    setHref("wa-high-link", msgStrict);
    setHref("wa-low-link", msgStandard);
    setHref("wa-both-links", msgPackage);
    setHref("res-wa-high", msgStrict);
    setHref("res-wa-low", msgStandard);
  }
  updateTierLinksAndWhatsApp(currentAssetLabel, currentAssetId);

  window.copyPriorityLink = function (inputId) {
    const el = document.getElementById(inputId);
    if (!el) return;
    allowProgrammaticCopy = true;
    navigator.clipboard.writeText(el.value).finally(() => {
      setTimeout(() => { allowProgrammaticCopy = false; }, 200);
    });
  };

  function showStatutoryToast(triggerReason) {
    if (!copyWarningToast) return;
    const langToggle = document.getElementById("lang-toggle");
    const curLang = (langToggle && langToggle.value) || "en";
    const pack = I18N_DICT[curLang] || I18N_DICT.en;

    const headingEl = document.getElementById("toast-heading");
    const bodyEl = document.getElementById("toast-body");
    if (headingEl) headingEl.textContent = `${pack.toastHeading} [${triggerReason}]`;
    if (bodyEl) bodyEl.innerHTML = pack.legalWarningHtml;

    copyWarningToast.classList.remove("hidden");
    if (toastTimeoutId) clearTimeout(toastTimeoutId);
    toastTimeoutId = setTimeout(() => copyWarningToast.classList.add("hidden"), 4800);
  }

  function setEmojiShield(locked, reason = "OPTICAL_THREAT_DETECTED") {
    if (!locked && Date.now() < manualHoldUntil) locked = true;
    shieldLocked = locked;
    if (!viewport || !emojiOverlay) return;

    if (locked) {
      viewport.classList.add("threat-locked");
      emojiOverlay.classList.remove("hidden");
      if (!memeOverlayVisible) { memeOverlayVisible = true; startMemeVideo(); }
      if (reasonText) reasonText.textContent = reason;
      if (statusBadge) {
        statusBadge.textContent = "🚫 THREAT LOCKED: " + reason;
        statusBadge.className = "pill pill-danger";
      }
      if (valCamDiag) { valCamDiag.textContent = "🚨 " + reason; valCamDiag.style.color = "#f87171"; }
    } else {
      viewport.classList.remove("threat-locked");
      emojiOverlay.classList.add("hidden");
      if (memeOverlayVisible) { memeOverlayVisible = false; stopMemeVideo(); }
      if (statusBadge) {
        statusBadge.textContent = cameraHardwareEnabled
          ? "🛡️ ON-DEVICE AI GUARD ONLINE"
          : "🛡️ CLOUD SPOTLIGHT ACTIVE";
        statusBadge.className = "pill pill-safe";
      }
      if (valCamDiag) {
        valCamDiag.textContent = cameraHardwareEnabled
          ? "SAFE (ON-DEVICE AI ACTIVE)"
          : "CAM OFF (CLICK TO ENABLE)";
        valCamDiag.style.color = "#34d399";
      }
    }
  }

  async function reportFrontendBreach(reason) {
    manualHoldUntil = Date.now() + 4500;
    setEmojiShield(true, reason);
    showStatutoryToast(reason);
    setTimeout(() => {
      if (!cameraHardwareEnabled && Date.now() >= manualHoldUntil) setEmojiShield(false, "SAFE");
    }, 4600);
    try {
      await fetch("/api/log-breach", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reason }),
      });
      window.refreshAuditLogs();
    } catch (_) {}
  }

  window.triggerManualHoneypotTest = () => reportFrontendBreach("STATUTORY_IP_WARNING_DEMO_TEST");

  window.toggleHdmiPolicy = function () {
    blockExternalHdmi = !blockExternalHdmi;
    const btn = document.getElementById("hdmi-policy-btn");
    if (btn) btn.textContent = blockExternalHdmi ? "🖥️ HDMI: STRICT BLOCK" : "🖥️ HDMI: Projector Safe";
    const isExt = Boolean(window.screen && window.screen.isExtended);
    if (valMonitors) valMonitors.textContent = isExt ? "2+ Displays (Extended)" : "1 Internal Screen";
    if (blockExternalHdmi && isExt) reportFrontendBreach("EXTENDED_DISPLAY_HDMI_DETECTED");
  };

  window.switchCatalogWeave = function (styleKey, label) {
    heatmapMode = false;
    const t = Date.now();
    currentNormalImgSrc = `/api/demo_weave?style=${encodeURIComponent(styleKey)}&t=${t}`;
    currentHeatmapImgSrc = `/api/demo_weave?style=${encodeURIComponent(styleKey)}&heatmap=1&t=${t}`;
    if (viewport) viewport.classList.remove("heatmap-active");
    if (blurredLayer) blurredLayer.src = currentNormalImgSrc;
    if (clearLayer) clearLayer.src = currentNormalImgSrc;

    const heatBtn = document.getElementById("btn-heatmap-toggle");
    if (heatBtn) heatBtn.textContent = "🔥 8×8 DCT Heatmap";

    const dlZari = document.getElementById("catalog-dl-zari");
    const dlMeme = document.getElementById("catalog-dl-meme");
    if (dlZari) dlZari.href = `/api/demo_weave?style=${encodeURIComponent(styleKey)}&variant=zari&download=1`;
    if (dlMeme) dlMeme.href = `/api/demo_weave?style=${encodeURIComponent(styleKey)}&variant=meme&download=1`;

    const lbl = document.getElementById("active-weave-label");
    if (lbl) lbl.innerHTML = `Viewing: <strong>${label}</strong>`;
    document.querySelectorAll(".tab-chip").forEach((btn) => {
      btn.classList.toggle("active", btn.getAttribute("data-weave") === styleKey);
    });
    updateTierLinksAndWhatsApp(label, styleKey);
  };

  window.toggleHeatmapView = function () {
    heatmapMode = !heatmapMode;
    const btn = document.getElementById("btn-heatmap-toggle");
    if (!blurredLayer || !clearLayer || !viewport) return;
    viewport.classList.toggle("heatmap-active", heatmapMode);
    blurredLayer.src = heatmapMode ? currentHeatmapImgSrc : currentNormalImgSrc;
    clearLayer.src = heatmapMode ? currentHeatmapImgSrc : currentNormalImgSrc;
    if (btn) btn.textContent = heatmapMode ? "🖼️ Protected Weave View" : "🔥 8×8 DCT Heatmap";
  };

  if (viewport && clearLayer) {
    viewport.addEventListener("mousemove", (e) => {
      if (shieldLocked) return;
      const rect = viewport.getBoundingClientRect();
      clearLayer.style.clipPath = `circle(${SPOTLIGHT_RADIUS_PX}px at ${e.clientX - rect.left}px ${e.clientY - rect.top}px)`;
    });
    viewport.addEventListener("touchmove", (e) => {
      if (shieldLocked || !e.touches || !e.touches[0]) return;
      const rect = viewport.getBoundingClientRect();
      clearLayer.style.clipPath = `circle(${SPOTLIGHT_RADIUS_PX}px at ${e.touches[0].clientX - rect.left}px ${e.touches[0].clientY - rect.top}px)`;
    }, { passive: true });
    viewport.addEventListener("mouseleave", () => { clearLayer.style.clipPath = "circle(0px at 50% 50%)"; });
    viewport.addEventListener("contextmenu", (e) => { e.preventDefault(); reportFrontendBreach("RIGHT_CLICK_COPY_ATTEMPT_SEC51_63"); });
    viewport.addEventListener("dragstart", (e) => { e.preventDefault(); reportFrontendBreach("IMAGE_DRAG_COPY_ATTEMPT_SEC22"); });
  }

  document.addEventListener("copy", (e) => {
    if (allowProgrammaticCopy) return;
    const activeTag = document.activeElement ? document.activeElement.tagName : "";
    if (activeTag === "INPUT" || activeTag === "TEXTAREA") return;
    e.preventDefault();
    if (e.clipboardData) e.clipboardData.setData("text/plain", STATUTORY_PLAIN_TEXT);
    reportFrontendBreach("CLIPBOARD_COPY_BLOCKED_COPYRIGHT_ACT");
  });

  window.addEventListener("keyup", (e) => {
    if (e.key === "PrintScreen" || (e.metaKey && e.shiftKey && (e.key === "S" || e.key === "s"))) {
      try { navigator.clipboard.writeText(STATUTORY_PLAIN_TEXT); } catch (_) {}
      reportFrontendBreach("SCREENSHOT_BLOCKED_SEC51_63_COPYRIGHT_ACT");
    }
  });

  if (navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia) {
    navigator.mediaDevices.getDisplayMedia = async function () {
      reportFrontendBreach("BROWSER_SCREEN_SHARE_BLOCKED_SEC22");
      throw new Error("Heritage-Guard blocked unauthorized screen sharing.");
    };
  }

  function runAntiShutterFlicker() {
    if (antiShutterCanvas && !shieldLocked) {
      const ctx = antiShutterCanvas.getContext("2d");
      ctx.clearRect(0, 0, antiShutterCanvas.width, antiShutterCanvas.height);
      ctx.fillStyle = "rgba(20, 10, 30, 0.055)";
      for (let y = flickerPhase; y < antiShutterCanvas.height; y += 3) ctx.fillRect(0, y, antiShutterCanvas.width, 1);
      flickerPhase = (flickerPhase + 1) % 3;
    }
    requestAnimationFrame(runAntiShutterFlicker);
  }
  requestAnimationFrame(runAntiShutterFlicker);

  const langToggle = document.getElementById("lang-toggle");
  if (langToggle) {
    langToggle.addEventListener("change", (e) => {
      const pack = I18N_DICT[e.target.value] || I18N_DICT.en;
      const setTxt = (id, val, isHtml = false) => {
        const el = document.getElementById(id);
        if (!el || !val) return;
        if (isHtml) el.innerHTML = val;
        else el.textContent = val;
      };
      setTxt("ui-title", pack.title, true);
      setTxt("ui-catalog-heading", pack.catalogHeading);
      setTxt("ui-catalog-help", pack.catalogHelp);
      setTxt("ui-upload-heading", pack.uploadHeading);
      setTxt("ui-verify-heading", pack.verifyHeading);
      setTxt("ui-audit-heading", pack.auditHeading);
      setTxt("honeypot-title", pack.honeypotTitle);
      setTxt("legal-warning-text", pack.legalWarningHtml, true);
      setTxt("toast-heading", pack.toastHeading);
      setTxt("toast-body", pack.legalWarningHtml, true);
      setTxt("btn-protect", pack.btnProtect);
      setTxt("btn-verify", pack.btnVerify);
      setTxt("catalog-dl-zari", pack.dlZari);
      setTxt("catalog-dl-meme", pack.dlMeme);
      setTxt("wa-both-links", pack.waMaster);
    });
  }

  const protectForm = document.getElementById("protect-form");
  if (protectForm) {
    protectForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const pinInput = document.getElementById("weaver-pin-input");
      const activePin = weaverPin || (pinInput ? pinInput.value.trim() : "");
      if (!activePin) {
        alert("Weaver Studio is PIN-locked. Enter the Weaver PIN above and click 'Unlock Studio' first.");
        if (pinInput) pinInput.focus();
        return;
      }

      const btn = document.getElementById("btn-protect");
      btn.textContent = "⏳ Cloaking Saree & Generating Locked Buyer Links in Cloud RAM...";
      btn.disabled = true;

      try {
        const formData = new FormData(protectForm);
        const res = await fetch("/api/protect", {
          method: "POST",
          headers: { "X-Weaver-Pin": activePin },
          body: formData,
        });
        const data = await res.json();

        if (!res.ok) {
          alert(data.error || "Could not process the uploaded file.");
          return;
        }

        weaverPin = activePin;
        try { sessionStorage.setItem("hg_weaver_pin", activePin); } catch (_) {}

        document.getElementById("protect-result").classList.remove("hidden");
        document.getElementById("res-count").textContent =
          data.processed_count + (data.is_batch ? " (Batch ZIP)" : " (Dual PNG)");
        document.getElementById("res-hash").textContent = data.fingerprint;
        document.getElementById("res-lsb").textContent = data.watermark_payload;
        document.getElementById("res-psnr").textContent = data.psnr_db;
        document.getElementById("res-jpeg").textContent = data.jpeg_survival_pct;
        document.getElementById("res-verified").textContent = data.watermark_verified_post_cloak ? "INTACT (3-Zone)" : "NO";

        const dlZari = document.getElementById("download-zari-link");
        const dlMeme = document.getElementById("download-meme-link");
        const dlZip = document.getElementById("download-batch-zip");

        if (dlZari && data.zari_download_url) dlZari.href = data.zari_download_url;
        if (dlMeme && data.meme_download_url) dlMeme.href = data.meme_download_url;
        if (dlZip) {
          if (data.is_batch && data.zip_download_url) { dlZip.href = data.zip_download_url; dlZip.classList.remove("hidden"); }
          else dlZip.classList.add("hidden");
        }

        heatmapMode = false;
        if (viewport) viewport.classList.remove("heatmap-active");
        const heatBtn = document.getElementById("btn-heatmap-toggle");
        if (heatBtn) heatBtn.textContent = "🔥 8×8 DCT Heatmap";

        if (data.preview_url) {
          currentNormalImgSrc = data.preview_url;
          if (blurredLayer) blurredLayer.src = currentNormalImgSrc;
          if (clearLayer) clearLayer.src = currentNormalImgSrc;
        }
        if (data.heatmap_url) currentHeatmapImgSrc = data.heatmap_url;

        const fpShort = data.fp_short || data.fingerprint.slice(0, 12);
        const artisanId = document.getElementById("artisan-id").value || "WEAVER_TG_COOP_01";
        const cluster = document.getElementById("gi-cluster").value || "POCHAMPALLY_IKAT";
        const lbl = document.getElementById("active-weave-label");
        if (lbl) lbl.innerHTML = `Viewing: <strong>${artisanId} (${cluster})</strong>`;

        updateTierLinksAndWhatsApp(`${artisanId} (${cluster})`, fpShort);
        window.refreshAuditLogs();
      } catch (_) {
        alert("Network error while contacting Heritage-Guard cloud server.");
      } finally {
        const curLang = (langToggle && langToggle.value) || "en";
        btn.textContent = (I18N_DICT[curLang] || I18N_DICT.en).btnProtect;
        btn.disabled = false;
      }
    });
  }

  const verifyForm = document.getElementById("verify-form");
  if (verifyForm) {
    verifyForm.addEventListener("submit", async (e) => {
      e.preventDefault();
      const box = document.getElementById("verify-result");
      const formData = new FormData(verifyForm);
      try {
        const res = await fetch("/api/verify", { method: "POST", body: formData });
        const data = await res.json();
        box.classList.remove("hidden");
        if (!res.ok) {
          box.innerHTML = `<strong>⚠️ INVALID FILE</strong><br/>${data.error || "Please upload a valid image."}`;
          return;
        }
        if (data.verified) {
          const sqlLine = data.vault_match
            ? `<br/>SQL GI Vault Match: <strong>${data.vault_match}</strong>`
            : `<br/>SQL GI Vault Match: <em>Not in current RAM/SQL session (verified via 3-Zone LSB)</em>`;
          box.innerHTML =
            `<strong>✅ AUTHENTIC GI WEAVE VERIFIED</strong>` +
            `${sqlLine}<br/>` +
            `3-Zone LSB: <code>${data.extracted_watermark || "N/A"}</code><br/>` +
            `SHA-256 Hash: <code>${data.sha256_fingerprint}</code>`;
        } else {
          box.innerHTML =
            `<strong>⚠️ UNREGISTERED / SCRAPED IMAGE</strong><br/>` +
            `SHA-256 Hash: <code>${data.sha256_fingerprint || "N/A"}</code>`;
        }
        window.refreshAuditLogs();
      } catch (_) {
        box.classList.remove("hidden");
        box.innerHTML = `<strong>⚠️ VERIFICATION ERROR</strong><br/>Could not reach verification server.`;
      }
    });
  }

  window.refreshAuditLogs = async function () {
    try {
      const res = await fetch("/api/audit_logs", { cache: "no-store" });
      if (!res.ok) return;
      const logs = await res.json();
      const tbody = document.getElementById("audit-log-body");
      if (!tbody || !Array.isArray(logs) || logs.length === 0) return;
      tbody.innerHTML = logs
        .slice(0, 10)
        .map(
          (item) =>
            `<tr><td>${item.time_str || "--"}</td><td><strong>${item.event}</strong></td><td><code>${item.reason}</code></td></tr>`
        )
        .join("");
    } catch (_) {}
  };

  if (valDetector) valDetector.textContent = "Browser TF.js COCO-SSD";
  setEmojiShield(false);
  window.refreshAuditLogs();
  setInterval(window.refreshAuditLogs, 4000);
})();