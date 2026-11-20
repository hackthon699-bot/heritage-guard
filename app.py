"""
Heritage-Guard | Render Cloud Edition: app.py (v3.2 - Zero-PyTorch + Browser AI + SEO)
Optimized for Render Free Tier (512 MB RAM, ₹0, no credit card):
  - Lightweight Flask + OpenCV-Headless backend (~120 MB RAM)
  - Browser-Side AI (TensorFlow.js COCO-SSD + Privacy-Shutter Liveness) in Buyer-Only Mode
  - Weaver Studio PIN Lock (WEAVER_PIN env var, default: 2026) + unguessable studio download tokens
  - Full 3-hash SQLite GI Vault registration (source, 8x8 Zari-Work, Meme-Embedded)
  - Accurate JPEG Q=85 survival gate: JPEG(cloaked) vs JPEG(original)
  - Dynamic HTTPS /robots.txt, /sitemap.xml, and Google Search Console meta injection
"""

import os
import io
import re
import html
import time
import hmac
import secrets
import zipfile
import inspect
import threading
from collections import OrderedDict
import numpy as np
import cv2
from flask import Flask, jsonify, request, send_file, send_from_directory, Response
from werkzeug.middleware.proxy_fix import ProxyFix

from preprocessor import (
    preprocess_pipeline,
    extract_3zone_lsb,
    strip_exif_in_ram,
    generate_sha256_fingerprint,
)
from cloak_engine import apply_cloak
from db_manager import DatabaseManager

VERSION = "3.2-render"
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEAVER_PIN = os.environ.get("WEAVER_PIN", "2026").strip() or "2026"
MAX_RAM_ASSETS = 15

app = Flask(__name__, static_folder=BASE_DIR, template_folder=BASE_DIR)
app.config["MAX_CONTENT_LENGTH"] = 25 * 1024 * 1024  # 25 MB upload guard
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

DB_LOCK = threading.Lock()
RAM_LOCK = threading.Lock()
DEMO_LOCK = threading.Lock()

db_vault = DatabaseManager()
RAM_BUYER_VAULT = OrderedDict()
DEMO_WEAVE_CACHE = {}

DEMO_TITLES = {
    "ikat": "Pochampally Ikat GI #4",
    "gadwal": "Gadwal Zari Saree GI #10",
    "gollabhama": "Siddipet Gollabhama GI #188",
}


def log_security_event(event_dict: dict):
    ev = str(event_dict.get("event", "SECURITY_ALERT"))[:64]
    rsn = str(event_dict.get("reason", "UNKNOWN"))[:160]
    with DB_LOCK:
        try:
            db_vault.log_security_event(ev, rsn)
        except Exception:
            pass


def verify_protection_quality(orig_bgr: np.ndarray, cloaked_bgr: np.ndarray) -> dict:
    """Computes real PSNR and true JPEG(Q=85) sign agreement: JPEG(cloaked) vs JPEG(original)."""
    orig_f = orig_bgr.astype(np.float64)
    cloak_f = cloaked_bgr.astype(np.float64)
    mse = float(np.mean((orig_f - cloak_f) ** 2))
    psnr = 99.0 if mse < 1e-10 else float(10.0 * np.log10((255.0 ** 2) / mse))

    ok_o, enc_o = cv2.imencode(".jpg", orig_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 85])
    ok_c, enc_c = cv2.imencode(".jpg", cloaked_bgr, [int(cv2.IMWRITE_JPEG_QUALITY), 85])

    if ok_o and ok_c:
        dec_o = cv2.imdecode(enc_o, cv2.IMREAD_COLOR).astype(np.float64)
        dec_c = cv2.imdecode(enc_c, cv2.IMREAD_COLOR).astype(np.float64)
        delta_pre = cloak_f - orig_f
        delta_post = dec_c - dec_o
        mask = np.abs(delta_pre) > 1.0
        if np.any(mask):
            survival = float(np.mean(np.sign(delta_pre[mask]) == np.sign(delta_post[mask])) * 100.0)
        else:
            survival = 0.0
    else:
        survival = 0.0

    return {
        "psnr_db": round(psnr, 2),
        "jpeg_sign_agreement_pct": round(survival, 1),
        "passed": (psnr >= 26.0 and survival >= 70.0),
    }


@app.errorhandler(413)
def file_too_large(_err):
    return jsonify({"error": "Upload exceeds 25 MB limit. Please upload smaller or fewer saree photos."}), 413


