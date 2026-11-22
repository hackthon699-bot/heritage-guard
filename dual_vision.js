/**
 * Heritage-Guard v4.5.1 | Shared Alternating Dual-Model Browser AI: dual_vision.js
 * Tuned for both mobile phones and entry-level laptops (Ryzen 3 HP 15s 720p webcam):
 *  1. Every Frame (<1 ms): Privacy-Shutter / Covered-Lens / Frozen-Driver-Icon Liveness Check
 *  2. Every Frame (<2 ms): Calibrated 2-10 cm Hand-Near-Camera Laplacian Defocus Trap
 *  3. Even Frames: YOLOv10n ONNX (handles [1,300,6], [1,6,300], or [1,84,2100] outputs)
 *  4. Odd Frames:  YOLOv8n-OIV7 ONNX (601 classes: Camera, Tablet, Mobile phone & Face-Occlusion)
 *  5. Adaptive Pacing: 260 ms cadence on <=4-thread CPUs (Ryzen 3 / budget phones), 180 ms on faster CPUs
 */

(function (global) {
  const ORT_VER = "1.20.1";
  const ORT_SOURCES = [
    {
      script: `https://cdn.jsdelivr.net/npm/onnxruntime-web@${ORT_VER}/dist/ort.wasm.min.js`,
      wasmBase: `https://cdn.jsdelivr.net/npm/onnxruntime-web@${ORT_VER}/dist/`,
    },
    {
      script: `https://unpkg.com/onnxruntime-web@${ORT_VER}/dist/ort.wasm.min.js`,
      wasmBase: `https://unpkg.com/onnxruntime-web@${ORT_VER}/dist/`,
    },
  ];

  const DEFAULT_DUAL_CONFIG = {
    imgsz: 320,
    yolov10: {
      direct: [
        { id: 67, name: "cell phone", reason: "CELL_PHONE_DETECTED_V10", conf: 0.16, max_area: 1.0 },
        { id: 65, name: "remote", reason: "HANDHELD_OPTICAL_DEVICE_V10", conf: 0.24, max_area: 0.45 },
      ],
      proxy: [
        { id: 73, name: "book", reason: "HANDHELD_DEVICE_CASE_V10", conf: 0.30, max_area: 0.38 },
        { id: 63, name: "laptop", reason: "HANDHELD_SCREEN_V10", conf: 0.34, max_area: 0.36 },
        { id: 62, name: "tv", reason: "HANDHELD_SCREEN_V10", conf: 0.34, max_area: 0.36 },
        { id: 64, name: "mouse", reason: "HANDHELD_CAMERA_LENS_V10", conf: 0.30, max_area: 0.22 },
      ],
      person_ids: [0],
    },
    oiv7: {
      direct: [
        { id: 339, name: "Mobile phone", reason: "CELL_PHONE_DETECTED_OIV7", conf: 0.16, max_area: 1.0 },
        { id: 82, name: "Camera", reason: "CAMERA_OR_DSLR_DETECTED_OIV7", conf: 0.16, max_area: 1.0 },
      ],
      proxy: [],
      person_ids: [381],
      face_ids: [],
    },
  };

  let initPromise = null;
  let engineMode = "uninitialized"; // "dual_onnx" | "v10_only" | "oiv7_only" | "coco_fallback" | "liveness_only"
  let v10Session = null;
  let v10InputName = "images";
  let v10OutputName = "output0";
  let oiv7Session = null;
  let oiv7InputName = "images";
  let oiv7OutputName = "output0";
  let dualConfig = DEFAULT_DUAL_CONFIG;
  let cocoFallbackModel = null;

  function recommendedIntervalMs() {
    const cores = (navigator && navigator.hardwareConcurrency) || 4;
    return cores <= 4 ? 260 : 180;
  }

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

  async function loadOrtRuntime() {
    if (global.ort && global.ort.InferenceSession) return true;
    for (const src of ORT_SOURCES) {
      try {
        await loadScript(src.script);
        if (global.ort && global.ort.env && global.ort.env.wasm) {
          global.ort.env.wasm.numThreads = 1; // Safe without COOP/COEP headers on Render
          global.ort.env.wasm.simd = true;
          global.ort.env.wasm.wasmPaths = src.wasmBase;
          return true;
        }
      } catch (_) {}
    }
    return false;
  }

  async function loadOneOnnxSession(url, label, report) {
    try {
      report(`⏳ Downloading ${label} (cached after 1st visit)...`);
      const res = await fetch(url, { cache: "force-cache" });
      if (!res.ok) return null;
      const bytes = new Uint8Array(await res.arrayBuffer());
      if (bytes.byteLength < 100000) return null;
      report(`⏳ Compiling ${label}...`);
      const sess = await global.ort.InferenceSession.create(bytes, {
        executionProviders: ["wasm"],
        graphOptimizationLevel: "all",
      });
      return {
        session: sess,
        inputName: (sess.inputNames && sess.inputNames[0]) || "images",
        outputName: (sess.outputNames && sess.outputNames[0]) || "output0",
      };
    } catch (_) {
      return null;
    }
  }

  async function loadCocoFallback() {
    try {
      if (!global.tf) {
        await loadScript("https://cdn.jsdelivr.net/npm/@tensorflow/tfjs@4.22.0/dist/tf.min.js");
      }
      if (!global.cocoSsd) {
        await loadScript("https://cdn.jsdelivr.net/npm/@tensorflow-models/coco-ssd@2.2.3/dist/coco-ssd.min.js");
      }
      if (global.tf && global.tf.ready) await global.tf.ready();
      cocoFallbackModel = await global.cocoSsd.load({ base: "lite_mobilenet_v2" });
      engineMode = "coco_fallback";
      return engineMode;
    } catch (_) {
      engineMode = "liveness_only";
      return engineMode;
    }
  }

  async function init(onStatus) {
    if (initPromise) return initPromise;
    initPromise = (async () => {
      const report = (msg) => {
        if (typeof onStatus === "function") onStatus(msg);
      };

      try {
        report("⏳ Loading Dual Class Map...");
        const clsRes = await fetch("/static/dual_classes.json", { cache: "default" });
        if (clsRes.ok) {
          const parsed = await clsRes.json();
          if (parsed && parsed.yolov10 && parsed.oiv7) {
            dualConfig = parsed;
          }
        }
      } catch (_) {}

      report("⏳ Loading ONNX Web Engine...");
      const ortOk = await loadOrtRuntime();
      if (ortOk) {
        // Sequential loading prevents RAM spikes on phones & Ryzen 3 laptops
        const v10 = await loadOneOnnxSession("/static/yolov10n.onnx", "YOLOv10n Phone AI (~9 MB)", report);
        if (v10) {
          v10Session = v10.session;
          v10InputName = v10.inputName;
          v10OutputName = v10.outputName;
        }

        const oiv7 = await loadOneOnnxSession("/static/yolov8n-oiv7.onnx", "YOLOv8n-OIV7 Camera/Tablet AI (~14 MB)", report);
        if (oiv7) {
          oiv7Session = oiv7.session;
          oiv7InputName = oiv7.inputName;
          oiv7OutputName = oiv7.outputName;
        }
      }

      if (v10Session && oiv7Session) {
        engineMode = "dual_onnx";
        report("✅ Dual AI Ready: YOLOv10n + YOLOv8n-OIV7");
        return engineMode;
      }
      if (v10Session) {
        engineMode = "v10_only";
        report("✅ YOLOv10n Ready (Phones + Laplacian)");
        return engineMode;
      }
      if (oiv7Session) {
        engineMode = "oiv7_only";
        report("✅ YOLOv8n-OIV7 Ready (601 Classes)");
        return engineMode;
      }

      report("⏳ ONNX models not found — loading Backup AI...");
      return await loadCocoFallback();
    })();
    return initPromise;
  }

  function createSession() {
    const aiCanvas = document.createElement("canvas");
    aiCanvas.width = 320;
    aiCanvas.height = 320;
    const aiCtx = aiCanvas.getContext("2d", { willReadFrequently: true });

    const liveCanvas = document.createElement("canvas");
    liveCanvas.width = 96;
    liveCanvas.height = 72;
    const liveCtx = liveCanvas.getContext("2d", { willReadFrequently: true });

    const inputBuf = new Float32Array(3 * 320 * 320);

    const state = {
      frameCount: 0,
      prevGray: null,
      liveFrames: 0,
      frozenStreak: 0,
      livenessOk: false,
      baselineLapVar: 0,
      defocusStreak: 0,
      lastPersonSeenTs: 0,
      hadFace: false,
      noFaceStreak: 0,
      faceOccluded: false,
      personAbsentStreak: 0,
      aiHoldUntil: 0,
      lastAiReason: "CELL_PHONE_DETECTED_V10",
    };

    function reset() {
      state.frameCount = 0;
      state.prevGray = null;
      state.liveFrames = 0;
      state.frozenStreak = 0;
      state.livenessOk = false;
      state.baselineLapVar = 0;
      state.defocusStreak = 0;
      state.lastPersonSeenTs = 0;
      state.hadFace = false;
      state.noFaceStreak = 0;
      state.faceOccluded = false;
      state.personAbsentStreak = 0;
      state.aiHoldUntil = 0;
    }

    function runLivenessAndDefocus(videoEl) {
      liveCtx.drawImage(videoEl, 0, 0, 96, 72);
      const rgba = liveCtx.getImageData(0, 0, 96, 72).data;
      const n = 96 * 72;
      const gray = new Uint8Array(n);

      let sum = 0;
      let sumSq = 0;
      for (let i = 0, p = 0; i < n; i++, p += 4) {
        const y = (rgba[p] * 77 + rgba[p + 1] * 150 + rgba[p + 2] * 29) >> 8;
        gray[i] = y;
        sum += y;
        sumSq += y * y;
      }

      const mean = sum / n;
      const std = Math.sqrt(Math.max(0, sumSq / n - mean * mean));

      // 1. Covered lens / opaque physical privacy shutter
      if (mean < 16.0 || std < 7.5) {
        state.prevGray = gray;
        state.liveFrames = 0;
        state.livenessOk = false;
        return { threat: true, live: false, reason: "PRIVACY_SHUTTER_OR_COVERED_CAMERA" };
      }

      // 2. Frozen frame / Windows crossed-out camera driver icon
      if (state.prevGray) {
        let diffSum = 0;
        for (let i = 0; i < n; i++) diffSum += Math.abs(gray[i] - state.prevGray[i]);
        if (diffSum / n < 0.30) {
          state.frozenStreak++;
          state.liveFrames = 0;
        } else {
          state.frozenStreak = 0;
          state.liveFrames++;
          if (state.liveFrames >= 2) state.livenessOk = true;
        }
      } else {
        state.liveFrames = 1;
      }
      state.prevGray = gray;

      const frozenLimit = state.livenessOk ? 4 : 2;
      if (state.frozenStreak >= frozenLimit) {
        state.livenessOk = false;
        return { threat: true, live: false, reason: "PRIVACY_SHUTTER_OR_FROZEN_CAMERA" };
      }

      // 3. 2-10 cm Hand-Near-Camera Laplacian Defocus Trap (calibrated for soft 720p webcams)
      let lapSum = 0;
      let lapSumSq = 0;
      let lapCount = 0;
      for (let y = 14; y < 58; y++) {
        const row = y * 96;
        for (let x = 19; x < 77; x++) {
          const idx = row + x;
          const lap =
            gray[idx - 1] + gray[idx + 1] + gray[idx - 96] + gray[idx + 96] - 4 * gray[idx];
          lapSum += lap;
          lapSumSq += lap * lap;
          lapCount++;
        }
      }
      const lapMean = lapSum / lapCount;
      const lapVar = Math.max(0, lapSumSq / lapCount - lapMean * lapMean);

      const isAbsoluteHandBlur = lapVar < 11.0;
      const isRelativeDefocus =
        state.baselineLapVar > 24.0 && lapVar < state.baselineLapVar * 0.38 && lapVar < 36.0;

      if (isAbsoluteHandBlur || isRelativeDefocus) {
        state.defocusStreak++;
      } else {
        state.defocusStreak = 0;
        if (state.livenessOk) {
          state.baselineLapVar =
            state.baselineLapVar === 0 ? lapVar : state.baselineLapVar * 0.90 + lapVar * 0.10;
        }
      }

      if (state.defocusStreak >= 2) {
        return {
          threat: true,
          live: state.livenessOk,
          reason: "HAND_OR_OBJECT_NEAR_CAMERA_DEFOCUS",
        };
      }

      return { threat: false, live: state.livenessOk, reason: "SAFE" };
    }

    function prepareLetterboxTensor(videoEl) {
      const vw = videoEl.videoWidth || 320;
      const vh = videoEl.videoHeight || 240;
      const scale = Math.min(320 / vw, 320 / vh);
      const nw = Math.max(1, Math.round(vw * scale));
      const nh = Math.max(1, Math.round(vh * scale));
      const padX = Math.floor((320 - nw) / 2);
      const padY = Math.floor((320 - nh) / 2);

      // Standard Ultralytics 114-gray letterbox keeps portrait phone shapes undistorted
      aiCtx.fillStyle = "rgb(114, 114, 114)";
      aiCtx.fillRect(0, 0, 320, 320);
      aiCtx.drawImage(videoEl, 0, 0, vw, vh, padX, padY, nw, nh);

      const rgba = aiCtx.getImageData(0, 0, 320, 320).data;
      const area = 320 * 320;
      const gOff = area;
      const bOff = area * 2;
      const inv255 = 1.0 / 255.0;

      for (let i = 0, p = 0; i < area; i++, p += 4) {
        inputBuf[i] = rgba[p] * inv255;
        inputBuf[gOff + i] = rgba[p + 1] * inv255;
        inputBuf[bOff + i] = rgba[p + 2] * inv255;
      }

      return {
        tensor: new global.ort.Tensor("float32", inputBuf, [1, 3, 320, 320]),
        unpaddedArea: Math.max(1, nw * nh),
      };
    }

    function parseAnchorGridOutput(data, dims, cfg, unpaddedArea, updateFaceOcclusion) {
      const transposed = dims[1] > dims[2]; // Standard YOLOv8 ONNX: [1, 605, 2100]
      const channels = transposed ? dims[2] : dims[1];
      const anchors = transposed ? dims[1] : dims[2];

      const getScore = (clsId, j) =>
        transposed ? data[j * channels + (4 + clsId)] : data[(4 + clsId) * anchors + j];
      const getAreaRatio = (j) => {
        const bw = transposed ? data[j * channels + 2] : data[2 * anchors + j];
        const bh = transposed ? data[j * channels + 3] : data[3 * anchors + j];
        return (bw * bh) / unpaddedArea;
      };

      // 1. Direct threats (Mobile phone, Camera, Tablet computer, Remote, etc.)
      let bestThreat = "";
      let bestScore = 0;
      for (const item of cfg.direct || []) {
        if (item.id + 4 >= channels) continue;
        const thresh = item.conf;
        const maxA = item.max_area || 1.0;
        for (let j = 0; j < anchors; j++) {
          const sc = getScore(item.id, j);
          if (sc >= thresh && sc > bestScore) {
            if (maxA >= 1.0 || getAreaRatio(j) <= maxA) {
              bestScore = sc;
              bestThreat = item.reason;
            }
          }
        }
      }
      if (bestThreat) return bestThreat;

      // 2. Person presence
      let personPresent = false;
      for (const pid of cfg.person_ids || []) {
        if (pid + 4 >= channels) continue;
        for (let j = 0; j < anchors; j++) {
          if (getScore(pid, j) >= 0.25) {
            personPresent = true;
            break;
          }
        }
        if (personPresent) break;
      }
      if (personPresent) state.lastPersonSeenTs = Date.now();
      const recentPerson = personPresent || Date.now() - state.lastPersonSeenTs < 1500;

      // 3. Person-gated proxy devices
      if (recentPerson) {
        for (const item of cfg.proxy || []) {
          if (item.id + 4 >= channels) continue;
          const thresh = item.conf;
          const maxA = item.max_area || 0.38;
          for (let j = 0; j < anchors; j++) {
            const sc = getScore(item.id, j);
            if (sc >= thresh) {
              const ar = getAreaRatio(j);
              if (ar >= 0.015 && ar <= maxA) return item.reason;
            }
          }
        }
      }

      // 4. Continuous Face-Occlusion Lock (OIV7 frames only)
      if (updateFaceOcclusion && cfg.face_ids && cfg.face_ids.length > 0) {
        let faceVisible = false;
        for (const fid of cfg.face_ids) {
          if (fid + 4 >= channels) continue;
          for (let j = 0; j < anchors; j++) {
            if (getScore(fid, j) >= 0.22) {
              faceVisible = true;
              break;
            }
          }
          if (faceVisible) break;
        }

        if (faceVisible) {
          state.hadFace = true;
          state.noFaceStreak = 0;
          state.faceOccluded = false;
          state.personAbsentStreak = 0;
        } else if (personPresent) {
          state.personAbsentStreak = 0;
          if (state.hadFace) {
            state.noFaceStreak++;
            if (state.noFaceStreak >= 2) state.faceOccluded = true;
          }
        } else {
          state.personAbsentStreak++;
          if (state.personAbsentStreak >= 3) {
            state.faceOccluded = false;
            state.noFaceStreak = 0;
          }
        }
        if (state.faceOccluded) return "FACE_OCCLUDED_BY_DEVICE_OIV7";
      }

      return "";
    }

    function parseV10End2EndOutput(data, dims, cfg, unpaddedArea) {
      // Handles both [1, 300, 6] and transposed [1, 6, 300] safely across Ultralytics versions
      const transposed = dims[1] === 6 && dims[2] > 6;
      const numRows = transposed ? dims[2] : dims[1];
      const getVal = (j, k) => (transposed ? data[k * numRows + j] : data[j * 6 + k]);

      const directById = new Map((cfg.direct || []).map((it) => [it.id, it]));
      const proxyById = new Map((cfg.proxy || []).map((it) => [it.id, it]));
      const personSet = new Set(cfg.person_ids || [0]);

      let personPresent = false;
      let bestDirectReason = "";
      let bestDirectScore = 0;
      const proxyCandidates = [];

      for (let j = 0; j < numRows; j++) {
        const score = getVal(j, 4);
        if (score < 0.14) continue;

        const clsId = Math.round(getVal(j, 5));
        const x1 = getVal(j, 0);
        const y1 = getVal(j, 1);
        const x2 = getVal(j, 2);
        const y2 = getVal(j, 3);
        const areaRatio = (Math.max(0, x2 - x1) * Math.max(0, y2 - y1)) / unpaddedArea;

        if (personSet.has(clsId) && score >= 0.25) {
          personPresent = true;
          continue;
        }

        const dItem = directById.get(clsId);
        if (dItem && score >= dItem.conf && score > bestDirectScore) {
          if (dItem.max_area >= 1.0 || areaRatio <= dItem.max_area) {
            bestDirectScore = score;
            bestDirectReason = dItem.reason;
          }
          continue;
        }

        const pItem = proxyById.get(clsId);
        if (pItem && score >= pItem.conf && areaRatio >= 0.015 && areaRatio <= (pItem.max_area || 0.38)) {
          proxyCandidates.push(pItem.reason);
        }
      }

      if (bestDirectReason) return bestDirectReason;
      if (personPresent) state.lastPersonSeenTs = Date.now();
      const recentPerson = personPresent || Date.now() - state.lastPersonSeenTs < 1500;
      if (recentPerson && proxyCandidates.length > 0) return proxyCandidates[0];
      return "";
    }

    async function runOnnxModel(which, videoEl) {
      const isV10 = which === "v10";
      const sess = isV10 ? v10Session : oiv7Session;
      if (!sess) return "";

      const { tensor, unpaddedArea } = prepareLetterboxTensor(videoEl);
      let outTensor = null;

      try {
        const inputName = isV10 ? v10InputName : oiv7InputName;
        const outputName = isV10 ? v10OutputName : oiv7OutputName;
        const outputs = await sess.run({ [inputName]: tensor });
        outTensor = outputs[outputName] || outputs[Object.keys(outputs)[0]];
        const dims = outTensor.dims;
        const data = outTensor.data;

        if (isV10) {
          if (dims.length === 3 && (dims[2] === 6 || dims[1] === 6)) {
            return parseV10End2EndOutput(data, dims, dualConfig.yolov10, unpaddedArea);
          }
          return parseAnchorGridOutput(data, dims, dualConfig.yolov10, unpaddedArea, false);
        }
        return parseAnchorGridOutput(data, dims, dualConfig.oiv7, unpaddedArea, true);
      } finally {
        try { if (tensor && tensor.dispose) tensor.dispose(); } catch (_) {}
        try { if (outTensor && outTensor.dispose) outTensor.dispose(); } catch (_) {}
      }
    }

    async function runCocoFallback(videoEl) {
      const vw = videoEl.videoWidth || 320;
      const vh = videoEl.videoHeight || 240;
      const scale = Math.min(320 / vw, 320 / vh);
      const nw = Math.max(1, Math.round(vw * scale));
      const nh = Math.max(1, Math.round(vh * scale));
      const padX = Math.floor((320 - nw) / 2);
      const padY = Math.floor((320 - nh) / 2);
      aiCtx.fillStyle = "rgb(114, 114, 114)";
      aiCtx.fillRect(0, 0, 320, 320);
      aiCtx.drawImage(videoEl, 0, 0, vw, vh, padX, padY, nw, nh);

      const preds = await cocoFallbackModel.detect(aiCanvas, 12, 0.16);
      const personPresent = preds.some((p) => p.class === "person" && p.score >= 0.30);
      const unpaddedArea = Math.max(1, nw * nh);

      for (const p of preds) {
        const ar = (p.bbox[2] * p.bbox[3]) / unpaddedArea;
        if (p.class === "cell phone" && p.score >= 0.16) return "CELL_PHONE_DETECTED_BACKUP_AI";
        if (p.class === "remote" && p.score >= 0.24 && ar < 0.45) return "HANDHELD_OPTICAL_DEVICE_DETECTED";
        if (personPresent && p.class === "book" && p.score >= 0.30 && ar < 0.38) return "HANDHELD_DEVICE_CASE_DETECTED";
      }
      return "";
    }

    async function scan(videoEl) {
      const t0 = performance.now();
      const liveCheck = runLivenessAndDefocus(videoEl);

      if (liveCheck.threat) {
        return {
          threat_detected: true,
          camera_liveness_verified: liveCheck.live,
          reason: liveCheck.reason,
          latency_ms: Math.round(performance.now() - t0),
          detector: getDetectorLabel(),
        };
      }

      let aiThreat = "";
      if (engineMode === "dual_onnx") {
        // Alternate frames: Even -> YOLOv10n (Phones), Odd -> YOLOv8n-OIV7 (DSLRs, Tablets, Face Occlusion)
        const which = state.frameCount % 2 === 0 ? "v10" : "oiv7";
        state.frameCount++;
        aiThreat = await runOnnxModel(which, videoEl);
      } else if (engineMode === "v10_only") {
        aiThreat = await runOnnxModel("v10", videoEl);
      } else if (engineMode === "oiv7_only") {
        aiThreat = await runOnnxModel("oiv7", videoEl);
      } else if (engineMode === "coco_fallback" && cocoFallbackModel) {
        aiThreat = await runCocoFallback(videoEl);
      }

      const now = Date.now();
      if (aiThreat) {
        state.aiHoldUntil = now + 2500;
        state.lastAiReason = aiThreat;
      } else if (now < state.aiHoldUntil) {
        aiThreat = state.lastAiReason;
      }

      return {
        threat_detected: Boolean(aiThreat),
        camera_liveness_verified: liveCheck.live,
        reason: aiThreat || (liveCheck.live ? "SAFE_VIEWER_VERIFIED" : "VERIFYING_LIVE_CAMERA"),
        latency_ms: Math.round(performance.now() - t0),
        detector: getDetectorLabel(),
      };
    }

    return { scan, reset };
  }

  function getDetectorLabel() {
    if (engineMode === "dual_onnx") return "Dual YOLOv10n + YOLOv8n-OIV7";
    if (engineMode === "v10_only") return "Browser YOLOv10n + Laplacian";
    if (engineMode === "oiv7_only") return "Browser YOLOv8n-OIV7 (601 Classes)";
    if (engineMode === "coco_fallback") return "Backup COCO-SSD + Laplacian";
    return "Browser Liveness + Laplacian";
  }

  global.HGVisionEngine = {
    init,
    createSession,
    getDetectorLabel,
    recommendedIntervalMs,
    getMode: () => engineMode,
  };
})(window);