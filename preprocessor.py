"""
Heritage-Guard | Person 1 Module: preprocessor.py (v1.6)
Role: Zero-Retention RAM EXIF Stripper, Safe Resolution Guard,
      SHA-256 Fingerprinter, and 3-Zone Crop-Resilient LSB Watermarker.
"""

import hashlib
import cv2
import numpy as np

VERSION = "1.6"
MAGIC_HEADER = "HG|"
DEFAULT_MAX_DIM = 1600


def strip_exif_in_ram(raw_bytes: bytes, max_dim: int = DEFAULT_MAX_DIM) -> np.ndarray:
    """
    Decodes raw bytes directly into a clean BGR numpy array in RAM,
    stripping all EXIF/GPS metadata. Optionally caps oversized phone photos
    so large uploads never freeze the browser (pass max_dim=None during verification).
    """
    if not raw_bytes:
        raise ValueError("Empty image bytes passed to strip_exif_in_ram.")
    arr = np.frombuffer(raw_bytes, dtype=np.uint8)
    bgr = cv2.imdecode(arr, cv2.IMREAD_COLOR)
    if bgr is None or bgr.size == 0:
        raise ValueError("Invalid or corrupted image file. Please upload a valid PNG/JPG image.")

    if max_dim is not None:
        h, w = bgr.shape[:2]
        largest = max(h, w)
        if largest > max_dim:
            scale = max_dim / float(largest)
            new_w = max(8, int(round(w * scale)))
            new_h = max(8, int(round(h * scale)))
            bgr = cv2.resize(bgr, (new_w, new_h), interpolation=cv2.INTER_AREA)

    return bgr


def generate_sha256_fingerprint(bgr_img: np.ndarray) -> str:
    """Generates a deterministic SHA-256 hash of raw pixel data."""
    return hashlib.sha256(bgr_img.tobytes()).hexdigest()


def _text_to_bits(text: str) -> list:
    data = (MAGIC_HEADER + text + "\0").encode("utf-8")
    bits = []
    for byte in data:
        for shift in range(7, -1, -1):
            bits.append((byte >> shift) & 1)
    return bits


def _bits_to_text(bits: list) -> str:
    chars = bytearray()
    for i in range(0, len(bits) - 7, 8):
        val = 0
        for b in bits[i:i + 8]:
            val = (val << 1) | b
        if val == 0:
            break
        chars.append(val)
    try:
        decoded = chars.decode("utf-8", errors="ignore")
        if decoded.startswith(MAGIC_HEADER):
            return decoded[len(MAGIC_HEADER):]
    except Exception:
        pass
    return ""


def embed_3zone_lsb(bgr_img: np.ndarray, payload: str) -> np.ndarray:
    """
    Embeds redundant LSB watermark across 3 vertical zones (Top, Center, Bottom)
    so cropped saree photos still retain ownership attribution.
    """
    out = bgr_img.copy()
    h, w, _ = out.shape
    bits = _text_to_bits(payload)
    n_bits = len(bits)

    zones = [
        (4, max(5, h // 3)),
        (h // 3, max(h // 3 + 1, (2 * h) // 3)),
        ((2 * h) // 3, h),
    ]

    for y0, y1 in zones:
        region = out[y0:y1, :, 0]  # Blue channel LSB
        flat = region.reshape(-1)
        if flat.size < n_bits:
            continue
        for i, bit in enumerate(bits):
            flat[i] = (flat[i] & 0xFE) | bit
        out[y0:y1, :, 0] = flat.reshape(region.shape)

    return out


def extract_3zone_lsb(bgr_img: np.ndarray, max_chars: int = 96) -> str:
    """Extracts and majority-votes the 3-Zone LSB watermark payload."""
    if bgr_img is None or bgr_img.size == 0:
        return ""
    h, w, _ = bgr_img.shape
    max_bits = (len(MAGIC_HEADER) + max_chars + 1) * 8

    zones = [
        (4, max(5, h // 3)),
        (h // 3, max(h // 3 + 1, (2 * h) // 3)),
        ((2 * h) // 3, h),
    ]

    found = []
    for y0, y1 in zones:
        region = bgr_img[y0:y1, :, 0]
        flat = region.reshape(-1)
        take = min(flat.size, max_bits)
        bits = [int(v & 1) for v in flat[:take]]
        msg = _bits_to_text(bits)
        if msg:
            found.append(msg)

    if not found:
        return ""
    return max(set(found), key=found.count)


def preprocess_pipeline(
    raw_bytes: bytes,
    artisan_id: str = "WEAVER_TG_COOP_01",
    gi_cluster: str = "POCHAMPALLY_IKAT",
) -> dict:
    bgr = strip_exif_in_ram(raw_bytes, max_dim=DEFAULT_MAX_DIM)
    fp = generate_sha256_fingerprint(bgr)
    payload = f"{gi_cluster[:10]}|{artisan_id[:16]}|{fp[:10]}"
    watermarked = embed_3zone_lsb(bgr, payload)
    return {
        "image": watermarked,
        "fingerprint": fp,
        "watermark_payload": payload,
        "version": VERSION,
    }


if __name__ == "__main__":
    print(f"[TEST] Running preprocessor.py v{VERSION} self-test...")
    huge = np.random.randint(30, 220, (2400, 3200, 3), dtype=np.uint8)
    ok, buf = cv2.imencode(".png", huge)
    assert ok
    res = preprocess_pipeline(buf.tobytes(), "WEAVER_TEST_01", "POCHAMPALLY_IKAT")
    assert max(res["image"].shape[:2]) == DEFAULT_MAX_DIM, "Resize cap failed!"
    assert extract_3zone_lsb(res["image"]) == res["watermark_payload"], "LSB check failed!"
    print(f"[PASS] preprocessor.py v{VERSION} verified (resized to {res['image'].shape[:2]})!")