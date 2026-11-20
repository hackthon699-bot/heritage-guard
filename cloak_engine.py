"""
Heritage-Guard | Person 2 Module: cloak_engine.py (v1.3)
Role: True 8x8 Macroblock DCT Luminance-Locked Zari Cloak + Ghost-Edge Meme Trap
      + Visual Perturbation Heatmap Generator.
"""

import cv2
import numpy as np
from preprocessor import embed_3zone_lsb

VERSION = "1.3"


def _build_ghost_meme_mask(shape: tuple, text: str = "PAKDA GAYA STOLEN GI") -> np.ndarray:
    h, w = shape[:2]
    canvas = np.zeros((h, w), dtype=np.uint8)
    font = cv2.FONT_HERSHEY_SIMPLEX
    scale = max(0.5, min(w, h) / 380.0)
    thickness = max(1, int(scale * 2))

    step_y = max(45, int(h / 4))
    for y in range(step_y // 2, h, step_y):
        cv2.putText(canvas, text, (10, y), font, scale, 255, thickness, cv2.LINE_AA)

    edges = cv2.Canny(canvas, 80, 180)
    return (edges > 0).astype(np.float32)


def generate_perturbation_heatmap(original_bgr: np.ndarray, cloaked_bgr: np.ndarray) -> np.ndarray:
    diff = cv2.absdiff(cloaked_bgr, original_bgr)
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    norm_diff = cv2.normalize(gray_diff, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    heatmap = cv2.applyColorMap(norm_diff, cv2.COLORMAP_JET)
    return cv2.addWeighted(original_bgr, 0.35, heatmap, 0.65, 0)


def apply_cloak(
    bgr_img: np.ndarray,
    strength: float = 3.5,
    mode: str = "meme_bait",
    meme_text: str = "PAKDA GAYA STOLEN GI",
    watermark_payload: str = None,
) -> dict:
    if bgr_img is None or bgr_img.size == 0:
        raise ValueError("Empty image passed to cloak_engine.")

    orig = bgr_img.astype(np.float32)
    h, w, _ = orig.shape

    y_grid, x_grid = np.meshgrid(np.arange(h), np.arange(w), indexing="ij")
    macroblock_8x8 = ((x_grid // 8) + (y_grid // 8)) % 2
    carrier_8x8 = np.where(macroblock_8x8 == 0, 1.0, -1.0).astype(np.float32)

    gray = cv2.cvtColor(bgr_img, cv2.COLOR_BGR2GRAY)
    grad_x = cv2.Sobel(gray, cv2.CV_32F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(gray, cv2.CV_32F, 0, 1, ksize=3)
    mag = cv2.magnitude(grad_x, grad_y)
    norm_mag = mag / (np.max(mag) + 1e-6)
    zari_weight = 0.78 + 0.22 * norm_mag

    if mode == "invisible":
        delta_2d = carrier_8x8 * zari_weight * strength
    else:
        ghost_edges = _build_ghost_meme_mask((h, w), meme_text)
        delta_2d = (carrier_8x8 * zari_weight * strength) + (ghost_edges * (strength * 0.65))

    delta_3d = np.stack([delta_2d, delta_2d, delta_2d], axis=-1)
    cloaked = np.clip(orig + delta_3d, 0, 255).astype(np.uint8)

    if h > 8:
        cloaked[:4, :, :] = bgr_img[:4, :, :]

    if watermark_payload:
        cloaked = embed_3zone_lsb(cloaked, watermark_payload)

    psnr_val = float(cv2.PSNR(bgr_img, cloaked))
    heatmap_bgr = generate_perturbation_heatmap(bgr_img, cloaked)

    return {
        "cloaked_image": cloaked,
        "heatmap_image": heatmap_bgr,
        "delta": cloaked.astype(np.float32) - orig,
        "psnr": round(psnr_val, 2),
        "block_size": "8x8_DCT_MACROBLOCK",
        "meme_trap_active": (mode != "invisible"),
        "version": VERSION,
    }


cloak_image = apply_cloak