@app.after_request
def add_cache_headers(response):
    if request.path.lower().endswith((".mp4", ".webm", ".ogg")):
        response.headers["Cache-Control"] = "public, max-age=3600"
        return response
    if request.path.startswith("/api/") or request.path.startswith("/b/"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


def _check_weaver_pin() -> bool:
    pin = (
        request.headers.get("X-Weaver-Pin")
        or request.form.get("weaver_pin")
        or (request.get_json(silent=True) or {}).get("weaver_pin")
        or ""
    ).strip()
    if not pin:
        return False
    return hmac.compare_digest(pin, WEAVER_PIN)


def _call_apply_cloak(img_bgr: np.ndarray, mode: str, watermark_payload: str) -> dict:
    sig = inspect.signature(apply_cloak)
    kwargs = {"strength": 3.5, "mode": mode}
    if "meme_text" in sig.parameters and mode == "meme_bait":
        kwargs["meme_text"] = "PAKDA GAYA STOLEN GI"
    if "watermark_payload" in sig.parameters:
        kwargs["watermark_payload"] = watermark_payload
    return apply_cloak(img_bgr, **kwargs)


def execute_ram_protection_pipeline(
    raw_bytes: bytes,
    artisan_id: str = "WEAVER_TG_COOP_01",
    gi_cluster: str = "POCHAMPALLY_IKAT",
    cloak_mode: str = "meme_bait",
) -> dict:
    p1 = preprocess_pipeline(raw_bytes, artisan_id=artisan_id, gi_cluster=gi_cluster)
    p2_zari = _call_apply_cloak(p1["image"], "invisible", p1["watermark_payload"])
    p2_meme = _call_apply_cloak(p1["image"], "meme_bait", p1["watermark_payload"])

    primary = p2_zari if cloak_mode == "invisible" else p2_meme
    q_report = verify_protection_quality(p1["image"], primary["cloaked_image"])
    verified_lsb = extract_3zone_lsb(primary["cloaked_image"])

    zari_hash = generate_sha256_fingerprint(p2_zari["cloaked_image"])
    meme_hash = generate_sha256_fingerprint(p2_meme["cloaked_image"])
    primary_hash = zari_hash if cloak_mode == "invisible" else meme_hash

    with DB_LOCK:
        for h_val, mode_name, psnr_val in [
            (p1["fingerprint"], "source_preprocessed", primary["psnr"]),
            (zari_hash, "invisible_8x8_zari", p2_zari["psnr"]),
            (meme_hash, "meme_bait_8x8", p2_meme["psnr"]),
        ]:
            try:
                db_vault.register_gi_asset(
                    sha256_hash=h_val,
                    artisan_id=artisan_id,
                    gi_cluster=gi_cluster,
                    watermark_payload=p1["watermark_payload"],
                    cloak_mode=mode_name,
                    psnr_db=float(psnr_val),
                    jpeg_survival_pct=float(q_report["jpeg_sign_agreement_pct"]),
                )
            except Exception:
                pass

    return {
        "cloaked_bgr": primary["cloaked_image"],
        "zari_only_bgr": p2_zari["cloaked_image"],
        "meme_embedded_bgr": p2_meme["cloaked_image"],
        "heatmap_bgr": p2_meme.get("heatmap_image", primary.get("heatmap_image", primary["cloaked_image"])),
        "fingerprint": primary_hash,
        "zari_hash": zari_hash,
        "meme_hash": meme_hash,
        "watermark_payload": p1["watermark_payload"],
        "watermark_verified_post_cloak": (verified_lsb == p1["watermark_payload"]),
        "psnr_db": round(float(primary.get("psnr", q_report["psnr_db"])), 2),
        "jpeg_survival_pct": q_report["jpeg_sign_agreement_pct"],
        "quality_gate_passed": q_report["passed"],
    }


def _get_or_build_demo_weave(style: str = "ikat") -> dict:
    clean_style = style.lower() if style.lower() in DEMO_TITLES else "ikat"
    with DEMO_LOCK:
        if clean_style in DEMO_WEAVE_CACHE:
            return DEMO_WEAVE_CACHE[clean_style]

        h, w = 400, 640
        y, x = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")

        if clean_style == "gadwal":
            b = ((np.sin(x / 7.0) * 50) + 70).astype(np.uint8)
            g = ((np.cos(y / 11.0) * 65) + 135).astype(np.uint8)
            r = ((np.sin((x + y) / 9.0) * 70) + 175).astype(np.uint8)
            title = "GI GADWAL ZARI SAREE #TG-10"
            cluster = "GADWAL_ZARI"
        elif clean_style == "gollabhama":
            b = ((np.cos(x / 10.0) * 60) + 125).astype(np.uint8)
            g = ((np.sin(y / 8.0) * 55) + 85).astype(np.uint8)
            r = ((np.cos((x - y) / 12.0) * 65) + 160).astype(np.uint8)
            title = "GI SIDDIPET GOLLABHAMA #TG-188"
            cluster = "SIDDIPET_GOLLABHAMA"
        else:
            b = ((np.sin(x / 9.0) + np.cos(y / 9.0)) * 60 + 110).astype(np.uint8)
            g = ((np.sin((x + y) / 14.0)) * 55 + 90).astype(np.uint8)
            r = ((np.cos((x - y) / 11.0)) * 75 + 150).astype(np.uint8)
            title = "GI POCHAMPALLY IKAT #TG-04"
            cluster = "POCHAMPALLY_IKAT"

        synth_bgr = cv2.merge([b, g, r])
        synth_bgr[10:42, :, :] = (45, 185, 235)
        synth_bgr[h - 42:h - 10, :, :] = (45, 185, 235)
        cv2.putText(
            synth_bgr,
            title,
            (70, 210),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.95,
            (245, 250, 255),
            2,
            cv2.LINE_AA,
        )

        _, raw_buf = cv2.imencode(".png", synth_bgr)
        res = execute_ram_protection_pipeline(
            raw_buf.tobytes(),
            artisan_id=f"WEAVER_{clean_style.upper()}",
            gi_cluster=cluster,
        )
        _, png_zari = cv2.imencode(".png", res["zari_only_bgr"])
        _, png_meme = cv2.imencode(".png", res["meme_embedded_bgr"])
        _, png_heat = cv2.imencode(".png", res["heatmap_bgr"])

        bundle = {
            "zari": png_zari.tobytes(),
            "meme": png_meme.tobytes(),
            "heat": png_heat.tobytes(),
        }
        DEMO_WEAVE_CACHE[clean_style] = bundle
        return bundle


def _extract_gsc_token(raw_val: str) -> str:
    raw_val = (raw_val or "").strip()
    if not raw_val:
        return ""
    m = re.search(r'content=["\']([^"\']+)["\']', raw_val)
    return m.group(1).strip() if m else raw_val


def _public_root_url() -> str:
    root = request.url_root.rstrip("/")
    if root.startswith("http://") and ".onrender.com" in root:
        root = "https://" + root[len("http://"):]
    return root


# ---------------- HEALTH CHECK & SEO ----------------
@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok", "version": VERSION}), 200


@app.route("/")
def index():
    for candidate in ["index.html", os.path.join("templates", "index.html")]:
        full = os.path.join(BASE_DIR, candidate)
        if os.path.exists(full):
            with open(full, "r", encoding="utf-8") as f:
                page_html = f.read()

            gsc_token = _extract_gsc_token(os.environ.get("GOOGLE_SITE_VERIFICATION", ""))
            seo_block = (
                '\n  <meta name="description" content="Heritage Guard — GI Handloom Cybersecurity & Anti-Scraping Vault for Pochampally Ikat, Gadwal Zari, and authentic Indian textiles. Features 8x8 DCT cloaking, 3-Zone LSB watermarking, and on-device browser AI optical defense." />\n'
                '  <meta name="keywords" content="Heritage Guard, GI Handloom, Pochampally Ikat, Gadwal Zari, anti-scraping, textile IP protection, handloom watermark, DCT cloak" />\n'
                '  <meta property="og:title" content="Heritage Guard | GI Handloom Cybersecurity & Anti-Scraping Vault" />\n'
                '  <meta property="og:description" content="Protect authentic Indian handloom designs from digital scraping, CAD cloning, and camera theft in volatile RAM." />\n'
                '  <meta property="og:type" content="website" />\n'
            )
            if gsc_token:
                seo_block += f'  <meta name="google-site-verification" content="{html.escape(gsc_token)}" />\n'

            if "</head>" in page_html:
                page_html = page_html.replace("</head>", seo_block + "</head>", 1)

            page_html = re.sub(
                r"spotlight_shield\.js(?:\?v=[0-9.]+)?",
                "spotlight_shield.js?v=4.2",
                page_html,
            )
            return Response(page_html, mimetype="text/html")
    return "index.html not found in project directory.", 404


@app.route("/robots.txt")
def robots_txt():
    root = _public_root_url()
    txt = f"User-agent: *\nAllow: /\nDisallow: /api/\nSitemap: {root}/sitemap.xml\n"
    return Response(txt, mimetype="text/plain")


@app.route("/sitemap.xml")
def sitemap_xml():
    root = _public_root_url()
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url><loc>{root}/</loc><priority>1.0</priority></url>
  <url><loc>{root}/b/standard/ikat</loc><priority>0.8</priority></url>
  <url><loc>{root}/b/standard/gadwal</loc><priority>0.8</priority></url>
  <url><loc>{root}/b/standard/gollabhama</loc><priority>0.8</priority></url>
</urlset>"""
    return Response(xml, mimetype="application/xml")


@app.route("/static/<path:filename>")
def serve_static(filename):
    static_sub = os.path.join(BASE_DIR, "static", filename)
    if os.path.exists(static_sub):
        return send_from_directory(os.path.join(BASE_DIR, "static"), filename)
    return send_from_directory(BASE_DIR, filename)


# ---------------- CYBERGUARD BUYER-ONLY MODE (ON-DEVICE BROWSER AI) ----------------
BUYER_ONLY_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Heritage Guard | Protected GI Saree Buyer Inspection</title>
  <link rel="stylesheet" href="/static/style.css?v=4.0" />
  <style>
    .hidden { display: none !important; }
    .buyer-shell { max-width: 820px; margin: 22px auto; padding: 0 18px 36px; }
    .buyer-meta { display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 10px; margin-bottom: 12px; font-size: 0.84rem; color: #cbd5e1; }
    .buyer-gate-chip { padding: 7px 13px; border-radius: 6px; font-size: 0.76rem; font-weight: 700; border: 1px solid rgba(56, 189, 248, 0.45); background: rgba(15, 23, 52, 0.85); color: #93c5fd; }
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
    .camera-unlock-gate {
      position: absolute;
      inset: 0;
      z-index: 12;
      background: radial-gradient(circle at 50% 40%, #101e47 0%, #050816 100%);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      padding: 24px;
      gap: 10px;
    }
    .camera-unlock-gate.hidden { display: none !important; }
    .unlock-icon { font-size: 3.1rem; line-height: 1; }
    .camera-unlock-gate h3 { margin: 0; font-size: 1.18rem; color: #ffffff; }
    .camera-unlock-gate p { margin: 0; max-width: 470px; font-size: 0.83rem; color: #cbd5e1; line-height: 1.5; }
    .unlock-error-msg {
      color: #fecaca;
      background: rgba(127, 29, 29, 0.85);
      border: 1px solid #f87171;
      border-radius: 8px;
      padding: 8px 12px;
      font-size: 0.78rem;
      max-width: 470px;
    }
    .unlock-error-msg.hidden { display: none !important; }
    .btn-unlock-cam {
      background: linear-gradient(135deg, #4d88ff, #2563eb);
      color: #ffffff;
      border: 1px solid rgba(147, 197, 253, 0.6);
      padding: 12px 24px;
      border-radius: 8px;
      font-size: 0.9rem;
      font-weight: 700;
      cursor: pointer;
      box-shadow: 0 8px 24px rgba(77, 136, 255, 0.45);
      margin-top: 4px;
    }
    .btn-unlock-cam:disabled { opacity: 0.65; cursor: wait; }
    .hidden-buyer-video {
      position: fixed;
      bottom: 0;
      right: 0;
      width: 2px;
      height: 2px;
      opacity: 0.01;
      pointer-events: none;
    }
  </style>
</head>
<body>
  <div id="copy-warning-toast" class="copy-warning-toast hidden">
    <div class="toast-icon">⚖️</div>
    <div class="toast-content">
      <strong id="toast-heading">STATUTORY IP THEFT WARNING — COPY ATTEMPT LOGGED</strong>
      <p id="toast-body">
        Unauthorised copying or commercial reproduction of textile designs may constitute <strong>Intellectual Property Theft</strong>, punishable under Sections 51 and 63 of the Copyright Act, 1957, Section 22 of the Designs Act, 2000, and Section 39 of the GI Act, 1999. Legal action may result in imprisonment, fines and damages.
      </p>
    </div>
  </div>

  <header class="cyber-navbar">
    <div class="nav-inner">
      <div class="cyber-brand">
        <span class="cyber-logo-ring">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="12" cy="12" r="9" opacity="0.5"/>
            <path d="M12 3L4 7v5c0 5 3.5 8.5 8 10 4.5-1.5 8-5 8-10V7l-8-4z"/>
            <circle cx="12" cy="12" r="2.5" fill="currentColor"/>
          </svg>
        </span>
        <span class="brand-name">Heritage<strong>Guard</strong> <span class="gold-version">BUYER VAULT</span></span>
      </div>

      <div class="nav-cta-group">
        <span id="gate-mode-pill" class="buyer-gate-chip">__GATE_PILL__</span>
        <div id="guard-status-badge" class="pill __STATUS_CLASS__">__STATUS_INIT__</div>
        <select id="lang-toggle" class="cyber-select" aria-label="Language">
          <option value="en">🌐 English (EN)</option>
          <option value="te">🌐 తెలుగు (TE)</option>
          <option value="hi">🌐 हिन्दी (HI)</option>
        </select>
      </div>
    </div>
  </header>

  <main class="buyer-shell">
    <section class="v17-card showcase-panel">
      <div class="buyer-meta">
        <div>
          <span class="section-tag">LOCKED B2B BUYER INSPECTION • ON-DEVICE BROWSER AI</span>
          <h2 id="ui-asset-title" style="margin:2px 0 0 0;">__ASSET_LABEL__</h2>
        </div>
        <span id="val-cam-diag" style="font-weight:700; color:__DIAG_COLOR__;">__DIAG_INIT__</span>
      </div>

      <p class="v17-subtext" id="ui-buyer-help">
        Move your cursor or finger inside the frame to inspect threads through the 95px Spotlight Aperture. Zero camera frames ever leave your device — AI scanning runs locally in your browser.
      </p>

      <div id="weave-viewport" class="weave-viewport __INITIAL_LOCK_CLASS__">
        <img id="weave-blurred-layer" class="weave-blurred-layer" src="/api/asset_image/__ASSET_ID__" alt="Blurred Protected Weave" draggable="false" />
        <img id="weave-clear-layer" class="weave-clear-layer" src="/api/asset_image/__ASSET_ID__" alt="Protected Spotlight Weave" draggable="false" />
        <canvas id="anti-shutter-canvas" width="640" height="400"></canvas>

        <div id="camera-unlock-gate" class="camera-unlock-gate __GATE_OVERLAY_CLASS__">
          <div class="unlock-icon">🔒📷</div>
          <h3 id="unlock-gate-title">LIVE CAMERA REQUIRED TO UNLOCK GI SAREE</h3>
          <p id="unlock-gate-desc">
            This Tier-1 Zero-Trust GI link requires an unobstructed, live device camera (open physical privacy shutters). Zero photos or frames are uploaded — AI runs strictly on your own device.
          </p>
          <div id="unlock-error-msg" class="unlock-error-msg hidden"></div>
          <button id="btn-unlock-camera" class="btn-unlock-cam" type="button">
            📷 Turn On Camera to Unlock GI Saree
          </button>
        </div>

        <div id="emoji-shield-overlay" class="emoji-shield-overlay hidden">
          <div id="meme-honeypot" class="meme-honeypot">
            <video
              id="honeypot-meme-video"
              class="honeypot-meme-video"
              src="/static/pakda_gaya_meme.mp4"
              muted
              loop
              playsinline
              preload="auto"
            ></video>
            <div id="emoji-fallback" class="emoji-huge hidden">🚫📸⚖️</div>
            <h2 id="honeypot-title">PAKDA GAYA! UNAUTHORISED COPYING / OPTICAL THEFT BLOCKED</h2>
            <p id="shield-reason-text" class="reason-pill">CAMERA_OR_COPY_BLOCKED</p>
            <div class="legal-warning-box">
              <p id="legal-warning-text">
                ⚖️ <strong>STATUTORY LEGAL NOTICE:</strong> Unauthorised copying or commercial reproduction of textile designs may constitute <strong>Intellectual Property Theft</strong>, punishable under <strong>Sections 51 and 63 of the Copyright Act, 1957</strong>, <strong>Section 22 of the Designs Act, 2000</strong>, and <strong>Section 39 of the GI Act, 1999</strong>. Legal action may result in imprisonment, fines and damages.
              </p>
            </div>
            <p class="honeypot-sub">
              8×8 Zari Adversarial Poison &amp; GI Forensic Breach Log Recorded. Keep your camera unobstructed and lower all recording devices to restore access.
            </p>
          </div>
        </div>
      </div>

      <div class="legal-warning-box" style="max-width:100%; margin-top:14px;">
        <p id="static-buyer-legal-text">
          ⚖️ <strong>PROTECTED GI HANDLOOM DESIGN:</strong> Unauthorised copying or commercial reproduction of textile designs may constitute <strong>Intellectual Property Theft</strong>, punishable under Sections 51 and 63 of the Copyright Act, 1957, Section 22 of the Designs Act, 2000, and Section 39 of the GI Act, 1999. Legal action may result in imprisonment, fines and damages.
        </p>
      </div>
    </section>
  </main>

  <video id="buyer-cam-video" class="hidden-buyer-video" autoplay muted playsinline></video>
  <canvas id="buyer-liveness-canvas" width="96" height="72" style="display:none;"></canvas>

  <script>
  (function () {
    const GATE_MODE = "__GATE_MODE__";
    const SPOTLIGHT_RADIUS_PX = 95;
    const STATUTORY_PLAIN = "⚠️ STATUTORY LEGAL WARNING: Unauthorised copying or commercial reproduction of textile designs may constitute Intellectual Property Theft, punishable under Sections 51 and 63 of the Copyright Act, 1957, Section 22 of the Designs Act, 2000, and Section 39 of the GI Act, 1999. Legal action may result in imprisonment, fines and damages.";

    const I18N = {
      en: {
        help: "Move your cursor or finger inside the frame to inspect threads through the 95px Spotlight Aperture. Zero camera frames ever leave your device — AI scanning runs locally in your browser.",
        title: "PAKDA GAYA! UNAUTHORISED COPYING / OPTICAL THEFT BLOCKED",
        unlockBtn: "📷 Turn On Camera to Unlock GI Saree",
        unlockTitle: "LIVE CAMERA REQUIRED TO UNLOCK GI SAREE",
        legal: '⚖️ <strong>STATUTORY LEGAL NOTICE:</strong> Unauthorised copying or commercial reproduction of textile designs may constitute <strong>Intellectual Property Theft</strong>, punishable under <strong>Sections 51 and 63 of the Copyright Act, 1957</strong>, <strong>Section 22 of the Designs Act, 2000</strong>, and <strong>Section 39 of the GI Act, 1999</strong>. Legal action may result in imprisonment, fines and damages.'
      },
      te: {
        help: "95px స్పాట్‌లైట్ ద్వారా చేనేత డిజైన్‌ను పరిశీలించడానికి కర్సర్ లేదా వేలిని కదిలించండి. కెమెరా ఫ్రేమ్‌లు మీ పరికరాన్ని వదిలి వెళ్లవు — AI మీ బ్రౌజర్‌లోనే పనిచేస్తుంది.",
        title: "పట్టుబడ్డారు! అనధికార కాపీ / ఫోటో చోరీ నిరోధించబడింది",
        unlockBtn: "📷 GI చీరను చూడటానికి కెమెరా ఆన్ చేయండి",
        unlockTitle: "GI చీరను అన్‌లాక్ చేయడానికి లైవ్ కెమెరా అవసరం",
        legal: '⚖️ <strong>చట్టపరమైన హెచ్చరిక:</strong> చేనేత డిజైన్లను అనధికారికంగా కాపీ చేయడం <strong>మేధో సంపత్తి చోరీ (IP Theft)</strong> కిందకు వస్తుంది. ఇది <strong>కాపీరైట్ చట్టం 1957 (సెక్షన్లు 51 &amp; 63)</strong>, <strong>డిజైన్స్ చట్టం 2000 (సెక్షన్ 22)</strong> మరియు <strong>GI చట్టం 1999 (సెక్షన్ 39)</strong> ప్రకారం జైలు శిక్ష మరియు జరిమానాకు గురిచేస్తుంది.'
      },
      hi: {
        help: "95px स्पॉटलाइट के माध्यम से बुनाई देखने के लिए कर्सर या उंगली घुमाएं। कोई भी कैमरा फ्रेम आपके डिवाइस से बाहर नहीं जाता — AI सीधे आपके ब्राउज़र में चलता है।",
        title: "पकड़ा गया! अनधिकृत कॉपी / ऑप्टिकल चोरी ब्लॉक की गई",
        unlockBtn: "📷 GI साड़ी देखने के लिए कैमरा चालू करें",
        unlockTitle: "GI साड़ी अनलॉक करने के लिए लाइव कैमरा आवश्यक है",
        legal: '⚖️ <strong>वैधानिक कानूनी चेतावनी:</strong> कपड़ा डिजाइनों की अनधिकृत नकल <strong>बौद्धिक संपदा चोरी</strong> है, जो <strong>कॉपीराइट अधिनियम 1957 (धारा 51 व 63)</strong>, <strong>डिजाइन अधिनियम 2000 (धारा 22)</strong> और <strong>GI अधिनियम 1999 (धारा 39)</strong> के तहत दंडनीय है।'
      }
    };

    const viewport = document.getElementById("weave-viewport");
    const clearLayer = document.getElementById("weave-clear-layer");
    const overlay = document.getElementById("emoji-shield-overlay");
    const memeVideo = document.getElementById("honeypot-meme-video");
    const emojiFallback = document.getElementById("emoji-fallback");
    const unlockGate = document.getElementById("camera-unlock-gate");
    const unlockBtn = document.getElementById("btn-unlock-camera");
    const unlockErr = document.getElementById("unlock-error-msg");
    const reasonEl = document.getElementById("shield-reason-text");
    const badge = document.getElementById("guard-status-badge");
    const diag = document.getElementById("val-cam-diag");
    const canvas = document.getElementById("anti-shutter-canvas");
    const toast = document.getElementById("copy-warning-toast");
    const camVideo = document.getElementById("buyer-cam-video");
    const liveCanvas = document.getElementById("buyer-liveness-canvas");

    let cameraUnlocked = (GATE_MODE !== "strict");
    let shieldLocked = (GATE_MODE === "strict");
    let memeOverlayVisible = false;
    let manualHoldUntil = 0;
    let lastBreachLogTs = 0;
    let toastTimer = null;
    let flickerPhase = 0;
    let buyerStream = null;
    let scanTimer = null;
    let scanInFlight = false;

    let cocoModel = null;
    let prevGray = null;
    let liveFrames = 0;
    let frozenStreak = 0;

    if (memeVideo) {
      memeVideo.muted = true;
      memeVideo.defaultMuted = true;
      memeVideo.volume = 0;
      memeVideo.disablePictureInPicture = true;
      memeVideo.addEventListener("error", () => {
        memeVideo.classList.add("hidden");
        if (emojiFallback) emojiFallback.classList.remove("hidden");
      });
    }

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

    function logBreachDebounced(reason) {
      const now = Date.now();
      if (now - lastBreachLogTs < 4000) return;
      lastBreachLogTs = now;
      fetch("/api/log-breach", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ reason: "BUYER_" + reason })
      }).catch(() => {});
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

    function checkLivenessAndShutter() {
      const ctx = liveCanvas.getContext("2d", { willReadFrequently: true });
      ctx.drawImage(camVideo, 0, 0, 96, 72);
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
        liveFrames = 0;
        return { threat: true, live: false, reason: "PRIVACY_SHUTTER_OR_COVERED_CAMERA" };
      }

      if (prevGray) {
        let diffSum = 0;
        for (let i = 0; i < n; i++) {
          diffSum += Math.abs(gray[i] - prevGray[i]);
        }
        const diff = diffSum / n;
        if (diff < 0.32) {
          frozenStreak++;
          liveFrames = 0;
        } else {
          frozenStreak = 0;
          liveFrames++;
        }
      } else {
        liveFrames = 1;
      }
      prevGray = gray;

      const limit = cameraUnlocked ? 4 : 2;
      if (frozenStreak >= limit) {
        return { threat: true, live: false, reason: "PRIVACY_SHUTTER_OR_FROZEN_CAMERA" };
      }
      return { threat: false, live: liveFrames >= 2, reason: "SAFE" };
    }

    function moveSpotlight(clientX, clientY) {
      if (shieldLocked || !cameraUnlocked || !viewport || !clearLayer) return;
      const rect = viewport.getBoundingClientRect();
      clearLayer.style.clipPath = `circle(${SPOTLIGHT_RADIUS_PX}px at ${clientX - rect.left}px ${clientY - rect.top}px)`;
    }

    viewport.addEventListener("mousemove", (e) => moveSpotlight(e.clientX, e.clientY));
    viewport.addEventListener("touchmove", (e) => {
      if (e.touches && e.touches[0]) {
        e.preventDefault();
        moveSpotlight(e.touches[0].clientX, e.touches[0].clientY);
      }
    }, { passive: false });
    viewport.addEventListener("mouseleave", () => { clearLayer.style.clipPath = "circle(0px at 50% 50%)"; });

    function stopBuyerCameraStream() {
      if (scanTimer) { clearTimeout(scanTimer); scanTimer = null; }
      if (buyerStream) {
        try { buyerStream.getTracks().forEach((t) => t.stop()); } catch (_) {}
        buyerStream = null;
      }
      if (camVideo) { try { camVideo.srcObject = null; } catch (_) {} }
      prevGray = null;
      liveFrames = 0;
      frozenStreak = 0;
    }

    function showLiveShutterGateWarning(reasonCode) {
      shieldLocked = true;
      viewport.classList.add("threat-locked");
      overlay.classList.add("hidden");
      if (memeOverlayVisible) { memeOverlayVisible = false; stopMemeVideo(); }
      if (unlockGate) unlockGate.classList.remove("hidden");
      if (unlockBtn) {
        unlockBtn.disabled = true;
        unlockBtn.textContent = "⏳ Waiting for Open Live Camera...";
      }
      if (unlockErr) {
        unlockErr.textContent = "🚫 Camera shutter closed or lens covered (" + reasonCode + "). Open/uncover your camera to unlock automatically.";
        unlockErr.classList.remove("hidden");
      }
      badge.textContent = "🔒 BLOCKED: " + reasonCode;
      badge.className = "pill pill-danger";
      diag.textContent = "🚨 " + reasonCode;
      diag.style.color = "#f87171";
      logBreachDebounced(reasonCode);
    }

    function lockForClosedCamera(reasonCode, friendlyMsg) {
      cameraUnlocked = false;
      shieldLocked = true;
      stopBuyerCameraStream();

      viewport.classList.add("threat-locked");
      overlay.classList.add("hidden");
      if (memeOverlayVisible) { memeOverlayVisible = false; stopMemeVideo(); }
      if (unlockGate) unlockGate.classList.remove("hidden");
      if (unlockBtn) {
        unlockBtn.disabled = false;
        const curLang = document.getElementById("lang-toggle").value || "en";
        unlockBtn.textContent = (I18N[curLang] || I18N.en).unlockBtn;
      }
      if (unlockErr && friendlyMsg) {
        unlockErr.textContent = friendlyMsg;
        unlockErr.classList.remove("hidden");
      }
      badge.textContent = "🔒 CAMERA OFF — VAULT LOCKED";
      badge.className = "pill pill-danger";
      diag.textContent = "🔒 " + reasonCode;
      diag.style.color = "#f87171";
      logBreachDebounced(reasonCode);
    }

    function setShield(locked, reason) {
      if (!locked && GATE_MODE === "strict" && !cameraUnlocked) locked = true;
      if (!locked && Date.now() < manualHoldUntil) locked = true;
      shieldLocked = locked;

      if (GATE_MODE === "strict" && !cameraUnlocked) {
        viewport.classList.add("threat-locked");
        return;
      }

      if (locked) {
        viewport.classList.add("threat-locked");
        overlay.classList.remove("hidden");
        if (!memeOverlayVisible) { memeOverlayVisible = true; startMemeVideo(); }
        reasonEl.textContent = reason;
        badge.textContent = "🚫 BLOCKED: " + reason;
        badge.className = "pill pill-danger";
        diag.textContent = "🚨 " + reason;
        diag.style.color = "#f87171";
        logBreachDebounced(reason);
      } else {
        viewport.classList.remove("threat-locked");
        overlay.classList.add("hidden");
        if (memeOverlayVisible) { memeOverlayVisible = false; stopMemeVideo(); }
        if (unlockGate) unlockGate.classList.add("hidden");
        if (unlockErr) unlockErr.classList.add("hidden");
        badge.textContent = GATE_MODE === "strict" ? "🛡️ ON-DEVICE AI CAMERA ACTIVE" : "🛡️ SPOTLIGHT + 8x8 ZARI CLOAK";
        badge.className = "pill pill-safe";
        diag.textContent = GATE_MODE === "strict" ? "SAFE (BROWSER AI ACTIVE)" : "STANDARD PREVIEW";
        diag.style.color = "#34d399";
      }
    }

    function triggerBreach(reason) {
      manualHoldUntil = Date.now() + 4500;
      if (cameraUnlocked) {
        setShield(true, reason);
        if (GATE_MODE === "standard") {
          setTimeout(() => { if (Date.now() >= manualHoldUntil) setShield(false, "SAFE"); }, 4600);
        }
      }
      if (toast) {
        document.getElementById("toast-heading").textContent = "STATUTORY IP THEFT WARNING [" + reason + "]";
        toast.classList.remove("hidden");
        if (toastTimer) clearTimeout(toastTimer);
        toastTimer = setTimeout(() => toast.classList.add("hidden"), 5000);
      }
      logBreachDebounced(reason);
    }

    async function runBrowserAIScanLoop() {
      if (GATE_MODE !== "strict" || !buyerStream) return;

      const track = buyerStream.getVideoTracks()[0];
      if (!buyerStream.active || !track || track.readyState !== "live" || track.muted) {
        lockForClosedCamera("CAMERA_CLOSED_OR_MUTED", "Your camera was turned off or paused. Turn your camera back ON to continue viewing.");
        return;
      }

      if (!scanInFlight && camVideo.readyState >= 2 && camVideo.videoWidth > 0) {
        scanInFlight = true;
        try {
          const liveCheck = checkLivenessAndShutter();
          if (liveCheck.threat) {
            if (!cameraUnlocked) showLiveShutterGateWarning(liveCheck.reason);
            else setShield(true, liveCheck.reason);
          } else {
            let aiThreat = "";
            if (cocoModel) {
              const preds = await cocoModel.detect(camVideo, 8, 0.24);
              const personPresent = preds.some((p) => p.class === "person" && p.score >= 0.35);
              for (const p of preds) {
                if (p.class === "cell phone" && p.score >= 0.25) {
                  aiThreat = "CELL_PHONE_DETECTED_BROWSER_AI";
                  break;
                }
                if (personPresent && (p.class === "remote" || p.class === "book") && p.score >= 0.45) {
                  aiThreat = "HANDHELD_OPTICAL_DEVICE_DETECTED";
                  break;
                }
              }
            }

            if (aiThreat) {
              if (!cameraUnlocked) showLiveShutterGateWarning(aiThreat);
              else setShield(true, aiThreat);
            } else if (!cameraUnlocked) {
              if (liveCheck.live) {
                cameraUnlocked = true;
                setShield(false, "LIVE_CAMERA_VERIFIED");
              } else if (unlockBtn) {
                unlockBtn.textContent = "⏳ Verifying Live Camera Sensor...";
              }
            } else {
              setShield(false, "SAFE_VIEWER_VERIFIED");
            }
          }
        } catch (_) {
        } finally {
          scanInFlight = false;
        }
      }

      if (buyerStream) {
        scanTimer = setTimeout(runBrowserAIScanLoop, 280);
      }
    }

    async function startBuyerCameraGate() {
      if (buyerStream) return;
      if (unlockErr) unlockErr.classList.add("hidden");

      if (!window.isSecureContext || !navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        lockForClosedCamera("HTTPS_REQUIRED_FOR_CAMERA", "Browser blocked camera access because this link is not secure HTTPS.");
        return;
      }

      if (unlockBtn) {
        unlockBtn.disabled = true;
        unlockBtn.textContent = "⏳ Requesting Camera & Loading On-Device AI...";
      }

      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: { facingMode: "user", width: { ideal: 320 }, height: { ideal: 240 } },
          audio: false
        });

        buyerStream = stream;
        camVideo.srcObject = stream;
        await camVideo.play();

        const track = stream.getVideoTracks()[0];
        if (track) {
          track.onended = () => lockForClosedCamera("CAMERA_TURNED_OFF", "Camera access was ended. Keep your camera ON to inspect this GI handloom design.");
          track.onmute = () => lockForClosedCamera("CAMERA_MUTED_OR_BLOCKED", "Camera feed was interrupted or blocked. Keep your camera active to continue.");
        }

        if (unlockBtn) unlockBtn.textContent = "⏳ Loading On-Device AI Phone Detector...";
        await ensureBrowserAI();

        if (unlockBtn) unlockBtn.textContent = "⏳ Verifying Live Camera Sensor...";
        scanTimer = setTimeout(runBrowserAIScanLoop, 250);
      } catch (err) {
        const msg =
          err && err.name === "NotAllowedError"
            ? "Camera permission was denied. Tap 'Allow' on the camera popup to unlock this Tier-1 GI saree."
            : err && err.name === "NotFoundError"
            ? "No camera was found on this device. A live camera is required for Tier-1 links."
            : "Could not access your camera (" + (err && err.name ? err.name : "Error") + ").";
        lockForClosedCamera("CAMERA_PERMISSION_DENIED", msg);
      }
    }

    if (unlockBtn) unlockBtn.addEventListener("click", startBuyerCameraGate);
    window.addEventListener("pagehide", () => { stopBuyerCameraStream(); stopMemeVideo(); });

    document.addEventListener("contextmenu", (e) => { e.preventDefault(); triggerBreach("RIGHT_CLICK_BLOCKED"); });
    document.addEventListener("dragstart", (e) => { e.preventDefault(); triggerBreach("IMAGE_DRAG_BLOCKED"); });
    document.addEventListener("copy", (e) => {
      e.preventDefault();
      if (e.clipboardData) e.clipboardData.setData("text/plain", STATUTORY_PLAIN);
      triggerBreach("CLIPBOARD_COPY_BLOCKED");
    });
    window.addEventListener("keydown", (e) => {
      const k = (e.key || "").toLowerCase();
      if (e.key === "F12" || ((e.ctrlKey || e.metaKey) && ["c", "s", "u", "p", "i", "j"].includes(k))) {
        e.preventDefault();
        try { navigator.clipboard.writeText(STATUTORY_PLAIN); } catch (_) {}
        triggerBreach("HOTKEY_" + k.toUpperCase() + "_BLOCKED");
      }
    });
    window.addEventListener("keyup", (e) => {
      if (e.key === "PrintScreen" || (e.metaKey && e.shiftKey && e.key.toLowerCase() === "s")) {
        try { navigator.clipboard.writeText(STATUTORY_PLAIN); } catch (_) {}
        triggerBreach("SCREENSHOT_BLOCKED");
      }
    });
    document.addEventListener("visibilitychange", () => { if (document.hidden) triggerBreach("TAB_SWITCH_OR_SCREEN_SHARE"); });
    if (navigator.mediaDevices && navigator.mediaDevices.getDisplayMedia) {
      navigator.mediaDevices.getDisplayMedia = async function () {
        triggerBreach("SCREEN_SHARE_BLOCKED");
        throw new Error("Blocked by Heritage-Guard");
      };
    }

    document.getElementById("lang-toggle").addEventListener("change", (e) => {
      const p = I18N[e.target.value] || I18N.en;
      document.getElementById("ui-buyer-help").textContent = p.help;
      document.getElementById("honeypot-title").textContent = p.title;
      document.getElementById("legal-warning-text").innerHTML = p.legal;
      document.getElementById("static-buyer-legal-text").innerHTML = p.legal;
      document.getElementById("toast-body").innerHTML = p.legal;
      const ut = document.getElementById("unlock-gate-title");
      if (ut) ut.textContent = p.unlockTitle;
      if (unlockBtn && !unlockBtn.disabled) unlockBtn.textContent = p.unlockBtn;
    });

    function runFlicker() {
      if (canvas && !shieldLocked && cameraUnlocked) {
        const ctx = canvas.getContext("2d");
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.fillStyle = "rgba(20, 10, 30, 0.055)";
        for (let y = flickerPhase; y < canvas.height; y += 3) ctx.fillRect(0, y, canvas.width, 1);
        flickerPhase = (flickerPhase + 1) % 3;
      }
      requestAnimationFrame(runFlicker);
    }
    requestAnimationFrame(runFlicker);
  })();
  </script>
</body>
</html>
"""


@app.route("/b/<gate>/<asset_id>")
def buyer_only_view(gate, asset_id):
    clean_gate = "standard" if gate.lower() == "standard" else "strict"
    clean_id = asset_id.strip()

    with RAM_LOCK:
        rec = RAM_BUYER_VAULT.get(clean_id)

    label = rec["label"] if rec else DEMO_TITLES.get(clean_id.lower(), "GI Protected Handloom Saree")

    is_strict = clean_gate == "strict"
    gate_pill = "🔒 TIER-1: BIOMETRIC VAULT" if is_strict else "🛡️ TIER-2: CATALOG PREVIEW"
    status_init = "🔒 CAMERA REQUIRED TO UNLOCK" if is_strict else "🛡️ SPOTLIGHT + 8x8 ZARI CLOAK"
    status_class = "pill-danger" if is_strict else "pill-safe"
    diag_init = "CAMERA OFF — LOCKED" if is_strict else "STANDARD PREVIEW"
    diag_color = "#f87171" if is_strict else "#34d399"
    initial_lock_class = "threat-locked" if is_strict else ""
    gate_overlay_class = "" if is_strict else "hidden"

    page = (
        BUYER_ONLY_HTML
        .replace("__GATE_MODE__", clean_gate)
        .replace("__ASSET_ID__", html.escape(clean_id))
        .replace("__ASSET_LABEL__", html.escape(label))
        .replace("__GATE_PILL__", gate_pill)
        .replace("__STATUS_INIT__", status_init)
        .replace("__STATUS_CLASS__", status_class)
        .replace("__DIAG_INIT__", diag_init)
        .replace("__DIAG_COLOR__", diag_color)
        .replace("__INITIAL_LOCK_CLASS__", initial_lock_class)
        .replace("__GATE_OVERLAY_CLASS__", gate_overlay_class)
    )
    return page, 200, {"Content-Type": "text/html; charset=utf-8"}


# ---------------- API ROUTES ----------------
@app.route("/api/weaver_unlock", methods=["POST"])
def api_weaver_unlock():
    if _check_weaver_pin():
        return jsonify({"unlocked": True})
    return jsonify({"unlocked": False, "error": "Invalid Weaver PIN"}), 403


@app.route("/api/lan_info", methods=["GET"])
def api_lan_info():
    root = _public_root_url()
    return jsonify({
        "lan_ip": "cloud",
        "port": int(os.environ.get("PORT", "10000")),
        "public_url": root,
        "tunnel_status": "active",
        "cloud_mode": True,
    })


@app.route("/api/asset_image/<asset_id>", methods=["GET"])
def api_asset_image(asset_id):
    clean_id = asset_id.strip()
    with RAM_LOCK:
        rec = RAM_BUYER_VAULT.get(clean_id)
    if rec:
        return send_file(io.BytesIO(rec["primary"]), mimetype="image/png")

    bundle = _get_or_build_demo_weave(clean_id)
    return send_file(io.BytesIO(bundle["meme"]), mimetype="image/png")


@app.route("/api/studio_asset/<asset_id>", methods=["GET"])
def api_studio_asset(asset_id):
    clean_id = asset_id.strip()
    token = request.args.get("token", "").strip()
    with RAM_LOCK:
        rec = RAM_BUYER_VAULT.get(clean_id)

    if not rec:
        return jsonify({"error": "Asset expired from volatile RAM vault."}), 404
    if not token or not hmac.compare_digest(token, rec["studio_token"]):
        return jsonify({"error": "Forbidden: Valid Weaver Studio token required."}), 403

    variant = request.args.get("variant", "primary").lower()
    download = request.args.get("download", "0") == "1"

    if variant == "zip":
        if not rec.get("zip"):
            return jsonify({"error": "No batch ZIP available for single upload."}), 404
        return send_file(
            io.BytesIO(rec["zip"]),
            mimetype="application/zip",
            as_attachment=True,
            download_name=f"heritage_guard_batch_{clean_id}.zip",
        )

    if variant == "heat":
        img_bytes = rec["heat"]
        dl_name = f"heatmap_8x8_{clean_id}.png"
    elif variant == "zari":
        img_bytes = rec["zari"]
        dl_name = f"zariwork_8x8_{clean_id}.png"
    elif variant == "meme":
        img_bytes = rec["meme"]
        dl_name = f"meme_embedded_{clean_id}.png"
    else:
        img_bytes = rec["primary"]
        dl_name = f"protected_{clean_id}.png"

    return send_file(
        io.BytesIO(img_bytes),
        mimetype="image/png",
        as_attachment=download,
        download_name=dl_name if download else None,
    )


@app.route("/api/demo_weave", methods=["GET"])
def api_demo_weave():
    style = request.args.get("style", "ikat").lower()
    want_heatmap = request.args.get("heatmap", "0") == "1"
    variant = request.args.get("variant", "meme").lower()
    download = request.args.get("download", "0") == "1"

    bundle = _get_or_build_demo_weave(style)
    if want_heatmap:
        img_bytes = bundle["heat"]
        dl_name = f"{style}_8x8_perturbation_heatmap.png"
    elif variant == "zari":
        img_bytes = bundle["zari"]
        dl_name = f"{style}_8x8_zariwork_cloaked.png"
    else:
        img_bytes = bundle["meme"]
        dl_name = f"{style}_meme_embedded_cloaked.png"

    return send_file(
        io.BytesIO(img_bytes),
        mimetype="image/png",
        as_attachment=download,
        download_name=dl_name if download else None,
    )


@app.route("/api/protect", methods=["POST"])
def api_protect_upload():
    if not _check_weaver_pin():
        return jsonify({"error": "Weaver Studio is PIN-locked. Enter the Weaver PIN above to upload & cloak sarees."}), 403

    uploaded_files = request.files.getlist("files") or request.files.getlist("file")
    if not uploaded_files:
        return jsonify({"error": "No image files uploaded."}), 400

    artisan_id = (request.form.get("artisan_id", "WEAVER_TG_COOP_01").strip() or "WEAVER_TG_COOP_01")[:32]
    gi_cluster = (request.form.get("gi_cluster", "POCHAMPALLY_IKAT").strip() or "POCHAMPALLY_IKAT")[:32]
    cloak_mode = request.form.get("cloak_mode", "meme_bait").strip()

    results = []
    zip_buffer = io.BytesIO()

    try:
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zf:
            for idx, f_obj in enumerate(uploaded_files):
                raw_bytes = f_obj.read()
                if not raw_bytes:
                    continue
                res = execute_ram_protection_pipeline(
                    raw_bytes,
                    artisan_id=artisan_id,
                    gi_cluster=gi_cluster,
                    cloak_mode=cloak_mode,
                )
                _, png_zari = cv2.imencode(".png", res["zari_only_bgr"])
                _, png_meme = cv2.imencode(".png", res["meme_embedded_bgr"])
                _, png_heat = cv2.imencode(".png", res["heatmap_bgr"])

                zari_bytes = png_zari.tobytes()
                meme_bytes = png_meme.tobytes()
                heat_bytes = png_heat.tobytes()
                primary_bytes = zari_bytes if cloak_mode == "invisible" else meme_bytes

                zf.writestr(f"zariwork_8x8_{idx + 1}_{artisan_id}.png", zari_bytes)
                zf.writestr(f"meme_embedded_{idx + 1}_{artisan_id}.png", meme_bytes)
                results.append((res, primary_bytes, zari_bytes, meme_bytes, heat_bytes))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception as exc:
        return jsonify({"error": f"Image processing failed: {exc}"}), 500

    if not results:
        return jsonify({"error": "Empty or unreadable image upload."}), 400

    first_res, first_primary, first_zari, first_meme, first_heat = results[0]
    is_batch = len(results) > 1
    fp_short = first_res["fingerprint"][:12]
    studio_token = secrets.token_urlsafe(12)

    with RAM_LOCK:
        RAM_BUYER_VAULT[fp_short] = {
            "primary": first_primary,
            "zari": first_zari,
            "meme": first_meme,
            "heat": first_heat,
            "zip": zip_buffer.getvalue() if is_batch else None,
            "label": f"{artisan_id} ({gi_cluster})",
            "studio_token": studio_token,
        }
        RAM_BUYER_VAULT.move_to_end(fp_short)
        while len(RAM_BUYER_VAULT) > MAX_RAM_ASSETS:
            RAM_BUYER_VAULT.popitem(last=False)

    log_security_event({
        "event": "CLOUD_BATCH_PROTECT" if is_batch else "CLOUD_RAM_PROTECT",
        "reason": f"{len(results)} asset(s) [ID:{fp_short}] for {artisan_id}",
    })

    ts = int(time.time() * 1000)
    return jsonify({
        "is_batch": is_batch,
        "processed_count": len(results),
        "fingerprint": first_res["fingerprint"],
        "fp_short": fp_short,
        "watermark_payload": first_res["watermark_payload"],
        "watermark_verified_post_cloak": first_res["watermark_verified_post_cloak"],
        "psnr_db": first_res["psnr_db"],
        "jpeg_survival_pct": first_res["jpeg_survival_pct"],
        "quality_gate_passed": first_res["quality_gate_passed"],
        "preview_url": f"/api/studio_asset/{fp_short}?variant=primary&token={studio_token}&t={ts}",
        "heatmap_url": f"/api/studio_asset/{fp_short}?variant=heat&token={studio_token}&t={ts}",
        "zari_download_url": f"/api/studio_asset/{fp_short}?variant=zari&download=1&token={studio_token}",
        "meme_download_url": f"/api/studio_asset/{fp_short}?variant=meme&download=1&token={studio_token}",
        "zip_download_url": f"/api/studio_asset/{fp_short}?variant=zip&download=1&token={studio_token}" if is_batch else None,
    })


@app.route("/api/verify", methods=["POST"])
def api_verify_upload():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded."}), 400
    raw_bytes = request.files["file"].read()
    try:
        bgr = strip_exif_in_ram(raw_bytes, max_dim=None)
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400
    except Exception:
        return jsonify({"error": "Could not decode image file."}), 400

    extracted = extract_3zone_lsb(bgr)
    fp = generate_sha256_fingerprint(bgr)
    with DB_LOCK:
        vault_rec = db_vault.get_gi_asset_by_hash(fp)

    log_security_event({
        "event": "FORENSIC_VERIFY_SCAN",
        "reason": f"SQL_MATCH:{vault_rec['artisan_id']}" if vault_rec else (extracted or "UNREGISTERED_IMAGE"),
    })

    return jsonify({
        "verified": bool(extracted or vault_rec),
        "extracted_watermark": extracted,
        "sha256_fingerprint": fp,
        "vault_match": (
            f"{vault_rec['artisan_id']} ({vault_rec['gi_cluster']} • {vault_rec['cloak_mode']})"
            if vault_rec
            else None
        ),
    })


@app.route("/api/log-breach", methods=["POST"])
def api_log_breach():
    data = request.get_json(silent=True) or {}
    reason = str(data.get("reason", "FRONTEND_HONEYPOT_TRIGGER"))[:120]
    log_security_event({"event": "HONEYPOT_LOCKOUT", "reason": reason})
    return jsonify({"logged": True})


@app.route("/api/audit_logs", methods=["GET"])
def api_audit_logs():
    with DB_LOCK:
        logs = db_vault.get_recent_security_logs(limit=15)
    return jsonify(logs)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "10000"))
    app.run(host="0.0.0.0", port=port, debug=False, threaded=True)